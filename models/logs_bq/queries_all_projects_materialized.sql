{{
    config(
        partition_by={
            "field": "date",
            "data_type": "date",
            "granularity": "month",
        }
    )
}}

SELECT 
    * 
FROM `datario.logs_bq.queries_all_projects`
