from fastapi import FastAPI

from exceptions.handlers import register_exception_handlers
from routes.auth_routes import auth_router
from routes.management_routes import management_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(management_router)
register_exception_handlers(app)
