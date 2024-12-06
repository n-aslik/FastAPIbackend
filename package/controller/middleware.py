from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException,Depends,Security,status
from package.service.jwt_hand import Payloads
from package.service.jwt_hand import parse_token

security=HTTPBearer()
async def checkautherization(sec_route:HTTPAuthorizationCredentials=Security(security)):
    if not sec_route.scheme=="Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid auth scheme")
    token=sec_route.credentials
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Token is empty")
    return await parse_token(token)
    
    
    