from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from schemas.login import LoginSchema
from services.auth import (
    verify_refresh_token,
    create_user,
    login_user,
    login_user_form,
)
from core.security import create_token

from models import User
from models.session import get_session

from schemas.user import UserSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def authenticate():
    """Rota de autenticação"""
    return {"mensagem": "Rota de autenticação"}


@auth_router.post("/users")
async def create_account(
    user_schema: UserSchema, session: Session = Depends(get_session)
):
    new_user = create_user(user_schema=user_schema, session=session)

    return {
        "mensagem": "usuário cadastrado com sucesso!",
        "id": new_user.id,
        "email": new_user.email,
    }


@auth_router.post("/sessions")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    login_u = login_user(login_schema=login_schema, session=session)

    return {
        "access_token": login_u["access_token"],
        "refresh_token": login_u["refresh_token"],
        "token_type": "Bearer",
    }


@auth_router.post("/login-form")
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    login_f = login_user_form(form_data=form_data, session=session)

    return {"access_token": login_f["access_token"], "token_type": "Bearer"}


@auth_router.patch("/sessions")
async def user_refresh_token(user: User = Depends(verify_refresh_token)):
    access_token = create_token(user.id, "access")
    return {"access_token": access_token, "token_type": "Bearer"}
