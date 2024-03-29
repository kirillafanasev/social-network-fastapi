from fastapi import FastAPI
from db.database import database
from app.exceptions.handlers import register_handlers
from routers import home, login, register, find_friends, logout
from api.v1 import find_friends as api_v1_find_friends


def get_application() -> FastAPI:
    application = FastAPI()

    @application.on_event('startup')
    async def starup():
        await database.connect()
        application.state.db = database

    @application.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    application.include_router(home.router)
    application.include_router(login.router)
    application.include_router(register.router)
    application.include_router(find_friends.router)
    application.include_router(logout.router)
    application.include_router(api_v1_find_friends.router)

    register_handlers(application)

    return application


app = get_application()
