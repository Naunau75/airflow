{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM `{{ env_var('GCP_PROJECT_ID') }}.raw_data.users_raw`
)

SELECT
    id as user_id,
    name as full_name,
    lower(email) as email, -- Nettoyage: email en minuscule
    phone,
    website,
    CURRENT_TIMESTAMP() as ingested_at
FROM source
WHERE email IS NOT NULL