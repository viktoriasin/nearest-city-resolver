import pytest

from aiohttp_server.server.main import init_app
from aiohttp_server.server.settings import load_config


@pytest.fixture
async def client(aiohttp_client):
    config = load_config('admin_config.yaml')  # TODO: Использовать тестовый конфиг с отдельной БД
    app = await init_app(config)
    return await aiohttp_client(app)
