from datetime import timedelta, datetime, timezone

import jwt

from core.config import settings
from exceptions.user_exceptions import InsufficientPermission

ALGORITHM = "HS256"


def verificar_autorizacao(usuario):
    if not usuario.admin:
        raise InsufficientPermission


def criar_convite(
    id_cargo,
    id_convite,
    duracao_convite=timedelta(minutes=int(settings.INVITE_EXPIRE_MINUTES)),
):
    data_expiracao = datetime.now(timezone.utc) + duracao_convite
    dict_info = {"id": str(id_convite), "cargo": str(id_cargo), "exp": data_expiracao}
    jwt_encoded = jwt.encode(dict_info, settings.SECRET_KEY, ALGORITHM)
    return jwt_encoded
