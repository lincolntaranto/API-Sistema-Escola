from datetime import timedelta

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import oauth2_schema, settings
from core.security import ALGORITHM, verify_password, get_password_hash, create_token
from exceptions.user_exceptions import (
    AccessDenied,
    EmailAlreadyRegistered,
    UserNotFoundOrIncorrectPassword,
)
from models import User
from models.session import get_session
from schemas.login import LoginSchema
from schemas.user import UserSchema
from services.invite import verify_invite
from services.user import get_user_by_id_or_none, get_user_by_email_or_none


def verify_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        user_id = int(dict_info.get("sub"))
        type_token = dict_info.get("type")
    except InvalidTokenError:
        raise AccessDenied
    if type_token != "access":
        raise AccessDenied
    user = get_user_by_id_or_none(user_id=user_id, session=session)
    if not user:
        raise AccessDenied
    return user


def verify_refresh_token(
    refresh_token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
):
    try:
        dict_info = jwt.decode(refresh_token, settings.SECRET_KEY, ALGORITHM)
        user_id = int(dict_info.get("sub"))
        type_token = dict_info.get("type")
    except InvalidTokenError:
        raise AccessDenied
    if type_token != "refresh":
        raise AccessDenied
    user = get_user_by_id_or_none(user_id=user_id, session=session)
    if not user:
        raise AccessDenied
    return user


def authenticate_user(email, password, session) -> User | None:
    user = get_user_by_email_or_none(email=email, session=session)
    if not user:
        return None
    elif not verify_password(password, user.password):
        return None
    return user


def create_user(user_schema: UserSchema, session: Session) -> User:
    user = session.execute(
        select(User).where(User.email == user_schema.email)
    ).scalar_one_or_none()
    if user:
        raise EmailAlreadyRegistered
    else:
        role_id = int(verify_invite(user_schema.invite, session))
        hashed_password = get_password_hash(user_schema.password)
        new_user = User(
            name=user_schema.name,
            password=hashed_password,
            role_id=role_id,
            email=user_schema.email,
            phone=user_schema.phone,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


def login_user(login_schema: LoginSchema, session: Session) -> dict:
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise UserNotFoundOrIncorrectPassword

    return {
        "access_token": create_token(user.id, "access"),
        "refresh_token": create_token(user.id, "refresh", timedelta(days=5)),
    }


def login_user_form(form_data: OAuth2PasswordRequestForm, session: Session) -> dict:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise UserNotFoundOrIncorrectPassword
    access_token = create_token(user.id, "access")
    return {"access_token": access_token, "token_type": "Bearer"}
