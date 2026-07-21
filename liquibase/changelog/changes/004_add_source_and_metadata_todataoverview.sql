-liquibase formatted sql

--changeset benedikt:015-add-source-and-metadata-to-data-overview
ALTER TABLE data_overview
ADD COLUMN IF NOT EXISTS source VARCHAR(255) NOT NULL DEFAULT '',
ADD COLUMN IF NOT EXISTS context TEXT NOT NULL DEFAULT '',
ADD COLUMN IF NOT EXISTS location VARCHAR(255) NOT NULL DEFAULT '',
ADD COLUMN IF NOT EXISTS link TEXT NOT NULL DEFAULT '';