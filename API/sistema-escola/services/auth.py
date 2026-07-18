from datetime import timedelta

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import oauth2_schema, settings
from core.security import ALGORITHM, verify_password, get_password_hash, criar_token
from exceptions.user_exceptions import (
    AccessDenied,
    EmailAlreadyRegistered,
    UserNotFoundOrIncorrectPassword,
)
from models import Usuario
from models.session import get_session
from schemas.login import LoginSchema
from schemas.usuario import UsuarioSchema
from services.convite import verificar_convite
from services.user import get_user_by_id_or_none, get_user_by_email_or_none


def verificar_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_info.get("sub"))
        type_token = dict_info.get("type")
    except InvalidTokenError:
        raise AccessDenied
    if type_token != "access":
        raise AccessDenied
    usuario = get_user_by_id_or_none(id_user=id_usuario, session=session)
    if not usuario:
        raise AccessDenied
    return usuario


def verify_refresh_token(
    refresh_token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
):
    try:
        dict_info = jwt.decode(refresh_token, settings.SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get("sub"))
        type_token = dict_info.get("type")
    except InvalidTokenError:
        raise AccessDenied
    if type_token != "refresh":
        raise AccessDenied
    user = get_user_by_id_or_none(id_user=id_user, session=session)
    if not user:
        raise AccessDenied
    return user


def autenticar_usuario(email, senha, session):
    usuario = get_user_by_email_or_none(email=email, session=session)
    if not usuario:
        return False
    elif not verify_password(senha, usuario.senha):
        return False
    return usuario


def create_user(usuario_schema: UsuarioSchema, session: Session) -> Usuario:
    usuario = session.execute(
        select(Usuario).where(Usuario.email == usuario_schema.email)
    ).scalar_one_or_none()
    if usuario:
        raise EmailAlreadyRegistered
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
        return novo_usuario


def login_user(login_schema: LoginSchema, session: Session) -> dict:
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise UserNotFoundOrIncorrectPassword

    return {
        "access_token": criar_token(usuario.id, "access"),
        "refresh_token": criar_token(usuario.id, "refresh", timedelta(days=5)),
    }


def login_user_form(form_data: OAuth2PasswordRequestForm, session: Session) -> dict:
    usuario = autenticar_usuario(form_data.username, form_data.password, session)
    if not usuario:
        raise UserNotFoundOrIncorrectPassword
    access_token = criar_token(usuario.id, "access")
    return {"access_token": access_token, "token_type": "Bearer"}
