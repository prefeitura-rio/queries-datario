{{
    config(
        materialized='incremental',
        unique_key='id_chamado',
        partition_by={
            "field": "data_particao",
            "data_type": "date",
            "granularity": "month",
        }    
    )
}}

SELECT 
    * except(descricao)
FROM `rj-segovi.adm_central_atendimento_1746.chamado`