from fastapi import FastAPI
from package.controller.book_router import router as b_router
from package.controller.user_router import router as u_router
from database.dbconn import async_get_db
from package.controller.auth import router as a_router
import uvicorn



app=FastAPI()
async def async_get_database():
    conn=async_get_db(conn)
    try:
        yield conn
    finally:
        conn.close()
        

app.include_router(u_router)
app.include_router(b_router)
app.include_router(a_router)
if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=5500)




        
    


    
    