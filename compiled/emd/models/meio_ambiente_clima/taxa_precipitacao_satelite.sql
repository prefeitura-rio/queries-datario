

SELECT
 * 
FROM `rj-cor.meio_ambiente_clima.taxa_precipitacao_satelite`
WHERE data_particao < CURRENT_DATE('America/Sao_Paulo')
