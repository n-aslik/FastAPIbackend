from fastapi import APIRouter,Depends 
from .book_queries import get_books,get_book_by_id,create_books,update_book,delete_books,check_as_response,check_as_publish
from ..bookdir.schema import Book,DeleteBook,CreateBook,ResponseBook,PublishedBook
from ..database import create_db
from ..auth.jwt_router import get_current_user
from typing import Annotated

router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/",response_model=None)
async def print_books(book:Annotated[Book,Depends(get_current_user)],db=Depends(create_db))->list[Book]:
    return await get_books(db,book=book)
@router.get("/{id}",response_class=None)
async def print_books_by_id(id:int,book:Annotated[Book,Depends(get_current_user)],db=Depends(create_db))->Book:
    return await get_book_by_id(db,id=id,book=book)
@router.post("/",response_model=None)
async def add_book(book:Annotated[CreateBook,Depends(get_current_user)],db=Depends(create_db))->CreateBook:
    return await create_books(db,book=book)
@router.put("/{id}",response_model=None)
async def edit_book(id:int,book:Annotated[CreateBook,Depends(get_current_user)],db=Depends(create_db))->CreateBook:
    return await update_book(db,book=book,id=id)
@router.delete("/{id}",response_model=None)
async def remove_book(id:int,book:Annotated[CreateBook,Depends(get_current_user)],db=Depends(create_db))->DeleteBook:
    return await delete_books(db,book=book,id=id)
@router.patch("/{id}",response_model=None)
async def check_in_response(id:int,book:Annotated[CreateBook,Depends(get_current_user)],db=Depends(create_db))->ResponseBook:
    return await check_as_response(db,id=id,book=book)
@router.patch("/{id}",response_model=None)
async def publish_book(id:int,book:Annotated[CreateBook,Depends(get_current_user)],db=Depends(create_db))->ResponseBook:
    return await check_as_publish(db,id=id,book=book)

