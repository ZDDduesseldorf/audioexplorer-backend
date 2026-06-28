## Import APIs

The FastAPI application provides import endpoints for inserting records into the database.

Currently supported imports:

```text
categories
data_overview
```

Both imports support `1..N` records per uploaded `.npz` file.

The endpoints are implemented in:

```text
app/api/import_controller.py
```

## Available Endpoints

```text
POST /api/v1/imports/categories
POST /api/v1/imports/data-overview
```

## Import Flow

The import logic is split into controller, service and repository layers.

```text
Controller
-> receives the uploaded .npz file

Service
-> reads and validates the NumPy arrays
-> builds the insert records

Repository
-> inserts the records into PostgreSQL
```

For `data_overview`, the uploaded file contains `category_keys`.

The database table `data_overview` stores:

```text
category_technical_key
```

Therefore, the related categories must already exist before importing `data_overview`.

## Expected Test Files

The test files are generated with:

```text
scripts/create_sample_import_file.py
```

Run from the project root using Git Bash:

```bash
python -m scripts.create_sample_import_file
```

This creates both test files:

```text
sample_category_import.npz
sample_data_overview_import.npz
```

## Start with Docker Compose

Start the application and database:

```bash
docker compose up --build
```

Or start them in the background:

```bash
docker compose up --build -d
```

After startup, the API documentation is available at:

```text
http://localhost:8000/docs
```

## Import Categories

Import categories first:

```bash
curl -X POST "http://localhost:8000/api/v1/imports/categories" \
  -F "file=@sample_category_import.npz"
```

Expected response:

```json
{
  "imported_rows": 2,
  "message": "Category import completed."
}
```

Verify the imported categories:

```sql
SELECT
    technical_key,
    id,
    category_key,
    display_name,
    created_at,
    updated_at
FROM categories
ORDER BY id;
```

The sample categories should appear:

```text
music
dog
```

## Import Data Overview

After the categories exist, import the data overview records:

```bash
curl -X POST "http://localhost:8000/api/v1/imports/data-overview" \
  -F "file=@sample_data_overview_import.npz"
```

Expected response:

```json
{
  "imported_rows": 2,
  "message": "Data overview import completed."
}
```

Verify the imported data overview records:

```sql
SELECT
    technical_key,
    uuid,
    umap_x,
    umap_y,
    umap_z,
    label,
    category_technical_key,
    filename,
    anomalie_isolation_forest,
    anomalie_lof,
    anomalie_lof_label,
    anomalie_isolation_forest_label,
    created_at,
    updated_at
FROM data_overview
ORDER BY updated_at DESC;
```

## Important Notes

The current imports use normal inserts, not upserts.

This means:

```text
New records       -> insert succeeds
Existing records  -> database constraint error
```

If the same test files are uploaded twice, the second import will fail because of unique constraints.

For repeated tests, delete the sample data first:

```sql
DELETE FROM data_overview
WHERE uuid IN (
    '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a',
    '5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b'
);

DELETE FROM categories
WHERE category_key IN (
    'music',
    'dog'
);
```

The delete order is important because `data_overview` references `categories`.

## Current Scope

Supported:

```text
categories import
data_overview import
```

Not supported yet:

```text
label_proposal import
```