from sqlalchemy.orm import Session
from app.models.caja import Caja, EstadoCajaEnum
from typing import List, Optional

class CajaRepository:
    """
    Repositorio para acceso a datos de Caja
    """

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Caja]:
        """Obtener todas las cajas"""
        return self.db.query(Caja).all()

    def find_by_id(self, id: int) -> Optional[Caja]:
        """Buscar caja por ID"""
        return self.db.query(Caja).filter(Caja.id == id).first()

    def find_by_estado(self, estado: EstadoCajaEnum) -> List[Caja]:
        """Buscar cajas por estado"""
        return self.db.query(Caja).filter(Caja.estado == estado).all()

    def find_caja_abierta(self) -> Optional[Caja]:
        """Obtener la caja actualmente abierta"""
        return self.db.query(Caja).filter(Caja.estado == EstadoCajaEnum.ABIERTA).first()

    def save(self, caja: Caja) -> Caja:
        """Guardar o actualizar caja"""
        self.db.add(caja)
        self.db.commit()
        self.db.refresh(caja)
        return caja

    def delete_by_id(self, id: int) -> bool:
        """Eliminar caja por ID"""
        caja = self.find_by_id(id)
        if caja:
            self.db.delete(caja)
            self.db.commit()
            return True
        return False
