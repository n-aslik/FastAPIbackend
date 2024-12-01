import asyncpg
import psycopg 
async def get_db():
    global connect
    connect = await psycopg.AsyncConnection.connect(
        "postgresql://postgres:@@sl8998@localhost/bookblogdb"
    )
    try:
        yield connect
    finally:
        await connect.close()





    

        
