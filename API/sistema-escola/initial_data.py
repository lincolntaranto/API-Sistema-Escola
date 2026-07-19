from datetime import date

from sqlalchemy.orm import Session

from core.config import settings
from core.security import get_password_hash
from models import Role, Classroom, Student, User
from models.classroom import Shifts
from models.session import SessionLocal


def seed_roles(session: Session):
    """Funcao para criar um cargo inicial."""
    if session.query(Role).count() == 0:
        session.add(Role(name="Diretor"))
        session.commit()
        print("Role inicial criado com sucesso!")
    else:
        print("Já existe um cargo no sistema!")


def create_initial_superuser(session: Session):
    """Função para criar primeiro usuário ADMIN."""
    password = settings.INITIAL_PASSWORD
    hashed_password = get_password_hash(password)
    if session.query(User).count() == 0:
        session.add(
            User(
                name="Omega",
                password=hashed_password,
                role_id=1,
                email=settings.INITIAL_EMAIL,
                phone="123",
                admin=True,
            )
        )
        session.commit()
        print("Super usuário inicial criado com sucesso!")
    else:
        print("Já existe uma conta inicial no sistema!")


def seed_classrooms(session: Session):
    """Funcao para criar uma classroom inicial."""
    if session.query(Classroom).count() == 0:
        session.add(
            Classroom(
                name="TurmaZero",
                school_year="Primeiro year",
                year=2026,
                shift=Shifts.afternoon,
            )
        )
        print("Classroom inicial criada com sucesso!")
        session.commit()
    else:
        print("Já existe uma classroom no sistema!")


def seed_students(session: Session):
    """Funcao para criar um aluno inicial."""
    if session.query(Student).count() == 0:
        session.add(
            Student(
                name="Lion-O",
                birth_date=date(2011, 7, 29),
                classroom=1,
                parents_name="Leona",
                guardian_phone="21585444721",
            )
        )
        print("Aluno inicial criado com sucesso!")
        session.commit()
    else:
        print("Já existe um aluno no sistema!")


if __name__ == "__main__":
    with SessionLocal() as session:
        seed_roles(session)
        create_initial_superuser(session)
        seed_classrooms(session)
        seed_students(session)
