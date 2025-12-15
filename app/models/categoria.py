from sqlalchemy import Column, Integer, String
from app.database import Base

class Categoria(Base):
    """
    Modelo de Categoria de productos
    """
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
