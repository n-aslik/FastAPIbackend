import psycopg
from psycopg_pool import AsyncConnectionPool
from functools import lru_cache

db_url="user=posrgres password=@@sl8998 host=localhost port=5432 db_name=bookblogdb"

@lru_cache
def async_get_db():
    return AsyncConnectionPool(conninfo=db_url)

