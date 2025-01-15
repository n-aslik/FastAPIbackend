from fastapi import HTTPException, status
import jwt
from datetime import datetime,timedelta
from os import getenv
from pydantic import BaseModel



jwt_secret=getenv("secret")
jwt_algorithm=getenv("algorithm")
# access_expire_token=30


class Payloads(BaseModel):
    user_id:int
    username:str
    role:str
    otp_verify:str
    exp:datetime

async def create_access_token (user_id:int,username:str,role:str,otp_verify:str)->str:
    payload=Payloads(
        user_id=user_id,
        username=username,
        role=role,
        otp_verify=otp_verify,
        exp=(datetime.now()+timedelta(minutes=15))
    ).model_dump()
    encoded_token=jwt.encode(payload,jwt_secret,algorithm=jwt_algorithm)
    return encoded_token

async def create_refresh_token (user_id:int,username:str,role:str,otp_verify:str)->str:
    payload=Payloads(
        user_id=user_id,
        username=username,
        role=role,
        otp_verify=otp_verify,
        exp=(datetime.now()+timedelta(days=7))
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
    
    


