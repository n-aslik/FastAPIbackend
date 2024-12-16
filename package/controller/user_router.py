from fastapi import APIRouter,Depends,Query,Path,HTTPException,status,Response
from schemas.users import User,UpdateUser,Block_User
from package.service.users import updateuser, view_user_by_id,print_users, blockeduser
from package.controller.middleware import checkautherization
from typing import Any
from package.service.jwt_hand import Payloads







router=APIRouter(
    prefix="/api/users",tags=["users"]

)
@router.get("/",response_model=None)
async def print_user(users:Payloads=Depends(checkautherization),lock:bool=Query(),role:str=Query())->Any:
    if users.otp_veryfied=="ok":
        if users.role!="admin" and users.role!="user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        if role=="admin" and users.role=="user"  :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        return await print_users(lock,role)

@router.get("/{id}",response_model=None)
async def print_user_by_id(users:Payloads=Depends(checkautherization),id:int=Path(ge=1),lock:bool=Query(),role:str=Query())->Any:
    if users.otp_veryfied=="ok":
        if users.role!="admin" and users.role!="user" :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        if role=="admin" and users.role=="user" :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        return await view_user_by_id(lock,role,id)

@router.put("/{id}",response_model=None)
async def edit_user(user:UpdateUser,users:Payloads=Depends(checkautherization),id:int=Path(ge=1))->Any:
    if users.otp_veryfied=="ok":
        if users.role!="admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        return await updateuser(id,user)

@router.delete("/{id}",response_model=None)
async def block_user(user:Block_User, users:Payloads=Depends(checkautherization),id:int=Path(ge=1))->Any:
    if users.otp_veryfied=="ok":
        if users.role!="admin" :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
        return await blockeduser(id,user)





