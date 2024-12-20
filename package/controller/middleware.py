from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException,Security,status
from package.service.jwt_hand import parse_token
from package.repository import user_queries
from utils import hash

security=HTTPBearer()


async def checkautherization(sec_route:HTTPAuthorizationCredentials=Security(security)):
    if not sec_route.scheme=="Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid auth scheme")
    token=sec_route.credentials
    pload=await parse_token(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is empty")
    if pload.otp_verify!="yes":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="OTP is not verified")
    return await parse_token(token)

async def createuser(username:str,password:str,otp:str):
    hash_password=await hash.hashed_password(password)
    get_user=await user_queries.get_user_by_uname_and_password(username,hash_password)
    if not get_user:
        return await user_queries.create_user(username,hash_password,otp)
    
async def generate_otp(username:str,password:str,otp:str):
    hash_password=await hash.hashed_password(password)
    get_user=await user_queries.get_user_by_uname_and_password(username,hash_password)
    if get_user:
        return await user_queries.update_otp(otp)
        

async def verify_user_otp(otp_val:str):
    otp=await user_queries.get_otp(otp_val)
    if not isinstance(otp,dict):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Invalid otp data format")
    if otp_val!=otp["otp"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    await user_queries.verify_otp(otp_val)
    return {"message":"Verify is successful"}
       

         


