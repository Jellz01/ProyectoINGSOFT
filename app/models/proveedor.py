from sqlalchemy import Column, Integer, String
from app.database import Base

class Proveedor(Base):
    """
    Modelo de Proveedor
    """
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ruc = Column(String(20), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)
