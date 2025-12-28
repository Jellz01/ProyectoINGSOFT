from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.proveedor import Proveedor
from app.models.categoria import Categoria
from app.models.producto import Producto

def test_create_producto(test_client: TestClient, db_session: Session):
    """
    Prueba la creación de un nuevo producto.
    """
    # 1. Crear dependencias (Proveedor y Categoria)
    proveedor_data = {"nombre": "Proveedor Test", "ruc": "12345678901"}
    new_proveedor = Proveedor(**proveedor_data)
    db_session.add(new_proveedor)
    db_session.commit()
    db_session.refresh(new_proveedor)

    categoria_data = {"nombre": "Categoria Test"}
    new_categoria = Categoria(**categoria_data)
    db_session.add(new_categoria)
    db_session.commit()
    db_session.refresh(new_categoria)

    # 2. Datos del nuevo producto
    producto_data = {
        "nombre": "Producto Test",
        "codigo": "P-001",
        "precio_compra": 10.0,
        "precio_venta": 15.0,
        "stock": 100,
        "stock_minimo": 10,
        "categoria_id": new_categoria.id,
        "proveedor_id": new_proveedor.id
    }

    # 3. Realizar la petición para crear el producto
    response = test_client.post("/api/productos/", json=producto_data)

    # 4. Verificar la respuesta
    assert response.status_code == 201
    response_data = response.json()
    assert "data" in response_data
    data = response_data["data"]
    assert data["nombre"] == producto_data["nombre"]
    assert data["codigo"] == producto_data["codigo"]
    assert "id" in data

    # 5. Verificar que el producto se guardó en la base de datos
    # Nota: El modelo Producto no se importa directamente aquí para la verificación
    # en la BD, ya que la prueba se centra en la respuesta de la API.
    # La verificación de la BD se hace para asegurar la persistencia.
    db_producto = db_session.get(Producto, data["id"])
    assert db_producto is not None
    assert db_producto.nombre == "Producto Test"
