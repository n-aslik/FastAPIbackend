from fastapi.responses import JSONResponse
from fastapi import HTTPException,APIRouter,Depends
from .schema import UserCreate,BlockUser,User
import psycopg

async def get_db():
    global connect
    connect = await psycopg.AsyncConnection.connect(
        "postgresql://postgres:@@sl8998@localhost/bookblogdb"
    )
    try:
        yield connect
    finally:
        await connect.close()



# user_perm=get_current_user()
# for i in user_perm[u]

async def get_users(user:User):
    async with connect.cursor() as curs:
        users= await curs.execute("SELECT * FROM users as u WHERE u.isblocked=%s",(user.isblocked))
        if not users:
            raise HTTPException(status_code=404,detail="users not found")
        return {"users":users}
        
async def get_user_by_id(id:int,user:User):
    async with connect.cursor() as curs:
        users=await curs.execute("SELECT * FROM users as u WHERE u.isblocked=%s AND u.id=%s", (id,user.isblocked))
        if not users:
            raise HTTPException(status_code=404,detail="user`s by id not found")
        return {"user":users}
        
async def update_user(user:UserCreate,id:int):
    try:
        async with connect.cursor() as curs:
            users=await curs.execute("UPDATE users as u SET u.username=%s,u.password =%s,u.email=%s WHERE u.id=%s ",(id,user.username,user.password,user.email))
            if users: 
                return JSONResponse(content=users)
            else:
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def blocked (id:int,user:BlockUser):
    try:
        async with connect.cursor() as curs:
            users=await curs.execute("UPDATE users as u SET u.isblocked=%s WHERE u.id=%s",(id,user.isblocked))
            if users:
                return JSONResponse(content=users)
            else:   
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
    

