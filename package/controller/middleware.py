from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException,Security,status
from package.service.jwt_hand import parse_token
from package.repository import user_queries

security=HTTPBearer()


async def checkautherization(sec_route:HTTPAuthorizationCredentials=Security(security)):
    if not sec_route.scheme=="Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid auth scheme")
    token=sec_route.credentials
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is empty")
    return await parse_token(token)
   

async def verify_user_otp(otp_val:str):
    otp=await user_queries.get_otp(otp_val)
    if not isinstance(otp,dict):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Invalid otp data format")
    if otp_val!=otp["otp"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    await user_queries.verify_otp(otp_val)
    return {"message":"Verify is successful"}
       

         


