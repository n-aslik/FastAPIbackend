from fastapi import Depends
from schemas.users import User,UpdateUser,Block_User
from package.repository.user_queries import get_user_by_id, get_users, update_user, blocked,create_user
from utils.hash import hashed_password

async def createuser(user:User=Depends()):
    user.password=await hashed_password(user.password)
    new_user=await create_user(user)
    return new_user

async def updateuser(id:int,user:UpdateUser=Depends()):
    user.password=await hashed_password(user.password)
    users=await update_user(user.username,user.password,id)
    return users

async def blockeduser(id:int,user:Block_User=Depends()):
    users= await blocked(id,user.isblocked)
    return users

async def print_users(lock:bool,role:str):
    users=await get_users(lock,role)
    return {"users":users}

async def view_user_by_id(lock:bool,role:str,id:int):
    users=await get_user_by_id(lock,role,id)
    return {"user":users}
    

        
    
    

