from fastapi import HTTPException,status
from database.dbconn import async_get_db
from asyncpg  import Connection
import json





async def create_user(username:str,password:str,otp:str):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.create_user($1,$2,$3);",username,password,otp)
    

async def update_user(username:str,password:str,id:int):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.update_user($1,$2,$3);",username,password,id)
    
    
async def get_users(lock:bool):
    db:Connection=await async_get_db()
    users=await db.fetchval("SELECT authuser.get_all_users($1);",lock)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = json.loads(users)
    for  i in user:
        i["password"]="****"
    return user

async def get_otp(uotp:str):
    db:Connection=await async_get_db()
    users=await db.fetchval("SELECT authuser.get_user_otp($1);",uotp)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = json.loads(users)
    return user
    
    
async def get_user_by_uname_and_password(username: str, password: str):
    db: Connection = await async_get_db()
    user = await db.fetchval("SELECT authuser.get_user_by_username_and_password($1, $2);", username, password)
    if not user:
        raise ValueError("User not found or incorrect password")
    users = json.loads(user)
    return users

async def get_user_by_id(lock:bool,id:int):
    db:Connection=await async_get_db()
    user=await db.fetchval("SELECT  authuser.get_user_by_id($1,$2);",lock,id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    users=json.loads(user)
    users["password"]="****"
    return users
    
async def blocked (id:int,lock:bool):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.locked_user($1,$2);",lock,id)
    
async def update_otp (otp:str):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.update_otp($1);",otp)
    
    
async def verify_otp(uotp:str):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.verify_otp($1)",uotp)
    
   
async def disable_otp_verify(id:int):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.disable_verify($1)",id)

