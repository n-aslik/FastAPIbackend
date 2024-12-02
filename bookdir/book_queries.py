from fastapi import HTTPException,status,APIRouter,Depends
from fastapi.responses import JSONResponse
from .schema import CreateBook,ResponseBook,PublishedBook,Book
from ..database import async_get_db
from psycopg import Connection






async def get_books(book:Book,db:Connection=Depends(async_get_db)):
    books=await db.execute("SELECT b.title,b.description, u.username, b.comment,b.janr FROM account.books as b JOIN account.users as u ON b.author_id=u.id WHERE b.isresponse=%s and b.ispublished=%s ",(book.isresponse,book.ispublished)).fetchall()
    if not books:
        raise HTTPException(status_code=404,detail="books not found")
    return {"books":books}
        
async def get_book_by_id(id:int, book:Book,db:Connection=Depends(async_get_db)):
    books=await db.execute("SELECT b.title,b.description, u.username, b.comment,b.janr FROM account.books as b JOIN account.users as u ON b.author_id=u.id WHERE b.isresponse=%s and b.ispublished=%s and b.id=%s ",(book.isresponse,book.ispublished,id)).fetchone()
    if not books:
        raise HTTPException(status_code=404,detail="book`s by id not found")
    return {"book":books}

async def create_books(book:CreateBook,db:Connection=Depends(async_get_db)):
    await db.execute("INSERT into account.books(title,description,author_id,comment,janr) VALUES(%s,%s,%s,%s,%s)",(book.title,book.description,book.author_id,book.comment,book.janr))
    
            
    
async def delete_books(id:int,db:Connection=Depends(async_get_db)):
   await db.execute("DELETE from account.books as b WHERE b.id=%s",(id))
        

async def update_book(book:CreateBook,id:int,db:Connection=Depends(async_get_db)):
    books=await db.execute("UPDATE account.books SET title=%s, description=%s,author_id=%s,comment=%s,janr=%s WHERE id=%s",(book.title,book.description,book.author_id,book.comment,book.janr,id)).fetchone()
    if books:   
        return JSONResponse(content=books)
    else:
        raise HTTPException(status_code=400,detail="bad request")
    
    
async def check_as_response(id:int,book:ResponseBook,db:Connection=Depends(async_get_db)):
    books=await db.execute("UPDATE account.books SET isresponse=%s WHERE id=%s",(id,book.isresponse)).fetchone()
    if books:
        return JSONResponse(content=books)
    else:
        raise HTTPException(status_code=400,detail="bad request")
   
    
async def check_as_publish(id:int,book:PublishedBook,db:Connection=Depends(async_get_db)):
    books=await db.execute("UPDATE account.books SET ispublished=%s WHERE id=%s",(id,book.ispublished)).fetchone()
    if books:
        return JSONResponse(content=books)
    else:
        raise HTTPException(status_code=400,detail="bad request")
    
    
