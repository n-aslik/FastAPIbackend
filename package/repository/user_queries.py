from fastapi import HTTPException,status
from database.dbconn import async_get_db
from asyncpg  import Connection
from package.service.jwt_hand import create_access_token, create_refresh_token
from schemas import users
from utils import hash
import datetime


async def create_user(data: users.User):
    with async_get_db() as db:
        cur = db.cursor()
        hash_password = await hash.hashed_password(data.password)
        cur.execute("CALL authuser.create_user(%s, %s, %s);",(data.username, hash_password, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")


async def update_user(id:int, data: users.UpdateUser):
    with async_get_db() as db:
        cur = db.cursor()
        hash_password=await hash.hashed_password(data.password)
        cur.execute("CALL authuser.update_user(%s, %s, %s, %s, %s);" ,(data.username, hash_password, role, id, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")


async def change_password(username:str, password: str):
    with async_get_db() as db:
        cur = db.cursor()
        hash_password =await hash.hashed_password(password)
        cur.execute("CALL authuser.change_password(%s, %s, %s);" ,(username, hash_password, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")

async def login(data: users.Signs):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.login(%s, %s, %s);" ,(data.username, data.password, '{}'))
        users = cur.fetchone()[0]
        print(users)
        if users['status'] == 0:
            users['access_token'] = create_access_token(users['id'], data.username, data.role )
            users['refresh_token'] = create_refresh_token(users['id'], data.username, data.role)
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")
 
async def get_user_by_id(id:int):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("SELECT  authuser.get_user_by_id(%s);", (id,))
        users = cur.fetchone()[0]
        users["password"]="****"
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")
      
