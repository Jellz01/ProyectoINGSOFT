from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.schemas.common import ResponseRest, ErrorRest

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"]
)

@router.get("/", response_model=ResponseRest)
def consultar_usuarios(db: Session = Depends(get_db)):
    """Consultar todos los usuarios"""
    try:
        service = UsuarioService(db)
        usuarios = service.consultar()
        return ResponseRest(data=usuarios)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/{id}", response_model=ResponseRest)
def consultar_usuario(id: int, db: Session = Depends(get_db)):
    """Consultar usuario por ID"""
    try:
        service = UsuarioService(db)
        usuario = service.consultar_por_id(id)
        return ResponseRest(data=usuario)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.post("/", response_model=ResponseRest, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear nuevo usuario"""
    try:
        service = UsuarioService(db)
        usuario_creado = service.crear(usuario)
        return ResponseRest(data=usuario_creado)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR002", mensaje=str(e))])

@router.put("/{id}", response_model=ResponseRest)
def actualizar_usuario(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """Actualizar usuario existente"""
    try:
        service = UsuarioService(db)
        usuario_actualizado = service.actualizar(id, usuario)
        return ResponseRest(data=usuario_actualizado)
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR003", mensaje=str(e))])

@router.delete("/{id}", response_model=ResponseRest)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    """Eliminar usuario"""
    try:
        service = UsuarioService(db)
        service.eliminar(id)
        return ResponseRest(data={"mensaje": "Usuario eliminado correctamente"})
    except ValueError as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR404", mensaje=str(e))])
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR004", mensaje=str(e))])
