from jose import JWTError, jwt
from fastapi import APIRouter,Depends
from datetime import datetime,timedelta
from passlib.context import CryptContext
from decouple import config
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from ..usersdir.schema import UserLogin

from ..database import async_get_db
from psycopg.rows import class_row

async_pool=async_get_db()





router=APIRouter(
    prefix="/token",tags=["login"]
)

#Init secret and algoritm
SECRET=config("secret")
ALGORITHM=config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = config("access_token_expire_minute")
#Return token response

pswd_context=CryptContext(schemes=["bcrypt"],deprecated='auto')

def hash_pswd(password:str)->str:
    return pswd_context.hash(password)
def verify_pswd(plain_pswd:str,hash_pswd:str)->bool:
    return pswd_context.verify(plain_pswd,hash_pswd)

def create_access_token(data:dict,expires_delta:timedelta=None):
    token_encode=data.copy()
    expire=datetime.now()+(expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    token_encode.update({"exp":expire})
    return jwt.encode(token_encode,SECRET,algorithm=ALGORITHM)

async def authenticate_user(user:UserLogin,password:str):
    async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(UserLogin))as cur:
        await cur.execute("SELECT password FROM users WHERE username = %s", [user.username,])
        result = await cur.fetchone()
        if user and verify_pswd(password, user["password"]):
            return user
        return None

oauth_schene=OAuth2PasswordBearer(tokenUrl="login")
async def get_current_user(token:str=Depends(oauth_schene)):
    try:
        payload=jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        role:str=payload.get("sub")
        if username is None and role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
        return username,role
    except JWTError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
    
    
    
    
