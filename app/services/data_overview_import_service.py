from io import BytesIO
from typing import Any
from uuid import UUID

import numpy as np
from numpy.typing import NDArray
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.repositories.data_overview_records import DataOverviewInsertRecord
from app.repositories.data_overview_repository import DataOverviewRepository


class DataOverviewImportError(Exception):
    pass


class DataOverviewImportService:
    def __init__(self, session: Session) -> None:
        self.category_repository = CategoryRepository(session)
        self.data_overview_repository = DataOverviewRepository(session)

    def import_npz_file(self, file_content: bytes) -> int:
        npz_file = self._read_npz_file(file_content)

        required_arrays = [
            "uuids",
            "umap",
            "labels",
            "category_keys",
            "filenames",
            "anomalie_isolation_forest",
            "anomalie_lof",
            "anomalie_lof_labels",
            "anomalie_isolation_forest_labels",
        ]

        self._validate_required_arrays(
            npz_file_files=set(npz_file.files),
            required_arrays=required_arrays,
        )

        uuids = npz_file["uuids"]
        umap = npz_file["umap"]
        labels = npz_file["labels"]
        category_keys = npz_file["category_keys"]
        filenames = npz_file["filenames"]
        anomalie_isolation_forest = npz_file["anomalie_isolation_forest"]
        anomalie_lof = npz_file["anomalie_lof"]
        anomalie_lof_labels = npz_file["anomalie_lof_labels"]
        anomalie_isolation_forest_labels = npz_file["anomalie_isolation_forest_labels"]

        row_count = len(uuids)

        if row_count == 0:
            raise DataOverviewImportError(
                "Import file must contain at least one row.",
            )

        self._validate_lengths(
            row_count=row_count,
            arrays={
                "labels": labels,
                "category_keys": category_keys,
                "filenames": filenames,
                "anomalie_isolation_forest": anomalie_isolation_forest,
                "anomalie_lof": anomalie_lof,
                "anomalie_lof_labels": anomalie_lof_labels,
                "anomalie_isolation_forest_labels": (anomalie_isolation_forest_labels),
            },
        )

        if umap.shape != (row_count, 3):
            raise DataOverviewImportError(
                "Array 'umap' must have shape (row_count, 3).",
            )

        records = self._build_insert_records(
            uuids=uuids,
            umap=umap,
            labels=labels,
            category_keys=category_keys,
            filenames=filenames,
            anomalie_isolation_forest=anomalie_isolation_forest,
            anomalie_lof=anomalie_lof,
            anomalie_lof_labels=anomalie_lof_labels,
            anomalie_isolation_forest_labels=anomalie_isolation_forest_labels,
            row_count=row_count,
        )

        return self.data_overview_repository.insert_many(records)

    def _read_npz_file(self, file_content: bytes) -> Any:
        try:
            return np.load(BytesIO(file_content), allow_pickle=False)
        except Exception as error:
            raise DataOverviewImportError(
                "Could not read uploaded NumPy file.",
            ) from error

    def _validate_required_arrays(
        self,
        npz_file_files: set[str],
        required_arrays: list[str],
    ) -> None:
        missing_arrays = [
            array_name
            for array_name in required_arrays
            if array_name not in npz_file_files
        ]

        if missing_arrays:
            raise DataOverviewImportError(
                f"Missing arrays in upload: {missing_arrays}",
            )

    def _validate_lengths(
        self,
        row_count: int,
        arrays: dict[str, NDArray[Any]],
    ) -> None:
        for array_name, array in arrays.items():
            if len(array) != row_count:
                raise DataOverviewImportError(
                    f"Array '{array_name}' must have {row_count} entries.",
                )

    def _build_insert_records(
        self,
        uuids: NDArray[Any],
        umap: NDArray[Any],
        labels: NDArray[Any],
        category_keys: NDArray[Any],
        filenames: NDArray[Any],
        anomalie_isolation_forest: NDArray[Any],
        anomalie_lof: NDArray[Any],
        anomalie_lof_labels: NDArray[Any],
        anomalie_isolation_forest_labels: NDArray[Any],
        row_count: int,
    ) -> list[DataOverviewInsertRecord]:
        category_key_values = {str(category_key) for category_key in category_keys}

        category_technical_keys = (
            self.category_repository.find_technical_keys_by_category_keys(
                category_key_values,
            )
        )

        missing_category_keys = category_key_values - set(
            category_technical_keys.keys(),
        )

        if missing_category_keys:
            raise DataOverviewImportError(
                f"Unknown category keys: {sorted(missing_category_keys)}",
            )

        records: list[DataOverviewInsertRecord] = []

        for index in range(row_count):
            category_key = str(category_keys[index])

            try:
                parsed_uuid = UUID(str(uuids[index]))
            except ValueError as error:
                raise DataOverviewImportError(
                    f"Invalid UUID at row {index}: {uuids[index]}",
                ) from error

            records.append(
                {
                    "uuid": parsed_uuid,
                    "umap_x": float(umap[index][0]),
                    "umap_y": float(umap[index][1]),
                    "umap_z": float(umap[index][2]),
                    "label": str(labels[index]),
                    "category_technical_key": (category_technical_keys[category_key]),
                    "filename": str(filenames[index]),
                    "anomalie_isolation_forest": float(
                        anomalie_isolation_forest[index],
                    ),
                    "anomalie_lof": float(anomalie_lof[index]),
                    "anomalie_lof_label": str(anomalie_lof_labels[index]),
                    "anomalie_isolation_forest_label": str(
                        anomalie_isolation_forest_labels[index],
                    ),
                },
            )

        return records
