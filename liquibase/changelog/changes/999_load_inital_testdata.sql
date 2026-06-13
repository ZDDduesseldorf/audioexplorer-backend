--liquibase formatted sql

--changeset gerrit:006-insert-initial-categories
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

--changeset gerrit:007-insert-initial-data-overview
INSERT INTO data_overview (
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
)
VALUES
    (
        '001',
        5.12,
        6.3,
        0,
        'laughing',
        'laugh',
        'a_RA1_01_01__xh6fC2ZfwU_moan.wav',
        58.6,
        59.7,
        'noise'
    ),
    (
        '002',
        2.12,
        9.3,
        0,
        'laughing',
        'laugh',
        'a_RA2_056_XSoJqdPi4Iw_groaning.wav',
        58.6,
        59.7,
        'noise'
    ),
    (
        '003',
        7.12,
        3.3,
        0,
        'laughing',
        'laugh',
        'a_RA2_093_FL1LUiqNITo_oohsound.wav',
        58.6,
        59.7,
        'noise'
    )
ON CONFLICT (uuid) DO UPDATE
SET
    umap_x = EXCLUDED.umap_x,
    umap_y = EXCLUDED.umap_y,
    umap_z = EXCLUDED.umap_z,
    label = EXCLUDED.label,
    category_key = EXCLUDED.category_key,
    filename = EXCLUDED.filename,
    anomalie_isolation_forest = EXCLUDED.anomalie_isolation_forest,
    anomalie_lof = EXCLUDED.anomalie_lof,
    anomalie_label = EXCLUDED.anomalie_label,
    updated_at = CURRENT_TIMESTAMP;