import psycopg
from psycopg.rows import dict_row

db_parameter={
    "user":"postgres",
    "password":"@@sl8998",
    "host":"localhost",
    "port":5432,
}
async def  async_get_db():
    conn=  psycopg.connect(**db_parameter,autocommit=False,row_factory=dict_row)
    return conn
    

