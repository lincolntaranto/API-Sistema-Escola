from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.log import Log
from models.session import get_session
from models import Aluno, Usuario, Turma
from schemas.aluno.aluno import AlunoSchema
from schemas.aluno.aluno_update import AlunoUpdateSchema
from schemas.turma.turma import TurmaSchema
from security import verificar_token

management_router = APIRouter(prefix="/management", tags=["management"])

@management_router.get("/alunos")
async def mostrar_alunos(id_aluno: int,
                         session: Session = Depends(get_session),
                         usuario: Usuario = Depends(verificar_token)):
    """"Rota para consultar alunos registrados no sistema."""

    aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="ID de aluno inexistente!")
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="consultar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi consultado."
    )
    session.add(log)
    session.commit()
    return {"nome" : aluno.nome,
            "turma": aluno.turma,
            "data_nascimento" : aluno.data_nascimento,
            "responsavel" : aluno.nome_responsavel,
            "celular_responsavel" : aluno.celular_responsavel}

@management_router.post("/cadastrar_aluno")
async def cadastrar_aluno(aluno_schema: AlunoSchema,
                          session: Session = Depends(get_session),
                          usuario: Usuario = Depends(verificar_token)):

    """Rota para cadastrar um aluno no sistema"""

    aluno= session.query(Aluno).filter(Aluno.nome == aluno_schema.nome,
                                       Aluno.data_nascimento == aluno_schema.data_nascimento,
                                       Aluno.nome_responsavel == aluno_schema.nome_responsavel).first()
    if aluno:
        raise HTTPException(status_code=400, detail="Aluno já cadastrado")
    novo_aluno = Aluno(
        nome=aluno_schema.nome,
        data_nascimento=aluno_schema.data_nascimento,
        turma=aluno_schema.turma,
        nome_responsavel=aluno_schema.nome_responsavel,
        celular_responsavel=aluno_schema.numero_responsavel
    )
    session.add(novo_aluno)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        id_aluno=novo_aluno.id,
        acao= "cadastrar_aluno",
        descricao=f"Aluno {novo_aluno.nome}, da turma {novo_aluno.turma} foi cadastrado."
    )
    session.add(log)
    session.commit()
    session.refresh(novo_aluno)
    return {
        "mensagem": "Aluno cadastrado com sucesso!",
        "id": novo_aluno.id,
        "nome": novo_aluno.nome,
        "turma": novo_aluno.turma
    }

@management_router.delete("/apagar_aluno")
async def apagar_aluno(id_aluno: int,
                       session: Session = Depends(get_session),
                       usuario: Usuario = Depends(verificar_token)):

    """Rota para deletar um aluno do sistema"""

    aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="ID de aluno inexistente!")
    session.delete(aluno)
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="deletar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi deletado."
    )
    session.add(log)
    session.commit()
    return {
        "mensagem": "Aluno deletado com sucesso!",
        "id": aluno.id,
        "nome": aluno.nome,
        "turma": aluno.turma
    }

@management_router.patch("/atualizar_aluno")
async def atualizar_aluno(id_aluno: int,
                          aluno_update_schema: AlunoUpdateSchema,
                          session: Session = Depends(get_session),
                          usuario: Usuario = Depends(verificar_token)
                          ):
    """Rota para atualizar um aluno do sistema."""

    aluno = session.get(Aluno, id_aluno)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno inexistente!")

    if aluno_update_schema.nome is not None:
        aluno.nome = aluno_update_schema.nome
    if aluno_update_schema.data_nascimento is not None:
        aluno.data_nascimento = aluno_update_schema.data_nascimento
    if aluno_update_schema.turma is not None:
        aluno.turma = aluno_update_schema.turma
    if aluno_update_schema.nome_responsavel is not None:
        aluno.nome_responsavel = aluno_update_schema.nome_responsavel
    if aluno_update_schema.numero_responsavel is not None:
        aluno.celular_responsavel = aluno_update_schema.numero_responsavel

    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="atualizar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi atualizado."
    )

    session.add(log)
    session.commit()
    session.refresh(aluno)

    return{
        "mensagem": "Aluno atualizado com sucesso!",
        "id": aluno.id,
        "nome": aluno.nome
    }

@management_router.get("/turmas")
async def mostrar_turmas(id_turma: int,
                         session: Session = Depends(get_session),
                         usuario: Usuario = Depends(verificar_token)):
    """Rota para consultar turmas no sistema"""

    turma = session.query(Turma).filter(Turma.id == id_turma).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma inexistente!")
    log = Log(
        id_usuario=usuario.id,
        #id_turma=turma.id, // adição futura
        acao="consultar_turma",
        descricao=f"Turma {turma.nome}, de ID {turma.id}, foi consultada."
    )
    session.add(log)
    session.commit()
    return{
        "turma": turma.nome,
        "serie": turma.serie,
        "ano": turma.ano,
        "turno": turma.turno
    }

@management_router.post("/cadastrar_turma")
async def cadastrar_turma(turma_schema: TurmaSchema,
                          session: Session = Depends(get_session),
                          usuario: Usuario = Depends(verificar_token)
):
    """Rota para cadastrar uma turma no sistema"""

    turma= session.query(Turma).filter(Turma.nome == turma_schema.nome,
                                       Turma.serie == turma_schema.serie,
                                       Turma.turno == turma_schema.turno).first()
    if turma:
        raise HTTPException(status_code=400, detail="Turma já cadastrada!")
    nova_turma = Turma(
        nome=turma_schema.nome,
        serie=turma_schema.serie,
        ano=turma_schema.ano,
        turno=turma_schema.turno
    )
    session.add(nova_turma)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        acao="cadastrar_turma",
        descricao=f"Turma {nova_turma.nome}, de ID {nova_turma.id}, foi cadastrada!"
    )
    session.add(log)
    session.commit()
    session.refresh(nova_turma)
    return{
        "mensagem": "Turma cadastrada com sucesso!",
        "id": nova_turma.id,
        "nome": nova_turma.nome,
        "serie": nova_turma.serie,
        "ano": nova_turma.ano,
        "turno": nova_turma.turno
    }