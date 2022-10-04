{{
    config(
        materialized='incremental',
        unique_key="primary_key",
        partition_by={
            "field": "data_particao",
            "data_type": "date",
            "granularity": "month",
        },
        post_hook='CREATE OR REPLACE TABLE `rj-cor.meio_ambiente_clima_staging.quantidade_agua_precipitavel_satelite_last_partition_datario` AS (SELECT CURRENT_DATETIME("America/Sao_Paulo") AS data_particao)'
    )
}}

SELECT
 * 
FROM `rj-cor.meio_ambiente_clima.quantidade_agua_precipitavel_satelite`

{% if is_incremental() %}

{% set max_partition = run_query(
    "
    SELECT IF(
        max(data_particao) > CURRENT_DATETIME('America/Sao_Paulo'), CURRENT_DATETIME('America/Sao_Paulo'), max(data_particao)
        ) as gr 
    FROM `rj-cor.meio_ambiente_clima_staging.quantidade_agua_precipitavel_satelite_last_partition_datario`
    ").columns[0].values()[0] %}

WHERE
    data_particao >= EXTRACT(DATE FROM SAFE_CAST("{{ max_partition }}" AS DATETIME)) AND
    horario >= SAFE_CAST(CONCAT(EXTRACT(HOUR FROM SAFE_CAST("{{ max_partition }}" AS DATETIME)), ":00:00") AS TIME)

{% endif %}
