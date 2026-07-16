from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.config import settings, oauth2_schema
from exceptions.cargo_exceptions import PositionNotFound
from exceptions.invite_exceptions import InvalidInvite
from exceptions.user_exceptions import AccessDenied

import jwt
from jwt import InvalidTokenError

from pwdlib import PasswordHash

from datetime import datetime, timedelta, timezone

from models import Convite
from models.session import get_session
from services.cargo import get_position_by_id_or_none
from services.convite import get_invite_by_id_or_none
from services.user import (
    get_user_by_id_or_none,
    get_user_by_email_or_none,
)

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha enviada com a senha hasheada.

    Args:
        plain_password (str): senha não hasheada enviado pelo usuário.
        hashed_password (str): senha hasheada no BD.

    Returns:
        bool: Retorna True ou False..
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Pega a senha enviada pelo usuário, hasheia e retorna o hash da senha.

    Args:
        password (str): senha enviada pelo usuário.

    Returns:
        str: senha hasheada.
    """
    return password_hash.hash(password)


ALGORITHM = "HS256"


def criar_token(
    id_usuario,
    type_token: str,
    duracao_token=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao, "type": type_token}
    jwt_encoded = jwt.encode(dic_info, settings.SECRET_KEY, ALGORITHM)
    return jwt_encoded


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


def verificar_convite(token: str, session: Session):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        id_convite = int(dict_info.get("id"))
        id_cargo = int(dict_info.get("cargo"))
    except InvalidTokenError:
        raise InvalidInvite
    cargo = get_position_by_id_or_none(id_position=id_cargo, session=session)
    if not cargo:
        raise PositionNotFound
    usado = (
        session.query(Convite).filter(Convite.id == id_convite, Convite.usado).first()
    )
    if usado:
        raise HTTPException(status_code=401, detail="Convite já usado!")
    convite_valido = get_invite_by_id_or_none(id_invite=id_convite, session=session)
    convite_valido.usado = True
    return cargo.id
