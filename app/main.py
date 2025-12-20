from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Importar modelos para crear las tablas
from app.models import categoria, usuario, producto, proveedor, cliente, venta, caja

# Importar routers
from app.controllers import (
    categoria_controller,
    usuario_controller,
    producto_controller,
    proveedor_controller,
    cliente_controller,
    venta_controller,
    caja_controller,
    reporte_controller
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MiTienda - Sistema de Gestión de Minimercado",
    description="API REST para la gestión integral de un minimercado",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(categoria_controller.router)
app.include_router(usuario_controller.router)
app.include_router(producto_controller.router)
app.include_router(proveedor_controller.router)
app.include_router(cliente_controller.router)
app.include_router(venta_controller.router)
app.include_router(caja_controller.router)
app.include_router(reporte_controller.router)

@app.get("/")
def root():
    """
    Endpoint raíz - Información del sistema
    """
    return {
        "sistema": "MiTienda",
        "version": "1.0.0",
        "descripcion": "Sistema de Gestión de Minimercado",
        "documentacion": "/docs"
    }

@app.get("/health")
def health_check():
    """
    Endpoint de verificación de salud del sistema
    """
    return {"status": "OK", "message": "Sistema funcionando correctamente"}
