from fastapi import HTTPException,status
from schemas.books import CreateBook
from database.dbconn import async_get_db
from asyncpg import Connection
import json



async def get_books(isresp:bool,ispub:bool):
    db:Connection= await async_get_db()
    books=await db.fetchval("SELECT authuser.get_all_books($1,$2) ",isresp,ispub)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    book=json.loads(books)
    return book
    
         
async def get_book_by_id(id:int,resp:bool,pub:bool):
    db:Connection= await async_get_db()
    books=await db.fetchval("SELECT authuser.get_book_by_id($1,$2,$3) ",resp,pub,id)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    book=json.loads(books)
    return book
    
    
async def create_books(book:CreateBook):
    db:Connection= await async_get_db()
    await db.execute("CALL authuser.create_book($1,$2,$3,$4,$5)",book.title,book.description,book.user_id,book.comment,book.janr)
    return{"title":book.title,"description":book.description,"user_id":book.user_id,"comment":book.comment,"janr":book.janr}
    
    
async def delete_books(id:int):
    db:Connection= await async_get_db()
    await db.execute("CALL authuser.delete_book($1)",id)
    
    
async def update_book(title:str,description:str,comment:str,janr:str,id:int):
    db:Connection= await async_get_db()
    await db.execute("CALL authuser.update_book($1,$2,$3,$4,$5)",title,description,comment,janr,id)
    
    
async def check_as_response(id:int,isresp:bool):
    db:Connection= await async_get_db()
    await db.execute("CALL authuser.response_book($1,$2) ",isresp,id)
    
    
async def check_as_publish(id:int,ispub:bool):
    db:Connection= await async_get_db()
    await db.execute("CALL authuser.public_book($1,$2) ",ispub,id)
    
        