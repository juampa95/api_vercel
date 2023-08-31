import requests

print(requests.get("http://127.0.0.1:8000/").json())
print("-"*100)
print(requests.get("http://127.0.0.1:8000/items/0").json())


print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"name": "Screwdriver", "price": 3.99, "count": 5, "id": 4, "category": "tools"},
    ).json()
)



print(requests.get("http://127.0.0.1:8000/itemsj/").json())