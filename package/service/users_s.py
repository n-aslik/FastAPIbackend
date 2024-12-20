from fastapi import Depends
from schemas.users import UpdateUser,Block_User
from package.repository import user_queries
from utils.hash import hashed_password


    
async def updateuser(id:int,user:UpdateUser=Depends()):
    user.password=await hashed_password(user.password)
    users=await user_queries.update_user(user.username,user.password,id)
    return users

async def blockeduser(id:int,user:Block_User=Depends()):
    users= await user_queries.blocked(id,user.isblocked)
    return users

async def print_users(lock:bool):
    users=await user_queries.get_users(lock)
    return {"users":users}

async def view_user_by_id(lock:bool,id:int):
    users=await user_queries.get_user_by_id(lock,id)
    return {"user":users}


async def verify_disable(id:int):
    await user_queries.disable_otp_verify(id)
    return {"message":"Disable  otp verify is successful"}
    

        
    
    

