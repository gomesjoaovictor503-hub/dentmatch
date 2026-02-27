from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..services.comparador import calcular_similaridade
from ..core.security import get_usuario_atual

router = APIRouter(
    prefix="/dentes",
    tags=["Dentes"]
)


# 🔹 Dependência de banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Criar dente (protegido)
@router.post("/")
def criar_dente(
    dente: schemas.DenteCreate,
    usuario=Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    novo_dente = models.Dente(**dente.dict())

    db.add(novo_dente)
    db.commit()
    db.refresh(novo_dente)

    return novo_dente


# 🔹 Listar todos os dentes
@router.get("/")
def listar_dentes(
    usuario=Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    return db.query(models.Dente).all()


# 🔥 Comparar dentes (NOVO MOTOR AJUSTADO)
@router.get("/comparar/{dente_id}")
def comparar_dentes(
    dente_id: int,
    usuario=Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):

    dente_base = db.query(models.Dente).filter(
        models.Dente.id == dente_id
    ).first()

    if not dente_base:
        raise HTTPException(status_code=404, detail="Dente não encontrado")

    todos_dentes = db.query(models.Dente).all()

    ranking = []

    for outro in todos_dentes:

        if outro.id == dente_base.id:
            continue

        similaridade = calcular_similaridade(dente_base, outro)

        # Ignora arcada/tipo incompatível
        if similaridade is None:
            continue

        ranking.append({
            "id": outro.id,
            "marca": outro.marca,
            "linha": outro.linha,
            "modelo": outro.modelo,
            "arcada": outro.arcada,
            "tipo": outro.tipo,
            "formato": outro.formato,
            "similaridade": similaridade
        })

    ranking.sort(key=lambda x: x["similaridade"], reverse=True)

    melhor = ranking[0] if ranking else None

    return {
        "dente_base": {
            "id": dente_base.id,
            "marca": dente_base.marca,
            "linha": dente_base.linha,
            "modelo": dente_base.modelo,
            "arcada": dente_base.arcada,
            "tipo": dente_base.tipo,
            "formato": dente_base.formato
        },
        "melhor_equivalente": melhor,
        "ranking": ranking
    }
