from fastapi import HTTPException,status
from schemas.books import CreateBook,ResponseBook,PublishedBook,Book
from fastapi.responses import JSONResponse
from database.dbconn import async_get_db
from asyncpg import Connection



async def get_books(isresp:bool,ispub:bool):
    try:
        db:Connection= await async_get_db()

        books=await db.fetch("SELECT b.title,b.description, u.id, b.comment,b.janr FROM books as b JOIN users as u ON b.user_id=u.id WHERE b.isresponse=$1 and b.ispublished=$2 ",isresp,ispub)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return books
    except RuntimeError as re:
        await db.close()
        return re
    
        
        
async def get_book_by_id(id:int,resp:bool,pub:bool):
    try: 
        db:Connection= await async_get_db()
        books=await db.fetchrow("SELECT b.title,b.description, u.username, b.comment,b.janr FROM books as b JOIN users as u ON b.user_id=u.id WHERE b.isresponse=$1 and b.ispublished=$2 and b.id=$3 ",resp,pub,id)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return books
    except RuntimeError as re:
        await db.close()
        return re
    
        

async def create_books(book:CreateBook):
    try:
        db:Connection= await async_get_db()
        books=await db.execute("INSERT into books(title,description,user_id,comment,janr) VALUES($1,$2,$3,$4,$5) RETURNING title,description,user_id,comment,janr ",book.title,book.description,book.user_id,book.comment,book.janr)
        if not books:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return books
    except RuntimeError as re:
        await db.close()
        return re
    
        
            
    
async def delete_books(id:int):
    try:
        db:Connection= await async_get_db()
        books=await db.execute("DELETE from books as b WHERE b.id=$1",id)
        if not books:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return books
    except RuntimeError as re:
        await db.close()
        return re
    
            
        

async def update_book(title:str,description:str,authorid:int,comment:str,janr:str,id:int):
    try:
        db:Connection= await async_get_db()
        books=await db.execute("UPDATE books SET title=$1, description=$2,user_id=$3,comment=$3,janr=$4 WHERE id=$5",title,description,authorid,comment,janr,id)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return books
    except RuntimeError as re:
        await db.close()
        return re
    
            
    
    
async def check_as_response(id:int,isresp:bool):
    try:
        db:Connection= await async_get_db()
        books=await db.execute("UPDATE books SET isresponse=$1 WHERE id=$2",id,isresp)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return books     
    except RuntimeError as re:
        await db.close()
        return re
    
        
    
async def check_as_publish(id:int,ispub:bool):
    try:
        db:Connection= await async_get_db()
        books=await db.execute("UPDATE books SET ispublished=$1 WHERE id=$2",id,ispub)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return books     
    except RuntimeError as re:
        await db.close()
        return re
    
        