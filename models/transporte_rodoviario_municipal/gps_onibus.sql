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
    * except(flag_em_operacao, flag_trajeto_correto, flag_trajeto_correto_hist, status)
FROM `rj-smtr.br_rj_riodejaneiro_veiculos.gps_sppo`
WHERE data < "2022-07-16"

-- {% if is_incremental() %}

-- {% set max_partition = run_query("SELECT gr FROM (SELECT IF(max(data) > CURRENT_DATE('America/Sao_Paulo'), CURRENT_DATE('America/Sao_Paulo'), max(data)) as gr FROM " ~ this ~ ")").columns[0].values()[0] %}

-- AND
--     data > ("{{ max_partition }}")

-- {% endif %}