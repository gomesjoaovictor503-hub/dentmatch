from fastapi import FastAPI
from .routers import dentes
from .routers import auth
from .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(dentes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "DentMatch API ativa 🚀"}
