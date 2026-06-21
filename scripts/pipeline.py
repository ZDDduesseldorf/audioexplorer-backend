from app.services.model import DataOverviewJSON
from app.services.json_utils import write_json_file
from app.services.metadata_utils import load_all_metadata
from scripts.run_audio_preprocessing import run_audio_preprocessing
from app.services.embedding_service import compute_embedding_from_list_ProcessedAudios
from app.services.umap_service import calculate_umap_2d_from_list_embeddings
from app.services.anomaly_detection.anomaly_service import AnomalyService
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
json_path = BASE_DIR / "data" / "data_overview.json"


def calculate_umap_from_audio(
    path_audio_folder, path_metadata, target_path_audios, target_path_json
):
    # TODO: korrekte Funktionen ergänzen

    # Funktion Audio Preproceesing
    audios_preprocessed = run_audio_preprocessing(path_audio_folder, target_path_audios)

    # Embedding Berechnung
    embeddings = compute_embedding_from_list_ProcessedAudios(audios_preprocessed)
    # Anomalie
    anomaly_service = AnomalyService()
    anomaly_results = anomaly_service.calculate_anomalies(embeddings)

    # UMAP

    umap_results = calculate_umap_2d_from_list_embeddings(embeddings)

    # Metadaten (label, category, filename) laden
    metadata_results = load_all_metadata(path_metadata)

    list_DataOverview = create_DataOverview(
        metadata_results, umap_results, anomaly_results
    )

    save_results_as_json(list_DataOverview, target_path_json)


def save_results_as_json(
    list_DataOverview: list[DataOverviewJSON], target_json_path: Path
) -> None:

    # Ergebnisse von vorheriger Funktion als data_overview.json speichern
    result = {}

    for item in list_DataOverview:
        result[item.uuid] = {
            "umap_x": item.umap_x,
            "umap_y": item.umap_y,
            "umap_z": item.umap_z,
            "label": item.label,
            "category": item.category,
            "filename": item.filename,
            "anomalie_isolation_forest": item.anomalie_isolation_forest,
            "anomalie_LOF": item.anomalie_LOF,
            "anomalie_isolation_forest_label": item.anomalie_isolation_forest_label,
            "anomalie_LOF_label": item.anomalie_LOF_label,
        }

    write_json_file(target_json_path, result)


# TODO: def save_embeddings_as_json(embeddings):


def create_DataOverview(
    metadata_results: dict, umap_results: dict, anomaly_results: dict
) -> list[DataOverviewJSON]:

    # TODO: Add handle missing values
    list_DataOverview = []

    # umändern zu dict aus Audio_files

    for uuid, item in umap_results.items():
        metadata = metadata_results.get(uuid)

        if metadata is None:
            print(f"UUID fehlt in metadata_results: {uuid}")
            continue

        anomaly = anomaly_results.get(uuid)

        if anomaly is None:
            print(f"UUID fehlt in anomaly_results: {uuid}")
            continue

        dataOverview_uuid = DataOverviewJSON(
            uuid=uuid,
            umap_x=item["umap_x"],
            umap_y=item["umap_y"],
            umap_z=item["umap_z"],
            label=metadata["label"],
            category=metadata["category"],
            filename=metadata["filename"],
            anomalie_isolation_forest=anomaly["scores"]["isolation_forest"],
            anomalie_LOF=anomaly["scores"]["lof"],
            anomalie_isolation_forest_label=anomaly["labels"]["isolation_forest"],
            anomalie_LOF_label=anomaly["labels"]["lof"],
        )

        list_DataOverview.append(dataOverview_uuid)

    return list_DataOverview
