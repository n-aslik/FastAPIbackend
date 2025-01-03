from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from package.controller.book_router import router as b_router
from package.controller.user_router import router as u_router
from database.dbconn import async_get_db
from package.controller.auth import router as a_router
import uvicorn
from os import getenv



app=FastAPI()
async def async_get_database():
    conn=async_get_db()
    try:
        yield conn
    finally:
        conn.close()
origins=[
    getenv("origin")
]        
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(u_router)
app.include_router(b_router)
app.include_router(a_router)
if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=5500)




        
    


    
    