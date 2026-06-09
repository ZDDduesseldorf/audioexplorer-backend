from app.repo.json_objects import DataOverviewJSON
from app.service.json_utils import write_json_file
from app.service.metadata_utils import load_all_metadata
from pathlib import Path


def calculate_umap_from_audio():
    # TODO: korrekte Funktionen ergänzen
    # Funktion lade Audios
    # audios = load_audios(file_path)  # list[AudioData]
    # Funktion Audio Preproceesing
    # audio_preprocessed = preprocess_audio(audios)  # list[PreprocessedAudio]
    # Embedding Berechnung
    # embeddings = calculate_embeddings(audio_preprocessed) # list[EmbeddingData]
    # Anomalie

    # anomaly_results = calculate_anomaly(embeddings)
    anomaly_results = {
        "uuid1": {
            "anomalie_isolation_forest": -0.1,
            "anomalie_LOF": 1.2,
            "anomalie_label": "normal",
        },
        "uuid2": {
            "anomalie_isolation_forest": -0.8,
            "anomalie_LOF": 2.7,
            "anomalie_label": "anomaly",
        },
    }
    # UMAP

    # umap_results = calculate_umap(embeddings)
    umap_results = {
        "uuid1": {"umap_x": 0.1, "umap_y": 0.2, "umap_z": 0.3},
        "uuid2": {"umap_x": 0.4, "umap_y": 0.5, "umap_z": 0.6},
    }

    # Metadaten (label, category, filename) laden
    metadata_results = load_all_metadata()

    list_DataOverview = create_DataOverview(
        metadata_results, umap_results, anomaly_results
    )

    save_results_as_json(list_DataOverview)


def save_results_as_json(list_DataOverview: list[DataOverviewJSON]):
    BASE_DIR = Path(__file__).resolve().parents[1]
    json_path = BASE_DIR / "data" / "data_overview_write.json"
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
            "anomalie_label": item.anomalie_label,
        }

    write_json_file(json_path, result)


# TODO: def save_embeddings_as_json(embeddings):


def create_DataOverview(
    metadata_results: dict, umap_results: dict, anomaly_results: dict
):

    # TODO: Add handle missing values
    list_DataOverview = []

    # umändern zu dict aus Audio_files

    for uuid, item in metadata_results.items():
        dict_umap = umap_results.get(uuid, {})
        dict_anomaly = anomaly_results.get(uuid, {})

        dataOverview_uuid = DataOverviewJSON(
            uuid=uuid,
            umap_x=dict_umap["umap_x"],
            umap_y=dict_umap["umap_y"],
            umap_z=dict_umap["umap_z"],
            label=item["label"],
            category=item["category"],
            filename=item["filename"],
            anomalie_isolation_forest=dict_anomaly["anomalie_isolation_forest"],
            anomalie_LOF=dict_anomaly["anomalie_LOF"],
            anomalie_label=dict_anomaly["anomalie_label"],
        )

        list_DataOverview.append(dataOverview_uuid)

    return list_DataOverview
