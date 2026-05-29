from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.log import Log
from models.session import get_session
from models import Aluno, Usuario, usuario
from schemas.aluno import AlunoSchema
from security import verificar_token

management_router = APIRouter(prefix="/management", tags=["management"], dependencies=[Depends(verificar_token)])

@management_router.get("/alunos")
async def mostrar_alunos():
    """"Rota para mostrar a lista de alunos no sistema."""
    return {"mensagem" : "Você acessou a rota de alunos"}

@management_router.post("/cadastrar_aluno")
async def cadastrar_aluno(aluno_schema: AlunoSchema, session: Session = Depends(get_session), usuario: Usuario = Depends(verificar_token)):
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
    log = Log(
        id_usuario=usuario.id,
        acao= "cadastrar_aluno",
        descricao=f"Aluno {novo_aluno.nome}, da turma {novo_aluno.turma} foi cadastrado."
    )
    session.add(log)
    session.add(novo_aluno)
    session.commit()
    session.refresh(novo_aluno)
    return {
        "mensagem": "Aluno cadastrado com sucesso!",
        "id": novo_aluno.id,
        "nome": novo_aluno.nome,
        "turma": novo_aluno.turma
    }

@management_router.delete("/apagar_aluno")
async def apagar_aluno(id_aluno: int, session: Session = Depends(get_session), usuario: Usuario = Depends(verificar_token)):
    aluno = session.query(Aluno).filter(Aluno.id == id_aluno).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="ID de aluno inexistente!")
    session.delete(aluno)
    log = Log(
        id_usuario=usuario.id,
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