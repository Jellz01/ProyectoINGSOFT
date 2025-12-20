"""
Script para inicializar datos de prueba en la base de datos
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.categoria import Categoria
from app.models.usuario import Usuario, RolEnum, EstadoEnum
from app.models.proveedor import Proveedor
from app.models.producto import Producto

def init_db():
    """
    Inicializar base de datos con datos de prueba
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Verificar si ya hay datos
        if db.query(Usuario).count() > 0:
            print("La base de datos ya tiene datos. Omitiendo inicialización.")
            return

        print("Inicializando datos de prueba...")

        # Crear categorías
        categorias = [
            Categoria(nombre="Bebidas", descripcion="Bebidas y refrescos"),
            Categoria(nombre="Lácteos", descripcion="Productos lácteos"),
            Categoria(nombre="Panadería", descripcion="Productos de panadería"),
            Categoria(nombre="Limpieza", descripcion="Productos de limpieza"),
            Categoria(nombre="Snacks", descripcion="Snacks y golosinas"),
        ]
        db.add_all(categorias)
        db.commit()
        print(f"✓ Creadas {len(categorias)} categorías")

        # Crear usuarios
        usuarios = [
            Usuario(
                nombre="Administrador",
                usuario="admin",
                password="admin123",
                rol=RolEnum.ADMINISTRADOR,
                estado=EstadoEnum.ACTIVO
            ),
            Usuario(
                nombre="Juan Pérez",
                usuario="cajero1",
                password="cajero123",
                rol=RolEnum.CAJERO,
                estado=EstadoEnum.ACTIVO
            ),
            Usuario(
                nombre="María García",
                usuario="inventario1",
                password="inv123",
                rol=RolEnum.INVENTARIO,
                estado=EstadoEnum.ACTIVO
            ),
        ]
        db.add_all(usuarios)
        db.commit()
        print(f"✓ Creados {len(usuarios)} usuarios")

        # Crear proveedores
        proveedores = [
            Proveedor(
                nombre="Distribuidora La Favorita",
                ruc="1234567890001",
                telefono="02-2345678",
                email="ventas@favorita.com",
                direccion="Av. Principal 123"
            ),
            Proveedor(
                nombre="Alimentos del Valle",
                ruc="0987654321001",
                telefono="02-2876543",
                email="info@alimentosvalle.com",
                direccion="Calle Secundaria 456"
            ),
        ]
        db.add_all(proveedores)
        db.commit()
        print(f"✓ Creados {len(proveedores)} proveedores")

        # Crear productos
        productos = [
            Producto(
                nombre="Coca Cola 2L",
                codigo="COC2L001",
                precio_compra=1.50,
                precio_venta=2.00,
                stock=50,
                stock_minimo=10,
                categoria_id=1,
                proveedor_id=1
            ),
            Producto(
                nombre="Leche Entera 1L",
                codigo="LEC1L001",
                precio_compra=0.80,
                precio_venta=1.20,
                stock=30,
                stock_minimo=15,
                categoria_id=2,
                proveedor_id=2
            ),
            Producto(
                nombre="Pan Integral",
                codigo="PAN001",
                precio_compra=0.50,
                precio_venta=0.75,
                stock=20,
                stock_minimo=10,
                categoria_id=3,
                proveedor_id=2
            ),
            Producto(
                nombre="Detergente 1kg",
                codigo="DET1K001",
                precio_compra=2.00,
                precio_venta=3.00,
                stock=25,
                stock_minimo=5,
                categoria_id=4,
                proveedor_id=1
            ),
            Producto(
                nombre="Papas Fritas 200g",
                codigo="SNK200001",
                precio_compra=1.00,
                precio_venta=1.50,
                stock=40,
                stock_minimo=20,
                categoria_id=5,
                proveedor_id=1
            ),
        ]
        db.add_all(productos)
        db.commit()
        print(f"✓ Creados {len(productos)} productos")

        print("\n✅ Inicialización completada exitosamente!")
        print("\nCredenciales de usuario:")
        print("- Admin: usuario='admin', password='admin123'")
        print("- Cajero: usuario='cajero1', password='cajero123'")
        print("- Inventario: usuario='inventario1', password='inv123'")

    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
