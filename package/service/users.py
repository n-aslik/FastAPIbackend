from fastapi import HTTPException,status,Depends
from schemas.users import User,UpdateUser
from package.repository.user_queries import get_user_by_id, get_users, update_user, blocked,get_user_by_username_and_password,create_user
from utils.hash import hashed_password

async def createuser(user:User=Depends()):
    try:
        user.password=await hashed_password(user.password)
        new_user=await create_user(user)
        if not new_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return new_user
    except Exception as e:
        return e

async def updateuser(id:int,user:UpdateUser=Depends()):
    user.password=await hashed_password(user.password)
    users=await update_user(user.username,user.password,id)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return users

async def blockeduser(lock:bool,id:int):
    users= await blocked(id,lock)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return users

async def print_users(lock:bool):
    users=await get_users(lock)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return users

async def view_user_by_id(lock:bool,id:int):
    users=await get_user_by_id(id,lock)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return users
    

        
    
    

