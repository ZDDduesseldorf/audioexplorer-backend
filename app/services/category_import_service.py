from io import BytesIO
from typing import Any

import numpy as np
from numpy.typing import NDArray
from sqlalchemy.orm import Session

from app.repositories.category_records import CategoryInsertRecord
from app.repositories.category_repository import CategoryRepository


class CategoryImportError(Exception):
    pass


class CategoryImportService:
    def __init__(self, session: Session) -> None:
        self.category_repository = CategoryRepository(session)

    def import_npz_file(self, file_content: bytes) -> int:
        npz_file = self._read_npz_file(file_content)

        required_arrays = [
            "ids",
            "category_keys",
            "display_names",
        ]

        self._validate_required_arrays(
            npz_file_files=set(npz_file.files),
            required_arrays=required_arrays,
        )

        ids = npz_file["ids"]
        category_keys = npz_file["category_keys"]
        display_names = npz_file["display_names"]

        row_count = len(ids)

        if row_count == 0:
            raise CategoryImportError(
                "Import file must contain at least one row.",
            )

        self._validate_lengths(
            row_count=row_count,
            arrays={
                "category_keys": category_keys,
                "display_names": display_names,
            },
        )

        records = self._build_insert_records(
            ids=ids,
            category_keys=category_keys,
            display_names=display_names,
            row_count=row_count,
        )

        return self.category_repository.insert_many(records)

    def _read_npz_file(self, file_content: bytes) -> Any:
        try:
            return np.load(BytesIO(file_content), allow_pickle=False)
        except Exception as error:
            raise CategoryImportError(
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
            raise CategoryImportError(
                f"Missing arrays in upload: {missing_arrays}",
            )

    def _validate_lengths(
        self,
        row_count: int,
        arrays: dict[str, NDArray[Any]],
    ) -> None:
        for array_name, array in arrays.items():
            if len(array) != row_count:
                raise CategoryImportError(
                    f"Array '{array_name}' must have {row_count} entries.",
                )

    def _build_insert_records(
        self,
        ids: NDArray[Any],
        category_keys: NDArray[Any],
        display_names: NDArray[Any],
        row_count: int,
    ) -> list[CategoryInsertRecord]:
        records: list[CategoryInsertRecord] = []

        for index in range(row_count):
            records.append(
                {
                    "id": int(ids[index]),
                    "category_key": str(category_keys[index]),
                    "display_name": str(display_names[index]),
                },
            )

        return records
