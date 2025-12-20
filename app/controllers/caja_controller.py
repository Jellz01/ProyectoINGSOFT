from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.caja_service import CajaService
from app.schemas.caja import CajaCreate, MovimientoCajaCreate
from app.schemas.common import ResponseRest, ErrorRest
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/cajas",
    tags=["Caja"]
)

class CerrarCajaRequest(BaseModel):
    monto_final: float

@router.get("/", response_model=ResponseRest)
def consultar_cajas(db: Session = Depends(get_db)):
    """Consultar todas las cajas"""
    try:
        service = CajaService(db)
        cajas = service.consultar()
        return ResponseRest(data=cajas)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/abierta", response_model=ResponseRest)
def obtener_caja_abierta(db: Session = Depends(get_db)):
    """Obtener la caja actualmente abierta"""
    try:
        service = CajaService(db)
        caja = service.obtener_caja_abierta()
        return ResponseRest(data=caja)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/{id}", response_model=ResponseRest)
def consultar_caja(id: int, db: Session = Depends(get_db)):
    """Consultar caja por ID"""
    try:
        service = CajaService(db)
        caja = service.consultar_por_id(id)
        return ResponseRest(data=caja)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.post("/abrir", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def abrir_caja(caja: CajaCreate, db: Session = Depends(get_db)):
    """Abrir nueva caja"""
    try:
        service = CajaService(db)
        caja_abierta = service.abrir_caja(caja)
        return ResponseRest(data=caja_abierta)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR002", mensaje=str(e))])

@router.post("/{id}/cerrar", response_model=ResponseRest)
def cerrar_caja(id: int, request: CerrarCajaRequest, db: Session = Depends(get_db)):
    """Cerrar caja"""
    try:
        service = CajaService(db)
        caja_cerrada = service.cerrar_caja(id, request.monto_final)
        return ResponseRest(data=caja_cerrada)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])

@router.post("/{id}/movimientos", response_model=ResponseRest)
def registrar_movimiento(id: int, movimiento: MovimientoCajaCreate, db: Session = Depends(get_db)):
    """Registrar movimiento en caja"""
    try:
        service = CajaService(db)
        caja_actualizada = service.registrar_movimiento(id, movimiento)
        return ResponseRest(data=caja_actualizada)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])
