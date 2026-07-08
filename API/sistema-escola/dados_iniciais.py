from datetime import date

from sqlalchemy.orm import Session

from core.config import settings
from core.security import get_password_hash
from models import Cargo, Turma, Aluno, Usuario
from models.session import SessionLocal


def popular_cargos(session: Session):
    """Funcao para criar um cargo inicial."""
    if session.query(Cargo).count() == 0:
        session.add(Cargo(nome="Diretor"))
        session.commit()
        print("Cargo inicial criado com sucesso!")
    else:
        print("Já existe um cargo no sistema!")


def create_initial_superuser(session: Session):
    """Função para criar primeiro usuário ADMIN."""
    password = settings.INITIAL_PASSWORD
    hash_senha = get_password_hash(password)
    if session.query(Usuario).count() == 0:
        session.add(
            Usuario(
                nome="Omega",
                senha=hash_senha,
                cargo=1,
                email=settings.INITIAL_EMAIL,
                numero="123",
                admin=True,
            )
        )
        session.commit()
        print("Super usuário inicial criado com sucesso!")
    else:
        print("Já existe uma conta inicial no sistema!")


def popular_turmas(session: Session):
    """Funcao para criar uma turma inicial."""
    if session.query(Turma).count() == 0:
        session.add(
            Turma(nome="TurmaZero", serie="Primeiro ano", ano=2026, turno="tarde")
        )
        print("Turma inicial criada com sucesso!")
        session.commit()
    else:
        print("Já existe uma turma no sistema!")


def popular_alunos(session: Session):
    """Funcao para criar um aluno inicial."""
    if session.query(Aluno).count() == 0:
        session.add(
            Aluno(
                nome="Lion-O",
                data_nascimento=date(2011, 7, 29),
                turma=1,
                nome_responsavel="Leona",
                celular_responsavel="21585444721",
            )
        )
        print("Aluno inicial criado com sucesso!")
        session.commit()
    else:
        print("Já existe um aluno no sistema!")


if __name__ == "__main__":
    with SessionLocal() as session:
        popular_cargos(session)
        create_initial_superuser(session)
        popular_turmas(session)
        popular_alunos(session)
