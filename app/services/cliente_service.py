from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from typing import List

class ClienteService:
    """
    Servicio para lógica de negocio de Cliente
    """

    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def consultar(self) -> List[ClienteResponse]:
        """Consultar todos los clientes"""
        clientes = self.repository.find_all()
        return [ClienteResponse.model_validate(c) for c in clientes]

    def consultar_por_id(self, id: int) -> ClienteResponse:
        """Consultar cliente por ID"""
        cliente = self.repository.find_by_id(id)
        if not cliente:
            raise ValueError(f"Cliente con ID {id} no encontrado")
        return ClienteResponse.model_validate(cliente)

    def crear(self, cliente_data: ClienteCreate) -> ClienteResponse:
        """Crear nuevo cliente"""
        if self.repository.find_by_cedula(cliente_data.cedula):
            raise ValueError(f"La cédula '{cliente_data.cedula}' ya está registrada")

        cliente = Cliente(**cliente_data.model_dump())
        cliente_guardado = self.repository.save(cliente)
        return ClienteResponse.model_validate(cliente_guardado)

    def actualizar(self, id: int, cliente_data: ClienteUpdate) -> ClienteResponse:
        """Actualizar cliente existente"""
        cliente = self.repository.find_by_id(id)
        if not cliente:
            raise ValueError(f"Cliente con ID {id} no encontrado")

        for key, value in cliente_data.model_dump(exclude_unset=True).items():
            setattr(cliente, key, value)

        cliente_actualizado = self.repository.save(cliente)
        return ClienteResponse.model_validate(cliente_actualizado)

    def eliminar(self, id: int) -> bool:
        """Eliminar cliente"""
        if not self.repository.find_by_id(id):
            raise ValueError(f"Cliente con ID {id} no encontrado")
        return self.repository.delete_by_id(id)
