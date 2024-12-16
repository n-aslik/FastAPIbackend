from pydantic import BaseModel
from typing import Optional



class User(BaseModel): 
    id:Optional[int]
    username:Optional[str]
    password:Optional[str]
    role:Optional[str]
    isblocked:Optional[bool]=None
    otp_veryfied:Optional[str]
    otp:str|None=None
    

class UpdateUser(BaseModel):
    username:Optional[str]=None
    password:Optional[str]=None
    
    
class Sign_Up(BaseModel):
    username:str
    password:str
    role:str="user"
    otp_veryfied:str="no"
    
class Sign_in(BaseModel):
    username:str
    password:str
    
class Block_User(BaseModel):
    isblocked:Optional[bool]=None
    
