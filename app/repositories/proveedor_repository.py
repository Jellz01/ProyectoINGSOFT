from sqlalchemy.orm import Session
from app.models.proveedor import Proveedor
from typing import List, Optional

class ProveedorRepository:
    """
    Repositorio para acceso a datos de Proveedor
    """

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Proveedor]:
        """Obtener todos los proveedores"""
        return self.db.query(Proveedor).all()

    def find_by_id(self, id: int) -> Optional[Proveedor]:
        """Buscar proveedor por ID"""
        return self.db.query(Proveedor).filter(Proveedor.id == id).first()

    def save(self, proveedor: Proveedor) -> Proveedor:
        """Guardar o actualizar proveedor"""
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def delete_by_id(self, id: int) -> bool:
        """Eliminar proveedor por ID"""
        proveedor = self.find_by_id(id)
        if proveedor:
            self.db.delete(proveedor)
            self.db.commit()
            return True
        return False
