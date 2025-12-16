from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class EstadoVentaEnum(str, enum.Enum):
    INICIADA = "INICIADA"
    EN_EDICION = "EN_EDICION"
    PENDIENTE_PAGO = "PENDIENTE_PAGO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"

class Venta(Base):
    """
    Modelo de Venta
    """
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(Enum(EstadoVentaEnum), nullable=False, default=EstadoVentaEnum.INICIADA)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)

    # Relaciones
    usuario = relationship("Usuario")
    cliente = relationship("Cliente")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base):
    """
    Modelo de Detalle de Venta
    """
    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")
