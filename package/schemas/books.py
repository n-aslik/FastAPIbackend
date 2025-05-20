from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    user_id: Optional[int] = None
    comment: Optional[str] = None
    janr: str
    isresponse: Optional[bool] = False
    ispublished: Optional[bool] = False
    
class CreateBook(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: Optional[int] = None
    comment: Optional[str] = None
    janr: str
    isresponse: Optional[bool] = False
    ispublished: Optional[bool] = False
    



   
    
