

SELECT
 * 
FROM `rj-cor.meio_ambiente_clima.meteorologia_inmet`
WHERE data_particao < CURRENT_DATE('America/Sao_Paulo')

