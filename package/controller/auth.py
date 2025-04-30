from fastapi import Depends,APIRouter
from schemas import users
from typing import Any
from package.repository import user_queries
from package.controller import middleware
import random
from datetime import datetime,timedelta



router=APIRouter(prefix="/api",tags=["auth"])

@router.post("/sign-up",response_model=users.Signs)
async def sign_up(user:users.Signs):
    return await user_queries.create_user(user.username,user.password)
    
@router.post("/sign-in", response_model = users.Signs)
async def login(users: users.Signs):
    return await user_queries.login(users)

@router.put("/change-password")
async def change_password(username:str):
    symbols = [['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',0,1,2,3,4,5,6,7,8,9,'!','/','?','*',"$",'.']]
    password = "".join(str(random.choice(symbols))for _ in range(6))
    return await user_queries.change_password(username, password)

    









    