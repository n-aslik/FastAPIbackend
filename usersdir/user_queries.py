from fastapi import HTTPException,Depends
from fastapi.responses import JSONResponse
from .schema import UserCreate,BlockUser,User
from ..database import create_db 
from ..auth.jwt_handler import get_current_user

# user_perm=get_current_user()
# for i in user_perm[u]

async def get_users(user:User,db=Depends(create_db)):
    users= await db.execute("SELECT * FROM users as u WHERE u.isblocked=%s",(user.isblocked))
    if not users:
        raise HTTPException(status_code=404,detail="users not found")
    return {"users":users}
async def get_user_by_id(id:int,user:User,db=Depends(create_db)):
    users=await db.execute("SELECT * FROM users as u WHERE u.isblocked=%s AND u.id=%s", (id,user.isblocked))
    if not users:
        raise HTTPException(status_code=404,detail="user`s by id not found")
    return {"user":users}
async def update_user(user:UserCreate,id:int,db=Depends(create_db)):
    try:
        users=await db.execute("UPDATE users as u SET u.username=%s,u.password =%s,u.email=%s WHERE u.id=%s ",(id,user.username,user.password,user.email))
        if users: 
            return JSONResponse(content=users)
        else:
            raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def blocked (id:int,user:BlockUser,db=Depends(create_db)):
    try:
        users=await db.execute("UPDATE users as u SET u.isblocked=%s WHERE u.id=%s",(id,user.isblocked))
        if users:
            return JSONResponse(content=users)
        else:
            raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
    
