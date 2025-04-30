from fastapi import Depends,APIRouter
from schemas import users
from typing import Any
from package.service.auth import sign_in
from package.repository import user_queries
from package.controller import middleware
import random
from datetime import datetime,timedelta



router=APIRouter(prefix="/api",tags=["auth"])

@router.post("/sign-up",response_model=users.Signs)
async def sign_up(user:users.Signs=Depends())->Any:
    users = await user_queries.create_user(user.username,user.password)
    if users['status']==0:
        return users

    
@router.post("/sign-in",response_model=None)
async def login(users:users.Signs=Depends())->Any:
    access_token=await sign_in(users.username,users.password)
    return access_token
    









    