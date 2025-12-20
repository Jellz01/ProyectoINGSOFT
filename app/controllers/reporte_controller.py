from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.producto_repository import ProductoRepository
from app.repositories.venta_repository import VentaRepository
from app.schemas.common import ResponseRest, ErrorRest
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/api/reportes",
    tags=["Reportes"]
)

@router.get("/productos-bajo-stock", response_model=ResponseRest)
def reporte_productos_bajo_stock(db: Session = Depends(get_db)):
    """
    Reporte de productos con stock bajo
    """
    try:
        repo = ProductoRepository(db)
        productos = repo.find_bajo_stock()

        reporte = {
            "titulo": "Productos con Stock Bajo",
            "fecha": datetime.now().isoformat(),
            "total": len(productos),
            "productos": [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "codigo": p.codigo,
                    "stock_actual": p.stock,
                    "stock_minimo": p.stock_minimo,
                    "diferencia": p.stock_minimo - p.stock
                }
                for p in productos
            ]
        }

        return ResponseRest(data=reporte)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/ventas-del-dia", response_model=ResponseRest)
def reporte_ventas_del_dia(db: Session = Depends(get_db)):
    """
    Reporte de ventas del día actual
    """
    try:
        repo = VentaRepository(db)
        hoy_inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        hoy_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        ventas = repo.find_by_fecha(hoy_inicio, hoy_fin)

        total_ventas = sum(v.total for v in ventas)

        reporte = {
            "titulo": "Ventas del Día",
            "fecha": datetime.now().isoformat(),
            "cantidad_ventas": len(ventas),
            "total_vendido": total_ventas,
            "ventas": [
                {
                    "id": v.id,
                    "fecha": v.fecha.isoformat(),
                    "total": v.total,
                    "estado": v.estado.value,
                    "cantidad_productos": len(v.detalles)
                }
                for v in ventas
            ]
        }

        return ResponseRest(data=reporte)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])

@router.get("/resumen-inventario", response_model=ResponseRest)
def reporte_resumen_inventario(db: Session = Depends(get_db)):
    """
    Reporte resumen del inventario
    """
    try:
        repo = ProductoRepository(db)
        productos = repo.find_all()

        total_productos = len(productos)
        valor_inventario = sum(p.precio_compra * p.stock for p in productos)
        productos_sin_stock = len([p for p in productos if p.stock == 0])
        productos_bajo_stock = len(repo.find_bajo_stock())

        reporte = {
            "titulo": "Resumen de Inventario",
            "fecha": datetime.now().isoformat(),
            "total_productos": total_productos,
            "valor_total_inventario": valor_inventario,
            "productos_sin_stock": productos_sin_stock,
            "productos_bajo_stock": productos_bajo_stock
        }

        return ResponseRest(data=reporte)
    except Exception as e:
        return ResponseRest(errors=[ErrorRest(codigo="ERR001", mensaje=str(e))])
