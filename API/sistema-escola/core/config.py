from fastapi.security import OAuth2PasswordBearer

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    INVITE_EXPIRE_MINUTES: str
    INITIAL_PASSWORD: str
    INITIAL_EMAIL: str

    model_config = {"env_file": ".env"}


settings = Settings()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login-form")
