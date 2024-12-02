from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id:int
    title:str
    description:Optional[str]=None
    author:str
    comment:Optional[str]=None
    janr:str
    isresponse:Optional[bool]
    ispublished:Optional[bool]
class CreateBook(BaseModel):
    title:str
    description:Optional[str]=None
    author_id:int
    comment:Optional[str]=None
    janr:str
    
class ResponseBook(BaseModel):
    isresponse:Optional[bool]
class PublishedBook(BaseModel):
    ispublished:Optional[bool]



   
    
