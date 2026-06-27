import bcrypt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.config import settings, oauth2_schema
from models import Usuario, Cargo

from jose import jwt, JWTError

from datetime import datetime, timedelta, timezone

from models.convites import Convite
from models.session import get_session


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), hash.encode("utf-8"))


ALGORITHM = "HS256"


def criar_token(
    id_usuario, duracao_token=timedelta(int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_encoded = jwt.encode(dic_info, settings.SECRET_KEY, ALGORITHM)
    return jwt_encoded


def verificar_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado!")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido!")
    return usuario


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not verificar_senha(senha, usuario.senha):
        return False
    return usuario


def verificar_autorizacao(usuario):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Permissão insuficiente!")


def criar_convite(
    id_cargo, id_convite, duracao_convite=timedelta(int(settings.INVITE_EXPIRE_MINUTES))
):
    data_expiracao = datetime.now(timezone.utc) + duracao_convite
    dict_info = {"id": str(id_convite), "cargo": str(id_cargo), "exp": data_expiracao}
    jwt_encoded = jwt.encode(dict_info, settings.SECRET_KEY, ALGORITHM)
    return jwt_encoded


def verificar_convite(token: str, session: Session):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        id_convite = int(dict_info.get("id"))
        id_cargo = int(dict_info.get("cargo"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Convite invalido!")
    cargo = session.query(Cargo).filter(Cargo.id == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=401, detail="Cargo invalido!")
    usado = (
        session.query(Convite)
        .filter(Convite.id == id_convite, Convite.usado(True))
        .first()
    )
    if usado:
        raise HTTPException(status_code=401, detail="Convite já usado!")
    convite_valido = session.query(Convite).filter(Convite.id == id_convite).first()
    convite_valido.usado = True
    return cargo.id
