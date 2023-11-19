{{ 
    config(
        materialized='incremental',
        partition_by={
                "field": "data",
                "data_type": "date",
                "granularity": "day"
        },
        incremental_strategy='insert_overwrite'
    )
}}

SELECT 
    * except(flag_em_operacao, flag_trajeto_correto, flag_trajeto_correto_hist, status)
FROM `rj-smtr.br_rj_riodejaneiro_veiculos.gps_brt`
WHERE data <= DATE("{{ var("date_range_end") }}")

{% if is_incremental() %}

{% if var("date_range_start") == "None" %}

{% set date_range_start = run_query("SELECT gr FROM (SELECT IF(MAX(data) > DATE('" ~ var("date_range_end") ~ "'), DATE('" ~ var("date_range_end") ~ "'), MAX(data)) AS gr FROM " ~ this ~ ")").columns[0].values()[0] %}

{% else %}

{% set date_range_start = var("date_range_start") %}

{% endif %}

AND
    data >= DATE("{{ date_range_start }}")

{% endif %}