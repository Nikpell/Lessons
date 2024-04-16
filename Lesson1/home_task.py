"""
Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию
 (например, кофейни, музеи, парки и т.д.).
Используйте API Foursquare для поиска заведений в указанной категории.
Получите название заведения, его адрес и рейтинг для каждого из них.
Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

"""

import json
import requests


def get_id(city, place):
    """
    replay dictionary with names of institutions, addresses, id from city and category
    :param city:
    :param place:
    :return:
    """
    endpoint = "https://api.foursquare.com/v3/places/search"
    client_id = "QLRWPO1QPU2MYWO44SU0I4YTHB3RLESJHJSHMNAMLGXXTHNC"
    client_secret = "51DA3DFMWUG4CEKTLXQY1T0FXRPSP5WFS4YZG4BICGKSYTKH"

    param = {
        'client_id': client_id,
        'client_secret': client_secret,
        'near': city,
        'query': place,
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
    }

    response = requests.get(endpoint, params=param, headers=headers)
    base = dict()
    if response.status_code == 200:
        data = json.loads(response.text)
        venues = data['results']
        for ven in venues:
            base.update({ven['name']: [ven['location']['formatted_address'], ven['fsq_id']]})
    else:
        print(f'Failure, {response.status_code}')
    return base


def input_data():
    """
    receive category from user
    :return:
    """
    category = input('Введите категорию для поиска: ')
    return category


def get_fsq_id(category):
    """
    replay dictionary with names of institutions, addresses, id from category
    :param category:
    :return:
    """

    url = "https://api.foursquare.com/v3/autocomplete"
    headers = {
        "accept": "application/json",
        "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
    }
    param = {
        'query': category,
    }
    response = requests.get(url, headers=headers, params=param)
    if response.status_code == 200:
        data = json.loads(response.text)
        base = {}
        for x in data['results']:
            if x.get('text') is not None and x.get('place') is not None:
                base.update({x['text'].get('primary'): [x['text'].get('secondary'), x['place'].get('fsq_id')]})
    else:
        print(f'Failure, {response.status_code}')
    return base


def get_data(base):
    """
    change id to rating(float)
    :param base:
    :return:
    """
    for key in base:
        endpoint = f"https://api.foursquare.com/v3/places/{base[key].pop(1)}?fields=rating"
        headers = {
            "Accept": "application/json",
            "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
        }
        response = requests.get(endpoint, headers=headers)
        base[key].append(json.loads(response.text).get('rating', 'нет рейтинга'))
    return base


def print_task(base):
    """
    print dictionary
    :param base:
    :return:
    """
    for key, value in base.items():
        print(f"Название': {key}")
        print(f"Адрес: {value[0]}")
        print(f'Рейтинг; {value[1]}')
        print()




if __name__ == "__main__":
    category = input_data()
    base = get_fsq_id(category)
    print_task(get_data(base))
