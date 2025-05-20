from fastapi import APIRouter,Depends ,Path,Query
from ..repository import book_queries
from ..schemas import books
from typing import Any
from . import middleware
from ..service.jwt_hand import Payloads



router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/books",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def print_books(resp:bool=Query(),pub:bool=Query())->Any:
    return await book_queries.get_books(resp,pub)

@router.get("/books_by_id",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def view_books_by_id(id:int=Path(ge=1),resp:bool=Query(),pub:bool=Query())->Any:
    return await book_queries.get_book_by_id(id,resp,pub)

@router.post("/book",response_model=books.CreateBook)
async def add_book(book:books.CreateBook,user:Payloads=Depends(middleware.checkautherization))->Any:
    book.user_id=user.user_id
    return await book_queries.create_books(book)

@router.put("/book",response_model=books.Book,dependencies=[Depends(middleware.checkautherization)])
async def edit_book(book:books.CreateBook,id:int=Path())->Any:
    return await book_queries.update_book(id,book)

@router.delete("/book",dependencies=[Depends(middleware.checkautherization_admin_permission)])
async def remove_book(id:int=Path(ge=1)):
    return await book_queries.delete_books(id)

@router.patch("/response-book",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def check_in_response(id:int=Path(ge=1))->Any:
    return await book_queries.check_as_response(id)

@router.patch("/publish-book",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def publish_book(id:int=Path(ge=1))->Any:
    return await book_queries.check_as_publish(id)

