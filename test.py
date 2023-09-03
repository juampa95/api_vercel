import requests

url = "https://api-vercel-git-main-juampa95.vercel.app/book/"

# Realiza la solicitud POST
response = requests.post(url, json=book_data)

# Verifica si la solicitud se realizó con éxito
if response.status_code == 200:
    new_book = response.json()
    print(f"Libro agregado exitosamente: {new_book}")
else:
    print(f"Error al agregar el libro. Código de estado: {response.status_code}")
    print(response.text)