from pydantic import BaseModel
from typing import Optional
from app.models.usuario import RolEnum, EstadoEnum

class UsuarioBase(BaseModel):
    """
    Schema base de Usuario
    """
    nombre: str
    usuario: str
    rol: RolEnum

class UsuarioCreate(UsuarioBase):
    """
    Schema para crear Usuario
    """
    password: str

class UsuarioUpdate(BaseModel):
    """
    Schema para actualizar Usuario
    """
    nombre: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[RolEnum] = None
    estado: Optional[EstadoEnum] = None

class UsuarioResponse(UsuarioBase):
    """
    Schema de respuesta de Usuario (sin password)
    """
    id: int
    estado: EstadoEnum

    class Config:
        from_attributes = True
