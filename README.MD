[![Python Version](https://img.shields.io/badge/python-3.14-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Linter: Ruff](https://img.shields.io/badge/linter-ruff-black?style=flat-square&logo=ruff)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)

# Sistema Escola

API voltada para auxiliar na administração de secretarias escolares.

---

## Tecnologias

- **FastAPI** — framework web
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL** — banco de dados
- **Alembic** — migrations
- **Pydantic Settings** — configurações via `.env`
- **Argon2** — hash de senha
- **PyJWT** — JWT
- **Docker + Docker Compose** — containerização
- **pytest + testcontainers** — testes de integração com Postgres isolado

---

## Estrutura

```
sistema-escola/
├── alembic/                  # Migrations
├── core/
│   ├── __init__.py
│   ├── authorization.py      # Verificação de autorização por cargo
│   ├── config.py             # Configurações da aplicação
│   ├── security.py           # JWT e autenticação
│   └── crud.py               # Funções auxiliares de CRUD
│
├── exceptions/
│   ├── __init__.py
│   ├── aluno_exceptions.py    # Exceções de domínio de aluno
│   ├── handlers.py            # Registro centralizado dos exception handlers
│   └── nota_exceptions.py     # Exceções de domínio de nota
│
├── models/
│   ├── __init__.py
│   ├── aluno.py                # Model de alunos
│   ├── base.py                 # Base declarativa do SQLAlchemy
│   ├── cargo.py                # Model de cargos
│   ├── convites.py             # Model de convites
│   ├── log.py                  # Model de logs do sistema
│   ├── nota.py                 # Model de notas
│   ├── session.py              # Sessão do banco
│   ├── turma.py                # Model de turmas
│   └── usuario.py              # Model de usuários
│
├── routers/
│   ├── __init__.py
│   ├── auth_routes.py         # Rotas de autenticação
│   └── management_routes.py   # Rotas de gerenciamento
│
├── services/
│   ├── __init__.py
│   ├── aluno.py                # Regras de negócio de aluno
│   ├── cargo.py                # Regras de negócio de cargo
│   ├── convite.py              # Regras de negócio de convite
│   ├── nota.py                 # Regras de negócio de nota
│   └── turma.py                # Regras de negócio de turma
│
├── schemas/
│   ├── aluno/
│   │   ├── __init__.py
│   │   ├── aluno.py           # Schema de aluno
│   │   └── aluno_update.py    # Schema de atualização de aluno
│   │
│   ├── nota/
│   │   ├── nota.py            # Schema de nota
│   │   └── nota_update.py     # Schema de atualização de nota
│   │
│   ├── turma/
│   │   ├── turma.py           # Schema de turma
│   │   └── turma_update.py    # Schema de atualização de turma
│   │
│   ├── __init__.py
│   ├── cargo.py               # Schema de cargo
│   ├── convite.py             # Schema de convite
│   ├── login.py               # Schema de login
│   └── usuario.py             # Schema de usuário
│
├── tests/
│   ├── conftest.py            # Fixtures base do pytest
│   ├── test_auth.py           # Testes de autenticação
│   └── test_management.py     # Testes das rotas de gerenciamento
│
├── dados_iniciais.py          # Seed de dados iniciais
├── main.py                    # Entrypoint da aplicação
├── Dockerfile                 # Imagem Docker da API
├── docker-compose.yml         # Orquestra API + banco
├── .dockerignore
├── .env-exemplo               # Exemplo de variáveis de ambiente
├── .pre-commit-config.yaml    # Configuração do pre-commit
├── alembic.ini
├── requirements.txt           # Dependências do projeto
└── README.md
```

---

## Arquitetura

O projeto segue uma arquitetura em camadas:

- **`routers/`** — recebem a requisição HTTP, chamam o service correspondente e devolvem a resposta. Não acessam o banco diretamente nem tratam exceções de domínio manualmente (isso é feito pelos handlers globais).
- **`services/`** — concentram as regras de negócio: consultas ao banco, validações, criação de logs de auditoria e commits. Nenhum acesso ao banco deve acontecer diretamente nos routers.
- **`exceptions/`** — exceções de domínio (ex: `StudentNotFound`, `GradeNotFound`), levantadas pelos services e tratadas globalmente via `exceptions/handlers.py`, registrado em `main.py`.
- **`models/`** — mapeamento ORM das tabelas, usando a sintaxe `Mapped`/`mapped_column` do SQLAlchemy 2.0.

Ações sensíveis (cadastro, atualização e remoção de registros) geram um registro na tabela `Log`, e a exclusão de alunos é feita via **soft delete** (campo `deletado`), preservando o histórico de auditoria.

---

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/lincolntaranto/API-Sistema-Escola.git
cd sistema-escola
```

### 2. Configure o `.env`

```bash
cp .env-exemplo .env
```

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/sistema_escola
SECRET_KEY=sua_chave_secreta
ACCESS_TOKEN_EXPIRE_MINUTES=30
INITIAL_EMAIL=admin@sistemaescola.com
INITIAL_PASSWORD=sua_senha_inicial
```

---

## Rodando com Docker

### 1. Suba os containers

```bash
docker compose up -d --build
```

### 2. Rode as migrations

```bash
# Migrations
docker compose exec api alembic upgrade head
```

### 3. Popule o banco

```bash
# Seed para dados inciais
docker compose exec api python dados_iniciais.py
```

A documentação interativa estará disponível em `http://localhost:8000/docs`.

---

## Rodando os testes

Os testes usam [testcontainers](https://testcontainers.com/) para subir um Postgres descartável a cada execução. **É necessário ter o Docker 
rodando localmente**.

```bash
pytest
```

Cada teste roda isolado: o banco é limpo (com reset de sequence) entre um teste e outro, e as fixtures cuidam de 
popular cargo/superusuário automaticamente.

---

## Rotas

Todas as rotas da API são versionadas e vivem sob o prefixo `/api/v1`, para permitir mudanças futuras (`/api/v2`) sem quebrar clientes que já dependem do contrato atual.

### Auth — `/api/v1/auth`

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/auth/` | Rota de health-check da autenticação | ❌ |
| POST | `/api/v1/auth/usuarios` | Cria um novo usuário (requer convite) | ❌ |
| POST | `/api/v1/auth/sessions` | Login com email e senha, retorna access e refresh token | ❌ |
| POST | `/api/v1/auth/login-form` | Login via formulário OAuth2 (usado pelo `/docs`) | ❌ |
| PATCH | `/api/v1/auth/sessions` | Gera um novo access token a partir do refresh token | ✅ (refresh token) |

### Management — `/api/v1`

#### Alunos

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/alunos/{id_aluno}` | Consulta um aluno pelo ID | ✅ |
| GET | `/api/v1/alunos` | Lista alunos com filtros (`turma`, `nome`) e paginação (`pagina`, `tamanho`) | ✅ |
| POST | `/api/v1/alunos` | Cadastra um novo aluno | ✅ |
| DELETE | `/api/v1/alunos/{id_aluno}` | Remove um aluno do sistema (soft delete) | ✅ |
| PATCH | `/api/v1/alunos/{id_aluno}` | Atualiza os dados de um aluno | ✅ |

#### Turmas

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/turmas/{id_turma}` | Consulta uma turma pelo ID | ✅ |
| POST | `/api/v1/turmas` | Cadastra uma nova turma | ✅ |
| DELETE | `/api/v1/turmas/{id_turma}` | Remove uma turma do sistema | ✅ |
| PATCH | `/api/v1/turmas/{id_turma}` | Atualiza os dados de uma turma | ✅ |

#### Cargos

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/cargos/{id_cargo}` | Consulta um cargo pelo ID | ✅ |
| POST | `/api/v1/cargos` | Cadastra um novo cargo | ✅ |
| DELETE | `/api/v1/cargos/{id_cargo}` | Remove um cargo do sistema | ✅ |
| PATCH | `/api/v1/cargos/{id_cargo}` | Atualiza os dados de um cargo | ✅ |

#### Notas

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/alunos/{id_aluno}/notas` | Consulta notas de um aluno (filtra por `materia`, `bimestre`, `ano`) | ✅ |
| POST | `/api/v1/notas` | Cadastra uma nova nota | ✅ |
| PATCH | `/api/v1/notas/{id_nota}` | Atualiza uma nota existente | ✅ |

#### Convites

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/api/v1/convites` | Cria um convite para cadastro de usuário | ✅ |

---

## Dados iniciais

O arquivo Python chamado `dados_iniciais.py` popula o banco com um cargo inicial ("Diretor") e um superusuário 
administrador, usando as credenciais definidas em `INITIAL_EMAIL`/`INITIAL_PASSWORD` no `.env`.