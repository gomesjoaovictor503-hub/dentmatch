from sqlalchemy import Column, Integer, String, Float
from .database import Base
from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class Dente(Base):
    __tablename__ = "dentes"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    linha = Column(String)
    modelo = Column(String)
    tipo = Column(String)  # incisivo, canino etc

    largura_mm = Column(Float)
    altura_mm = Column(Float)
    proporcao = Column(Float)
    formato = Column(String)  # oval, triangular, quadrado
    canino_a_canino = Column(Float)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    telefone = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    profissao = Column(String, nullable=False)

    senha_hash = Column(String, nullable=False)

    tipo_usuario = Column(String, default="cliente")
    ativo = Column(Boolean, default=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
