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
│   ├── config.py             # Configurações da aplicação
│   ├── security.py           # JWT, autenticação e autorização
│   └── crud.py               # Funções auxiliares de CRUD
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
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py         # Rotas de autenticação
│   └── management_routes.py   # Rotas de gerenciamento
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
│   ├── conftest.py            # Fixtures base do pytest (banco, client, auth)
│   └── test_auth.py           # Testes de autenticação
│
├── dados_iniciais.py          # Seed de dados iniciais (cargo, superusuário)
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

## Rodando com Docker (recomendado)

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

### Auth — `/auth`

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/criar_conta` | Cria um novo usuário (requer convite) | ❌ |
| POST | `/auth/login` | Login com email e senha, retorna JWT | ❌ |
| POST | `/auth/login-form` | Login via formulário OAuth2 (para o `/docs`) | ❌ |
| GET | `/auth/refresh` | Atualiza o token | ✅ |

### Management — `/management`

#### Alunos

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/management/alunos` | Consulta um aluno pelo ID | ✅ |
| POST | `/management/cadastrar_aluno` | Cadastra um novo aluno | ✅ |
| DELETE | `/management/apagar_aluno` | Remove um aluno do sistema | ✅ |
| PATCH | `/management/atualizar_aluno` | Atualiza os dados de um aluno | ✅ |

#### Turmas

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/management/turmas` | Consulta uma turma pelo ID | ✅ |
| POST | `/management/cadastrar_turma` | Cadastra uma nova turma | ✅ |
| DELETE | `/management/apagar_turma` | Remove uma turma do sistema | ✅ |
| PATCH | `/management/atualizar_turma` | Atualiza os dados de uma turma | ✅ |

#### Cargos

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/management/cargos` | Consulta um cargo pelo ID | ✅ |
| POST | `/management/cadastrar_cargo` | Cadastra um novo cargo | ✅ |
| DELETE | `/management/apagar_cargo` | Remove um cargo do sistema | ✅ |
| PATCH | `/management/atualizar_cargo` | Atualiza os dados de um cargo | ✅ |

#### Notas

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/management/notas` | Consulta notas de um aluno | ✅ |
| POST | `/management/cadastrar_nota` | Cadastra uma nova nota | ✅ |
| PATCH | `/management/atualizar_nota` | Atualiza uma nota existente | ✅ |

#### Convites

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/management/cadastrar_convite` | Cria um convite para cadastro de usuário | ✅ |

---

## Dados iniciais

O arquivo Python chamado `dados_iniciais.py` popula o banco com um cargo inicial ("Diretor") e um superusuário 
administrador, usando as credenciais definidas em `INITIAL_EMAIL`/`INITIAL_PASSWORD` no `.env`.