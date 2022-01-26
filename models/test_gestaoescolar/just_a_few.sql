{{ config(materialized='table') }}

SELECT
    Denominacao as denominacao,
    Endereco as endereco
FROM `datario.test_gestaoescolar_staging.escola`
LIMIT 1000