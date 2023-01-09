

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
WHERE data <= DATE("2022-12-16")









AND
    data > DATE("2022-11-30")

