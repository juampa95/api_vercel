import requests

url = "https://api-vercel-git-main-juampa95.vercel.app/med/"

response = requests.post(url, json={"name": "tafirol","drug": "paracetamol","concentration": "1 mg","form": "pills","gtin": "14569875632147"})

if response.status_code == 200:
    print("upload successful")
else:
    print(f"ERROR: {response.status_code}")
    print(response.text)
