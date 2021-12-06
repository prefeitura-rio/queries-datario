# Queries template

Esse é um template para um pacote DBT a ser importado no [repositório principal](https://github.com/prefeitura-rio/queries), que irá gerar um servidor RPC para execução dos projetos.

## Como usar esse template

- Faça um fork desse repositório ([docs](https://docs.github.com/pt/get-started/quickstart/fork-a-repo)).
- Modifique o nome do repositório, caso deseje.
- Configure os seguintes secrets no repositório:
  - `GKE_PROJECT`: identificador do projeto no GCP.
  - `GKE_CLUSTER_NAME`: nome do cluster no GKE.
  - `GKE_CLUSTER_ZONE`: zona do cluster no GKE.
  - `GKE_SA_KEY`: credenciais para uma conta de serviço com pleno acesso ao GKE, GCR e GCS. Preencher com o resultado de `cat sua-credencial.json | base64`.
- Modifique o nome do pacote em `dbt_project.yml` para o nome do seu projeto. Aproveite esse momento para ler, com calma, os comentários desse arquivo de configuração.
- [Crie contas de serviço](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) para seus projetos de desenvolvimento e produção. Caso tenha somente um projeto, pode usar a mesma conta para ambos os propósitos. **Nota:** **Jamais** faça commit de suas credenciais.
- Acesse o arquivo `profiles.yml` e se atente aos comentários, eles indicam os campos que devem ser alterados.
- Usando os arquivos de credencial, crie os secrets `credentials-dev` e `credentials-prod` [usando a flag `--from-file`](https://cloud.google.com/kubernetes-engine/docs/concepts/secret#creating_secrets_from_files).
- Faça o upload das alterações realizadas em seu repositório.
- Toda vez que houver uma alteração de código na branch `master`, uma instância atualizada do servidor RPC do DBT será criada em seu cluster, no devido namespace.

### Resources:

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
