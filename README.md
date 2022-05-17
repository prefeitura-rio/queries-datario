# Queries Datario

Esse repositório contém os modelos do DBT utilizados para disponibilização de dados públicos da Prefeitura da Cidade do Rio de Janeiro no BigQuery.

## Como adicionar dados?

Faça os procedimentos a seguir em uma nova branch com nome descritivo.

1. Caso seja um `dataset-id` já existente, acesse `models/<dataset-id>` e pule para o passo 4.

2. Caso seja um novo `dataset-id`, crie um novo diretório `models/<dataset-id>`.

3. No arquivo `dbt_project.yml` registre o `dataset-id` junto aos já existentes, conforme exemplo abaixo:

```yaml
models:
  emd:
    dataset-id:
      +materialized: view # Materialization type (view, table or incremental)
      +schema: dataset-id # Overrides the default schema (defaults to what is set on profiles.yml)
```

4. Crie os modelos que desejar em `models/<dataset-id>` como, por exemplo, `nome_da_tabela.sql`. Nesses arquivos, adicione o código SQL utilizado para gerar as tabelas desejadas. Quaisquer especificações de particionamento também devem ser inseridas ali.

5. Antes de fazer o merge da branch, garanta que os devidos metadados para a(s) nova(s) tabela(s) estão preenchidos no portal https://meta.dados.rio/, pois somente assim será possível gerar a documentação para publicação.
