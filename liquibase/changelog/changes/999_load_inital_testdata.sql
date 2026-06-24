--liquibase formatted sql

--changeset gerrit:011-insert-initial-categories
INSERT INTO categories (
    id,
    category_key,
    display_name
)
VALUES
    (1, 'laugh', 'lachen'),
    (2, 'cry', 'weinen'),
    (3, 'scream', 'schreien')
ON CONFLICT (category_key) DO UPDATE
SET
    id = EXCLUDED.id,
    display_name = EXCLUDED.display_name,
    updated_at = CURRENT_TIMESTAMP;

--changeset gerrit:012-insert-initial-data-overview
INSERT INTO data_overview (
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
    anomalie_isolation_forest_label
)
VALUES
    (
        '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d',
        5.12,
        6.3,
        0,
        'laughing',
        (
            SELECT technical_key
            FROM categories
            WHERE category_key = 'laugh'
        ),
        'a_RA1_01_01__xh6fC2ZfwU_moan.wav',
        58.6,
        59.7,
        'noise',
        'noise'
    ),
    (
        '2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e',
        2.12,
        9.3,
        0,
        'laughing',
        (
            SELECT technical_key
            FROM categories
            WHERE category_key = 'laugh'
        ),
        'a_RA2_056_XSoJqdPi4Iw_groaning.wav',
        58.6,
        59.7,
        'noise',
        'noise'
    ),
    (
        '3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f',
        7.12,
        3.3,
        0,
        'laughing',
        (
            SELECT technical_key
            FROM categories
            WHERE category_key = 'laugh'
        ),
        'a_RA2_093_FL1LUiqNITo_oohsound.wav',
        58.6,
        59.7,
        'noise',
        'noise'
    )
ON CONFLICT (uuid) DO UPDATE
SET
    umap_x = EXCLUDED.umap_x,
    umap_y = EXCLUDED.umap_y,
    umap_z = EXCLUDED.umap_z,
    label = EXCLUDED.label,
    category_technical_key = EXCLUDED.category_technical_key,
    filename = EXCLUDED.filename,
    anomalie_isolation_forest = EXCLUDED.anomalie_isolation_forest,
    anomalie_lof = EXCLUDED.anomalie_lof,
    anomalie_lof_label = EXCLUDED.anomalie_lof_label,
    anomalie_isolation_forest_label = EXCLUDED.anomalie_isolation_forest_label,
    updated_at = CURRENT_TIMESTAMP;