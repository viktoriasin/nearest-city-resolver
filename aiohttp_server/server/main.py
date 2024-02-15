import logging

from aiohttp import web

from aiohttp_server.client.client import AsyncClient
from aiohttp_server.server.db import init_db
from aiohttp_server.server.handler import CityHandler
from aiohttp_server.server.routes import setup_routes
from aiohttp_server.server.settings import load_config

logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def init_app(config):
    client = AsyncClient(config['map_api']['URL'])
    handler = CityHandler(client)
    app = web.Application()
    app['config'] = config
    await init_db(app)
    setup_routes(app, handler)
    return app


def main():
    config = load_config("admin_config.yaml")
    app = init_app(config)
    web.run_app(app)


if __name__ == '__main__':
    main()

