from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal
from ..services.comparador import (
    calcular_score_e_diferencas,
    score_para_percentual,
    classificar_similaridade
)

router = APIRouter(prefix="/dentes", tags=["Dentes"])


# ============================
# DEPENDÊNCIA DE BANCO
# ============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
# CRIAR DENTE
# ============================
@router.post("/", response_model=schemas.DenteResponse)
def criar_dente(dente: schemas.DenteCreate, db: Session = Depends(get_db)):
    novo_dente = models.Dente(**dente.dict())
    db.add(novo_dente)
    db.commit()
    db.refresh(novo_dente)
    return novo_dente


# ============================
# LISTAR DENTES
# ============================
@router.get("/")
def listar_dentes(db: Session = Depends(get_db)):
    return db.query(models.Dente).all()


# ============================
# COMPARAR DENTE
# ============================
@router.get("/comparar/{dente_id}")
def comparar_dente(dente_id: int, db: Session = Depends(get_db)):

    dente_base = db.query(models.Dente).filter(
        models.Dente.id == dente_id
    ).first()

    if not dente_base:
        return {"erro": "Dente não encontrado"}

    todos_dentes = db.query(models.Dente).filter(
        models.Dente.id != dente_id
    ).all()

    ranking = []

    for dente in todos_dentes:

        score, diferencas = calcular_score_e_diferencas(
            dente_base,
            dente
        )

        percentual = score_para_percentual(score)
        classificacao = classificar_similaridade(percentual)

        ranking.append({
            "id": dente.id,
            "marca": dente.marca,
            "modelo": dente.modelo,
            "formato": dente.formato,
            "similaridade": percentual,
            "classificacao": classificacao,
            "diferencas": diferencas
        })

    ranking.sort(
        key=lambda x: x["similaridade"],
        reverse=True
    )

    melhor = ranking[0] if ranking else None

    return {
        "dente_base": {
            "id": dente_base.id,
            "marca": dente_base.marca,
            "modelo": dente_base.modelo,
            "formato": dente_base.formato
        },
        "melhor_equivalente": melhor,
        "ranking": ranking
    }
