# MiTienda - Sistema de Gestión de Minimercado

Sistema backend para la gestión integral de un minimercado, desarrollado con FastAPI.

## Integrantes
- Joseph Wellesley
- Jose Abad
- Fabian Mendoza

## Tecnologías
- **Framework**: FastAPI
- **Base de Datos**: SQLite (SQLAlchemy ORM)
- **Documentación**: Swagger/OpenAPI (automático)

## Arquitectura

El sistema sigue una arquitectura por capas:

```
Cliente -> Controlador -> Servicio -> Repositorio -> Base de Datos
```

### Capas:
- **Modelos**: Entidades del dominio (Usuario, Producto, Venta, etc.)
- **Repositorios**: Acceso a datos
- **Servicios**: Lógica de negocio
- **Controladores**: Endpoints REST

## Módulos
- Configuración (Usuarios, Roles)
- Categorías
- Proveedores
- Inventario (Productos)
- Clientes
- Ventas
- Caja
- Reportes

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Jellz01/ProyectoINGSOFT.git
cd ProyectoINGSOFT
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. (Opcional) Inicializar base de datos con datos de prueba:
```bash
python -m app.init_data
```

6. Ejecutar aplicación:
```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

## Documentación API

Una vez ejecutada la aplicación, acceder a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del Proyecto

```
app/
├── models/         # Entidades del dominio
├── repositories/   # Acceso a datos
├── services/       # Lógica de negocio
├── controllers/    # Endpoints REST
├── schemas/        # Esquemas Pydantic
├── database.py     # Configuración BD
├── main.py         # Punto de entrada
└── init_data.py    # Script de datos iniciales
```

## Endpoints Principales

### Categorías
- `GET /api/categorias` - Listar todas las categorías
- `POST /api/categorias` - Crear categoría
- `GET /api/categorias/{id}` - Obtener categoría
- `PUT /api/categorias/{id}` - Actualizar categoría
- `DELETE /api/categorias/{id}` - Eliminar categoría

### Productos
- `GET /api/productos` - Listar todos los productos
- `GET /api/productos/bajo-stock` - Productos con stock bajo
- `POST /api/productos` - Crear producto
- `PUT /api/productos/{id}` - Actualizar producto
- `DELETE /api/productos/{id}` - Eliminar producto

### Ventas
- `GET /api/ventas` - Listar todas las ventas
- `POST /api/ventas` - Crear venta
- `POST /api/ventas/{id}/cancelar` - Cancelar venta

### Caja
- `POST /api/cajas/abrir` - Abrir caja
- `GET /api/cajas/abierta` - Obtener caja abierta
- `POST /api/cajas/{id}/cerrar` - Cerrar caja
- `POST /api/cajas/{id}/movimientos` - Registrar movimiento

### Reportes
- `GET /api/reportes/productos-bajo-stock` - Reporte de stock bajo
- `GET /api/reportes/ventas-del-dia` - Reporte de ventas del día
- `GET /api/reportes/resumen-inventario` - Resumen de inventario

## Características

- ✅ API REST completa con FastAPI
- ✅ Documentación automática con Swagger
- ✅ Arquitectura por capas (MVC)
- ✅ Base de datos SQLite con SQLAlchemy ORM
- ✅ Gestión de usuarios y roles
- ✅ Control de inventario con alertas de stock bajo
- ✅ Sistema de ventas con actualización automática de stock
- ✅ Control de caja con movimientos
- ✅ Reportes analíticos en tiempo real
- ✅ Validaciones de negocio
- ✅ Manejo de errores centralizado
