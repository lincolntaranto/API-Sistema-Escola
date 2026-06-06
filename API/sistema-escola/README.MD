# Sistema escola

API voltada para auxiliar na administração de secretarias escolares.

## Como usar?

- Clone o repositório
- Rode o comando: ```pip install -r requirements.txt``` para instalar as  dependências
- Configure o arquivo .env seguindo como base o arquivo .env-exemplo
- Rode o comando ```alembic upgrade head```
- Inicie o uvicorn
- Rode o arquivo dados_iniciais.py (opcional)

## Iniciando o uvicorn

```shell
uvicorn main:app --reload
```

## Principais tecnologias usadas

- FastAPI (para criação da API)
- Alembic (Para migração do banco de dados)
- Bcrypt (Para criptografia das senhas)
- Uvicorn
- Psycopg2 (Para funcionar com o PostgreSQL)

## Rotas

### Rotas de autenticação

- /criar_conta
- /login
- /login-form
- /refresh

### Rotas de gerenciamento

#### Alunos

- /management/alunos
- /management/cadastrar_aluno
- /management/apagar_aluno
- /management/atualizar_ano

#### Turmas

- /management/turmas
- /management/cadastrar_turma
- /management/apagar_turma
- /management/atualizar_turma

#### Cargos

- /management/cargos
- /management/cadastrar_cargo
- /management/apagar_cargo
- /management/atualizar_cargo

#### Notas

- /management/notas
- /management/cadastrar_nota
- /management/atualizar_nota

## Dados iniciais

O projeto contem um arquivo python chamado dados_iniciais.py, com ele você
pode popular o banco de dados alguns dados para fins de testes.