import json
import requests

url = 'https://jsonplaceholder.typicode.com/posts/1'
# respond = requests.get(url)
# if respond.status_code == 200:
#     print(respond.text)
# else:
#     print("False")

data = {
    "userId": 1,
    "title": "monster corporation",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}

# respond = requests.post(url[:-2], json=data)
# if respond.status_code == 201:
#     print(respond.text)
# else:
#     print("False")

# payload = {"field1": "value1", "field2": "value2"}
# respond = requests.put(url, json=payload)
# if respond.status_code == 200:
#     print(respond.text)
# else:
#     print(f"False: code {respond.status_code}")

respond = requests.delete(url)
if respond.status_code == 200:
    print(respond.text)
else:
    print("False")