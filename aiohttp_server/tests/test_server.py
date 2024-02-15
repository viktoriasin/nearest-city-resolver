from aiohttp_server.server.db import get_city_coordinates, get_cities
from aiohttp_server.server.utils import clean_city_name


async def test_two_same_post_request(client):
    route = "/cities/Волгоград"
    async with client.post(route) as resp1, client.post(route) as resp2:
        assert resp1.status == 201
        assert resp2.status == 201


async def test_addition_to_bd(client):
    city_name = 'Москва'
    route = f"/cities/{city_name}"
    async with client.post(route):
        async with client.app['db_pool'].acquire() as conn:
            lat, lon = await get_city_coordinates(conn, clean_city_name(city_name))
            assert lat is not None
            assert lon is not None
            cities = await get_cities(conn)
            assert clean_city_name(city_name) in [rec['city_name'] for rec in cities]


# TODO: Дописать тесты на все хэндлеры, замокать БД и поход в API
