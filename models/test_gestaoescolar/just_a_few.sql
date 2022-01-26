{{ config(materialized='table') }}

SELECT
    Denominacao as denominacao,
    Endereco as endereco
FROM `datario.test_gestaoescolar.escola`
LIMIT 1000