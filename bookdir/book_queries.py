from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from bookdir.schema import DeleteBook,CreateBook,ResponseBook,PublishedBook,Book
from database import pool


async def get_books(book:Book):
    async with pool.connection() as conn:
        async with conn.cursor() as curs:
            books= await curs.execute("SELECT b.title,b.description, u.username, b.comment,b.janr FROM book as b JOIN users as u ON b.author_id=u.id WHERE b.isresponse=%s and b.ispublished=%s ",(book.isresponse,book.ispublished))
            if not books:
                raise HTTPException(status_code=404,detail="books not found")
            return {"books":books}
        
async def get_book_by_id(id:int, book:Book):
    async with pool.connection() as conn:
        async with conn.cursor() as curs:
            books= await curs.execute("SELECT b.title,b.description, u.username, b.comment,b.janr FROM book as b JOIN users as u ON b.author_id=u.id WHERE b.isresponse=%s and b.ispublished=%s ",(book.isresponse,book.ispublished))
            if not books:
                raise HTTPException(status_code=404,detail="book`s by id not found")
            return {"book":books}

async def create_books(book:CreateBook):
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as curs:
                books=await curs.execute("INSERT into books(title,description,author_id,comment,janr) VALUES(%s,%s,%s,%s)",(book.title,book.description,book.author_id,book.comment,book.janr))
                if not books:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad request")
                return JSONResponse(content=books)
    except:
        return {}
    
    
async def delete_books(book:DeleteBook,id:int):
    async with pool.connection() as conn:
        async with conn.cursor() as curs:
            books=await curs.execute("DELETE from books as b WHERE b.id=%s",(book.id))
            if not books:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book id not found")
            return JSONResponse(content=book)

async def update_book(book:CreateBook,id:int):
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as curs:
                books=await curs.execute("UPDATE books SET title=%s, description=%s,author_id=%s,comment=%s,janr=%s WHERE id=%s",(book.title,book.description,book.author_id,book.comment,book.janr,id))
                if books:   
                    return JSONResponse(content=books)
                else:
                    raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def check_as_response(id:int,book:ResponseBook):
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as curs:
                books=await curs.execute("UPDATE books SET isresponse=%s WHERE id=%s",(id,book.isresponse))
                if books:
                    return JSONResponse(content=books)
                else:
                    raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def check_as_publish(id:int,book:PublishedBook):
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as curs:
                books=await curs.execute("UPDATE books SET ispublished=%s WHERE id=%s",(id,book.ispublished))
                if books:
                    return JSONResponse(content=books)
                else:
                    raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
    
