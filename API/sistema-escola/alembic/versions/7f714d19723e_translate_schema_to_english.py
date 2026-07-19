"""translate schema to english

Revision ID: 7f714d19723e
Revises: 17f351e1289a
Create Date: 2026-07-19 05:33:24.257822

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7f714d19723e"
down_revision: Union[str, Sequence[str], None] = "17f351e1289a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # cargos → roles
    op.rename_table("cargos", "roles")
    op.alter_column("roles", "nome", new_column_name="name")

    # turmas → classrooms
    op.rename_table("turmas", "classrooms")
    op.alter_column("classrooms", "nome", new_column_name="name")
    op.alter_column("classrooms", "serie", new_column_name="school_year")
    op.alter_column("classrooms", "ano", new_column_name="year")
    op.alter_column("classrooms", "turno", new_column_name="shift")
    op.execute("ALTER TYPE turnos RENAME TO shifts")
    op.execute("ALTER TYPE shifts RENAME VALUE 'manha' TO 'morning'")
    op.execute("ALTER TYPE shifts RENAME VALUE 'tarde' TO 'afternoon'")
    op.execute("ALTER TYPE shifts RENAME VALUE 'noite' TO 'night'")

    # alunos → students
    op.rename_table("alunos", "students")
    op.alter_column("students", "nome", new_column_name="name")
    op.alter_column("students", "data_nascimento", new_column_name="birth_date")
    op.alter_column("students", "turma", new_column_name="classroom")
    op.alter_column("students", "nome_responsavel", new_column_name="parents_name")
    op.alter_column("students", "celular_responsavel", new_column_name="guardian_phone")
    op.alter_column("students", "deletado", new_column_name="deleted")

    # usuarios → users
    op.rename_table("usuarios", "users")
    op.alter_column("users", "nome", new_column_name="name")
    op.alter_column("users", "senha", new_column_name="password")
    op.alter_column("users", "cargo", new_column_name="role_id")
    op.alter_column("users", "numero", new_column_name="phone")

    # notas → grades
    op.rename_table("notas", "grades")
    op.alter_column("grades", "id_aluno", new_column_name="student_id")
    op.alter_column("grades", "materia", new_column_name="school_subject")
    op.alter_column("grades", "nota", new_column_name="grade")
    op.alter_column("grades", "bimestre", new_column_name="bimester")
    op.alter_column("grades", "ano", new_column_name="year")

    # convites → invites
    op.rename_table("convites", "invites")
    op.alter_column("invites", "usado", new_column_name="used")

    # logs (tabela já em inglês)
    op.alter_column("logs", "id_usuario", new_column_name="user_id")
    op.alter_column("logs", "id_aluno", new_column_name="student_id")
    op.alter_column("logs", "acao", new_column_name="action")
    op.alter_column("logs", "descricao", new_column_name="description")
    op.alter_column("logs", "data_hora", new_column_name="timestamp")


def downgrade() -> None:
    """Downgrade schema."""
    # logs
    op.alter_column("logs", "timestamp", new_column_name="data_hora")
    op.alter_column("logs", "description", new_column_name="descricao")
    op.alter_column("logs", "action", new_column_name="acao")
    op.alter_column("logs", "student_id", new_column_name="id_aluno")
    op.alter_column("logs", "user_id", new_column_name="id_usuario")

    # invites → convites
    op.alter_column("invites", "used", new_column_name="usado")
    op.rename_table("invites", "convites")

    # grades → notas
    op.alter_column("grades", "year", new_column_name="ano")
    op.alter_column("grades", "bimester", new_column_name="bimestre")
    op.alter_column("grades", "grade", new_column_name="nota")
    op.alter_column("grades", "school_subject", new_column_name="materia")
    op.alter_column("grades", "student_id", new_column_name="id_aluno")
    op.rename_table("grades", "notas")

    # users → usuarios
    op.alter_column("users", "phone", new_column_name="numero")
    op.alter_column("users", "role_id", new_column_name="cargo")
    op.alter_column("users", "password", new_column_name="senha")
    op.alter_column("users", "name", new_column_name="nome")
    op.rename_table("users", "usuarios")

    # students → alunos
    op.alter_column("students", "deleted", new_column_name="deletado")
    op.alter_column("students", "guardian_phone", new_column_name="celular_responsavel")
    op.alter_column("students", "parents_name", new_column_name="nome_responsavel")
    op.alter_column("students", "classroom", new_column_name="turma")
    op.alter_column("students", "birth_date", new_column_name="data_nascimento")
    op.alter_column("students", "name", new_column_name="nome")
    op.rename_table("students", "alunos")

    # classrooms → turmas
    op.execute("ALTER TYPE shifts RENAME VALUE 'morning' TO 'manha'")
    op.execute("ALTER TYPE shifts RENAME VALUE 'afternoon' TO 'tarde'")
    op.execute("ALTER TYPE shifts RENAME VALUE 'night' TO 'noite'")
    op.execute("ALTER TYPE shifts RENAME TO turnos")
    op.alter_column("classrooms", "shift", new_column_name="turno")
    op.alter_column("classrooms", "year", new_column_name="ano")
    op.alter_column("classrooms", "school_year", new_column_name="serie")
    op.alter_column("classrooms", "name", new_column_name="nome")
    op.rename_table("classrooms", "turmas")

    # roles → cargos
    op.alter_column("roles", "name", new_column_name="nome")
    op.rename_table("roles", "cargos")
