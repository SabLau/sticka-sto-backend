import requests

put_data = {
    "quantity": 15,
    "sticker_id": 1,
}

res = requests.put('http://127.0.0.1:5000/inventory_update', json=put_data)
if res.ok:
    print(res.json())
