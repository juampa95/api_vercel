import requests

url = "https://api-vercel-git-main-juampa95.vercel.app/author/"

author_data = {
    "name": "Juan Pablo Manzano",
    "age": 28
}

response = requests.post(url, json=author_data)

if response.status_code == 200:
    new_author = response.json()
    print(f"Autor creado exitosamente: {new_author}")
else:
    print(f"Error al crear el autor. Código de estado: {response.status_code}")
    print(response.text)


url = "https://api-vercel-git-main-juampa95.vercel.app/book/"

book_data = {
    "title": "Como hacer una API",
    "rating": 5.0,
    "author_id": 2
}

# Realiza la solicitud POST
response = requests.post(url, json=book_data)

# Verifica si la solicitud se realizó con éxito
if response.status_code == 200:
    new_book = response.json()
    print(f"Libro agregado exitosamente: {new_book}")
else:
    print(f"Error al agregar el libro. Código de estado: {response.status_code}")
    print(response.text)


url = "https://api-vercel-git-main-juampa95.vercel.app/delete-book/14"

response = requests.delete(url, json=book_data)



if response.status_code == 200:
    print("Libro eliminado exitosamente")
else:
    print(f"Error al eliminar el libro. Código de estado: {response.status_code}")
    print(response.text)