
SELECT 
    *
FROM `rj-sme.educacao_basica.aluno_turma`
WHERE data_particao < CURRENT_DATE('America/Sao_Paulo')

