SELECT 
  DATETIME(ts, "America/Sao_Paulo") as ts,
  street,
  subtype,
  confidence,
  reportRating,
  nThumbsUp,
  ST_X(geo) AS long,
  ST_y(geo) AS lat,
FROM `waze-public-dataset.partner_EscritriodeDadosdoRiodeJaneiro.view_alerts_clustered`
WHERE ts > '2021-01-01'
 AND subtype='HAZARD_ON_ROAD_POT_HOLE'