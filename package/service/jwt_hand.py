from fastapi import Depends,HTTPException, status
import jwt
from typing import Optional
from datetime import datetime,timedelta
from os import getenv
from pydantic import BaseModel



jwt_secret=getenv("secret")
jwt_algorithm=getenv("algorithm")
access_expire_token=30


class Payloads(BaseModel):
    user_id:int
    username:str
    role:str
    otp_veryfied:str
    exp:datetime

async def create_access_token (user_id:int,username:str,role:str,otp_veryfied:str)->str:
    payload=Payloads(
        user_id=user_id,
        username=username,
        role=role,
        otp_veryfied=otp_veryfied,
        exp=(datetime.now()+timedelta(minutes=30))
    ).model_dump()
    encoded_token=jwt.encode(payload,jwt_secret,algorithm=jwt_algorithm)
    return encoded_token

async def parse_token (token:str)->Payloads:
    try:
        decoded_token=jwt.decode(token,jwt_secret,algorithms=jwt_algorithm)
        payload=Payloads(**decoded_token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    


