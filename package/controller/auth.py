from fastapi import Depends,HTTPException,status,APIRouter,Body
from schemas.users import Sign_in,Sign_Up
from typing import Any
from package.service.auth import sign_in
from package.service.users import createuser
from database.dbconn import async_get_db




router=APIRouter(prefix="/api",tags=["auth"])
@router.post("/sign-up",response_model=Sign_Up)
async def sign_up(user:Sign_Up=Depends())->Any:
    users=await createuser(user)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User add not successful")
    return {"username":user.username,"password":user.password,"role":user.role}
    
@router.post("/sign-in",response_model=None)
async def login(users:Sign_in=Depends())->Any:
    try:
        access_token=await sign_in(users.username,users.password)
        return {"access token":access_token,"token type":"Bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
        
       