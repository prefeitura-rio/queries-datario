{{
    config(
        partition_by={
            "field": "data_particao",
            "data_type": "date",
            "granularity": "year",
        }    
    )
}}

SELECT * FROM `rj-sme.educacao_basica.coc`