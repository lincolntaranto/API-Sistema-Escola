from datetime import timedelta, datetime, timezone

import jwt

from core.config import settings
from exceptions.user_exceptions import InsufficientPermission

ALGORITHM = "HS256"


def verify_authorization(user):
    if not user.admin:
        raise InsufficientPermission


def create_invite(
    role_id,
    invite_id,
    invite_duration=timedelta(minutes=int(settings.INVITE_EXPIRE_MINUTES)),
):
    expiration_date = datetime.now(timezone.utc) + invite_duration
    dict_info = {"id": str(invite_id), "role": str(role_id), "exp": expiration_date}
    jwt_encoded = jwt.encode(dict_info, settings.SECRET_KEY, ALGORITHM)
    return jwt_encoded
