from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.crud import update_model
from models.convites import Convite
from models.log import Log
from models.session import get_session
from models import Aluno, Usuario, Cargo, Nota
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

    cargo = session.query(Cargo).filter(Cargo.id == id_cargo).first()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo inexistente!")
    log = Log(
        id_usuario=usuario.id,
        acao="consultar_cargo",
        descricao=f"Cargo {cargo.nome}, de ID {cargo.id}, foi consultado.",
    )
    session.add(log)
    session.commit()
    return {"nome": cargo.nome}


@management_router.post("/cadastrar_cargo")
async def cadastrar_cargo(
    cargo_schema: CargoSchema,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(verificar_token),
):
    """Rota para cadastrar um cargo no sistema."""

    verificar_autorizacao(usuario)
    cargo = session.query(Cargo).filter(Cargo.nome == cargo_schema.nome).first()

    if cargo:
        raise HTTPException(status_code=400, detail="Cargo já cadastrado!")
    novo_cargo = Cargo(nome=cargo_schema.nome)
    session.add(novo_cargo)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        acao="cadastrar_cargo",
        descricao=f"Cargo {novo_cargo.nome}, de ID {novo_cargo.id}, foi cadastrado!",
    )
    session.add(log)
    session.commit()
    session.refresh(novo_cargo)
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
    cargo = session.query(Cargo).filter(Cargo.id == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo inexistente!")
    session.delete(cargo)
    log = Log(
        id_usuario=usuario.id,
        acao="deletar_cargo",
        descricao=f"Cargo {cargo.nome}, de ID {cargo.id}, foi deletado.",
    )
    session.add(log)
    session.commit()
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
    cargo = session.get(Cargo, id_cargo)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo inexistente!")
    update_model(obj=cargo, schema=cargo_schema)

    log = Log(
        id_usuario=usuario.id,
        acao="atualizar_cargo",
        descricao=f"Cargo {cargo.nome}, de ID {cargo.id}, foi atualizado.",
    )
    session.add(log)
    session.commit()
    session.refresh(cargo)

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

    aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
    nota = (
        session.query(Nota)
        .filter(
            Nota.aluno == id_aluno,
            Nota.materia == materia,
            Nota.bimestre == bimestre,
            Nota.ano == ano,
        )
        .first()
    )
    if not aluno:
        raise HTTPException(status_code=404, detail="ID de aluno inexistente!")
    if not nota:
        raise HTTPException(
            status_code=404, detail="Esse aluno não possui notas registradas!"
        )
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="consultar_nota",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} teve a nota consultada.",
    )
    session.add(log)
    session.commit()
    return {
        "nome": nota.aluno,
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

    nota = (
        session.query(Nota)
        .filter(
            Nota.aluno == nota_schema.aluno,
            Nota.materia == nota_schema.materia,
            Nota.bimestre == nota_schema.bimestre,
            Nota.ano == nota_schema.ano,
        )
        .first()
    )
    if nota:
        raise HTTPException(
            status_code=400,
            detail=f"A nota de {nota_schema.materia} do bimestre {nota_schema.bimestre}"
            f"já foi cadastrada, se ela foi inserida errada, por favor use a rota"
            f"de atualização para muda-la.",
        )
    nova_nota = Nota(
        aluno=nota_schema.aluno,
        materia=nota_schema.materia,
        nota=nota_schema.nota,
        bimestre=nota_schema.bimestre,
        ano=nota_schema.ano,
    )
    session.add(nova_nota)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        id_aluno=nova_nota.aluno,
        acao="cadastrar_nota",
        descricao=f"Nota de ID {nova_nota.id} da materia {nova_nota.materia}, do bimestre {nova_nota.bimestre} e do ano"
        f" {nova_nota.ano}, foi cadastrada.",
    )
    session.add(log)
    session.commit()
    session.refresh(nova_nota)
    return {
        "mensagem": "Nota cadastrada com sucesso!",
        "id": nova_nota.id,
        "id_aluno": nova_nota.aluno,
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
        id_aluno=nota.aluno,
        acao="atualizar_nota",
        descricao=f"Nota de ID {nota.id}, da materia {nota.materia} e do bimestre {nota.bimestre}, foi atualizada.",
    )

    session.add(log)
    session.commit()
    session.refresh(nota)

    return {
        "mensagem": "Nota atualizada com sucesso!",
        "id": nota.id,
        "aluno_id": nota.aluno,
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
