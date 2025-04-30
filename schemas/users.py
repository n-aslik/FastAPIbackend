from pydantic import BaseModel
from typing import Optional



class User(BaseModel): 
    id:Optional[int]
    username: Optional[str]
    password: Optional[str]
    role: Optional[str] = "user"
    isblocked: Optional[bool] = None
    
class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = "user"
    
class Signs(BaseModel):
    username: str
    password: str
    
    
class ChangePassword(BaseModel):
    password: str
    


   
