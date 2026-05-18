import pytest
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.main import app
from src.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    """
    Проверяет, что приложение запущено в тестовом режиме
    """
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    """
    Создает асинхронный http клиент для тестирования
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    """
    Инициализирует тестовую базу данных перед запуском тестов
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
