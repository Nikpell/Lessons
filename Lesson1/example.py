import requests
import json


def get_fsq_id():
    url = "https://api.foursquare.com/v3/autocomplete"
    headers = {
        "accept": "application/json",
        "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
    }
    param = {
        'query': "bar",
    }
    response = requests.get(url, headers=headers, params=param)
    if response.status_code == 200:
        data = json.loads(response.text)
        base = {}
        # print(data)
        for x in data['results']:
            if x.get('text') is not None and x.get('place') is not None:
               base.update({x['text'].get('primary'): [x['text'].get('secondary'), x['place'].get('fsq_id')]})
    else:
        print(f'Failure, {response.status_code}')
    return base


def get_data(base):
    for x in fsq_id_lst:
        endpoint = f"https://api.foursquare.com/v3/places/{x}?fields=rating"

        headers = {
            "Accept": "application/json",
            "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
        }

        response = requests.get(endpoint, headers=headers)
        data = json.loads(response.text)
        print(data)


fsq_id_lst = get_fsq_id()
# get_data(fsq_id_lst[:1])
