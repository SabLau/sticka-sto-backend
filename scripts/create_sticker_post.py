import requests

post_data = {
    "name": "jeff1",
    "img_url": "https://s3.cointelegraph.com/storage/uploads/view/bad02e8b57a64d349aa5eec318298b4b.png",
    "price": 150.00,
    "total_sold": 2,
    "quantity": 4
}
print("hello")
res = requests.post('http://127.0.0.1:5000/create_sticker', json=post_data)
if res.ok:
    print(res.json())
