import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from core.config import settings
from dados_iniciais import (
    popular_cargos,
    create_initial_superuser,
    popular_alunos,
    popular_turmas,
)
from main import app
from models.base import Base
from models.session import get_session


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:17", driver="psycopg2") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="session")
def client(test_engine):
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clear_database(test_engine):
    yield
    with Session(test_engine) as session:
        table_names = ", ".join(f'"{t.name}"' for t in Base.metadata.sorted_tables)
        session.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE"))
        session.commit()


@pytest.fixture(autouse=True)
def cargo(test_engine):
    with Session(test_engine) as session:
        popular_cargos(session=session)


@pytest.fixture(autouse=True)
def super_user(test_engine):
    with Session(test_engine) as session:
        create_initial_superuser(session=session)


@pytest.fixture(autouse=True)
def classroom(test_engine):
    with Session(test_engine) as session:
        popular_turmas(session=session)


@pytest.fixture(autouse=True)
def student(test_engine):
    with Session(test_engine) as session:
        popular_alunos(session=session)


@pytest.fixture()
def token(client):
    response = client.post(
        "/auth/login",
        json={
            "email": settings.INITIAL_EMAIL,
            "senha": settings.INITIAL_PASSWORD,
        },
    )
    return response.json()["access_token"]


@pytest.fixture()
def invite(client, token):
    response = client.post(
        "/management/cadastrar_convite",
        json={"id_cargo": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["convite_token"]
