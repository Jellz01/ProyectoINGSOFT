from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.proveedor_service import ProveedorService
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate
from app.schemas.common import ResponseRest, ErrorRest

router = APIRouter(
    prefix="/api/proveedores",
    tags=["Proveedores"]
)

@router.get("/", response_model=ResponseRest)
def consultar_proveedores(db: Session = Depends(get_db)):
    """Consultar todos los proveedores"""
    try:
        service = ProveedorService(db)
        proveedores = service.consultar()
        return ResponseRest(data=proveedores)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/{id}", response_model=ResponseRest)
def consultar_proveedor(id: int, db: Session = Depends(get_db)):
    """Consultar proveedor por ID"""
    try:
        service = ProveedorService(db)
        proveedor = service.consultar_por_id(id)
        return ResponseRest(data=proveedor)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.post("/", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    """Crear nuevo proveedor"""
    try:
        service = ProveedorService(db)
        proveedor_creado = service.crear(proveedor)
        return ResponseRest(data=proveedor_creado)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR002", mensaje=str(e))])

@router.put("/{id}", response_model=ResponseRest)
def actualizar_proveedor(id: int, proveedor: ProveedorUpdate, db: Session = Depends(get_db)):
    """Actualizar proveedor existente"""
    try:
        service = ProveedorService(db)
        proveedor_actualizado = service.actualizar(id, proveedor)
        return ResponseRest(data=proveedor_actualizado)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])

@router.delete("/{id}", response_model=ResponseRest)
def eliminar_proveedor(id: int, db: Session = Depends(get_db)):
    """Eliminar proveedor"""
    try:
        service = ProveedorService(db)
        service.eliminar(id)
        return ResponseRest(data={"mensaje": "Proveedor eliminado correctamente"})
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR004", mensaje=str(e))])
