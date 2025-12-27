from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductoBase(BaseModel):
    """
    Schema base de Producto
    """
    nombre: str
    codigo: str
    precio_compra: float
    precio_venta: float
    stock: int
    stock_minimo: int
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    """
    Schema para crear Producto
    """
    pass

class ProductoUpdate(BaseModel):
    """
    Schema para actualizar Producto
    """
    nombre: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None

class ProductoResponse(ProductoBase):
    """
    Schema de respuesta de Producto
    """
    id: int
    model_config = ConfigDict(from_attributes=True)
