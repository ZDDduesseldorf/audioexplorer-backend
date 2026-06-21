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

    uuid UUID NOT NULL UNIQUE,
    umap_x DOUBLE PRECISION NOT NULL,
    umap_y DOUBLE PRECISION NOT NULL,
    umap_z DOUBLE PRECISION NOT NULL,
    label VARCHAR(255) NOT NULL,
    category_technical_key BIGINT NOT NULL,
    filename TEXT NOT NULL,
    anomalie_isolation_forest DOUBLE PRECISION NOT NULL,
    anomalie_lof DOUBLE PRECISION NOT NULL,
    anomalie_lof_label VARCHAR(255) NOT NULL,
    anomalie_isolation_forest_label VARCHAR(255) NOT NULL,

    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_data_overview_category
        FOREIGN KEY (category_technical_key)
        REFERENCES categories (technical_key)
);

--changeset gerrit:003-create-data-overview-index-category-technical-key
CREATE INDEX IF NOT EXISTS idx_data_overview_category_technical_key
    ON data_overview (category_technical_key);

--changeset gerrit:004-create-data-overview-index-label
CREATE INDEX IF NOT EXISTS idx_data_overview_label
    ON data_overview (label);

--changeset gerrit:005-create-data-overview-index-anomalie-lof-label
CREATE INDEX IF NOT EXISTS idx_data_overview_anomalie_lof_label
    ON data_overview (anomalie_lof_label);

--changeset gerrit:006-create-data-overview-index-anomalie-isolation-forest-label
CREATE INDEX IF NOT EXISTS idx_data_overview_anomalie_isolation_forest_label
    ON data_overview (anomalie_isolation_forest_label);

--changeset gerrit:007-create-label-proposal-table
CREATE TABLE IF NOT EXISTS label_proposal (
    technical_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id VARCHAR(255) NOT NULL,
    file_hash VARCHAR(255) NOT NULL,
    category_technical_key BIGINT NOT NULL,
    display_name VARCHAR(255) NOT NULL,

    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_label_proposal_category
        FOREIGN KEY (category_technical_key)
        REFERENCES categories (technical_key)
);

--changeset gerrit:008-create-label-proposal-index-user-id
CREATE INDEX IF NOT EXISTS idx_label_proposal_user_id
    ON label_proposal (user_id);

--changeset gerrit:009-create-label-proposal-index-file-hash
CREATE INDEX IF NOT EXISTS idx_label_proposal_file_hash
    ON label_proposal (file_hash);

--changeset gerrit:010-create-label-proposal-index-category-technical-key
CREATE INDEX IF NOT EXISTS idx_label_proposal_category_technical_key
    ON label_proposal (category_technical_key);