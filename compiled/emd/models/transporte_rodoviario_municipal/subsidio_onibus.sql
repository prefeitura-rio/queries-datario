

SELECT
  * except(valor_penalidade),
  IFNULL(valor_penalidade, 0) as valor_penalidade
FROM
  `rj-smtr.dashboard_subsidio_sppo.sumario_servico_dia_historico`

WHERE 
    data <= DATE("2022-12-16")
AND
    data NOT BETWEEN DATE('2023-02-17') AND DATE('2023-02-22') -- Dias do carnaval (pagamento pela média).

