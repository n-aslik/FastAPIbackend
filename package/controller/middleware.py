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
    if pload.role!="user" and pload.role =="admin":
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    return await parse_token(token)

async def checkautherization_admin_permission(sec_route:HTTPAuthorizationCredentials=Security(security)):
    if not sec_route.scheme=="Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid auth scheme")
    token=sec_route.credentials
    pload=await parse_token(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is empty")
    if pload.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    return await parse_token(token)

async def verify_user_otp(otp_val:str):
    hash_otp=await hash.hashed_password(otp_val)
    otp=await user_queries.get_otp(hash_otp)
    if not isinstance(otp,dict):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Invalid otp data format")
    if hash_otp!=otp.get("otp"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    await user_queries.verify_otp(hash_otp)
    return {"message":"Verify is successful"}
       

         


