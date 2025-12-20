from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.categoria_service import CategoriaService
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.schemas.common import ResponseRest, ErrorRest
from typing import List

router = APIRouter(
    prefix="/api/categorias",
    tags=["Categorías"]
)

@router.get("/", response_model=ResponseRest)
def consultar_categorias(db: Session = Depends(get_db)):
    """
    Consultar todas las categorías
    """
    try:
        service = CategoriaService(db)
        categorias = service.consultar()
        return ResponseRest(data=categorias)
    except Exception as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR001", mensaje=str(e))]
        )

@router.get("/{id}", response_model=ResponseRest)
def consultar_categoria(id: int, db: Session = Depends(get_db)):
    """
    Consultar categoría por ID
    """
    try:
        service = CategoriaService(db)
        categoria = service.consultar_por_id(id)
        return ResponseRest(data=categoria)
    except ValueError as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR404", mensaje=str(e))]
        )
    except Exception as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR001", mensaje=str(e))]
        )

@router.post("/", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva categoría
    """
    try:
        service = CategoriaService(db)
        categoria_creada = service.crear(categoria)
        return ResponseRest(data=categoria_creada)
    except Exception as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR002", mensaje=str(e))]
        )

@router.put("/{id}", response_model=ResponseRest)
def actualizar_categoria(
    id: int,
    categoria: CategoriaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar categoría existente
    """
    try:
        service = CategoriaService(db)
        categoria_actualizada = service.actualizar(id, categoria)
        return ResponseRest(data=categoria_actualizada)
    except ValueError as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR404", mensaje=str(e))]
        )
    except Exception as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR003", mensaje=str(e))]
        )

@router.delete("/{id}", response_model=ResponseRest)
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    """
    Eliminar categoría
    """
    try:
        service = CategoriaService(db)
        service.eliminar(id)
        return ResponseRest(data={"mensaje": "Categoría eliminada correctamente"})
    except ValueError as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR404", mensaje=str(e))]
        )
    except Exception as e:
        return ResponseRest(
            errors=[ErrorRest(codigo="ERR004", mensaje=str(e))]
        )
