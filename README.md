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

```bash
docker-compose up
```


## API Endpoints

### Sound Endpoints
*Lea*


### Import Endpoints
*Lea*


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

### Data Overview
*Benni*


### Category
*Benni*


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