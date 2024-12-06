from pydantic import BaseModel
from typing import Optional

class User(BaseModel): 
    id:Optional[int]
    username:Optional[str]
    password:Optional[str]
    role:Optional[str]
    isblocked:Optional[bool]=False
    
class ViewUser(BaseModel): 
    id:Optional[int]
    username:Optional[str]
    role:Optional[str]
    isblocked:Optional[bool]=False

class UpdateUser(BaseModel):
    username:Optional[str]=None
    password:Optional[str]=None
    
    
class Sign_Up(BaseModel):
    username:str
    password:str
    role:str="user"
    
class Sign_in(BaseModel):
    username:str
    password:str
    

