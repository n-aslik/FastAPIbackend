from fastapi import APIRouter,Depends ,Path,Query
from package.repository import book_queries
from schemas import books
from typing import Any
from package.controller import middleware
from package.service.jwt_hand import Payloads



router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def print_books(resp:bool=Query(),pub:bool=Query())->Any:
    return await book_queries.get_books(resp,pub)

@router.get("/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def view_books_by_id(id:int=Path(ge=1),resp:bool=Query(),pub:bool=Query())->Any:
    return await book_queries.get_book_by_id(id,resp,pub)

@router.post("/",response_model=books.CreateBook)
async def add_book(book:books.CreateBook,user:Payloads=Depends(middleware.checkautherization))->Any:
    book.user_id=user.user_id
    return await book_queries.create_books(book)

@router.put("/{id}",response_model=books.Book,dependencies=[Depends(middleware.checkautherization)])
async def edit_book(book:books.Book,id:int=Path())->Any:
    return await book_queries.update_book(id,book)

@router.delete("/{id}",dependencies=[Depends(middleware.checkautherization_admin_permission)])
async def remove_book(id:int=Path(ge=1)):
    return await book_queries.delete_books(id)

@router.patch("/response/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def check_in_response(book:books.ResponseBook,id:int=Path(ge=1))->Any:
    return await book_queries.check_as_response(id,book)

@router.patch("/publish/{id}",response_model=None,dependencies=[Depends(middleware.checkautherization)])
async def publish_book(book:books.PublishedBook,id:int=Path(ge=1))->Any:
    return await book_queries.check_as_publish(id,book)

