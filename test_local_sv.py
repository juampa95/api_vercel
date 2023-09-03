import requests
import os
import httpx

print(requests.get("http://127.0.0.1:8000/").json())
print("-" * 100)
print(requests.get("http://127.0.0.1:8000/itemsj/0").json())

print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"name": "Screwdriver", "price": 3.99, "count": 5, "id": 4, "category": "tools"},
    ).json()
)

print(requests.get("http://127.0.0.1:8000/itemsj/").json())



KV_REST_API_URL = os.getenv("KV_REST_API_URL") + "/set/user_1_session/session_token_value"
KV_REST_API_TOKEN = os.getenv("KV_REST_API_TOKEN")

# URL de tu servidor FastAPI
url = KV_REST_API_URL

# Datos que deseas cargar manualmente (deben coincidir con el modelo Pydantic)
data = {
    "name": "Nuevo Elemento",
    "price": 10.99,
    "count": 5,
    "id": 1,
    "category": "Herramientas"  # Debes usar una cadena para la categoría
}

# Realiza una solicitud POST para cargar el elemento
response = requests.post(url, json=data)

# Verifica la respuesta del servidor
if response.status_code == 200:
    print("Elemento cargado exitosamente.")
else:
    print("Error al cargar el elemento.")