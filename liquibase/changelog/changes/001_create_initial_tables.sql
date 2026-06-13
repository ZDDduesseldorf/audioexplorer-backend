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

--changeset gerrit:002-create-data-overview-table
CREATE TABLE IF NOT EXISTS data_overview (
    technical_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    uuid VARCHAR(255) NOT NULL UNIQUE,
    umap_x DOUBLE PRECISION NOT NULL,
    umap_y DOUBLE PRECISION NOT NULL,
    umap_z DOUBLE PRECISION NOT NULL,
    label VARCHAR(255) NOT NULL,
    category_key VARCHAR(255) NOT NULL,
    filename TEXT NOT NULL,
    anomalie_isolation_forest DOUBLE PRECISION NOT NULL,
    anomalie_lof DOUBLE PRECISION NOT NULL,
    anomalie_label VARCHAR(255) NOT NULL,

    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_data_overview_category
        FOREIGN KEY (category_key)
        REFERENCES categories (category_key)
);

--changeset gerrit:003-create-data-overview-index-category
CREATE INDEX IF NOT EXISTS idx_data_overview_category_key
    ON data_overview (category_key);

--changeset gerrit:004-create-data-overview-index-label
CREATE INDEX IF NOT EXISTS idx_data_overview_label
    ON data_overview (label);

--changeset gerrit:005-create-data-overview-index-anomalie-label
CREATE INDEX IF NOT EXISTS idx_data_overview_anomalie_label
    ON data_overview (anomalie_label);