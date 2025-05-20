from pydantic import BaseModel
from typing import Optional



class User(BaseModel): 
    username: str
    phone_number: str
    
class Login(BaseModel):
    phone_number: str
    password: str



   
