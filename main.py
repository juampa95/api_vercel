from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


# items = {
#     0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
#     1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
#     2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
# }

# Leer datos desde el archivo JSON --- REVISAR ESTA PARTE ---- FUNCIONA PERO REVISAR IGUALMENTE Y TRADUCIR
def leer_datos_desde_json():
    with open("data.json", "r") as archivo_json:
        datos = json.load(archivo_json)
    items_data = datos.get("items", [])
    return items_data

print(leer_datos_desde_json())

# Escribir datos en el archivo JSON
def escribir_datos_en_json(items):
    items_data = [item.dict() for item in items]
    datos = {"items": items_data}
    with open("data.json", "w") as archivo_json:
        json.dump(datos, archivo_json, indent=4)


# Controlador para obtener todos los elementos
@app.get("/itemsj/")
def obtener_items():
    # Leer los datos desde el archivo JSON
    items = leer_datos_desde_json()
    return {"items": items}


# FastAPI handles JSON serialization and deserialization for us.
# We can simply use built-in python and Pydantic types, in this case dict[int, Item].
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")

    return items[item_id]


@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        HTTPException(status_code=400, detail=f'Item with {item.id=} already exist.')
    items[item.id] = item
    return {"added": item}