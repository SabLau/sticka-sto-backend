import requests

put_data = {
    "sticker_name": "buff doge",
    "img_url": "https://i.kym-cdn.com/photos/images/newsfeed/001/582/307/98c.jpg",
    "price": 5,
    "total_sold": 14,
    "sticker_id": 1,
}

res = requests.put('http://127.0.0.1:5000/stickers_update', json=put_data)
if res.ok:
    print(res.json())