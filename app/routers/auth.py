from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas
from ..core.security import (
    hash_senha,
    verificar_senha,
    criar_token
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existente = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    novo_user = models.User(
        username=user.username,
        senha_hash=hash_senha(user.senha)
    )

    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)

    return {"mensagem": "Usuário criado com sucesso"}


@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verificar_senha(user.senha, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Senha incorreta")

    token = criar_token({"sub": usuario.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
