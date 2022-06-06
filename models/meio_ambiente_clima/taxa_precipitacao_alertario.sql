{{
    config(
        materialized='incremental',
        unique_key="primary_key",
        partition_by={
            "field": "data_particao",
            "data_type": "date",
            "granularity": "month",
        },
        post_hook='CREATE OR REPLACE TABLE `rj-cor.meio_ambiente_clima_staging.taxa_precipitacao_alertario_last_partition_datario` AS (SELECT CURRENT_DATETIME("America/Sao_Paulo") AS data_particao)'
    )
}}

SELECT
 * 
FROM `rj-cor.meio_ambiente_clima.taxa_precipitacao_alertario`
WHERE data_particao < CURRENT_DATE('America/Sao_Paulo')

{% if is_incremental() %}

{% set max_partition = run_query(
    "SELECT DATE(gr) FROM (
        SELECT IF(
            max(data_particao) > CURRENT_DATE('America/Sao_Paulo'), CURRENT_DATE('America/Sao_Paulo'), max(data_particao)
            ) as gr 
        FROM `rj-cor.meio_ambiente_clima_staging.taxa_precipitacao_alertario_last_partition_datario`
        )
    ").columns[0].values()[0] %}

AND
    data_particao > ("{{ max_partition }}")

{% endif %}
