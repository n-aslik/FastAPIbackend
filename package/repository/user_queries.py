from fastapi import HTTPException,status
from ...database.dbconn import async_get_db
from asyncpg  import Connection
import random
from ..service.jwt_hand import create_access_token, create_refresh_token
from ..schemas import users
import datetime


async def create_user(data: users.User):
    with async_get_db() as db:
        symbols = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',0,1,2,3,4,5,6,7,8,9,'!','/','?','*',"$",'.']
        password = "".join(str(random.choice(symbols))for _ in range(6))
        cur = db.cursor()
        cur.execute("CALL authuser.create_user(%s, %s, %s, %s);",(data.username, password, data.phone_number, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")


async def update_user(id:int, data: users.User):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.update_user(%s, %s, %s, %s);" ,(data.username, data.phone_number,  id, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")


async def forgot_password(phone:str, password: str):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.forgot_password(%s, %s, %s);" ,(phone, password, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")


async def change_password(phone:str, password: str, new_password: str):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.change_password(%s, %s, %s, %s);" ,(phone, password, new_password, '{}'))
        users = cur.fetchone()[0]
        if users['status'] == 0:
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")

async def login(data: users.Login):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.login(%s, %s, %s);" ,(data.phone_number, data.password, '{}'))
        users = cur.fetchone()[0]
        print(users)
        if users['status'] == 0:
            users['access_token'] = create_access_token(users['id'], data.phone_number, users['role'] )
            users['refresh_token'] = create_refresh_token(users['id'], data.phone_number, users['role'])
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")
 
async def get_user_by_id(id:int):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("SELECT  authuser.get_user_by_id(%s);", (id,))
        users = cur.fetchone()[0]
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{users}")
      
