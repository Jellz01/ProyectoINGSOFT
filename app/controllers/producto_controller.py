from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.schemas.common import ResponseRest, ErrorRest

router = APIRouter(
    prefix="/api/productos",
    tags=["Productos"]
)

@router.get("/", response_model=ResponseRest)
def consultar_productos(db: Session = Depends(get_db)):
    """Consultar todos los productos"""
    try:
        service = ProductoService(db)
        productos = service.consultar()
        return ResponseRest(data=productos)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/bajo-stock", response_model=ResponseRest)
def consultar_productos_bajo_stock(db: Session = Depends(get_db)):
    """Consultar productos con stock bajo"""
    try:
        service = ProductoService(db)
        productos = service.consultar_bajo_stock()
        return ResponseRest(data=productos)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/{id}", response_model=ResponseRest)
def consultar_producto(id: int, db: Session = Depends(get_db)):
    """Consultar producto por ID"""
    try:
        service = ProductoService(db)
        producto = service.consultar_por_id(id)
        return ResponseRest(data=producto)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.post("/", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear nuevo producto"""
    try:
        service = ProductoService(db)
        producto_creado = service.crear(producto)
        return ResponseRest(data=producto_creado)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR002", mensaje=str(e))])

@router.put("/{id}", response_model=ResponseRest)
def actualizar_producto(id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    """Actualizar producto existente"""
    try:
        service = ProductoService(db)
        producto_actualizado = service.actualizar(id, producto)
        return ResponseRest(data=producto_actualizado)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])

@router.delete("/{id}", response_model=ResponseRest)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    """Eliminar producto"""
    try:
        service = ProductoService(db)
        service.eliminar(id)
        return ResponseRest(data={"mensaje": "Producto eliminado correctamente"})
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR004", mensaje=str(e))])
