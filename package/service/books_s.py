
from fastapi import Depends
from schemas.books import PublishedBook,ResponseBook,Book,CreateBook
from package.repository import book_queries

async def createbook(book:CreateBook):
    books=await book_queries.create_books(book)
    return books

async def updatebook(book:Book,id:int):
    books=await book_queries.update_book(book.title,book.description,book,book.comment,book.janr,id)
    return books

async def print_all_books(isresp:bool,ispub):
    books=await book_queries.get_books(isresp,ispub)
    return {"books":books}

async def print_books_by_id(id:int,resp:bool,pub:bool):
    books=await book_queries.get_book_by_id(id,resp,pub)
    return {"book":books}

async def check_book_resp(id:int,book:ResponseBook=Depends()):
    books=await book_queries.check_as_response(id,book.isresponse)
    return books

async def check_book_pub(id:int,book:PublishedBook=Depends()):
    books=await book_queries.check_as_publish(id,book.ispublished)
    return books

async def delete_book_by_id(id:int):
    books=await book_queries.delete_books(id)
    return books