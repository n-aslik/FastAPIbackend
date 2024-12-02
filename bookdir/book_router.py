from fastapi import APIRouter,Depends 
from .book_queries import get_books,get_book_by_id,create_books,update_book,delete_books,check_as_response,check_as_publish
from .schema import Book,DeleteBook,CreateBook,ResponseBook,PublishedBook
from ..auth.jwt_router import get_current_user



router=APIRouter(prefix="/api/books",tags=["books"])

@router.get("/",response_model=Book)
async def print_books(book:Book=Depends(get_current_user)):
    return await get_books(book=book)
@router.get("/{id}",response_model=Book)
async def print_books_by_id(id:int,book:Book=Depends(get_current_user)):
    return await get_book_by_id(id=id,book=book)
@router.post("/",response_model=CreateBook)
async def add_book(book:CreateBook=Depends(get_current_user)):
    return await create_books(book=book)
@router.put("/{id}",response_model=CreateBook)
async def edit_book(id:int,book:CreateBook=Depends(get_current_user)):
    return await update_book(book=book,id=id)
@router.delete("/{id}",response_model=DeleteBook)
async def remove_book(id:int,book:DeleteBook=Depends(get_current_user)):
    return await delete_books(book=book,id=id)
@router.patch("/{id}",response_model=ResponseBook)
async def check_in_response(id:int,book:ResponseBook=Depends(get_current_user)):
    return await check_as_response(id=id,book=book)
@router.patch("/{id}",response_model=PublishedBook)
async def publish_book(id:int,book:PublishedBook=Depends(get_current_user)):
    return await check_as_publish(id=id,book=book)

