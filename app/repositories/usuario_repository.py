from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from typing import List, Optional

class UsuarioRepository:
    """
    Repositorio para acceso a datos de Usuario
    """

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Usuario]:
        """Obtener todos los usuarios"""
        return self.db.query(Usuario).all()

    def find_by_id(self, id: int) -> Optional[Usuario]:
        """Buscar usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == id).first()

    def find_by_usuario(self, usuario: str) -> Optional[Usuario]:
        """Buscar usuario por nombre de usuario"""
        return self.db.query(Usuario).filter(Usuario.usuario == usuario).first()

    def save(self, usuario: Usuario) -> Usuario:
        """Guardar o actualizar usuario"""
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete_by_id(self, id: int) -> bool:
        """Eliminar usuario por ID"""
        usuario = self.find_by_id(id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False
