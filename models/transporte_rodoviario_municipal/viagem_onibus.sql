{{
    config(
        partition_by={
            "field": "data",
            "data_type": "date",
            "granularity": "day",
        }    
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
WHERE data >= "2022-06-01"

-- {% if is_incremental() %}

-- {% set max_partition = run_query("SELECT gr FROM (SELECT IF(max(data) > CURRENT_DATE('America/Sao_Paulo'), CURRENT_DATE('America/Sao_Paulo'), max(data)) as gr FROM " ~ this ~ ")").columns[0].values()[0] %}

-- AND
--     data > ("{{ max_partition }}")

-- {% endif %}