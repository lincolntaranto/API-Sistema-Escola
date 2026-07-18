from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import get_password_hash
from services.convite import verificar_convite
from exceptions.user_exceptions import UserNotFound, EmailAlreadyRegistered
from models import Usuario
from schemas.usuario import UsuarioSchema


def get_user_by_id(id_user: int, session: Session) -> Usuario:
    user = session.execute(
        select(Usuario).where(Usuario.id == id_user)
    ).scalar_one_or_none()
    if not user:
        raise UserNotFound
    return user


def get_user_by_id_or_none(id_user: int, session: Session) -> Usuario | None:
    user = session.execute(
        select(Usuario).where(Usuario.id == id_user)
    ).scalar_one_or_none()
    if not user:
        return None
    return user


def get_user_by_email_or_none(email: int, session: Session) -> Usuario | None:
    user = session.execute(
        select(Usuario).where(Usuario.email == email)
    ).scalar_one_or_none()
    if not user:
        return None
    return user


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
