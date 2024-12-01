from fastapi import FastAPI
from .usersdir.user_router import router as u_router
from .bookdir.book_router import router as b_router
from .auth.jwt_router import router as auth_router
from .database import get_connect_db

app=FastAPI()

get_connect_db

    

app.include_router(u_router)
app.include_router(b_router)
app.include_router(auth_router)






        
    


    
    