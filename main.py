import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.exc import SQLAlchemyError

from schema import Book as SchemaBook
from schema import Author as SchemaAuthor

from models import Book as ModelBook
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['POSTGRES_URI'])


@app.get("/")
async def root():
    return {"message": "Server is up and running!"}


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    try:
        db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
        db.session.add(db_book)
        db.session.commit()
        db.session.flush()
        return db_book
    except SQLAlchemyError as e:
        db.session.rollback()  # Realiza un rollback en caso de error
        return {"error": str(e)}


@app.get('/book/')
async def book():
    book = db.session.query(ModelBook).all()
    return book


@app.post('/author/', response_model=SchemaAuthor)
async def author(author: SchemaAuthor):
    try:
        db_author = ModelAuthor(name=author.name, age=author.age)
        db.session.add(db_author)
        db.session.commit()
        return db_author
    except SQLAlchemyError as e:
        db.session.rollback()  # Realiza un rollback en caso de error
        return {"error": str(e)}


@app.get('/author/')
async def author():
    author = db.session.query(ModelAuthor).all()
    return author


@app.delete('delete_book/{id_book}')
async def del_book(id_book:int):
    try:
        book = db.session.query(ModelBook).filter_by(id=id_book).first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        db.session.delete(book)
        db.session.commit()

        return {'message': 'book deleted'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


