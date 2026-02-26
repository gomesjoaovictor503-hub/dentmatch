from fastapi import FastAPI
from .database import engine
from . import models
from .routers import dentes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(dentes.router)


@app.get("/")
def root():
    return {"message": "DentMatch API está funcionando 🚀"}
