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
WHERE data BETWEEN "2022-06-01" AND DATE_SUB(DATE("{{ var("run_date") }}"), INTERVAL 1 DAY)