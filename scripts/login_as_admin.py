import requests
import os

get_data = {
    "email": "admin@email.com",
    "password": "password"
}

res = requests.post('http://127.0.0.1:5000/admin_auth', json=get_data)
if res.ok:
    print(res.json())
