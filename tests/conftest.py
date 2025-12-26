# Fixtures for testing the FastAPI application
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

# --- Configuración de la Base de Datos de Pruebas ---

# Usar una base de datos SQLite en memoria para las pruebas
# La opción check_same_thread es necesaria para SQLite.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixtures de Pytest ---

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Fixture para configurar la base de datos de prueba una vez por sesión.
    """
    # Eliminar la base de datos de prueba si existe de una ejecución anterior
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    # Crear todas las tablas en la base de datos de prueba
    Base.metadata.create_all(bind=engine)
    yield
    # Limpieza: cerrar todas las conexiones y eliminar la base de datos
    engine.dispose()
    os.remove("./test.db")


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture para crear una sesión de base de datos para cada función de prueba.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Fixture que crea un TestClient para cada prueba, sobreescribiendo la dependencia `get_db`
    para usar la sesión de base de datos de prueba.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    # Limpiar el override después de la prueba
    app.dependency_overrides.pop(get_db, None)

