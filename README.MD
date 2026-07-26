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
│   ├── student_exceptions.py  # Exceções de domínio de aluno
│   ├── role_exceptions.py     # Exceções de domínio de cargo
│   ├── invite_exceptions.py   # Exceções de domínio de convite
│   ├── grade_exceptions.py    # Exceções de domínio de nota
│   ├── classroom_exceptions.py # Exceções de domínio de turma
│   ├── handlers.py            # Registro centralizado dos exception handlers
│   └── user_exceptions.py     # Exceções de domínio de usuário
│
├── models/
│   ├── __init__.py
│   ├── student.py              # Model de alunos
│   ├── base.py                 # Base declarativa do SQLAlchemy
│   ├── role.py                 # Model de cargos
│   ├── invite.py               # Model de convites
│   ├── log.py                  # Model de logs do sistema
│   ├── grade.py                # Model de notas
│   ├── session.py              # Sessão do banco
│   ├── classroom.py            # Model de turmas
│   └── user.py                 # Model de usuários
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py         # Rotas de autenticação
│   └── management_routes.py   # Rotas de gerenciamento
│
├── services/
│   ├── __init__.py
│   ├── student.py              # Regras de negócio de aluno
│   ├── auth.py                 # Regras de negócio de autenticação
│   ├── role.py                 # Regras de negócio de cargo
│   ├── invite.py               # Regras de negócio de convite
│   ├── grade.py                # Regras de negócio de nota
│   ├── classroom.py            # Regras de negócio de turma
│   └── user.py                 # Regras de negócio de usuário
│
├── schemas/
│   ├── student/
│   │   ├── __init__.py
│   │   ├── student.py         # Schema de aluno
│   │   └── student_update.py  # Schema de atualização de aluno
│   │
│   ├── grade/
│   │   ├── grade.py           # Schema de nota
│   │   └── grade_update.py    # Schema de atualização de nota
│   │
│   ├── classroom/
│   │   ├── classroom.py       # Schema de turma
│   │   └── classroom_update.py # Schema de atualização de turma
│   │
│   ├── __init__.py
│   ├── role.py                # Schema de cargo
│   ├── invite.py              # Schema de convite
│   ├── login.py               # Schema de login
│   └── user.py                # Schema de usuário
│
├── tests/
│   ├── conftest.py            # Fixtures base do pytest
│   ├── test_auth.py           # Testes de autenticação
│   └── test_management.py     # Testes das rotas de gerenciamento
│
├── initial_data.py            # Seed de dados iniciais
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

- **`routes/`** — recebem a requisição HTTP, chamam o service correspondente e devolvem a resposta. Não acessam o banco diretamente nem tratam exceções de domínio manualmente (isso é feito pelos handlers globais).
- **`services/`** — concentram as regras de negócio: consultas ao banco, validações, criação de logs de auditoria e commits. Nenhum acesso ao banco deve acontecer diretamente nos routers.
- **`exceptions/`** — exceções de domínio (ex: `StudentNotFound`, `GradeNotFound`), levantadas pelos services e tratadas globalmente via `exceptions/handlers.py`, registrado em `main.py`.
- **`models/`** — mapeamento ORM das tabelas, usando a sintaxe `Mapped`/`mapped_column` do SQLAlchemy 2.0.

Ações sensíveis (cadastro, atualização e remoção de registros) geram um registro na tabela `Log`, e a exclusão de alunos é feita via **soft delete** (campo `deleted`), preservando o histórico de auditoria.

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
# Seed para dados iniciais
docker compose exec api python initial_data.py
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
| POST | `/api/v1/auth/users` | Cria um novo usuário (requer convite) | ❌ |
| POST | `/api/v1/auth/sessions` | Login com email e senha, retorna access e refresh token | ❌ |
| POST | `/api/v1/auth/login-form` | Login via formulário OAuth2 (usado pelo `/docs`) | ❌ |
| PATCH | `/api/v1/auth/sessions` | Gera um novo access token a partir do refresh token | ✅ (refresh token) |

### Management — `/api/v1`

#### Students

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/students/{student_id}` | Consulta um aluno pelo ID | ✅ |
| GET | `/api/v1/students` | Lista alunos com filtros (`classroom`, `name`) e paginação (`page`, `size`) | ✅ |
| POST | `/api/v1/students` | Cadastra um novo aluno | ✅ |
| DELETE | `/api/v1/students/{student_id}` | Remove um aluno do sistema (soft delete) | ✅ |
| PATCH | `/api/v1/students/{student_id}` | Atualiza os dados de um aluno | ✅ |

#### Classrooms

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/classrooms/{classroom_id}` | Consulta uma turma pelo ID | ✅ |
| POST | `/api/v1/classrooms` | Cadastra uma nova turma | ✅ |
| DELETE | `/api/v1/classrooms/{classroom_id}` | Remove uma turma do sistema | ✅ |
| PATCH | `/api/v1/classrooms/{classroom_id}` | Atualiza os dados de uma turma | ✅ |

#### Roles

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/roles/{role_id}` | Consulta um cargo pelo ID | ✅ |
| POST | `/api/v1/roles` | Cadastra um novo cargo | ✅ |
| DELETE | `/api/v1/roles/{role_id}` | Remove um cargo do sistema | ✅ |
| PATCH | `/api/v1/roles/{role_id}` | Atualiza os dados de um cargo | ✅ |

#### Grades

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/api/v1/students/{student_id}/grades` | Consulta notas de um aluno (filtra por `school_subject`, `bimester`, `year`) | ✅ |
| POST | `/api/v1/grades` | Cadastra uma nova nota | ✅ |
| PATCH | `/api/v1/grades/{grade_id}` | Atualiza uma nota existente | ✅ |

#### Invites

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/api/v1/invites` | Cria um convite para cadastro de usuário | ✅ |

---

## Dados iniciais

O arquivo Python chamado `initial_data.py` popula o banco com um cargo inicial ("Diretor") e um superusuário 
administrador, usando as credenciais definidas em `INITIAL_EMAIL`/`INITIAL_PASSWORD` no `.env`.


---

## Decisões Técnicas

### Migração do Bcrypt para Argon2

O projeto iniciou com bcrypt, pois era único algoritmo de hashing de senhas que eu conhecia até então e o único que me 
foi ensinado a usar. Após algum tempo trabalhando no projeto notei que o repositório oficial do FastAPI (criado pelo 
Tiangolo) utilizava Argon2 e incluía uma função para migrar senhas de bcrypt para Argon2. Após essa observação eu 
resolvi pesquisar o porquê de ele ter feito essa migração e quais eram as vantagens. Descobri que:

- O bcrypt é uma tecnologia de 1999 e, apesar de ainda ser seguro, é resistente 
  apenas em custo computacional (CPU), sem controle sobre uso de memória.
- O Argon2 foi o vencedor da Password Hashing Competition (2013–2015) e é 
  atualmente recomendado pela OWASP como primeira escolha para hashing de senhas.
- Por ser memory-hard (exige quantidade configurável de RAM por hash), o Argon2 
  encarece significativamente ataques com GPUs e ASICs, algo que o bcrypt não mitiga.
- O bcrypt trunca silenciosamente senhas com mais de 72 bytes, uma limitação que 
  o Argon2 não possui.

Com base nisso, resolvi migrar o projeto para Argon2id utilizando a biblioteca  `argon2-cffi`, que através da 
interface `PasswordHash.recommended()` já entrega os parâmetros de custo (memória, tempo e paralelismo) recomendados, 
sem que eu precise configurá-los manualmente.

### Arquitetura

Optei por usar uma versão simplificada da arquitetura em camadas pelo fato desse ser um dos primeiros projetos onde
eu estou tentando aplicar uma organização mais séria. Em relação às outras arquiteturas como a Microservices,
Hexagonal, Clean Architecture entre outras, ainda preciso estudá-las mais a fundo, mas pretendo explorá-las em
futuros projetos.

