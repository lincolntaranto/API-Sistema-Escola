import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from core.config import oauth2_schema, settings
from core.security import ALGORITHM, verify_password
from exceptions.user_exceptions import AccessDenied
from models.session import get_session
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
