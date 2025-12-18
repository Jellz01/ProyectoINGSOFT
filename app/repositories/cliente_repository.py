from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from typing import List, Optional

class ClienteRepository:
    """
    Repositorio para acceso a datos de Cliente
    """

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Cliente]:
        """Obtener todos los clientes"""
        return self.db.query(Cliente).all()

    def find_by_id(self, id: int) -> Optional[Cliente]:
        """Buscar cliente por ID"""
        return self.db.query(Cliente).filter(Cliente.id == id).first()

    def find_by_cedula(self, cedula: str) -> Optional[Cliente]:
        """Buscar cliente por cédula"""
        return self.db.query(Cliente).filter(Cliente.cedula == cedula).first()

    def save(self, cliente: Cliente) -> Cliente:
        """Guardar o actualizar cliente"""
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def delete_by_id(self, id: int) -> bool:
        """Eliminar cliente por ID"""
        cliente = self.find_by_id(id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
