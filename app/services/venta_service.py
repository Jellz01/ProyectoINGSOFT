from sqlalchemy.orm import Session
from app.repositories.venta_repository import VentaRepository
from app.repositories.producto_repository import ProductoRepository
from app.models.venta import Venta, DetalleVenta, EstadoVentaEnum
from app.schemas.venta import VentaCreate, VentaResponse
from typing import List

class VentaService:
    """
    Servicio para lógica de negocio de Venta
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = VentaRepository(db)
        self.producto_repository = ProductoRepository(db)

    def consultar(self) -> List[VentaResponse]:
        """Consultar todas las ventas"""
        ventas = self.repository.find_all()
        return [VentaResponse.model_validate(v) for v in ventas]

    def consultar_por_id(self, id: int) -> VentaResponse:
        """Consultar venta por ID"""
        venta = self.repository.find_by_id(id)
        if not venta:
            raise ValueError(f"Venta con ID {id} no encontrada")
        return VentaResponse.model_validate(venta)

    def crear(self, venta_data: VentaCreate) -> VentaResponse:
        """Crear nueva venta"""
        # Crear venta
        venta = Venta(
            usuario_id=venta_data.usuario_id,
            cliente_id=venta_data.cliente_id,
            estado=EstadoVentaEnum.INICIADA
        )

        total = 0.0
        # Procesar detalles
        for detalle_data in venta_data.detalles:
            # Verificar stock
            producto = self.producto_repository.find_by_id(detalle_data.producto_id)
            if not producto:
                raise ValueError(f"Producto con ID {detalle_data.producto_id} no encontrado")

            if producto.stock < detalle_data.cantidad:
                raise ValueError(f"Stock insuficiente para producto {producto.nombre}")

            # Crear detalle
            subtotal = detalle_data.cantidad * detalle_data.precio_unitario
            detalle = DetalleVenta(
                producto_id=detalle_data.producto_id,
                cantidad=detalle_data.cantidad,
                precio_unitario=detalle_data.precio_unitario,
                subtotal=subtotal
            )
            venta.detalles.append(detalle)
            total += subtotal

            # Actualizar stock
            producto.stock -= detalle_data.cantidad
            self.producto_repository.save(producto)

        venta.total = total
        venta.estado = EstadoVentaEnum.COMPLETADA

        venta_guardada = self.repository.save(venta)
        return VentaResponse.model_validate(venta_guardada)

    def cancelar(self, id: int) -> VentaResponse:
        """Cancelar venta"""
        venta = self.repository.find_by_id(id)
        if not venta:
            raise ValueError(f"Venta con ID {id} no encontrada")

        if venta.estado == EstadoVentaEnum.CANCELADA:
            raise ValueError("La venta ya está cancelada")

        # Devolver stock
        for detalle in venta.detalles:
            producto = self.producto_repository.find_by_id(detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
                self.producto_repository.save(producto)

        venta.estado = EstadoVentaEnum.CANCELADA
        venta_actualizada = self.repository.save(venta)
        return VentaResponse.model_validate(venta_actualizada)
