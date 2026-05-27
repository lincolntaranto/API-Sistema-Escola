from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.session import get_session
from models import Aluno
from schemas.aluno import AlunoSchema

management_router = APIRouter(prefix="/management", tags=["management"])

@management_router.get("/alunos")
async def mostrar_alunos():
    """"Rota para mostrar a lista de alunos no sistema."""
    return {"mensagem" : "Você acessou a rota de alunos"}

@management_router.post("/cadastrar_aluno")
async def cadastrar_aluno(aluno_schema: AlunoSchema, session: Session = Depends(get_session)):
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
    session.commit()
    session.refresh(novo_aluno)
    return {
        "mensagem": "Aluno cadastrado com sucesso!",
        "id": novo_aluno.id,
        "nome": novo_aluno.nome,
        "turma": novo_aluno.turma
    }
