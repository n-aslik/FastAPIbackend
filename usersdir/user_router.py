from fastapi import APIRouter,Depends
from ..usersdir.schema import User,UserCreate,BlockUser
from .user_queries import get_user_by_id,get_users,update_user,blocked
from ..auth.jwt_handler import get_current_user
from typing import Annotated
from ..database import create_db

router=APIRouter(
    prefix="/api/users",tags=["users"]

)
@router.get("/")
async def print_user(user:Annotated[User,Depends(get_current_user)],db=Depends(create_db))->list[User]:
    return await get_users(db,user=user)
@router.get("/{id}")
async def print_user_by_id(id:int,user:Annotated[User,Depends(get_current_user)],db=Depends(create_db))->User:
    return await get_user_by_id(db,id=id,user=user)
@router.put("/{id}")
async def edit_user(id:int,user:Annotated[UserCreate,Depends(get_current_user)],db=Depends(create_db))->UserCreate:
    return await update_user(db,user=user,id=id)
@router.patch("/{id}")
async def block_user(id:int,user:Annotated[BlockUser,Depends(get_current_user)],db=Depends(create_db))->BlockUser:
    return await blocked(db,id=id,user=user)




