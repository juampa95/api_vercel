import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.exc import SQLAlchemyError

from schema import Book as SchemaBook
from schema import Author as SchemaAuthor

from models import Book as ModelBook
from models import Author as ModelAuthor


from models import Medic, Doctor, Prescriptions, Patients, PrescriptionDetails
from schema import Doctor as SchemaDoctor
from schema import Medic as SchemaMedic


import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['POSTGRES_URI'])


@app.get("/")
async def root():
    return {"message": "Server is up and running!"}

# Medicine

@app.get('/med/')
async def medics():
    medics = db.session.query(Medic).all()
    return medics


@app.get('/med/{med_id}', response_model=SchemaMedic)
async def query_medics_by_id(med_id: int):
    db_medic = db.session.query(Medic).filter_by(id=med_id).first()

    if db_medic is None:
        raise HTTPException(status_code=404, detail=f'Medic with ID {med_id} does not found')
    return db_medic


@app.post('/med/', response_model=SchemaMedic)
async def create_med(med: SchemaMedic):
    try:
        db_med = Medic(name=med.name, drug=med.drug, concentration=med.concentration, form=med.form, gtin=med.gtin)
        db.session.add(db_med)
        db.session.commit()
        return db_med

    except SQLAlchemyError as e:
        db.session.rollback()  # Realiza un rollback en caso de error
        return {"error": str(e)}


# Doctors

@app.get('/doc/')
async def doc():
    doc = db.session.query(Doctor).all()
    return doc

@app.get('/doc/{doc_id}', response_model=SchemaDoctor)
async def query_doctor_by_id(doc_id: int):
    db_doc = db.session.query(Doctor).filter_by(id=doc_id).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail=f'Doctor with ID {doc_id} does not found')
    return db_doc

@app.get('/doc/dni/{doc_dni}', response_model=SchemaDoctor)
async def query_doctor_by_id(doc_dni: int):
    db_doc = db.session.query(Doctor).filter_by(personal_id=doc_dni).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail=f'Doctor with Personal ID {doc_dni} does not found')
    return db_doc


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


@app.get('/book/{book_id}', response_model=SchemaBook)
async def query_book_by_id(book_id: int):
    db_book = db.session.query(ModelBook).filter_by(id=book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail=f'Book with ID {book_id} does not found')

    return db_book



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


@app.delete('/delete-book/{id_book}')
async def del_book(id_book:int):
    try:
        book = db.session.query(ModelBook).filter_by(id=id_book).first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        db.session.delete(book)
        db.session.commit()
        db.session.refresh(book)

        return {'message': 'book deleted'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}



# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


