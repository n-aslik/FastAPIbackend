from fastapi import APIRouter,Depends ,Path,Query,HTTPException,status,Body
from package.service.books_s import createbook, updatebook, check_book_pub, check_book_resp, print_all_books, print_books_by_id,delete_book_by_id
from schemas.books import Book,CreateBook,ResponseBook,PublishedBook
from typing import Any
from package.controller.middleware import checkautherization
from package.service.jwt_hand import Payloads



router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/",response_model=None)
async def print_books(users:Payloads=Depends(checkautherization),resp:bool=Query(),pub:bool=Query())->Any:
     return await print_all_books(resp,pub)

@router.get("/{id}",response_model=None)
async def view_books_by_id(users:Payloads=Depends(checkautherization),id:int=Path(ge=1),resp:bool=Query(),pub:bool=Query())->Any:
    return await print_books_by_id(id,resp,pub)

@router.post("/",response_model=CreateBook)
async def add_book(book:CreateBook,users:Payloads=Depends(checkautherization))->Any:
    book.user_id=users.user_id
    return await createbook(book)

@router.put("/{id}",response_model=CreateBook)
async def edit_book(book:CreateBook,id:int=Path(),users:Payloads=Depends(checkautherization))->Any:
    if users.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await updatebook(id,book)

@router.delete("/{id}")
async def remove_book(users:Payloads=Depends(checkautherization),id:int=Path(ge=1)):
    if users.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await delete_book_by_id(id)

@router.patch("/response/{id}",response_model=None)
async def check_in_response(book:ResponseBook,users:Payloads=Depends(checkautherization),id:int=Path(ge=1))->Any:
    if users.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await check_book_resp(id,book)

@router.patch("/publish/{id}",response_model=None)
async def publish_book(book:PublishedBook,users:Payloads=Depends(checkautherization),id:int=Path(ge=1))->Any:
    if users.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied")
    else:
        return await check_book_pub(id,book)

