from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.caja import EstadoCajaEnum, TipoMovimientoEnum

class MovimientoCajaBase(BaseModel):
    """
    Schema base de MovimientoCaja
    """
    tipo: TipoMovimientoEnum
    monto: float
    descripcion: Optional[str] = None

class MovimientoCajaCreate(MovimientoCajaBase):
    """
    Schema para crear MovimientoCaja
    """
    pass

class MovimientoCajaResponse(MovimientoCajaBase):
    """
    Schema de respuesta de MovimientoCaja
    """
    id: int
    fecha: datetime
    venta_id: Optional[int] = None

    class Config:
        from_attributes = True

class CajaBase(BaseModel):
    """
    Schema base de Caja
    """
    monto_inicial: float
    usuario_id: int

class CajaCreate(CajaBase):
    """
    Schema para crear Caja (apertura)
    """
    pass

class CajaResponse(CajaBase):
    """
    Schema de respuesta de Caja
    """
    id: int
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime] = None
    monto_final: Optional[float] = None
    estado: EstadoCajaEnum
    movimientos: List[MovimientoCajaResponse] = []

    class Config:
        from_attributes = True
