from sqlalchemy.orm import Session
from app.models.producto import Producto
from typing import List, Optional

class ProductoRepository:
    """
    Repositorio para acceso a datos de Producto
    """

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Producto]:
        """Obtener todos los productos"""
        return self.db.query(Producto).all()

    def find_by_id(self, id: int) -> Optional[Producto]:
        """Buscar producto por ID"""
        return self.db.query(Producto).filter(Producto.id == id).first()

    def find_by_codigo(self, codigo: str) -> Optional[Producto]:
        """Buscar producto por código"""
        return self.db.query(Producto).filter(Producto.codigo == codigo).first()

    def find_bajo_stock(self) -> List[Producto]:
        """Obtener productos con stock bajo"""
        return self.db.query(Producto).filter(Producto.stock <= Producto.stock_minimo).all()

    def save(self, producto: Producto) -> Producto:
        """Guardar o actualizar producto"""
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete_by_id(self, id: int) -> bool:
        """Eliminar producto por ID"""
        producto = self.find_by_id(id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
