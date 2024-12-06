from fastapi import APIRouter,Depends,Query,Path,HTTPException,status
from schemas.users import User,UpdateUser
from package.service.users import updateuser, view_user_by_id,print_users, blockeduser
from package.controller.middleware import checkautherization
from typing import Any,List
from package.service.jwt_hand import Payloads



router=APIRouter(
    prefix="/api/users",tags=["users"]

)
@router.get("/",response_model=None)
async def print_user(users:Payloads=Depends(checkautherization),lock:bool=Query())->Any:
    if users.user_id>1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await print_users(lock)

@router.get("/{id}",response_model=None)
async def print_user_by_id(users:Payloads=Depends(checkautherization),id:int=Path(ge=1),lock:bool=Query())->Any:
    if users.user_id>1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await view_user_by_id(id,lock)

@router.put("/{id}",response_model=None)
async def edit_user(user:UpdateUser,users:Payloads=Depends(checkautherization),id:int=Path(ge=1))->Any:
    if users.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await updateuser(id,user)

@router.delete("/{id}")
async def block_user(user:User,users:Payloads=Depends(checkautherization),id:int=Path(ge=1)):
    if users.role!="admin" :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await blockeduser(id,lock=True)






