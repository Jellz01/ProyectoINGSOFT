from sqlalchemy.orm import Session
from app.models.venta import Venta, EstadoVentaEnum
from typing import List, Optional
from datetime import datetime

class VentaRepository:
    """
    Repositorio para acceso a datos de Venta
    """

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Venta]:
        """Obtener todas las ventas"""
        return self.db.query(Venta).all()

    def find_by_id(self, id: int) -> Optional[Venta]:
        """Buscar venta por ID"""
        return self.db.query(Venta).filter(Venta.id == id).first()

    def find_by_estado(self, estado: EstadoVentaEnum) -> List[Venta]:
        """Buscar ventas por estado"""
        return self.db.query(Venta).filter(Venta.estado == estado).all()

    def find_by_fecha(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Venta]:
        """Buscar ventas por rango de fechas"""
        return self.db.query(Venta).filter(
            Venta.fecha >= fecha_inicio,
            Venta.fecha <= fecha_fin
        ).all()

    def save(self, venta: Venta) -> Venta:
        """Guardar o actualizar venta"""
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def delete_by_id(self, id: int) -> bool:
        """Eliminar venta por ID"""
        venta = self.find_by_id(id)
        if venta:
            self.db.delete(venta)
            self.db.commit()
            return True
        return False
