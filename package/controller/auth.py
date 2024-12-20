from fastapi import Depends,HTTPException,status,APIRouter
from schemas import users
from typing import Any
from package.service.auth import sign_in
from package.controller import middleware
import random





router=APIRouter(prefix="/api",tags=["auth"])

@router.post("/sign-up",response_model=users.Registrer)
async def sign_up(user:users.Sign_Up=Depends())->Any:
    otp="".join(str(random.randint(0,9))for _ in range(6))
    await middleware.createuser(user.username,user.password,otp)
    await middleware.generate_otp(user.username,user.password,otp)
    return {"username":user.username,"password":"****","otp":otp}
    
    
@router.post("/sign-in",response_model=None)
async def login(users:users.Sign_in=Depends())->Any:
    try:
        access_token=await sign_in(users.username,users.password)
        return access_token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

@router.post("/otp-ver")
async def verified_otp(otp_val:str):
    return await middleware.verify_user_otp(otp_val)
    









    