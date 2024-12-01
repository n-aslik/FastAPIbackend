from psycopg_pool import AsyncConnectionPool


postgres_url ="postgresql://postgres:@@sl8998@localhost/bookblogdb"

async def get_connect_db():
    global pool
    pool=AsyncConnectionPool(conninfo=postgres_url)
    try:
        yield
    finally:
        await pool.close()
    

        
