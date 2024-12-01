from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool
from .usersdir.user_router import router as u_router
from .bookdir.book_router import router as b_router
from .auth.jwt_router import router as auth_router
from contextlib import asynccontextmanager

postgres_url ="postgresql://postgres:@@sl8998@localhost/bookblogdb"

app=FastAPI()

pool:AsyncConnectionPool=None
@asynccontextmanager
async def lifespan(app:FastAPI):
    global pool
    pool=AsyncConnectionPool(conninfo=postgres_url)
    try:
        yield
    finally:
        await pool.close()
app=FastAPI(lifespan=lifespan)

async def get_db():
    async with pool.connection() as conn:
        yield conn
    

app.include_router(u_router)
app.include_router(b_router)
app.include_router(auth_router)



        
    


    
    