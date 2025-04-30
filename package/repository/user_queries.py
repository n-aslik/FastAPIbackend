from fastapi import HTTPException,status
from database.dbconn import async_get_db
from asyncpg  import Connection
import json
from utils import hash
import datetime


async def create_user(username:str,password:str):
    db:Connection=await async_get_db()
    hash_password=await hash.hashed_password(password)
    users = await db.execute("CALL authuser.create_user($1, $2, $3);",username,hash_password,'{}')
    if users['status'] == 0:
        return users

async def update_user(username:str,password:str,role:str,id:int):
    db:Connection=await async_get_db()
    hash_password=await hash.hashed_password(password)
    users = await db.execute("CALL authuser.update_user($1, $2, $3, $4, $5);",username, hash_password, role, id, '{}')
    if users['status'] == 0:
        return users


async def get_user_by_uname_and_password(username: str, password: str):
    db: Connection = await async_get_db()
    users = await db.fetchval("SELECT authuser.get_user_by_username_and_password($1, $2);", username, password)
    if not users:
        raise ValueError("User not found or incorrect password")
    return users

async def get_user_by_id(id:int):
    db:Connection=await async_get_db()
    users=await db.fetchval("SELECT  authuser.get_user_by_id($1);",id)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    users["password"]="****"
    return users
      
