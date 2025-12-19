from sqlalchemy.orm import Session
from app.repositories.categoria_repository import CategoriaRepository
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from typing import List

class CategoriaService:
    """
    Servicio para lógica de negocio de Categoria
    """

    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def consultar(self) -> List[CategoriaResponse]:
        """
        Consultar todas las categorías
        """
        categorias = self.repository.find_all()
        return [CategoriaResponse.model_validate(cat) for cat in categorias]

    def consultar_por_id(self, id: int) -> CategoriaResponse:
        """
        Consultar categoría por ID
        """
        categoria = self.repository.find_by_id(id)
        if not categoria:
            raise ValueError(f"Categoría con ID {id} no encontrada")
        return CategoriaResponse.model_validate(categoria)

    def crear(self, categoria_data: CategoriaCreate) -> CategoriaResponse:
        """
        Crear nueva categoría
        """
        categoria = Categoria(**categoria_data.model_dump())
        categoria_guardada = self.repository.save(categoria)
        return CategoriaResponse.model_validate(categoria_guardada)

    def actualizar(self, id: int, categoria_data: CategoriaUpdate) -> CategoriaResponse:
        """
        Actualizar categoría existente
        """
        categoria = self.repository.find_by_id(id)
        if not categoria:
            raise ValueError(f"Categoría con ID {id} no encontrada")

        # Actualizar campos
        for key, value in categoria_data.model_dump(exclude_unset=True).items():
            setattr(categoria, key, value)

        categoria_actualizada = self.repository.save(categoria)
        return CategoriaResponse.model_validate(categoria_actualizada)

    def eliminar(self, id: int) -> bool:
        """
        Eliminar categoría
        """
        if not self.repository.find_by_id(id):
            raise ValueError(f"Categoría con ID {id} no encontrada")
        return self.repository.delete_by_id(id)
