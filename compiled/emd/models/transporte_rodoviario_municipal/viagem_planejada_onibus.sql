

SELECT
  *
FROM
  `rj-smtr.projeto_subsidio_sppo.viagem_planejada`

WHERE 
    data <= DATE("2022-12-16")
AND
    data NOT BETWEEN DATE('2023-02-17') AND DATE('2023-02-22') -- Dias do carnaval (pagamento pela média).

