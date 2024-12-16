
from fastapi import Depends
from schemas.books import PublishedBook,ResponseBook,Book
from package.repository.book_queries import get_book_by_id, get_books, create_books, check_as_response, check_as_publish, update_book,delete_books
async def createbook(book:Book):
    books=await create_books(book)
    return books

async def updatebook(book:Book,id:int):
    books=await update_book(book.title,book.description,book,book.comment,book.janr,id)
    return books

async def print_all_books(isresp:bool,ispub):
    books=await get_books(isresp,ispub)
    return {"books":books}

async def print_books_by_id(id:int,resp:bool,pub:bool):
    books=await get_book_by_id(id,resp,pub)
    return {"book":books}

async def check_book_resp(id:int,book:ResponseBook=Depends()):
    books=await check_as_response(id,book.isresponse)
    return books

async def check_book_pub(id:int,book:PublishedBook=Depends()):
    books=await check_as_publish(id,book.ispublished)
    return books

async def delete_book_by_id(id:int):
    books=await delete_books(id)
    return books