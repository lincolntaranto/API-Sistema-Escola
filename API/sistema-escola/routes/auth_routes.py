from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from schemas.login import LoginSchema
from services.auth import (
    verify_refresh_token,
    create_user,
    login_user,
    login_user_form,
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


@auth_router.post("/usuarios")
async def criar_conta(
    usuario_schema: UsuarioSchema, session: Session = Depends(get_session)
):
    novo_usuario = create_user(usuario_schema=usuario_schema, session=session)

    return {
        "mensagem": "usuário cadastrado com sucesso!",
        "id": novo_usuario.id,
        "email": novo_usuario.email,
    }


@auth_router.post("/sessions")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    login_u = login_user(login_schema=login_schema, session=session)

    return {
        "access_token": login_u["access_token"],
        "refresh_token": login_u["refresh_token"],
        "token_type": "Bearer",
    }


@auth_router.post("/login-form")
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    login_f = login_user_form(form_data=dados_formulario, session=session)

    return {"access_token": login_f["access_token"], "token_type": "Bearer"}


@auth_router.patch("/sessions")
async def user_refresh_token(usuario: Usuario = Depends(verify_refresh_token)):
    acess_token = criar_token(usuario.id, "access")
    return {"acess_token": acess_token, "token_type": "Bearer"}
