from pydantic import BaseModel,EmailStr
from typing import Optional,Annotated

class User(BaseModel):
    id:int
    username:str
    password:str
    email:EmailStr
    role:str
    isblocked:bool
    
class Token(BaseModel):
    access_token:str
    token_type:str

class UserLogin(BaseModel):
    username:str
    password:str
    role:str
    email:EmailStr
    
class UserCheck(BaseModel):
    username:str
    password:str 
    
    
class UserCreate(BaseModel):
    username:str
    password:str
    email:EmailStr
    role:str
    isblocked:Optional[bool]
    
class BlockUser(BaseModel):
    isblocked:Optional[bool]
