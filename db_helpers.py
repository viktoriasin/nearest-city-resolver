from sqlalchemy import create_engine

from aiohttp_server.server.db import construct_db_url
from aiohttp_server.server.settings import load_config


def get_engine(db_config):
    db_url = construct_db_url(db_config)
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


def setup_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']
    db_pass = target_config['DB_PASS']

    with engine.connect() as conn:
        conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
        conn.execute("CREATE DATABASE %s" % db_name)
        conn.execute("ALTER DATABASE %s OWNER TO %s" % (db_name, db_user))
        conn.execute("GRANT ALL ON SCHEMA public TO %s" % db_user)


def teardown_db(executor_config=None, target_config=None):
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']

    with engine.connect() as conn:
        conn.execute("""
          SELECT pg_terminate_backend(pg_stat_activity.pid)
          FROM pg_stat_activity
          WHERE pg_stat_activity.datname = '%s'
            AND pid <> pg_backend_pid();""" % db_name)
        conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
        conn.execute("REVOKE ALL ON SCHEMA public FROM %s" % db_user)
        conn.execute("DROP ROLE IF EXISTS %s" % db_user)


def create_tables(target_config=None):
    engine = get_engine(target_config)
    with engine.connect() as conn:
        conn.execute('''
                CREATE TABLE cities(
                    city_name text PRIMARY KEY,
                    geog geography
                )
            ''')
        conn.execute("CREATE INDEX ON cities USING gist(geog);")


def drop_tables(target_config=None):
    engine = get_engine(target_config)

    with engine.connect() as conn:
        conn.execute('''
                DROP TABLE cities;
            ''')


if __name__ == '__main__':
    config = load_config("admin_config.yaml")['postgres']
    create_tables(target_config=config)
