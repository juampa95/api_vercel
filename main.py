# from enum import Enum
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import json
#
# app = FastAPI()
#
#
# class Category(Enum):
#     TOOLS = 'tools'
#     CONSUMABLES = 'consumables'
#
#
# class Item(BaseModel):
#     name: str
#     price: float
#     count: int
#     id: int
#     category: Category
#
## items = {
#     0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
#     1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
#     2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
# }
#

# # FastAPI handles JSON serialization and deserialization for us.
# # We can simply use built-in python and Pydantic types, in this case dict[int, Item].
# @app.get("/")
# def index() -> dict[str, dict[int, Item]]:
#     return {"items": items}
#
# @app.get("/items/{item_id}")
# def query_item_by_id(item_id: int) -> Item:
#     if item_id not in items:
#         HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
#
#     return items[item_id]
#
#
# @app.post("/")
# def add_item(item: Item) -> dict[str, Item]:
#     if item.id in items:
#         HTTPException(status_code=400, detail=f'Item with {item.id=} already exist.')
#     items[item.id] = item
#     return {"added": item}
############################################
#
# from enum import Enum
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import httpx
# import os
#
# app = FastAPI()
#
# class Category(Enum):
#     TOOLS = 'tools'
#     CONSUMABLES = 'consumables'
#
# class Item(BaseModel):
#     name: str
#     price: float
#     count: int
#     id: int
#     category: Category
#
#
# KV_REST_API_URL = os.getenv("KV_REST_API_URL") + "/set/user_1_session/session_token_value"
# KV_REST_API_TOKEN = os.getenv("KV_REST_API_TOKEN")
#
# # Crear una lista para almacenar los elementos cargados manualmente
# items = []
#
# # Ruta para cargar un elemento manualmente
# @app.post("/load_item/")
# async def load_item(item: Item):
#     # Verificar si el elemento ya existe en la lista
#     for existing_item in items:
#         if existing_item.id == item.id:
#             raise HTTPException(status_code=400, detail=f'Item with id {item.id} already exists.')
#
#     # Agregar el elemento a la lista
#     items.append(item)
#     return {"message": "Item loaded successfully"}
#
#
# @app.post("/load_item2/")
# async def load_item(item: Item):
#     # Aquí, en lugar de almacenar el elemento en una variable local,
#     # podrías enviarlo a tu base de datos KV en Vercel.
#     # Puedes hacer esto utilizando el servicio de almacenamiento de Vercel o una API personalizada.
#
#     # Simplemente devolvemos el elemento cargado como confirmación.
#     return item
#
# # Ruta para obtener todos los elementos cargados manualmente
# @app.get("/get_items/")
# async def get_items():
#     return items


import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Book as SchemaBook
from schema import Author as SchemaAuthor

from schema import Book
from schema import Author

from models import Book as ModelBook
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['POSTGRES_URL'])


@app.get("/")
async def root():
    return {"message": "hola gente"}


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.get('/book/')
async def book():
    book = db.session.query(ModelBook).all()
    return book


@app.post('/author/', response_model=SchemaAuthor)
async def author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.get('/author/')
async def author():
    author = db.session.query(ModelAuthor).all()
    return author


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


