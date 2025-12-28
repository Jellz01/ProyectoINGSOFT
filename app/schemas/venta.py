from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.venta import EstadoVentaEnum

class DetalleVentaBase(BaseModel):
    """
    Schema base de DetalleVenta
    """
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetalleVentaCreate(DetalleVentaBase):
    """
    Schema para crear DetalleVenta
    """
    pass

class DetalleVentaResponse(DetalleVentaBase):
    """
    Schema de respuesta de DetalleVenta
    """
    id: int
    subtotal: float

    model_config = ConfigDict(from_attributes=True)

class VentaBase(BaseModel):
    """
    Schema base de Venta
    """
    usuario_id: int
    cliente_id: Optional[int] = None

class VentaCreate(VentaBase):
    """
    Schema para crear Venta
    """
    detalles: List[DetalleVentaCreate] = []

class VentaResponse(VentaBase):
    """
    Schema de respuesta de Venta
    """
    id: int
    fecha: datetime
    total: float
    estado: EstadoVentaEnum
    detalles: List[DetalleVentaResponse] = []

    model_config = ConfigDict(from_attributes=True)
