{{ 
    config(
        materialized='incremental',
        partition_by={
                "field": "data",
                "data_type": "date",
                "granularity": "day"
        },
        unique_key=['data', 'servico'],
        incremental_strategy='insert_overwrite',
        require_partition_filter = true
    )
}}

SELECT
  *
FROM
  `rj-smtr.dashboard_subsidio_sppo.sumario_servico_dia_historico`

WHERE 
    data <= DATE("{{ var("date_range_end") }}")
AND
    (data < DATE('2023-02-17') OR data > DATE('2023-02-22')) -- Dias do carnaval (pagamento pela média).

{% if is_incremental() %}

{% if var("date_range_start") == "None" %}

{% set date_range_start = run_query("SELECT gr FROM (SELECT IF(MAX(data) > DATE('" ~ var("date_range_end") ~ "'), DATE('" ~ var("date_range_end") ~ "'), MAX(data)) AS gr FROM " ~ this ~ " WHERE data >= '2022-06-01')").columns[0].values()[0] %}

{% else %}

{% set date_range_start = var("date_range_start") %}

{% endif %}

AND
    data > DATE("{{ date_range_start }}")

{% endif %}