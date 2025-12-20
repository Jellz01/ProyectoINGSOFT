from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.cliente_service import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.schemas.common import ResponseRest, ErrorRest

router = APIRouter(
    prefix="/api/clientes",
    tags=["Clientes"]
)

@router.get("/", response_model=ResponseRest)
def consultar_clientes(db: Session = Depends(get_db)):
    """Consultar todos los clientes"""
    try:
        service = ClienteService(db)
        clientes = service.consultar()
        return ResponseRest(data=clientes)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/{id}", response_model=ResponseRest)
def consultar_cliente(id: int, db: Session = Depends(get_db)):
    """Consultar cliente por ID"""
    try:
        service = ClienteService(db)
        cliente = service.consultar_por_id(id)
        return ResponseRest(data=cliente)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.post("/", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crear nuevo cliente"""
    try:
        service = ClienteService(db)
        cliente_creado = service.crear(cliente)
        return ResponseRest(data=cliente_creado)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR002", mensaje=str(e))])

@router.put("/{id}", response_model=ResponseRest)
def actualizar_cliente(id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    """Actualizar cliente existente"""
    try:
        service = ClienteService(db)
        cliente_actualizado = service.actualizar(id, cliente)
        return ResponseRest(data=cliente_actualizado)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])

@router.delete("/{id}", response_model=ResponseRest)
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    """Eliminar cliente"""
    try:
        service = ClienteService(db)
        service.eliminar(id)
        return ResponseRest(data={"mensaje": "Cliente eliminado correctamente"})
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR004", mensaje=str(e))])
