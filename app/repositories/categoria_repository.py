from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from typing import List, Optional

class CategoriaRepository:
    """
    Repositorio para acceso a datos de Categoria
    """

    def __init__(self, db: Session):
        self.db = db

    def count(self) -> int:
        """Contar categorías"""
        return self.db.query(Categoria).count()

    def find_all(self) -> List[Categoria]:
        """Obtener todas las categorías"""
        return self.db.query(Categoria).all()

    def find_by_id(self, id: int) -> Optional[Categoria]:
        """Buscar categoría por ID"""
        return self.db.query(Categoria).filter(Categoria.id == id).first()

    def delete_all(self) -> None:
        """Eliminar todas las categorías"""
        self.db.query(Categoria).delete()
        self.db.commit()

    def delete_by_id(self, id: int) -> bool:
        """Eliminar categoría por ID"""
        categoria = self.find_by_id(id)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False

    def save(self, categoria: Categoria) -> Categoria:
        """Guardar o actualizar categoría"""
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def save_all(self, categorias: List[Categoria]) -> List[Categoria]:
        """Guardar múltiples categorías"""
        self.db.add_all(categorias)
        self.db.commit()
        for categoria in categorias:
            self.db.refresh(categoria)
        return categorias
