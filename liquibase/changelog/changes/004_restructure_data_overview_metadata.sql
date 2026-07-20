--liquibase formatted sql

--changeset benedikt:013-rename-filename-to-original-filename
ALTER TABLE data_overview
RENAME COLUMN filename TO original_filename;

--changeset benedikt:014-merge-context-location-into-additionale-information
ALTER TABLE data_overview
ADD COLUMN IF NOT EXISTS additional_information JSONB NOT NULL DEFAULT '{}'::jsonb;

UPDATE data_overview
SET additional_information = jsonb_build_object(
    'context', context,
    'location', location
);

ALTER TABLE data_overview
DROP COLUMN IF EXISTS context,
DROP COLUMN IF EXISTS location;

--changeset benedikt:015-drop-link-column
ALTER TABLE data_overview
DROP COLUMN IF EXISTS link;
