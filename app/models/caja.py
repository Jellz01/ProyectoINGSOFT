from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class EstadoCajaEnum(str, enum.Enum):
    ABIERTA = "ABIERTA"
    CERRADA = "CERRADA"

class TipoMovimientoEnum(str, enum.Enum):
    VENTA = "VENTA"
    APERTURA = "APERTURA"
    CIERRE = "CIERRE"
    RETIRO = "RETIRO"
    DEPOSITO = "DEPOSITO"

class Caja(Base):
    """
    Modelo de Caja
    """
    __tablename__ = "cajas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_apertura = Column(DateTime, nullable=False, default=datetime.now)
    fecha_cierre = Column(DateTime, nullable=True)
    monto_inicial = Column(Float, nullable=False)
    monto_final = Column(Float, nullable=True)
    estado = Column(Enum(EstadoCajaEnum), nullable=False, default=EstadoCajaEnum.ABIERTA)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relaciones
    usuario = relationship("Usuario")
    movimientos = relationship("MovimientoCaja", back_populates="caja", cascade="all, delete-orphan")

class MovimientoCaja(Base):
    """
    Modelo de Movimiento de Caja
    """
    __tablename__ = "movimientos_caja"

    id = Column(Integer, primary_key=True, index=True)
    caja_id = Column(Integer, ForeignKey("cajas.id"), nullable=False)
    tipo = Column(Enum(TipoMovimientoEnum), nullable=False)
    monto = Column(Float, nullable=False)
    descripcion = Column(String(255), nullable=True)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=True)

    # Relaciones
    caja = relationship("Caja", back_populates="movimientos")
    venta = relationship("Venta")
