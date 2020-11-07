import requests

post_data = {
    "shipping_address": "123 Boom boom",
    "stickers_list": [
        {"id": 1, "quantity": 3},
        {"id": 3, "quantity": 7},
        {"id": 4, "quantity": 2}
        ],
    "user_id": 1
}
res = requests.post('http://127.0.0.1:5000/create_order', json=post_data)
if res.ok:
    print(res.json())
