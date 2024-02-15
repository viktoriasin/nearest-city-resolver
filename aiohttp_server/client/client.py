import logging
import os

import aiohttp

from aiohttp_server.server.utils import check_and_extract_coordinate

logger = logging.getLogger(__name__)

class AsyncClient:

    def __init__(self, url):
        self.url = url

    async def get_city_coordinates_by_name(self, city_name):
        api_key = os.environ.get("API_MAP_KEY").strip()
        params = {'q': city_name, 'api_key': api_key}
        lon, lat = None, None
        async with aiohttp.ClientSession() as session:  # TODO: вынести на уровень выше; починить проблему с event loop
            try:
                async with session.get(self.url, params=params) as response:
                    status_code = response.status
                    if status_code == 200:
                        data = await response.json()
                        if data:
                            lon = check_and_extract_coordinate(data[0].get('lon', None), 'lon')
                            lat = check_and_extract_coordinate(data[0].get('lat', None), 'lat')
                    elif status_code == 401:
                        logger.ERROR(f'Wrong api key status = {status_code}')
                    elif status_code == 403:
                        logger.ERROR(f'User is blocked status = {status_code}')
                    elif status_code == 429:
                        logger.ERROR(f'Rate limit exceeded status = {status_code}')
                    elif status_code == 503:
                        logger.ERROR(f'Api server unavailable status = {status_code}')
                    else:
                        logger.ERROR(f'Unknown api error status = {status_code}')
            except aiohttp.ClientConnectorError as e:
                logger.ERROR(f'Connection Error', str(e))
        return lon, lat, status_code
