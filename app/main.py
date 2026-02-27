from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, dentes, admin
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DentMatch API")

app.include_router(auth.router)
app.include_router(dentes.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "DentMatch API ativa"}
