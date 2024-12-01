from fastapi import FastAPI
from .usersdir.user_router import router as u_router
from .bookdir.book_router import router as b_router
from .auth.jwt_router import router as auth_router
from contextlib import asynccontextmanager 
import psycopg


async def get_db():
    connect = await psycopg.AsyncConnection.connect(
        "postgresql://postgres:@@sl8998@localhost/bookblogdb"
    )
    try:
        yield connect
    finally:
        await connect.close()

@asynccontextmanager
async def lifespan(app:FastAPI):
    get_db()
    yield
app=FastAPI(lifespan=lifespan)



    

app.include_router(u_router)
app.include_router(b_router)
app.include_router(auth_router)






        
    


    
    