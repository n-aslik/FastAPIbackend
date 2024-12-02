from fastapi import APIRouter,Depends
from .schema import User,UserCreate,BlockUser
from .user_queries import get_user_by_id,get_users,update_user,blocked,create_user
from ..auth.jwt_handler import authenticate_user
from typing import Annotated
from fastapi.security import HTTPBasicCredentials



router=APIRouter(
    prefix="/api/users",tags=["users"]

)
@router.get("/protected")
async def protected(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)]):
    return {"message":"main route"}

@router.post("/")
async def create_new_user(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],user:UserCreate,db=Depends(authenticate_user)):
    return await create_user(db=db,user=user)

@router.get("/",response_model=User)
async def print_user(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],db=Depends(authenticate_user)):
    return await get_users(db=db,user=credentials)

@router.get("/{id}",response_model=User)
async def print_user_by_id(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,db=Depends(authenticate_user)):
    return await get_user_by_id(db=db,id=id,user=credentials)

@router.put("/{id}",response_model=UserCreate)
async def edit_user(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,db=Depends(authenticate_user)):
    return await update_user(db=db,user=credentials,id=id)

@router.delete("/{id}",response_model=BlockUser)
async def block_user(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,db=Depends(authenticate_user)):
    return await blocked(db=db,id=id,user=credentials)




