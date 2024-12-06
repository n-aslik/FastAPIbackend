from fastapi.responses import JSONResponse
from fastapi import HTTPException,status
from schemas.users import User
from database.dbconn import async_get_db
from asyncpg  import Connection








async def create_user(user:User):
    try:
        db:Connection=await async_get_db()
        users=await db.execute("INSERT INTO users(username,password,role) VALUES($1,$2,$3)RETURNING username,password role",user.username,user.password,user.role)
        if not users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return users
    except RuntimeError as re:
        await db.close()
        return re
               
        

async def update_user(username:str,password:str,id:int):
    try:
        db:Connection=await async_get_db()
        users=await db.execute("UPDATE users SET username=$1, password=$2 WHERE id=$3 ",username,password,id)
        if not users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return users
    except RuntimeError as re:
        await db.close()
        return re
    
async def get_users(lock:bool):
    try:
        db:Connection=await async_get_db()
        users=await db.fetch("SELECT u.username, u.role, u.isblocked FROM users as u WHERE u.isblocked=$1",lock)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users
    except RuntimeError as re:
        await db.close()
        return re
    
        


async def get_user_by_username_and_password(username:str,password:str):
    try:
        db:Connection=await async_get_db()
        users=await db.fetchrow("SELECT * FROM users WHERE username = $1 AND password = $2",username,password)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users
    except RuntimeError as re:
        await db.close()
        return re
    


    
async def get_user_by_id(id:int,lock:bool):
    try:
        db:Connection=await async_get_db()
        users=await db.fetchrow("SELECT u.username,u.role,u.isblocked FROM users as u WHERE u.isblocked=$1 AND u.id=$2", id,lock)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users
    except RuntimeError as re:
        await db.close()
        return re
    
    
        
async def blocked (id:int,lock:bool):
    try:
        db:Connection=await async_get_db()
        users=await db.execute("UPDATE users SET isblocked=$1 WHERE id=$2",id,lock)
        if not users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return users
    except RuntimeError as re:
        await db.close()
        return re
    

