import requests
import os

post_data = {
    "email": "admin@email.com",
    "name": "admin",
    "is_admin": True,
    "password": "password",
    "shipping_address": "123 daisy rd city state"
}

res = requests.post('http://127.0.0.1:5000/account_creation', json=post_data)
if res.ok:
    print(res.json())
