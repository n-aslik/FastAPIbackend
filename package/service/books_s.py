from fastapi import HTTPException,status
from schemas.books import Book,PublishedBook,ResponseBook
from package.repository.book_queries import get_book_by_id, get_books, create_books, check_as_response, check_as_publish, update_book,delete_books

async def createbook(book:Book):
    books=await create_books(book)
    if not books:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    elif books:
        raise HTTPException(status_code=status.HTTP_201_CREATED)
    return books

async def updatebook(book:Book,id:int):
    books=await update_book(book.title,book.description,book.author_id,book.comment,book.janr)
    if not books:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return books

async def print_all_books(isresp:bool,ispub):
    books=await get_books(isresp,ispub)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"books":books}

async def print_books_by_id(id:int,resp:bool,pub:bool):
    books=await get_book_by_id(id,resp,pub)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"book":books}

async def check_book_resp(id:int,book:ResponseBook):
    books=await check_as_response(id,book.isresponse)
    if not books:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return books

async def check_book_pub(id:int,book:PublishedBook):
    books=await check_as_publish(id,book.ispublished)
    if not books:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return books

async def delete_book_by_id(id:int):
    books=await delete_books(id)
    if not books:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return books