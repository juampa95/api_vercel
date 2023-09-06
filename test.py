import requests

#Medicine

url = "https://api-vercel-git-main-juampa95.vercel.app/med/"

response = requests.post(url, json={"name": "tafirol","drug": "paracetamol","concentration": "1 mg","form": "pills","gtin": "14569875632147"})

if response.status_code == 200:
    print("upload successful")
else:
    print(f"ERROR: {response.status_code}")
    print(response.text)

#Doctor

url = "https://api-vercel-git-main-juampa95.vercel.app/doc/"

response = requests.post(url, json={"personal_id": "38909654","name": "Juan Pablo","lastname": "Manzano"})

if response.status_code == 200:
    print("upload successful")
else:
    print(f"ERROR: {response.status_code}")
    print(response.text)

#Patient

url = "https://api-vercel-git-main-juampa95.vercel.app/patients/"

response = requests.post(url, json={"personal_id": "38909654","name": "Juan Pablo","lastname": "Manzano","date_of_birth":"1995-07-07"})

if response.status_code == 200:
    print("upload successful")
else:
    print(f"ERROR: {response.status_code}")
    print(response.text)
