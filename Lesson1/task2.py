import json
import requests

endpoint = "https://api.foursquare.com/v3/places/search"
client_id = "__"
client_secret = "__"

city = 'Perm' #input('Введите город: ')
place = 'bar' #input('Введите заведение: ')

param = {
    'client_id': client_id,
    'client_secret': client_secret,
    'near': city,
    'query': place
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

response = requests.get(endpoint, params=param, headers=headers)
base = dict()
if response.status_code == 200:
    data = json.loads(response.text)
    print(data)
#     venues = data['results']
#     for ven in venues:
#         # print(f"Название': {ven['name']}")
#         # print(f" Адрес: {ven['location']['address']}")
#         # print()
#         base.update({ven['name']: ven['location']['address']})
# else:
#     print(f'Failure, {response.status_code}')
#
# print(base)

with open('../Prev_HT/dict.json', 'w') as f:
    json.dump(base, f)

