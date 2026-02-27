from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from ..core.security import get_usuario_atual

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verificar_admin(usuario_payload, db):
    user = db.query(models.User).filter(
        models.User.email == usuario_payload["sub"]
    ).first()

    if not user or user.tipo_usuario != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas para administradores"
        )

    return user


# 📋 Listar todos os usuários
@router.get("/usuarios")
def listar_usuarios(
    usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    verificar_admin(usuario, db)

    usuarios = db.query(models.User).all()

    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "telefone": u.telefone,
            "cidade": u.cidade,
            "estado": u.estado,
            "profissao": u.profissao,
            "tipo_usuario": u.tipo_usuario,
            "ativo": u.ativo,
            "criado_em": u.criado_em
        }
        for u in usuarios
    ]


# 🔼 Promover usuário
@router.post("/promover/{user_id}")
def promover_usuario(
    user_id: int,
    usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    verificar_admin(usuario, db)

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.tipo_usuario = "admin"
    db.commit()

    return {"mensagem": "Usuário promovido a administrador"}


# 🔽 Desativar usuário
@router.post("/desativar/{user_id}")
def desativar_usuario(
    user_id: int,
    usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    verificar_admin(usuario, db)

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.ativo = False
    db.commit()

    return {"mensagem": "Usuário desativado com sucesso"}
