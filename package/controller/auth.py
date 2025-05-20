from fastapi import Depends,APIRouter,WebSocket,WebSocketDisconnect
from ..schemas import users
from typing import Any
from fastapi.responses import HTMLResponse
from ..repository import user_queries
from . import middleware
import random



router=APIRouter(prefix="/api",tags=["auth"])

@router.post("/sign-up")
async def sign_up(users: users.User):
    return await user_queries.create_user(users)
    
@router.post("/sign-in")
async def login(users: users.Login):
    return await user_queries.login(users)

@router.put("/forgot-password")
async def forgot_password(phone:str):
    symbols = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',0,1,2,3,4,5,6,7,8,9,'!','/','?','*',"$",'.']
    password = "".join(str(random.choice(symbols))for _ in range(6))
    return await user_queries.forgot_password(phone, password)

@router.put("/change-password")
async def change_password(phone:str, password:str, new_password: str):
    return await user_queries.change_password(phone, password, new_password)
