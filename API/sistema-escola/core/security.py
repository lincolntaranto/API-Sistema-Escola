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


def create_token(
    user_id,
    type_token: str,
    token_duration=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
):
    expiration_date = datetime.now(timezone.utc) + token_duration
    dic_info = {"sub": str(user_id), "exp": expiration_date, "type": type_token}
    jwt_encoded = jwt.encode(dic_info, settings.SECRET_KEY, ALGORITHM)
    return jwt_encoded
