from fastapi.testclient import TestClient

def test_root(test_client: TestClient):
    """
    Prueba que el endpoint raíz ("/") funciona y devuelve la información esperada.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["sistema"] == "MiTienda"
    assert data["version"] == "1.0.0"

def test_health_check(test_client: TestClient):
    """
    Prueba que el endpoint de salud ("/health") responde correctamente.
    """
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "message": "Sistema funcionando correctamente"}
