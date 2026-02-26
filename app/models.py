from sqlalchemy import Column, Integer, String, Float
from .database import Base


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
