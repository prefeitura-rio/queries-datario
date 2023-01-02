{{ 
    config(
        materialized='incremental',
        partition_by={
                "field": "data",
                "data_type": "date",
                "granularity": "day"
        },
        unique_key=['id_viagem'],
        incremental_strategy='insert_overwrite'
    )
}}

SELECT 
    data,
    consorcio,
    tipo_dia,
    id_empresa,
    id_veiculo,
    id_viagem,
    servico_informado as servico,
    shape_id,
    sentido,
    datetime_partida,
    datetime_chegada,
    tempo_viagem,
    distancia_planejada,
    perc_conformidade_shape,
    perc_conformidade_registros,
    versao_modelo
FROM rj-smtr.projeto_subsidio_sppo.viagem_completa 
WHERE data <= DATE_SUB(DATE("{{ var("date_range_end") }}"), INTERVAL 1 DAY)

{% if is_incremental() %}

{% if var("date_range_start") == "None" %}

{% set date_range_start = run_query("SELECT gr FROM (SELECT IF(MAX(data) > DATE_SUB(DATE('" ~ var("date_range_end") ~ "'), INTERVAL 1 DAY), DATE_SUB(DATE('" ~ var("date_range_end") ~ "'), INTERVAL 1 DAY), MAX(data)) AS gr FROM " ~ this ~ ")").columns[0].values()[0] %}

{% else %}

{% set date_range_start = var("date_range_start") %}

{% endif %}

AND
    data > DATE("{{ date_range_start }}")

{% endif %}