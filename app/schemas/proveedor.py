from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProveedorBase(BaseModel):
    """
    Schema base de Proveedor
    """
    nombre: str
    ruc: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    """
    Schema para crear Proveedor
    """
    pass

class ProveedorUpdate(BaseModel):
    """
    Schema para actualizar Proveedor
    """
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorResponse(ProveedorBase):
    """
    Schema de respuesta de Proveedor
    """
    id: int

    model_config = ConfigDict(from_attributes=True)
