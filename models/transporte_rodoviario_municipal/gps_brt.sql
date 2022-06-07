{{
    config(
        materialized='incremental',
        partition_by={
            "field": "data",
            "data_type": "date",
            "granularity": "day",
        }    
    )
}}

SELECT 
    * -- TODO: revisar colunas que serão materializadas
FROM `rj-smtr.br_rj_riodejaneiro_veiculos.gps_brt`
WHERE data < CURRENT_DATE('America/Sao_Paulo')

{% if is_incremental() %}

{% set max_partition = run_query("SELECT gr FROM (SELECT IF(max(data) > CURRENT_DATE('America/Sao_Paulo'), CURRENT_DATE('America/Sao_Paulo'), max(data)) as gr FROM " ~ this ~ ")").columns[0].values()[0] %}

AND
    data > ("{{ max_partition }}")

{% endif %}