from fastapi import HTTPException,status
from database.dbconn import async_get_db
from asyncpg  import Connection
import json
from utils import hash
import datetime


async def create_user(username:str,password:str,otp:str,exp:datetime):
    db:Connection=await async_get_db()
    hash_password=await hash.hashed_password(password)
    hash_otp=await hash.hashed_password(otp)
    await get_user_by_uname_and_password(username,password)
    await update_otp(hash_otp,username)
    await db.execute("CALL authuser.create_user($1,$2,$3,$4);",username,hash_password,hash_otp,exp)

async def update_user(username:str,password:str,role:str,id:int):
    db:Connection=await async_get_db()
    hash_password=await hash.hashed_password(password)
    await db.execute("CALL authuser.update_user($1,$2,$3,$4);",username,hash_password,role,id)
    
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

async def get_user_by_id(id:int):
    db:Connection=await async_get_db()
    user=await db.fetchval("SELECT  authuser.get_user_by_id($1);",id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    users=json.loads(user)
    users["password"]="****"
    return users
      
async def update_otp (otp:str,username:str):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.update_otp($1,$2);",otp,username)
    
async def verify_otp(uotp:str):
    db:Connection=await async_get_db()
    await db.execute("CALL authuser.verify_otp($1)",uotp)