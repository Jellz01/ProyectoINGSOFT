from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    """
    Schema base de Cliente
    """
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    """
    Schema para crear Cliente
    """
    pass

class ClienteUpdate(BaseModel):
    """
    Schema para actualizar Cliente
    """
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteResponse(ClienteBase):
    """
    Schema de respuesta de Cliente
    """
    id: int

    class Config:
        from_attributes = True
