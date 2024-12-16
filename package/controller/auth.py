from fastapi import Depends,HTTPException,status,APIRouter,Response
from schemas.users import Sign_in,Sign_Up,User
from typing import Any
from package.service.auth import sign_in
from package.service.users import createuser
from database.dbconn import async_get_db
from asyncpg import Connection
import random
import time
from package.controller.middleware import checkautherization
from package.service.jwt_hand import Payloads





router=APIRouter(prefix="/api",tags=["auth"])

@router.post("/sign-up",response_model=Sign_Up)
async def sign_up(user:Sign_Up=Depends())->Any:
    users=await createuser(user)
    if  users:
        raise HTTPException(status_code=status.HTTP_201_CREATED,detail="User add  successful")
    return {"username":user.username,"password":"****","role":user.role,"otp_veryfied":user.otp_veryfied}
    
@router.post("/sign-in",response_model=None)
async def login(users:Sign_in=Depends())->Any:
    try:
        access_token=await sign_in(users.username,users.password)
        return {"access token":access_token,"token type":"Bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
    
    
@router.post("/otp-gen",dependencies=[Depends(checkautherization)])
async def generate_otp():
    global otp
    otp=""
    for i in range(6):
        otp+=str(random.randint(0,9))
    return {"otp":otp}
    
@router.post("/otp-ver")
async def verified_otp(otpc:str,user:Payloads=Depends(checkautherization)):
    db:Connection=await async_get_db()
    if otpc==otp:
        user.otp_veryfied="ok"
    await db.execute("CALL authuser.update_user_otp2($1,$2)",user.otp_veryfied,user.user_id)
    return user.otp_veryfied

@router.post("/dis-otp")
async def verified_otp(user:Payloads=Depends(checkautherization)):
    db:Connection=await async_get_db()
    if user.otp_veryfied=="ok":
        user.otp_veryfied="no"
    await db.execute("CALL authuser.update_user_otp2($1,$2)",user.otp_veryfied,user.user_id)
    return user.otp_veryfied

    