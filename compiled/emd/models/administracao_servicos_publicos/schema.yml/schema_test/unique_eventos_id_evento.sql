
    
    

select
    id_evento as unique_field,
    count(*) as n_records

from `datario-dev`.`administracao_servicos_publicos`.`eventos`
where id_evento is not null
group by id_evento
having count(*) > 1


