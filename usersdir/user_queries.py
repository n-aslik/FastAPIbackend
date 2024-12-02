from fastapi.responses import JSONResponse
from fastapi import HTTPException,Depends,status
from .schema import UserCreate,BlockUser,User
from ..database import async_get_db
from psycopg import Connection
from ..auth.jwt_handler import Hashingpassword





async def get_user_by_username(username:str,db:Connection=Depends(async_get_db)):
    users=await db.execute("SELECT username FROM account.users as u WHERE u.username=%s",(username)).fetchone()
async def get_users(user:BlockUser,db:Connection=Depends(async_get_db)):
    users=await db.execute("SELECT * FROM account.users as u WHERE u.isblocked=%s",(user.isblocked)).fetchall()
    if not users:
        raise HTTPException(status_code=404,detail="users not found")
    return {"users":users}
        
async def get_user_by_id(id:int,user:User,db:Connection=Depends(async_get_db)):
    users=await db.execute("SELECT * FROM account.users as u WHERE u.isblocked=%s AND u.id=%s", (id,user.isblocked)).fetchone()
    if not users:
        raise HTTPException(status_code=404,detail="user`s by id not found")
    return {"user":users}

async def create_user(user:UserCreate,db:Connection=Depends(async_get_db)):
    users=await db.execute("INSERT INTO account.users (username, password) VALUES (%s, %s)", (user.username, Hashingpassword.hash_pswd(user.password)))
    if users:
        return {"message":"user add successful"}  
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="add user not succesful")
      
async def update_user(user:UserCreate,id:int,db:Connection=Depends(async_get_db)):
    users=await db.execute("UPDATE account.users as u SET u.username=%s,u.password =%s,u.email=%s WHERE u.id=%s ",(id,user.username,user.password,user.email)).fetchone()
    if users: 
        return JSONResponse(content=users)
    else:
        raise HTTPException(status_code=400,detail="bad request")
    
    
async def blocked (id:int,user:BlockUser,db:Connection=Depends(async_get_db)):
    users= await db.execute("UPDATE account.users as u SET u.isblocked=%s WHERE u.id=%s",(id,user.isblocked)).fetchone()
    if users:
        return JSONResponse(content=users)
    else:   
        raise HTTPException(status_code=400,detail="bad request")

    
    

