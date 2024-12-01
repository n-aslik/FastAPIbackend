from fastapi import APIRouter,Depends
from .schema import User,UserCreate,BlockUser
from .user_queries import get_user_by_id,get_users,update_user,blocked
from ..auth.jwt_handler import get_current_user


router=APIRouter(
    prefix="/api/users",tags=["users"]

)
@router.get("/",response_model=User)
async def print_user(user:User=Depends(get_current_user)):
    return await get_users(user=user)
@router.get("/{id}",response_model=User)
async def print_user_by_id(id:int,user:User=Depends(get_current_user)):
    return await get_user_by_id(id=id,user=user)
@router.put("/{id}",response_model=UserCreate)
async def edit_user(id:int,user:UserCreate=Depends(get_current_user)):
    return await update_user(user=user,id=id)
@router.patch("/{id}",response_model=BlockUser)
async def block_user(id:int,user:BlockUser=Depends(get_current_user)):
    return await blocked(id=id,user=user)




