from pydantic import BaseModel
from typing import List, Optional, Any

class ErrorRest(BaseModel):
    """
    Esquema para errores REST
    """
    codigo: str
    mensaje: str
    campo: Optional[str] = None

class ResponseRest(BaseModel):
    """
    Esquema genérico para respuestas REST
    """
    data: Optional[Any] = None
    errors: Optional[List[ErrorRest]] = None
