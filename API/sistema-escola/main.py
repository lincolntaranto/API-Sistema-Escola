from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACESS_TOKEN_EXPIRE_MINUTES")
app = FastAPI()

from routes.auth_routes import auth_router
from routes.management_routes import management_router

app.include_router(auth_router)
app.include_router(management_router)

