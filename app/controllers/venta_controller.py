from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.venta_service import VentaService
from app.schemas.venta import VentaCreate
from app.schemas.common import ResponseRest, ErrorRest

router = APIRouter(
    prefix="/api/ventas",
    tags=["Ventas"]
)

@router.get("/", response_model=ResponseRest)
def consultar_ventas(db: Session = Depends(get_db)):
    """Consultar todas las ventas"""
    try:
        service = VentaService(db)
        ventas = service.consultar()
        return ResponseRest(data=ventas)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/{id}", response_model=ResponseRest)
def consultar_venta(id: int, db: Session = Depends(get_db)):
    """Consultar venta por ID"""
    try:
        service = VentaService(db)
        venta = service.consultar_por_id(id)
        return ResponseRest(data=venta)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.post("/", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    """Crear nueva venta"""
    try:
        service = VentaService(db)
        venta_creada = service.crear(venta)
        return ResponseRest(data=venta_creada)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR002", mensaje=str(e))])

@router.post("/{id}/cancelar", response_model=ResponseRest)
def cancelar_venta(id: int, db: Session = Depends(get_db)):
    """Cancelar venta"""
    try:
        service = VentaService(db)
        venta_cancelada = service.cancelar(id)
        return ResponseRest(data=venta_cancelada)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])
