{{
    config(
        partition_by={
            "field": "data_particao",
            "data_type": "date",
            "granularity": "month",
        }
    )
}}

SELECT * FROM `rj-segovi.administracao_servicos_publicos_1746.chamado`