from fastapi import APIRouter,Depends 
from .book_queries import get_books,get_book_by_id,create_books,update_book,delete_books,check_as_response,check_as_publish
from .schema import Book,CreateBook,ResponseBook,PublishedBook
from ..auth.jwt_handler import authenticate_user
from typing import Annotated
from fastapi.security import HTTPBasicCredentials




router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/",response_model=Book)
async def print_books(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],db=Depends(authenticate_user)):
    return await get_books(db=db,book=credentials)

@router.get("/{id}",response_model=Book)
async def print_books_by_id(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,db=Depends(authenticate_user)):
    return await get_book_by_id(db=db,id=id,book=credentials)

@router.post("/",response_model=CreateBook)
async def add_book(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],db=Depends(authenticate_user)):
    return await create_books(db=db,book=credentials)

@router.put("/{id}",response_model=CreateBook)
async def edit_book(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,db=Depends(authenticate_user)):
    return await update_book(db=db,book=credentials,id=id)

@router.delete("/{id}")
async def remove_book(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,db=Depends(authenticate_user)):
    return await delete_books(db=db,book=credentials,id=id)

@router.patch("/{id}",response_model=ResponseBook)
async def check_in_response(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,book:ResponseBook,db=Depends(authenticate_user)):
    return await check_as_response(db=db,id=id,book=credentials)

@router.patch("/{id}",response_model=PublishedBook)
async def publish_book(credentials:Annotated[HTTPBasicCredentials,Depends(authenticate_user)],id:int,book:PublishedBook,db=Depends(authenticate_user)):
    return await check_as_publish(db=db,id=id,user=credentials)

