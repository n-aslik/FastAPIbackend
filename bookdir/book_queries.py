from fastapi import HTTPException,status,APIRouter,Depends
from fastapi.responses import JSONResponse
from .schema import CreateBook,ResponseBook,PublishedBook,Book
from ..database import async_get_db
from psycopg.rows import class_row

async_pool=async_get_db()




async def get_books(book:Book):
    async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(Book)) as cur:
        await cur.execute("SELECT b.title,b.description, u.username, b.comment,b.janr FROM book as b JOIN users as u ON b.author_id=u.id WHERE b.isresponse=%s and b.ispublished=%s ",[book.isresponse,book.ispublished])
        books=await cur.fetchall()
        if not books:
            raise HTTPException(status_code=404,detail="books not found")
        return {"books":books}
        
async def get_book_by_id(id:int, book:Book):
    async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(Book))as cur:
        await cur.execute("SELECT b.title,b.description, u.username, b.comment,b.janr FROM book as b JOIN users as u ON b.author_id=u.id WHERE b.isresponse=%s and b.ispublished=%s and b.id=%s ",[book.isresponse,book.ispublished,id])
        books =await cur.fetchone()
        if not books:
            raise HTTPException(status_code=404,detail="book`s by id not found")
        return {"book":books}

async def create_books(book:CreateBook):
    async with async_pool.connection() as curs:
        await curs.execute("INSERT into books(title,description,author_id,comment,janr) VALUES(%s,%s,%s,%s,%s)",[book.title,book.description,book.author_id,book.comment,book.janr])
        
            
    
async def delete_books(id:int):
    async with async_pool.connection() as curs:
        await curs.execute("DELETE from books as b WHERE b.id=%s",[id])
        

async def update_book(book:CreateBook,id:int):
    try:
        async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(CreateBook))as cur:
            await curs.execute("UPDATE books SET title=%s, description=%s,author_id=%s,comment=%s,janr=%s WHERE id=%s",(book.title,book.description,book.author_id,book.comment,book.janr,id))
            books=await cur.fetchone()
            if books:   
                return JSONResponse(content=books)
            else:
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def check_as_response(id:int,book:ResponseBook):
    try:
        async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(ResponseBook))as cur:
            await cur.execute("UPDATE books SET isresponse=%s WHERE id=%s",[id,book.isresponse])
            books=await cur.fetchone()
            if books:
                return JSONResponse(content=books)
            else:
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
async def check_as_publish(id:int,book:PublishedBook):
    try:
        async with async_pool.connection() as curs,curs.cursor(row_factory=class_row(PublishedBook))as cur:
            await cur.execute("UPDATE books SET ispublished=%s WHERE id=%s",[id,book.ispublished])
            books= await cur.fetchone()
            if books:
                return JSONResponse(content=books)
            else:
                raise HTTPException(status_code=400,detail="bad request")
    except:
        return {}
    
    
