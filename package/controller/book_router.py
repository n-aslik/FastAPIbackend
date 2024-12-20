from fastapi import APIRouter,Depends ,Path,Query
from package.service import books_s
from schemas import books
from typing import Any
from package.controller.middleware import checkautherization
from package.service.jwt_hand import Payloads



router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/",response_model=None,dependencies=[Depends(checkautherization)])
async def print_books(resp:bool=Query(),pub:bool=Query())->Any:
    return await books_s.print_all_books(resp,pub)

@router.get("/{id}",response_model=None,dependencies=[Depends(checkautherization)])
async def view_books_by_id(id:int=Path(ge=1),resp:bool=Query(),pub:bool=Query())->Any:
    return await books_s.print_books_by_id(id,resp,pub)

@router.post("/",response_model=books.CreateBook)
async def add_book(book:books.CreateBook,user:Payloads=Depends(checkautherization))->Any:
    book.user_id=user.user_id
    return await books_s.createbook(book)

@router.put("/{id}",response_model=books.Book,dependencies=[Depends(checkautherization)])
async def edit_book(book:books.Book,id:int=Path())->Any:
    return await books_s.updatebook(id,book)

@router.delete("/{id}",dependencies=[Depends(checkautherization)])
async def remove_book(id:int=Path(ge=1)):
    return await books_s.delete_book_by_id(id)

@router.patch("/response/{id}",response_model=None,dependencies=[Depends(checkautherization)])
async def check_in_response(book:books.ResponseBook,id:int=Path(ge=1))->Any:
    return await books_s.check_book_resp(id,book)

@router.patch("/publish/{id}",response_model=None,dependencies=[Depends(checkautherization)])
async def publish_book(book:books.PublishedBook,id:int=Path(ge=1))->Any:
    return await books_s.check_book_pub(id,book)

