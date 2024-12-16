from fastapi import HTTPException,status
from schemas.users import User
from database.dbconn import async_get_db
from asyncpg  import Connection
import json





async def create_user(user:User):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.create_user($1,$2,$3,$4);",user.username,user.password,user.role,user.otp_veryfied)
    
    

async def update_user(username:str,password:str,id:int):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.update_user($1,$2,$3);",username,password,id)
    
    
async def get_users(lock:bool,role:str):
    db:Connection=await async_get_db()
    users=await db.fetchval("SELECT authuser.get_all_users($1,$2);",lock,role)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = json.loads(users)
    for  i in user:
        i["password"]="****"
    return i
    
    
async def get_user_by_uname_and_password(username: str, password: str):
    db: Connection = await async_get_db()
    user = await db.fetchval("SELECT authuser.get_user_by_username_and_password($1, $2);", username, password)
    if not user:
        raise ValueError("User not found or incorrect password")
    users = json.loads(user)
    return users

    

async def get_user_by_id(lock:bool,role:str,id:int):
    db:Connection=await async_get_db()
    user=await db.fetchval("SELECT  authuser.get_user_by_id($1,$2,$3);", lock,role,id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    users=json.loads(user)
    return users
    
      
async def blocked (id:int,lock:bool):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.locked_user($1,$2);",lock,id)
    
    

