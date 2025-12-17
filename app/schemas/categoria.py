from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    """
    Schema base de Categoria
    """
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    """
    Schema para crear Categoria
    """
    pass

class CategoriaUpdate(BaseModel):
    """
    Schema para actualizar Categoria
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class CategoriaResponse(CategoriaBase):
    """
    Schema de respuesta de Categoria
    """
    id: int

    class Config:
        from_attributes = True
