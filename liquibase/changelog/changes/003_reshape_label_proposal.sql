--liquibase formatted sql

--changeset Lujlia:013-reshape-label-proposal
ALTER TABLE label_proposal
    DROP COLUMN user_id,
    DROP COLUMN file_hash,
    DROP COLUMN display_name,
    ADD COLUMN sample_uuid UUID NOT NULL;

ALTER TABLE label_proposal
    ADD CONSTRAINT fk_label_proposal_sample
        FOREIGN KEY (sample_uuid)
        REFERENCES data_overview (uuid);

--changeset Lujlia:014-create-label-proposal-index-sample-uuid
CREATE INDEX IF NOT EXISTS idx_label_proposal_sample_uuid
    ON label_proposal (sample_uuid);
