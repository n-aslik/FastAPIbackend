from fastapi import APIRouter,Depends,Query,Path
from schemas import users
from package.service import users_s 
from package.controller import middleware
from typing import Any
from package.controller import middleware

router=APIRouter(
    prefix="/api/users",tags=["users"]

)
@router.get("/",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def print_user()->Any:
    return await users_s.print_users(False)

@router.get("/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def print_user_by_id(id:int=Path(ge=1))->Any:
    return await users_s.view_user_by_id(False,id)

@router.put("/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def edit_user(user:users.UpdateUser,id:int=Path(ge=1))->Any:
   return await users_s.updateuser(id,user)

@router.delete("/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def block_user(user:users.Block_User,id:int=Path(ge=1))->Any:
     return await users_s.blockeduser(id,user)

@router.post("/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def disable_verify(id:int=Path(ge=1))->Any:
    return await users_s.verify_disable(id)






