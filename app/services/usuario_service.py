from sqlalchemy.orm import Session
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from typing import List

class UsuarioService:
    """
    Servicio para lógica de negocio de Usuario
    """

    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def consultar(self) -> List[UsuarioResponse]:
        """Consultar todos los usuarios"""
        usuarios = self.repository.find_all()
        return [UsuarioResponse.model_validate(u) for u in usuarios]

    def consultar_por_id(self, id: int) -> UsuarioResponse:
        """Consultar usuario por ID"""
        usuario = self.repository.find_by_id(id)
        if not usuario:
            raise ValueError(f"Usuario con ID {id} no encontrado")
        return UsuarioResponse.model_validate(usuario)

    def crear(self, usuario_data: UsuarioCreate) -> UsuarioResponse:
        """Crear nuevo usuario"""
        # Verificar que el nombre de usuario no exista
        if self.repository.find_by_usuario(usuario_data.usuario):
            raise ValueError(f"El nombre de usuario '{usuario_data.usuario}' ya existe")

        usuario = Usuario(**usuario_data.model_dump())
        usuario_guardado = self.repository.save(usuario)
        return UsuarioResponse.model_validate(usuario_guardado)

    def actualizar(self, id: int, usuario_data: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar usuario existente"""
        usuario = self.repository.find_by_id(id)
        if not usuario:
            raise ValueError(f"Usuario con ID {id} no encontrado")

        for key, value in usuario_data.model_dump(exclude_unset=True).items():
            setattr(usuario, key, value)

        usuario_actualizado = self.repository.save(usuario)
        return UsuarioResponse.model_validate(usuario_actualizado)

    def eliminar(self, id: int) -> bool:
        """Eliminar usuario"""
        if not self.repository.find_by_id(id):
            raise ValueError(f"Usuario con ID {id} no encontrado")
        return self.repository.delete_by_id(id)
