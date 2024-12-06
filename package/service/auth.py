from utils.hash import hashed_password
from package.repository.user_queries import get_user_by_username_and_password
from fastapi import HTTPException,status,Depends
from package.service.jwt_hand import create_access_token

async def sign_in(username:str,password:str)->dict:
    password =await hashed_password(password)
    try:
        users=await get_user_by_username_and_password(username,password)
        if  users is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
        access_token =await create_access_token(
            users["id"],
            users["username"],
            users["role"]
        )
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
       