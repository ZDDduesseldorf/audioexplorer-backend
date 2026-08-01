# Audioexplorer Backend

## Project Initialization

### Short Introduction

Audioexplorer is a web application for exploring and labeling audio samples. The backend provides APIs for data management, audio processing, and label proposals.

### Connected Repos

- **Frontend**: [audioexplorer-frontend](https://github.com/ZDDduesseldorf/audioexplorer-frontend)
- **Data Processor**: [audioexplorer-data-processor](https://github.com/ZDDduesseldorf/audioexplorer-data-processor)

### Installation

ToDo

### Application Start

To start the application you need a folder `data` with the preprocessed audio files from the data-processor repo.

TODO: Add json files or database import to start !!!!

```bash
docker-compose up
```

## API Endpoints

This repository provides three groups of API endpoints:

- Sound endpoints – Provide processed audio files, category information, and data overview entries to the frontend.
- Import endpoints – Import the generated `data_overview.npz` and `category.npz` files into the backend database.
- Label proposal endpoints – Support the workflow for categorizing audio files in the frontend by managing label proposals.

### Sound Endpoints

#### GET /api/v1/sounds/overviews

Returns all available data overview entries.

**Response:**

- list of JSON array of `DataOverview` objects

**DataOverview fields:**

| Field                             | Type               | Description                                     |
| --------------------------------- | ------------------ | ----------------------------------------------- |
| `uuid`                            | `string`           | Unique identifier of the audio file             |
| `umap_x`                          | `float`            | UMAP x-coordinate                               |
| `umap_y`                          | `float`            | UMAP y-coordinate                               |
| `umap_z`                          | `float`            | UMAP z-coordinate                               |
| `label`                           | `string`           | Assigned label                                  |
| `category`                        | `string`           | Category name                                   |
| `original_filename`               | `string`           | Original filename                               |
| `source`                          | `string`           | Source of the audio file                        |
| `additional_information`          | `dict[str, str]`   | Additional metadata                             |
| `anomalie_isolation_forest`       | `float`            | Isolation Forest anomaly score                  |
| `anomalie_LOF`                    | `float`            | Local Outlier Factor (LOF) score                |
| `anomalie_isolation_forest_label` | `string`           | Isolation Forest anomaly label                  |
| `anomalie_LOF_label`              | `string`           | LOF anomaly label                               |
| `nearest_neighbors`               | `dict[str, float]` | Mapping of neighboring UUIDs to their distances |

**Errors:**

- 500 - Internal server error

**Example:**

```bash
curl http://localhost:8000/api/v1/sounds/overviews
```

---

#### `GET /api/v1/sounds/overviews/{uuid}`

Returns the data overview for the specified audio file by uuid.

**Path Parameters:**

- `uuid` - UUID of the audio file

**Response:**

- `DataOverview` object

**Errors:**

- 404 - Datapoint {uuid} not found
- 500 - Internal server error

**Example:**

```bash
curl http://localhost:8000/api/v1/sounds/overviews/550e8400-e29b-41d4-a716-446655440000
```

---

#### `GET /api/v1/sounds/audio/{uuid}`

Sends the processed audio file for the specified UUID.

**Path Parameters:**

- `uuid` - UUID of the audio file

**Response:**

- WAV audio file (`audio/wav`)

**Errors:**

- 404 - Audio for {uuid} not found
- 500 - Internal server error

**Example:**

```bash
curl http://localhost:8000/api/v1/sounds/audio/550e8400-e29b-41d4-a716-446655440000 \
  -o audio.wav
```

---

#### `GET /api/v1/sounds/categories`

Returns all available categories.

**Response:**

- JSON array of `CategoryListItem` objects

**CategoryListItem fields:**

| Field  | Type      | Description                       |
| ------ | --------- | --------------------------------- |
| `id`   | `integer` | Unique identifier of the category |
| `key`  | `string`  | Stable category identifier        |
| `name` | `string`  | Display name of the category      |

**Errors:**

- 500 - Internal server error

**Example:**

```bash
curl http://localhost:8000/api/v1/sounds/categories
```

---

#### `GET /api/v1/sounds/categories/{category_id}`

Returns a single category by its ID.

**Path Parameters:**

- `category_id` - Numeric category ID

**Response:**

- `CategoryListItem` object

**Errors:**

- 404 - Category {id} not found
- 500 - Internal server error

**Example:**

```bash
curl http://localhost:8000/api/v1/sounds/categories/1
```

### Import Endpoints

#### POST /api/v1/import/data-overview

Imports data overview entries from an .npz file into the backend database.

The file must contain the generated data overview data in the expected structure.

**Request Body:**

- Content type: multipart/form-data
- Form field: file
- Supported file type: .npz

**Response:**

JSON object containing:

- imported_rows – Number of successfully imported data overview entries
- message – Import status message

**Errors:**

- 400 - The uploaded file is not an .npz file or contains invalid data
- 409 - At least one record already exists or violates a database constraint
- 500 - Internal server error

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/import/data-overview \ -F "file=@data_overview.npz"
```

**Response (200):**

```json
{
  "imported_rows": 120,
  "message": "Data overview import completed."
}
```

---

#### POST /api/v1/import/categories

Imports category entries from an .npz file into the backend database.

The file must contain the generated category data in the expected structure.

**Request Body:**

- Content type: multipart/form-data
- Form field: file
- Supported file type: .npz

**Response:**

JSON object containing:

- imported_rows – Number of successfully imported data overview entries
- message – Import status message

**Errors:**

- 400 - The uploaded file is not an .npz file or contains invalid data
- 409 - At least one category already exists or violates a database constraint
- 500 - Internal server error

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/import/categories \ -F "file=@category.npz"
```

**Response (200):**

```json
{
  "imported_rows": 12,
  "message": "Category import completed."
}
```

### Label Proposal Endpoints

#### Create Label Proposal

`POST /api/v1/sounds/labeled-samples`

Creates a new label proposal for an audio sample.

**Request Body:**

- `uuid` (string) - Audio sample UUID
- `category` (string) - Category key

**Response:**

- `message` (string) - Success message

**Errors:**

- 400 - Invalid UUID or category not found
- 422 - Validation error

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/sounds/labeled-samples \
  -H "Content-Type: application/json" \
  -d '{"uuid": "...", "category": "laugh"}'
```

**Response (200):**

```json
{
  "message": "Received label 'laugh' for sample '...'."
}
```

#### Export Label Proposals

`GET /api/v1/sounds/labeled-samples/export`

Downloads all label proposals as CSV file for download.

**Response:**

- CSV file with columns: `category`, `uuid`, `original_filename`, `source`

**Errors:**

- 500 - Internal server error

**Example:**

```bash
curl http://localhost:8000/api/v1/sounds/labeled-samples/export \
  -o category_proposals.csv
```

## Database

For more information check [LOCAL_START.md](LOCAL_START.md)

### Data Overview

_Benni_

### Category

_Benni_

### Label Proposal

Stores user-submitted labels for audio samples.

**Fields:**

- `technical_key` (BIGINT) - Primary key, auto-generated
- `sample_uuid` (UUID) - Foreign key to data_overview.uuid
- `category_technical_key` (BIGINT) - Foreign key to categories.technical_key
- `created_at` (TIMESTAMP) - When the proposal was created
- `updated_at` (TIMESTAMP) - When the proposal was last updated

**Relations:**

- References `data_overview(uuid)` - The audio sample being labeled
- References `categories(technical_key)` - The proposed category

**Indexes:**

- `idx_label_proposal_sample_uuid` - For finding proposals by sample
- `idx_label_proposal_category_technical_key` - For finding proposals by category

## API Documentation

Interactive API documentation available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
