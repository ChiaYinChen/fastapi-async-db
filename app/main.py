"""Main app."""
from fastapi import FastAPI

from .api import hello, login, user
from .db.base_class import metadata
from .db.session import database, engine

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(hello.router)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(login.router, tags=["login"])
