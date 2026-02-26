from pydantic import BaseModel


class DenteCreate(BaseModel):
    marca: str
    linha: str
    modelo: str
    tipo: str
    largura_mm: float
    altura_mm: float
    proporcao: float
    formato: str
    canino_a_canino: float


class DenteResponse(DenteCreate):
    id: int

    class Config:
        orm_mode = True
