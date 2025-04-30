from fastapi import HTTPException,status
from schemas.books import CreateBook
from database.dbconn import async_get_db
from asyncpg import Connection
import json



async def get_books(isresp:bool,ispub:bool):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("SELECT authuser.get_all_books(%s, %s) ", (isresp,ispub))
        books = cur.fetchone()[0]
        return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
         
async def get_book_by_id(id:int,resp:bool,pub:bool):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("SELECT authuser.get_book_by_id(%s, %s, %s) ", (resp, pub,id))
        books = cur.fetchone()[0]
        return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
async def create_books(book:CreateBook):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.create_book(%s, %s, %s, %s, %s, %s)", (book.title, book.description, book.user_id, book.comment, book.janr, '{}'))
        books = cur.fetchone()[0]
        if books['status'] == 0:
            return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
    
async def delete_books(id:int):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.delete_book(%s)", (id,))
        books = cur.fetchone()[0]
        if books['status'] == 0:
            return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
    
async def update_book(id: int, books: CreateBook):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.update_book(%s, %s, %s, %s, %s, %s)", (books.title, books.description, books.comment, books.janr, id, '{}'))
        books = cur.fetchone()[0]
        if books['status'] == 0:
            return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
    
async def check_as_response(id:int):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.response_book(%s, %s) ", id, '{}')
        books = cur.fetchone()[0]
        if books['status'] == 0:
            return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
    
async def check_as_publish(id:int):
    with async_get_db() as db:
        cur = db.cursor()
        cur.execute("CALL authuser.public_book(%s, %s) ", id, '{}')
        books = cur.fetchone()[0]
        if books['status'] == 0:
            return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
        