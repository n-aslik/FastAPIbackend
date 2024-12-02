from fastapi import APIRouter,Depends,HTTPException,Depends,status
from datetime import datetime,timedelta
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from ..usersdir.schema import UserLogin
from ..usersdir import user_queries
from ..database import async_get_db
from psycopg import  Connection
from typing import Annotated

security=HTTPBasic()
router=APIRouter(
    prefix="/token",tags=["login"]
)



async def authenticate_user(credentials:Annotated[HTTPBasicCredentials,Depends(security)],db:Connection=Depends(async_get_db)):
    user=user_queries.get_user_by_username(db,username=str(credentials.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"User {credentials.username} not found",headers={"WWW-Authenticate":"Basic"})
    return user




    
    
    
