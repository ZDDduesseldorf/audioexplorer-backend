# Audioexplorer Backend

## Project Initialization

### Short Introduction

Audioexplorer is a web application for exploring and labeling audio samples. The backend provides APIs for data management, audio processing, and label proposals.

### Connected Repos

- **Frontend**: [audioexplorer-frontend](https://github.com/ZDDduesseldorf/audioexplorer-frontend)
- **Data Processor**: [audioexplorer-data-processor](https://github.com/ZDDduesseldorf/audioexplorer-data-processor)

### System-Architecture
The project consists of several services that work together to provide the complete Audioexplorer application.\
The main components are:

- Frontend
- Backend
- PostgreSQL
- Liquibase
- data-processor


#### Frontend
The frontend provides the user interface of the application. It communicates via state management with the backend REST-API and displays the available audio data, metadata and calculated results to the user.\
The frontend is started as a separate container and connects to the backend through the configured API base URL.

#### Backend
The backend is implemented as a Python application.

It provides the API endpoints used by the frontend.

The backend is responsible for:

```text
receiving API requests
validating input data
reading data from the database
writing data to the database
returning API responses to the frontend
```

Database access is handled through the repository layer.

The basic backend structure is:

```text
Controller
-> receives HTTP requests

Service
-> contains application logic

Repository
-> handles database access

Model
-> represents database tables
```


#### PostgreSQL (Database)
PostgreSQL is used as the central database.

The database stores the application data and metadata.

Examples are:

```text
categories
data_overview records
label proposals
related metadata
```

The calculated data points are not primarily calculated by PostgreSQL. They are produced by the separate `data-processor` service.

#### Liquibase 
Liquibase is attached to the backend setup as a sidecar container.

It is responsible for applying database schema changes before the backend starts.

The startup order is:

```text
PostgreSQL starts
-> Liquibase waits for PostgreSQL
-> Liquibase applies database migrations
-> Backend starts after successful migration
```

This ensures that the backend runs against the expected database schema.

#### data-processor
The `data-processor` is a separate batch service.

It is responsible for calculating the data points used by the application.

This keeps the calculation logic separate from the backend API.

The backend focuses on:

```text
API access
validation
database interaction
providing data to the frontend
```

The `data-processor` focuses on:

```text
calculating data points
preparing processed data
batch-oriented processing
```

#### Service-Overview
```text
Frontend
-> provides the user interface
-> communicates with the backend API

Backend
-> provides REST API endpoints
-> reads and writes application data
-> uses services and repositories

PostgreSQL
-> stores application data and metadata

Liquibase
-> applies database migrations
-> runs before the backend starts

data-processor
-> calculates the data points
-> runs separately from the backend API
```
### Installation

If the application is started through containers, Docker Desktop is the required runtime environment.

In this setup, the following services run as containers:

```text
PostgreSQL
Liquibase
Backend
data-processor
```

#### Docker Desktop

Docker Desktop is required to run the containerized services.

It provides:

```text
Docker Engine
Docker Compose
local container runtime
local container networking
volume management
```

The services can then be started with Docker Compose.

Example:

```bash
docker compose up --build
```

Or in detached mode:

```bash
docker compose up --build -d
```

#### Git

Git is required to clone the repositories and work with the project source code.

It is also useful for running the project commands from Git Bash on Windows.

#### Node.js and npm

Because the frontend is not started as a container in this setup, Node.js and npm are required locally for the frontend.

The frontend can then be started separately from the frontend repository.

Example:

```bash
npm install
npm run dev
```

The frontend is not started as a container in this setup.
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

This project uses three data tables to structure the given audio files:

- **Data Overview** stores the metadata of every audio file.
- **Category** holds the fixed set of categories the sounds are clustered into.
- **Label Proposal** stores the user-submitted labels (subcategories).

For more information check [LOCAL_START.md](LOCAL_START.md)

### Data Overview

Stores the metadata of every audio file.

**Fields:**

- `technical_key` (BIGINT) - Primary key, auto-generated
- `uuid` (UUID) - Unique public identifier of the sample
- `umap_x` (FLOAT) - X coordinate of the UMAP embedding
- `umap_y` (FLOAT) - Y coordinate of the UMAP embedding
- `umap_z` (FLOAT) - Z coordinate of the UMAP embedding (not used right now)
- `label` (VARCHAR(255)) - Current label of the sample
- `category_technical_key` (BIGINT) - Foreign key to categories.technical_key
- `original_filename` (TEXT) - Filename of the source audio file
- `source` (VARCHAR(255)) - Origin of the audio file
- `additional_information` (JSONB) - Arbitrary key-value metadata, defaults to `{}`
- `anomalie_isolation_forest` (FLOAT) - Anomaly score of the Isolation Forest
- `anomalie_isolation_forest_label` (VARCHAR(255)) - Anomaly classification of the Isolation Forest
- `anomalie_lof` (FLOAT) - Anomaly score of the Local Outlier Factor
- `anomalie_lof_label` (VARCHAR(255)) - Anomaly classification of the Local Outlier Factor
- `nearest_neighbors` (JSONB) - Nearest neighbors list as UUID-to-distance mapping, defaults to `{}`
- `created_at` (TIMESTAMP) - When the entry was created
- `updated_at` (TIMESTAMP) - When the entry was last updated

**Relations:**

- References `categories(technical_key)` - The category the sample belongs to
- Referenced by `label_proposal(sample_uuid)` - The label proposals for this sample

**Indexes:**

- `idx_data_overview_category_technical_key` - For finding samples by category
- `idx_data_overview_label` - For filtering samples by label
- `idx_data_overview_anomalie_lof_label` - For filtering samples by LOF anomaly classification
- `idx_data_overview_anomalie_isolation_forest_label` - For filtering samples by Isolation Forest anomaly classification

### Category

Holds the fixed set of categories the sounds are clustered into.

**Fields:**

- `technical_key` (BIGINT) - Primary key, auto-generated
- `id` (INTEGER) - Unique business identifier of the category
- `category_key` (VARCHAR(255)) - Unique machine-readable key
- `display_name` (VARCHAR(255)) - Human-readable name
- `created_at` (TIMESTAMP) - When the category was created
- `updated_at` (TIMESTAMP) - When the category was last updated

**Relations:**

- Referenced by `data_overview(category_technical_key)` - The samples assigned to this category
- Referenced by `label_proposal(category_technical_key)` - The proposals suggesting this category

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
