from fastapi.responses import JSONResponse
from fastapi import HTTPException,APIRouter,Depends
from .schema import UserCreate,BlockUser,User
from ..database import async_get_db
from psycopg.rows import class_row

async_pool=async_get_db()





async def get_users(isblocked:bool):
    async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(User))as cur:
        await cur.execute("SELECT * FROM users as u WHERE u.isblocked=%s",[isblocked])
        users=await cur.fetchall()
        if not users:
            raise HTTPException(status_code=404,detail="users not found")
        return {"users":users}
        
async def get_user_by_id(id:int,user:User):
    async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(User))as cur:
        await cur.execute("SELECT * FROM users as u WHERE u.isblocked=%s AND u.id=%s", [id,user.isblocked])
        users =await cur.fetchone()
        if not users:
            raise HTTPException(status_code=404,detail="user`s by id not found")
        return {"user":users}
        
async def update_user(user:UserCreate,id:int):
    try:
        async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(UserCreate))as cur:
            await curs.execute("UPDATE users as u SET u.username=%s,u.password =%s,u.email=%s WHERE u.id=%s ",[id,user.username,user.password,user.email])
            users=await cur.fetchone()
            if users: 
                return JSONResponse(content=users)
            else:
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def blocked (id:int,user:BlockUser):
    try:
        async with async_pool.connection() as curs, curs.cursor(row_factory=class_row(BlockUser))as cur:
            await cur.execute("UPDATE users as u SET u.isblocked=%s WHERE u.id=%s",[id,user.isblocked])
            users= await cur.fetchone()
            if users:
                return JSONResponse(content=users)
            else:   
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
    

