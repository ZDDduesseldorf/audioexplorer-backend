--liquibase formatted sql

--changeset gerrit:011-add-nearest-neighbors-to-data-overview
ALTER TABLE data_overview
ADD COLUMN IF NOT EXISTS nearest_neighbors JSONB NOT NULL DEFAULT '{}'::jsonb;