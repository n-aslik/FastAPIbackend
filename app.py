from fastapi import FastAPI
from .usersdir.user_router import router as u_router
from .bookdir.book_router import router as b_router
from .auth.jwt_router import router as auth_router 
from .database import async_get_db
import asyncio
from contextlib import asynccontextmanager

async_conn=async_get_db()

async def check_async_connection_db():
    while True:
        await asyncio.sleep(600)
        print("check async connection")
        await async_conn.check()

@asynccontextmanager
async def lifespan(app:FastAPI):
    asyncio.create_task(check_async_connection_db())


app=FastAPI(lifespan=lifespan)



app.include_router(u_router)
app.include_router(b_router)
app.include_router(auth_router)





        
    


    
    