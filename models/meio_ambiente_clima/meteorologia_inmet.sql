{{
    config(
        partition_by={
            "field": "data_particao",
            "data_type": "date",
            "granularity": "month",
        },
    )
}}

SELECT * FROM `rj-cor.meio_ambiente_clima.meteorologia_inmet`