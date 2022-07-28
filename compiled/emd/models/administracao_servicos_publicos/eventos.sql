

SELECT
    *
FROM `rj-cor.administracao_servicos_publicos.eventos`
WHERE data_particao < CURRENT_DATE('America/Sao_Paulo')

