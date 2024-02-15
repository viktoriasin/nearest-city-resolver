import asyncpgsa

DB_POOL = 'db_pool'


async def init_db(app):
    dsn = construct_db_url(app['config']['postgres'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app[DB_POOL] = pool
    return pool


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    postgres_config = config
    return DSN.format(
        user=postgres_config['DB_USER'],
        password=postgres_config['DB_PASS'],
        database=postgres_config['DB_NAME'],
        host=postgres_config['DB_HOST'],
        port=postgres_config['DB_PORT'],
    )


async def get_city_coordinates(conn, city_name):
    # TODO: Заиспользовать ORM
    result = await conn.fetchrow(
        '''SELECT
          ST_X(geog::geometry) AS lon,
          ST_Y(geog::geometry) AS lat FROM cities
          WHERE city_name=$1''', city_name
    )
    lon, lat = None, None
    if result is not None:
        lon = result[0]
        lat = result[1]
    return lon, lat


async def add_city(conn, city_name, lon, lat):
    await conn.execute('''INSERT INTO cities (city_name, geog) VALUES ($1, ST_MakePoint($2, $3))
            ON CONFLICT (city_name) DO NOTHING''', city_name, lon, lat)


async def delete_city(conn, city_name):
    await conn.execute('''DELETE FROM cities WHERE cities.city_name = $1''', city_name)


async def get_cities(conn):
    return await conn.fetch(
        '''SELECT
          city_name,
          ST_X(geog::geometry) AS lon,
          ST_Y(geog::geometry) AS lat 
          FROM cities
        '''
    )


async def get_nearest_cities(conn, lon, lat):
    return await conn.fetch(
        '''SELECT city_name,
          ST_X(geog::geometry) AS lon,
          ST_Y(geog::geometry) AS lat 
        FROM cities 
        ORDER BY cities.geog <-> ST_MakePoint($1,$2)::geography LIMIT 2;'''
        , lon, lat)
