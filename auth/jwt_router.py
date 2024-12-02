from fastapi import APIRouter,Depends,HTTPException,status
from ..usersdir.schema import UserLogin,Token,UserCheck
from .jwt_handler import hash_pswd,authenticate_user,create_access_token,get_current_user
from ..database import async_get_db
from psycopg.rows import class_row

async_pool=async_get_db()

router=APIRouter(prefix="/api",tags={"auth"})



@router.post("/sign-up")
async def sign_up(user:UserLogin):
    async with async_pool.connection() as curs:
        hash_password=hash_pswd(user.password)
        await curs.execute("INSERT INTO users (username, password,role,email) VALUES (%s, %s,%s,%s)", [user.username, hash_password,user.role,user.email])
        return {"message":"user add successful"}
    
@router.post("/sign-in",response_model=Token)
async def sign_in(user:UserCheck):
    db_user=await authenticate_user(user.username,user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
    access_token=create_access_token("sub",user.username,user.role)
    return {"access token":access_token,"type":"Bearer"}
    

@router.get("/protected")
async def closing_routers(current_user:str=Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}
    


        
    
