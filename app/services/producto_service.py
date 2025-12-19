from sqlalchemy.orm import Session
from app.repositories.producto_repository import ProductoRepository
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from typing import List

class ProductoService:
    """
    Servicio para lógica de negocio de Producto
    """

    def __init__(self, db: Session):
        self.repository = ProductoRepository(db)

    def consultar(self) -> List[ProductoResponse]:
        """Consultar todos los productos"""
        productos = self.repository.find_all()
        return [ProductoResponse.model_validate(p) for p in productos]

    def consultar_por_id(self, id: int) -> ProductoResponse:
        """Consultar producto por ID"""
        producto = self.repository.find_by_id(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado")
        return ProductoResponse.model_validate(producto)

    def consultar_bajo_stock(self) -> List[ProductoResponse]:
        """Consultar productos con stock bajo"""
        productos = self.repository.find_bajo_stock()
        return [ProductoResponse.model_validate(p) for p in productos]

    def crear(self, producto_data: ProductoCreate) -> ProductoResponse:
        """Crear nuevo producto"""
        if self.repository.find_by_codigo(producto_data.codigo):
            raise ValueError(f"El código '{producto_data.codigo}' ya existe")

        producto = Producto(**producto_data.model_dump())
        producto_guardado = self.repository.save(producto)
        return ProductoResponse.model_validate(producto_guardado)

    def actualizar(self, id: int, producto_data: ProductoUpdate) -> ProductoResponse:
        """Actualizar producto existente"""
        producto = self.repository.find_by_id(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado")

        for key, value in producto_data.model_dump(exclude_unset=True).items():
            setattr(producto, key, value)

        producto_actualizado = self.repository.save(producto)
        return ProductoResponse.model_validate(producto_actualizado)

    def eliminar(self, id: int) -> bool:
        """Eliminar producto"""
        if not self.repository.find_by_id(id):
            raise ValueError(f"Producto con ID {id} no encontrado")
        return self.repository.delete_by_id(id)
