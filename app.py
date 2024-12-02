from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .usersdir.user_router import router as u_router
from .bookdir.book_router import router as b_router
from .database import async_get_db



app=FastAPI()

origins=[
    "http://localhost:5500",
    "http://127.0.0.1:5500"
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
async def async_get_database():
    conn=async_get_db()
    try:
        yield conn

    finally:
        conn.close()


app.include_router(u_router)
app.include_router(b_router)






        
    


    
    