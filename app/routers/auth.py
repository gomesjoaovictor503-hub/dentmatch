from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.security import get_usuario_atual
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

    total_users = db.query(models.User).count()

    tipo = "admin" if total_users == 0 else "cliente"

    existente = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_user = models.User(
        nome=user.nome,
        email=user.email,
        telefone=user.telefone,
        cidade=user.cidade,
        estado=user.estado,
        profissao=user.profissao,
        senha_hash=hash_senha(user.senha),
        tipo_usuario=tipo
    )

    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)

    return {
        "mensagem": "Usuário cadastrado com sucesso",
        "tipo_usuario": tipo
    }

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    usuario = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not usuario or not verificar_senha(user.senha, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = criar_token({"sub": usuario.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/me")
def me(usuario = Depends(get_usuario_atual), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == usuario["sub"]
    ).first()

    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "telefone": user.telefone,
        "cidade": user.cidade,
        "estado": user.estado,
        "profissao": user.profissao,
        "tipo_usuario": user.tipo_usuario,
        "ativo": user.ativo,
        "criado_em": user.criado_em
    }
@router.get("/admin-area")
def admin_area(
    usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.email == usuario["sub"]
    ).first()

    if user.tipo_usuario != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas para administradores"
        )

    return {"mensagem": "Bem-vindo à área administrativa"}
@router.post("/promover/{user_id}")
def promover_usuario(
    user_id: int,
    usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    user_admin = db.query(models.User).filter(
        models.User.email == usuario["sub"]
    ).first()

    if user_admin.tipo_usuario != "admin":
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem promover usuários"
        )

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.tipo_usuario = "admin"
    db.commit()

    return {"mensagem": "Usuário promovido a administrador"}
