# Local Development Setup

This project uses Docker Compose to start the Python application, a PostgreSQL database, and Liquibase for database migrations.

## Services

The local setup consists of three main services:

| Service | Purpose |
|---|---|
| `app` | Runs the Python/FastAPI application |
| `db` | Runs the PostgreSQL database |
| `liquibase` | Executes database migrations against PostgreSQL |

Liquibase is used as a separate migration container. It is not part of the Python application image and not part of the PostgreSQL image.

## Database Configuration

The local PostgreSQL database is started with the following configuration:

```text
Database: python_project
Username: app_user
Password: app_password
Host inside Docker network: db
Host from local machine: localhost
Port from local machine: 5432
```

The application should connect to the database using the internal Docker hostname:

```text
db
```

External tools such as DBeaver should connect through:

```text
localhost:5432
```

## Database Inspection with DBeaver

DBeaver can be used to inspect the local PostgreSQL database with a graphical user interface. This is useful for checking created tables, viewing inserted test data, running SQL queries, and verifying Liquibase migrations.

DBeaver is not required to run the application. It is only a development tool for manually accessing the database.

After the Docker Compose stack has been started, DBeaver can connect to PostgreSQL through the exposed local port:

```text
localhost:5432
```

The exact connection settings are described in the section **Connect with DBeaver** below.

## Start the Application Stack

Start all services with:

```bash
docker compose up --build
```

This starts the services in the following order:

1. PostgreSQL database starts.
2. Docker Compose waits until PostgreSQL is healthy.
3. Liquibase runs the database changelogs.
4. The Python application starts after Liquibase completed successfully.

## Liquibase Migration Mechanism

Liquibase executes the changelog defined in:

```text
liquibase/changelog/db.changelog-master.yaml
```

The master changelog includes the SQL migration files from:

```text
liquibase/changelog/changes/
```

Example:

```yaml
databaseChangeLog:
  - include:
      file: changes/001_create_initial_tables.sql
      relativeToChangelogFile: true

  - include:
      file: changes/002_insert_sample_data.sql
      relativeToChangelogFile: true
```

Each SQL migration file must use the Liquibase formatted SQL syntax.

Example:

```sql
--liquibase formatted sql

--changeset gerrit:001-create-categories-table
CREATE TABLE IF NOT EXISTS categories (
    technical_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id INTEGER NOT NULL UNIQUE,
    category_key VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Important format rules:

```text
Correct: --changeset gerrit:001-create-categories-table
Wrong:   --changeset:001-create-categories-table
Wrong:   -- changeset gerrit:001-create-categories-table
```

A changeset consists of:

```text
author:id
```

Example:

```text
gerrit:001-create-categories-table
```

Liquibase stores executed changesets in the database table:

```text
databasechangelog
```

Liquibase also uses the following lock table:

```text
databasechangeloglock
```

These tables are created automatically by Liquibase.

## Run Liquibase Manually

If the database is already running and only the migrations should be executed again, run:

```bash
docker compose run --rm liquibase
```

Liquibase only executes changesets that have not been executed yet.

## Connect with DBeaver

After starting the stack with:

```bash
docker compose up --build
```

open DBeaver and create a new PostgreSQL connection.

Use the following connection settings:

```text
Database Type: PostgreSQL
Host: localhost
Port: 5432
Database: python_project
Username: app_user
Password: app_password
```

If `localhost` does not work, use:

```text
127.0.0.1
```

Before connecting, verify that the PostgreSQL container is running:

```bash
docker ps
```

The port mapping should contain:

```text
0.0.0.0:5432->5432/tcp
```

In DBeaver, after connecting, the following tables should be visible:

```text
categories
data_overview
databasechangelog
databasechangeloglock
```

## Verify the Database Content

You can verify the database content either in DBeaver or directly through the PostgreSQL container.

Open a psql session:

```bash
docker exec -it python-project-postgres psql -U app_user -d python_project
```

List tables:

```sql
\dt
```

Check categories:

```sql
SELECT * FROM categories;
```

Check data overview records:

```sql
SELECT
    technical_key,
    uuid,
    umap_x,
    umap_y,
    umap_z,
    label,
    category_key,
    filename,
    anomalie_isolation_forest,
    anomalie_lof,
    anomalie_label
FROM data_overview;
```

Check executed Liquibase changesets:

```sql
SELECT
    id,
    author,
    filename,
    dateexecuted,
    orderexecuted
FROM databasechangelog
ORDER BY orderexecuted;
```

## Stop the Stack

Stop all running containers:

```bash
docker compose down
```

This keeps the PostgreSQL volume and therefore keeps the database data.

## Reset the Database

To fully reset the local database, including all tables and data, run:

```bash
docker compose down -v
docker compose up --build
```

The `-v` option removes the Docker volume used by PostgreSQL.

Use this only when the local database should be recreated from scratch.

## Add a New Migration

To add a new database change:

1. Create a new SQL file in:

```text
liquibase/changelog/changes/
```

Example:

```text
003_add_new_column.sql
```

2. Add the Liquibase formatted SQL header:

```sql
--liquibase formatted sql

--changeset gerrit:003-add-new-column
ALTER TABLE data_overview
ADD COLUMN example_column VARCHAR(255);
```

3. Include the new file in:

```text
liquibase/changelog/db.changelog-master.yaml
```

Example:

```yaml
databaseChangeLog:
  - include:
      file: changes/001_create_initial_tables.sql
      relativeToChangelogFile: true

  - include:
      file: changes/999_load_inital_testdata.sql
      relativeToChangelogFile: true
```

4. Run Liquibase:

```bash
docker compose run --rm liquibase
```

## Important Migration Rules

Do not edit already executed changesets after they have been applied to a database.

Liquibase tracks checksums for executed changesets. If an already executed changeset is changed afterwards, Liquibase may report a checksum validation error.

Instead of editing old changesets, create a new migration file with a new changeset ID.

Good:

```text
001_create_initial_tables.sql
002_insert_sample_data.sql
003_add_new_column.sql
004_update_column_type.sql
```

Bad:

```text
Changing 001_create_initial_tables.sql after it was already executed
```

## Troubleshooting

### Liquibase cannot find the PostgreSQL driver

Error example:

```text
Cannot find database driver: org.postgresql.Driver
```

This means the Liquibase container does not have the PostgreSQL JDBC driver available.

The Liquibase image should include the PostgreSQL JDBC driver or define it explicitly in the Liquibase Dockerfile.

### Liquibase does not recognize the SQL changelog

Error example:

```text
Formatted SQL changelogs require known formats
```

Check that every SQL migration file starts with:

```sql
--liquibase formatted sql
```

Also check that every changeset uses this format:

```sql
--changeset gerrit:001-some-description
```

### DBeaver cannot connect

Check whether the database container is running:

```bash
docker ps
```

Check whether port `5432` is exposed:

```text
0.0.0.0:5432->5432/tcp
```

If port `5432` is already used locally, change the port mapping in `docker-compose.yml`, for example:

```yaml
ports:
  - "5433:5432"
```

Then connect through DBeaver with:

```text
Host: localhost
Port: 5433
Database: python_project
Username: app_user
Password: app_password
```

### Database already contains old state

If the database contains old tables, old data, or broken Liquibase state, reset the local volume:

```bash
docker compose down -v
docker compose up --build
```

This removes the local PostgreSQL data volume and creates a fresh database.