from sqlalchemy import Column, Integer, String
from app.database import Base

class Cliente(Base):
    """
    Modelo de Cliente
    """
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(20), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)
