from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from schemas.login import LoginSchema
from core.security import (
    get_password_hash,
    autenticar_usuario,
    verify_refresh_token,
    verificar_convite,
)
from core.security import criar_token

from models import Usuario
from models.session import get_session

from schemas.usuario import UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def autenticar():
    """Rota de autenticação"""
    return {"mensagem": "Rota de autenticação"}


@auth_router.post("/criar_conta")
async def criar_conta(
    usuario_schema: UsuarioSchema, session: Session = Depends(get_session)
):
    usuario = (
        session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    )
    if usuario:
        raise HTTPException(status_code=400, detail="email já cadastrado!")
    else:
        cargo = int(verificar_convite(usuario_schema.convite, session))
        senha_criptografada = get_password_hash(usuario_schema.senha)
        novo_usuario = Usuario(
            nome=usuario_schema.nome,
            senha=senha_criptografada,
            cargo=cargo,
            email=usuario_schema.email,
            numero=usuario_schema.numero,
        )
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        return {
            "mensagem": "usuário cadastrado com sucesso!",
            "id": novo_usuario.id,
            "email": novo_usuario.email,
        }


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(
            status_code=400, detail="usuário não encontrado ou senha incorreta."
        )
    else:
        access_token = criar_token(usuario.id, "access")
        refresh_token = criar_token(usuario.id, "refresh", timedelta(days=5))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }


@auth_router.post("/login-form")
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    usuario = autenticar_usuario(
        dados_formulario.username, dados_formulario.password, session
    )
    if not usuario:
        raise HTTPException(
            status_code=400, detail="usuário não encontrado ou senha incorreta."
        )
    else:
        access_token = criar_token(usuario.id, "access")
        return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.get("/refresh")
async def user_refresh_token(usuario: Usuario = Depends(verify_refresh_token)):
    acess_token = criar_token(usuario.id, "access")
    return {"acess_token": acess_token, "token_type": "Bearer"}
