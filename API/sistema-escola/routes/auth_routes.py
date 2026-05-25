from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from security import hash_senha
from models import Usuario
from models.session import get_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """Rota de autenticação"""
    return {"mensagem" : "Rota de autenticação"}

@auth_router.post("/criar_conta")
async def criar_conta(nome: str, senha: str, cargo: int, email: str, numero: str, session: Session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado!")
    else:
        senha_criptografada = hash_senha(senha)
        novo_usuario = Usuario(nome = nome, senha = senha_criptografada, cargo = cargo, email = email, numero = numero)
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        return {
            "mensagem": "usuário cadastrado com sucesso!",
            "id": novo_usuario.id
            "email": novo_usuario.email
        }