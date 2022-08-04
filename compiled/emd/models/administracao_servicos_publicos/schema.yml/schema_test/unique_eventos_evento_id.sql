
    
    

select
    evento_id as unique_field,
    count(*) as n_records

from `datario-dev`.`dbt`.`eventos`
where evento_id is not null
group by evento_id
having count(*) > 1


