[![Python Version](https://img.shields.io/badge/python-3.14-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Linter: Ruff](https://img.shields.io/badge/linter-ruff-black?style=flat-square&logo=ruff)](https://github.com/astral-sh/ruff)

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

---

## Estrutura

```
sistema-escola/
├── alembic/                  # Migrations
├── core/
│   ├── __init__.py
│   ├── config.py             # Configurações da aplicação
│   └── security.py           # JWT, autenticação e autorização
│
├── models/
│   ├── __init__.py
│   ├── aluno.py              # Model de alunos
│   ├── base.py               # Base declarativa do SQLAlchemy
│   ├── cargo.py              # Model de cargos
│   ├── convites.py           # Model de convites
│   ├── log.py                # Model de logs do sistema
│   ├── nota.py               # Model de notas
│   ├── session.py            # Sessão do banco
│   ├── turma.py              # Model de turmas
│   └── usuario.py            # Model de usuários
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py        # Rotas de autenticação
│   └── management_routes.py  # Rotas de gerenciamento
│
├── schemas/
│   ├── aluno/
│   │   ├── __init__.py
│   │   ├── aluno.py          # Schema de aluno
│   │   └── aluno_update.py   # Schema de atualização de aluno
│   │
│   ├── nota/
│   │   ├── nota.py           # Schema de nota
│   │   └── nota_update.py    # Schema de atualização de nota
│   │
│   ├── turma/
│   │   ├── turma.py          # Schema de turma
│   │   └── turma_update.py   # Schema de atualização de turma
│   │
│   ├── __init__.py
│   ├── cargo.py              # Schema de cargo
│   ├── convite.py            # Schema de convite
│   ├── login.py              # Schema de login
│   └── usuario.py            # Schema de usuário
│
├── crud.py                   # Funções auxiliares de CRUD
├── dados_iniciais.py         # Seed de dados iniciais
├── main.py                   # Entrypoint da aplicação
├── .env-exemplo              # Exemplo de variáveis de ambiente
├── .pre-commit-config.yaml   # Configuração do pre-commit
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação principal
```

---

## Rotas

### Auth — `/auth`

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/criar_conta"` | Cria um novo usuário | ❌ |
| POST | `/auth/login` | Login com email e senha, retorna JWT | ❌ |
| POST | `/auth/login-form` | Login via formulário OAuth2 (para o `/docs`) | ❌ |
| GET | `/refresh` | Atualiza o token | ✅ |

### Management — `/management`

#### Alunos

| Método | Rota                          | Descrição                     | Auth |
| ------ | ----------------------------- | ----------------------------- | ---- |
| GET    | `/management/alunos`          | Consulta um aluno pelo ID     | ✅    |
| POST   | `/management/cadastrar_aluno` | Cadastra um novo aluno        | ✅    |
| DELETE | `/management/apagar_aluno`    | Remove um aluno do sistema    | ✅    |
| PATCH  | `/management/atualizar_aluno` | Atualiza os dados de um aluno | ✅    |

#### Turmas

| Método | Rota                          | Descrição                      | Auth |
| ------ | ----------------------------- | ------------------------------ | ---- |
| GET    | `/management/turmas`          | Consulta uma turma pelo ID     | ✅    |
| POST   | `/management/cadastrar_turma` | Cadastra uma nova turma        | ✅    |
| DELETE | `/management/apagar_turma`    | Remove uma turma do sistema    | ✅    |
| PATCH  | `/management/atualizar_turma` | Atualiza os dados de uma turma | ✅    |

#### Cargos

| Método | Rota                          | Descrição                     | Auth |
| ------ | ----------------------------- | ----------------------------- | ---- |
| GET    | `/management/cargos`          | Consulta um cargo pelo ID     | ✅    |
| POST   | `/management/cadastrar_cargo` | Cadastra um novo cargo        | ✅    |
| DELETE | `/management/apagar_cargo`    | Remove um cargo do sistema    | ✅    |
| PATCH  | `/management/atualizar_cargo` | Atualiza os dados de um cargo | ✅    |

#### Notas

| Método | Rota                         | Descrição                   | Auth |
| ------ | ---------------------------- | --------------------------- | ---- |
| GET    | `/management/notas`          | Consulta notas de um aluno  | ✅    |
| POST   | `/management/cadastrar_nota` | Cadastra uma nova nota      | ✅    |
| PATCH  | `/management/atualizar_nota` | Atualiza uma nota existente | ✅    |

#### Convites

| Método | Rota                            | Descrição                                | Auth |
| ------ | ------------------------------- | ---------------------------------------- | ---- |
| POST   | `/management/cadastrar_convite` | Cria um convite para cadastro de usuário | ✅    |


## Dados iniciais

O projeto contem um arquivo python chamado dados_iniciais.py, com ele você
pode popular o banco de dados alguns dados para fins de testes.