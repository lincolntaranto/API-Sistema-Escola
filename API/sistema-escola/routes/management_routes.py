from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.crud import update_model
from models.convites import Convite
from models.log import Log
from models.session import get_session
from models import Usuario, Cargo, Nota
from schemas.aluno.aluno import AlunoSchema
from schemas.aluno.aluno_update import AlunoUpdateSchema
from schemas.cargo import CargoSchema
from schemas.convite import ConviteSchema
from schemas.nota.nota import NotaSchema
from schemas.nota.nota_update import NotaUpdateSchema
from schemas.turma.turma import TurmaSchema
from schemas.turma.turma_update import TurmaUpdateSchema
from core.security import verificar_token, verificar_autorizacao, criar_convite
from services.aluno import (
    consult_student_by_id,
    register_student,
    delete_student,
    update_student,
)
from services.cargo import (
    consult_position,
    register_position,
    delete_position,
    update_position,
)
from services.nota import consult_grade, register_grade
from services.turma import (
    consult_classroom,
    register_classroom,
    delete_classroom,
    update_classroom,
)

management_router = APIRouter(prefix="/management", tags=["management"])


@management_router.get("/alunos")
async def mostrar_alunos(
    id_aluno: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para consultar alunos registrados no sistema."""

    aluno = consult_student_by_id(id_aluno=id_aluno, session=session, usuario=usuario)
    return {
        "nome": aluno.nome,
        "turma": aluno.turma,
        "data_nascimento": aluno.data_nascimento,
        "responsavel": aluno.nome_responsavel,
        "celular_responsavel": aluno.celular_responsavel,
    }


@management_router.post("/cadastrar_aluno")
async def cadastrar_aluno(
    aluno_schema: AlunoSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para cadastrar um aluno no sistema"""

    novo_aluno = register_student(
        aluno_schema=aluno_schema, session=session, usuario=usuario
    )
    return {
        "mensagem": "Aluno cadastrado com sucesso!",
        "id": novo_aluno.id,
        "nome": novo_aluno.nome,
        "turma": novo_aluno.turma,
    }


@management_router.delete("/apagar_aluno")
async def apagar_aluno(
    id_aluno: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para deletar um aluno do sistema"""

    aluno = delete_student(id_aluno=id_aluno, session=session, usuario=usuario)
    return {
        "mensagem": "Aluno deletado com sucesso!",
        "id": aluno.id,
        "nome": aluno.nome,
        "turma": aluno.turma,
    }


@management_router.patch("/atualizar_aluno")
async def atualizar_aluno(
    id_aluno: int,
    aluno_update_schema: AlunoUpdateSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para atualizar um aluno do sistema."""

    aluno = update_student(
        id_aluno=id_aluno,
        aluno_update_schema=aluno_update_schema,
        session=session,
        usuario=usuario,
    )

    return {
        "mensagem": "Aluno atualizado com sucesso!",
        "id": aluno.id,
        "nome": aluno.nome,
    }


@management_router.get("/turmas")
async def mostrar_turmas(
    id_turma: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para consultar turmas no sistema"""

    turma = consult_classroom(id_turma=id_turma, session=session, usuario=usuario)
    return {
        "turma": turma.nome,
        "serie": turma.serie,
        "ano": turma.ano,
        "turno": turma.turno,
    }


@management_router.post("/cadastrar_turma")
async def cadastrar_turma(
    turma_schema: TurmaSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para cadastrar uma turma no sistema"""

    nova_turma = register_classroom(
        turma_schema=turma_schema, session=session, usuario=usuario
    )
    return {
        "mensagem": "Turma cadastrada com sucesso!",
        "id": nova_turma.id,
        "nome": nova_turma.nome,
        "serie": nova_turma.serie,
        "ano": nova_turma.ano,
        "turno": nova_turma.turno,
    }


@management_router.delete("/apagar_turma")
async def apagar_turma(
    id_turma: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para apagar uma turma do sistema."""

    turma = delete_classroom(id_turma=id_turma, session=session, usuario=usuario)
    return {
        "mensagem": "Turma deletada com sucesso!",
        "id": turma.id,
        "nome": turma.nome,
        "serie": turma.serie,
        "turno": turma.turno,
        "ano": turma.ano,
    }


@management_router.patch("/atualizar_turma")
async def atualizar_turma(
    id_turma: int,
    turma_update_schema: TurmaUpdateSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para atualizar uma turma do sistema."""

    turma = update_classroom(
        id_turma=id_turma,
        turma_update_schema=turma_update_schema,
        session=session,
        usuario=usuario,
    )

    return {
        "mensagem": "Turma atualizada com sucesso!",
        "id": turma.id,
        "nome": turma.nome,
        "serie": turma.serie,
        "ano": turma.ano,
        "turno": turma.turno,
    }


@management_router.get("/cargos")
async def mostrar_cargos(
    id_cargo: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para consultar cargos no sistema."""

    cargo = consult_position(id_cargo=id_cargo, session=session, usuario=usuario)
    return {"nome": cargo.nome}


@management_router.post("/cadastrar_cargo")
async def cadastrar_cargo(
    cargo_schema: CargoSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para cadastrar um cargo no sistema."""

    verificar_autorizacao(usuario)
    novo_cargo = register_position(
        cargo_schema=cargo_schema, session=session, usuario=usuario
    )
    return {
        "mensagem": "Cargo cadastrado com sucesso!",
        "id": novo_cargo.id,
        "nome": novo_cargo.nome,
    }


@management_router.delete("/apagar_cargo")
async def apagar_cargo(
    id_cargo: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para apagar um cargo do sistema."""

    verificar_autorizacao(usuario)
    cargo = delete_position(id_cargo=id_cargo, session=session, usuario=usuario)
    return {
        "mensagem": "Cargo deletado com sucesso!",
        "id": cargo.id,
        "nome": cargo.nome,
    }


@management_router.patch("/atualizar_cargo")
async def atualizar_cargo(
    id_cargo: int,
    cargo_schema: CargoSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para atualizar um cargo no sistema."""

    verificar_autorizacao(usuario)
    cargo = update_position(
        id_cargo=id_cargo, cargo_schema=cargo_schema, session=session, usuario=usuario
    )

    return {"mensagem": "Cargo atualizado com sucesso!", "id": cargo.id}


@management_router.get("/notas")
async def mostrar_notas(
    id_aluno: int,
    materia: str,
    bimestre: int,
    ano: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """ "Rota para consultar notas de alunos no sistema."""
    nota = consult_grade(
        id_aluno=id_aluno,
        materia=materia,
        bimestre=bimestre,
        ano=ano,
        session=session,
        usuario=usuario,
    )
    return {
        "nome": nota.id_aluno,
        "ano": nota.ano,
        "materia": nota.materia,
        "bimestre": nota.bimestre,
        "nota": nota.nota,
    }


@management_router.post("/cadastrar_nota")
async def cadastrar_nota(
    nota_schema: NotaSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para cadastrar nota de um aluno no sistema."""

    nova_nota = register_grade(
        nota_schema=nota_schema, session=session, usuario=usuario
    )
    return {
        "mensagem": "Nota cadastrada com sucesso!",
        "id": nova_nota.id,
        "id_aluno": nova_nota.id_aluno,
        "ano": nova_nota.ano,
        "materia": nova_nota.materia,
        "bimestre": nova_nota.bimestre,
        "nota": nova_nota.nota,
    }


@management_router.patch("/atualizar_nota")
async def atualizar_nota(
    id_nota: int,
    nota_update_schema: NotaUpdateSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para atualizar uma nota do sistema."""
    nota = session.get(Nota, id_nota)
    if not nota:
        raise HTTPException(status_code=404, detail="Nota inexistente!")

    update_model(obj=nota, schema=nota_update_schema)

    log = Log(
        id_usuario=usuario.id,
        id_aluno=nota.id_aluno,
        acao="atualizar_nota",
        descricao=f"Nota de ID {nota.id}, da materia {nota.materia} e do bimestre {nota.bimestre}, foi atualizada.",
    )

    session.add(log)
    session.commit()
    session.refresh(nota)

    return {
        "mensagem": "Nota atualizada com sucesso!",
        "id": nota.id,
        "aluno_id": nota.id_aluno,
        "ano": nota.ano,
        "materia": nota.materia,
        "bimestre": nota.bimestre,
        "nota": nota.nota,
    }


@management_router.post("/cadastrar_convite")
async def cadastrar_convite(
    convite_schema: ConviteSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para cadastrar um convite no sistema."""

    verificar_autorizacao(usuario)
    cargo = session.query(Cargo).filter(Cargo.id == convite_schema.id_cargo).first()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo inexistente!")

    novo_convite = Convite()
    session.add(novo_convite)
    session.flush()
    token_convite = criar_convite(convite_schema.id_cargo, novo_convite.id)
    log = Log(
        id_usuario=usuario.id,
        acao="cadastrar_convite",
        descricao=f"Convite para o cargo de ID {convite_schema.id_cargo} foi cadastrado!",
    )
    session.add(log)
    session.commit()
    session.refresh(novo_convite)
    return {
        "mensagem": "Convite criado com sucesso!",
        "convite_token": token_convite,
        "id_cargo": convite_schema.id_cargo,
    }
