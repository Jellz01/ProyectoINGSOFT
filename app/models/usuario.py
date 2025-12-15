from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class RolEnum(str, enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    CAJERO = "CAJERO"
    INVENTARIO = "INVENTARIO"

class EstadoEnum(str, enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class Usuario(Base):
    """
    Modelo de Usuario del sistema
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    usuario = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)
    estado = Column(Enum(EstadoEnum), nullable=False, default=EstadoEnum.ACTIVO)
