from sqlalchemy.orm import Session
from app.repositories.proveedor_repository import ProveedorRepository
from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorResponse
from typing import List

class ProveedorService:
    """
    Servicio para lógica de negocio de Proveedor
    """

    def __init__(self, db: Session):
        self.repository = ProveedorRepository(db)

    def consultar(self) -> List[ProveedorResponse]:
        """Consultar todos los proveedores"""
        proveedores = self.repository.find_all()
        return [ProveedorResponse.model_validate(p) for p in proveedores]

    def consultar_por_id(self, id: int) -> ProveedorResponse:
        """Consultar proveedor por ID"""
        proveedor = self.repository.find_by_id(id)
        if not proveedor:
            raise ValueError(f"Proveedor con ID {id} no encontrado")
        return ProveedorResponse.model_validate(proveedor)

    def crear(self, proveedor_data: ProveedorCreate) -> ProveedorResponse:
        """Crear nuevo proveedor"""
        proveedor = Proveedor(**proveedor_data.model_dump())
        proveedor_guardado = self.repository.save(proveedor)
        return ProveedorResponse.model_validate(proveedor_guardado)

    def actualizar(self, id: int, proveedor_data: ProveedorUpdate) -> ProveedorResponse:
        """Actualizar proveedor existente"""
        proveedor = self.repository.find_by_id(id)
        if not proveedor:
            raise ValueError(f"Proveedor con ID {id} no encontrado")

        for key, value in proveedor_data.model_dump(exclude_unset=True).items():
            setattr(proveedor, key, value)

        proveedor_actualizado = self.repository.save(proveedor)
        return ProveedorResponse.model_validate(proveedor_actualizado)

    def eliminar(self, id: int) -> bool:
        """Eliminar proveedor"""
        if not self.repository.find_by_id(id):
            raise ValueError(f"Proveedor con ID {id} no encontrado")
        return self.repository.delete_by_id(id)
