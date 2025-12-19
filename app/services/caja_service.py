from sqlalchemy.orm import Session
from app.repositories.caja_repository import CajaRepository
from app.models.caja import Caja, MovimientoCaja, EstadoCajaEnum, TipoMovimientoEnum
from app.schemas.caja import CajaCreate, CajaResponse, MovimientoCajaCreate
from typing import List
from datetime import datetime

class CajaService:
    """
    Servicio para lógica de negocio de Caja
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = CajaRepository(db)

    def consultar(self) -> List[CajaResponse]:
        """Consultar todas las cajas"""
        cajas = self.repository.find_all()
        return [CajaResponse.model_validate(c) for c in cajas]

    def consultar_por_id(self, id: int) -> CajaResponse:
        """Consultar caja por ID"""
        caja = self.repository.find_by_id(id)
        if not caja:
            raise ValueError(f"Caja con ID {id} no encontrada")
        return CajaResponse.model_validate(caja)

    def obtener_caja_abierta(self) -> CajaResponse:
        """Obtener la caja actualmente abierta"""
        caja = self.repository.find_caja_abierta()
        if not caja:
            raise ValueError("No hay una caja abierta actualmente")
        return CajaResponse.model_validate(caja)

    def abrir_caja(self, caja_data: CajaCreate) -> CajaResponse:
        """Abrir nueva caja"""
        # Verificar que no haya una caja abierta
        caja_abierta = self.repository.find_caja_abierta()
        if caja_abierta:
            raise ValueError("Ya existe una caja abierta. Debe cerrarla primero")

        caja = Caja(
            monto_inicial=caja_data.monto_inicial,
            usuario_id=caja_data.usuario_id,
            estado=EstadoCajaEnum.ABIERTA
        )

        # Registrar movimiento de apertura
        movimiento = MovimientoCaja(
            tipo=TipoMovimientoEnum.APERTURA,
            monto=caja_data.monto_inicial,
            descripcion="Apertura de caja"
        )
        caja.movimientos.append(movimiento)

        caja_guardada = self.repository.save(caja)
        return CajaResponse.model_validate(caja_guardada)

    def cerrar_caja(self, id: int, monto_final: float) -> CajaResponse:
        """Cerrar caja"""
        caja = self.repository.find_by_id(id)
        if not caja:
            raise ValueError(f"Caja con ID {id} no encontrada")

        if caja.estado == EstadoCajaEnum.CERRADA:
            raise ValueError("La caja ya está cerrada")

        caja.estado = EstadoCajaEnum.CERRADA
        caja.fecha_cierre = datetime.now()
        caja.monto_final = monto_final

        # Registrar movimiento de cierre
        movimiento = MovimientoCaja(
            tipo=TipoMovimientoEnum.CIERRE,
            monto=monto_final,
            descripcion="Cierre de caja"
        )
        caja.movimientos.append(movimiento)

        caja_actualizada = self.repository.save(caja)
        return CajaResponse.model_validate(caja_actualizada)

    def registrar_movimiento(self, id: int, movimiento_data: MovimientoCajaCreate) -> CajaResponse:
        """Registrar movimiento en la caja"""
        caja = self.repository.find_by_id(id)
        if not caja:
            raise ValueError(f"Caja con ID {id} no encontrada")

        if caja.estado == EstadoCajaEnum.CERRADA:
            raise ValueError("No se pueden registrar movimientos en una caja cerrada")

        movimiento = MovimientoCaja(**movimiento_data.model_dump())
        caja.movimientos.append(movimiento)

        caja_actualizada = self.repository.save(caja)
        return CajaResponse.model_validate(caja_actualizada)
