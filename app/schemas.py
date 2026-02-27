from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

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
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    cidade: str
    estado: str
    profissao: str
    senha: str


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
