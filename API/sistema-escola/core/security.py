from core.config import settings

import jwt

from pwdlib import PasswordHash

from datetime import datetime, timedelta, timezone

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
