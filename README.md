# nearest-city-resolver

## Описание проекта

Это  HTTP-API, которое позволяет добавлять и удалять города с их координатами, а также по заданным координатам получать два ближайших места к ним.

Доступные хендлеры:
- `GET /cities` - получить список всех добавленных городов с их координатами
- `GET /cities/{name}` - получить координаты определенного города (при условии, что до этого он был добавлен в базу)
- `POST /cities/{name}` - добавить новый город
- `DELETE /cities/{name}` - удалить город из базы
- `GET /resolver?lat=52.479788&lon=62.185752` - получить два ближайших города к заданным координатам

## Установка и запуск проекта

1. Клонируем репозиторий, настриваем переменные окружения и устанавливаем зависимости.
2. Для работы проекта потребуется PostgreSQL c поддержкой работы с географическими объектами. Чтобы его настроить, нужно скачать и запустить PostGIS контейнер через докер:

    `docker run --name postgres -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=admin -d postgis/postgis`

3. Для получения координат городов используется стороннeе [API](https://geocode.maps.co/). Чтобы все заработало, необходимо зарегистрироваться на сайте и получить ключ доступа. После этого необходимо перейти в терминал и выполнить команду:
`export API_MAP_KEY='your_api_map_key'`

4. После этого необходимо перейти в корень проекта и запустить настройку БД:

   `python db_helpers.py`

5. После этого запускаем сервер командой:

   `python aiohttp_server/main.py`

## Тестирование

Запустить тесты можно командой:

`pytest tests/test_test_server.py`

## Используемые технологии

- `AIOHTTP`
- `asyncio`
- `PostgreSQL`
- `asyncpgsa`
- `PostGIS`
- `SQLAlchemy`
- `Pytest`
- `Docker`
