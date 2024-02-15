from aiohttp import web

from aiohttp_server.server import db
from aiohttp_server.server.db import DB_POOL
from aiohttp_server.server.utils import check_and_extract_coordinate, clean_city_name


class CityHandler:

    def __init__(self, client):
        self.client = client

    async def get_root(self, request):
        return web.FileResponse('./static/index.html')

    async def get_cities(self, request):
        json_result = []
        async with request.app[DB_POOL].acquire() as conn:
            result = await db.get_cities(conn)
        if result is not None:
            json_result = [{rec["city_name"]: [rec["lat"], rec["lon"]]} for rec in result]
        return web.Response(text=str(json_result), status=200, content_type="application/json")

    async def get_city(self, request):
        city_name = clean_city_name(request.match_info['name'])
        async with request.app[DB_POOL].acquire() as conn:
            lon, lat = await db.get_city_coordinates(conn, city_name)
        if lon is not None:
            json_result = {"city_name": city_name, "lat": lat, "lon": lon}
            return web.Response(text=str(json_result), status=200, content_type="application/json")
        else:
            return web.Response(text=f"City is not found", status=404)

    async def add_city(self, request):
        city_name = clean_city_name(request.match_info['name'])
        async with request.app[DB_POOL].acquire() as conn:
            lon, lat = await db.get_city_coordinates(conn, city_name)
            if lon is None:
                lon, lat, status_code = await self.client.get_city_coordinates_by_name(city_name)
                if lon is None or lat is None:
                    if status_code == 200:
                        return web.Response(text=f"Bad request", status=400)
                    else:
                        return web.Response(text=f"Api error", status=status_code)
                await db.add_city(conn, city_name, lon, lat)
        return web.Response(text=str({"city_name": city_name, "lon": lon, "lat": lat}), status=201, content_type="application/json")

    async def delete_city(self, request):
        city_name = clean_city_name(request.match_info['name'])
        async with request.app[DB_POOL].acquire() as conn:
            await db.delete_city(conn, city_name)
        return web.Response(status=200)

    async def resolve_coordinates(self, request):
        lon = check_and_extract_coordinate(request.rel_url.query.get('lon', None), 'lon')
        lat = check_and_extract_coordinate(request.rel_url.query.get('lat', None), 'lat')
        if lon is not None and lat is not None:
            async with request.app[DB_POOL].acquire() as conn:
                cities = await db.get_nearest_cities(conn, lon, lat)
                json_result = [{"city_name": rec["city_name"], "lat": rec["lat"], "lon": rec["lon"]} for rec in cities]
            return web.Response(text=str(json_result), status=200, content_type="application/json")
        else:
            return web.Response(text=f"Invalid coordinate", status=406)
