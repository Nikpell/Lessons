import requests  # Используется для отправки HTTP-запросов
from bs4 import BeautifulSoup  # Для парсинга HTML и XML документов
import urllib.parse  # Для склейки URL
from datetime import datetime  # Для работы с датами и временем
import time  # Для работы со временем
import re  # Для работы с регулярными выражениями
import json  # Для работы с форматом данных JSON


def join_url(link):
    return urllib.parse.urljoin('http://books.toscrape.com/catalogue/', link)


def get_soup_for_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


def get_data_from_page(soup):
    name = soup.find('div', class_='col-sm-6 product_main').find('h1').text
    price = soup.find('p', class_='price_color').text
    available = soup.find('p', class_='instock availability').text.strip()
    available = int(available.replace('In stock (', '').replace(' available)', ''))
    product_description = set(soup.find_all('p', attrs=False)) - set(soup.find_all('p', attrs=True))
    product_description = f'{product_description}'
    product_description = product_description.replace('{<p>', '').replace('</p>}', '')
    data = {'Name': name,
            'Price': price,
            'Availability': available,
            'Description': product_description
    }
    return data

def save_data_to_json(data, filename='books_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


with open('1.txt', 'r') as f:
    li = f.read()
li = li[1:-2]
li = li.split(',')
li = list(map(lambda x: x.replace("'", '').strip(), li))

li = [join_url(x) for x in li]
common_list = []
for url in li[:10]:
    soup = get_soup_for_page(url)
    common_list.append(get_data_from_page(soup))
save_data_to_json(common_list)



# def handle_exceptions(default_response_msg):
#     def exception_handler_decorator(func):
#         def decorated_function(*args, **kwargs):
#             try:
#                 # Call the original function
#                 return func(*args, **kwargs)
#             except Exception as error:
#                 # Handle the exception and provide the default response
#                 print(f"Exception occurred: {error}")
#                 return default_response_msg
#         return decorated_function
#     return exception_handler_decorator
#
# # Example usage
# @handle_exceptions(default_response_msg="An error occurred!")
# def divide_numbers_safely(dividend, divisor):
#     return dividend / divisor
#
# # Call the decorated function
# result = divide_numbers_safely(7, 0)  # This will raise a ZeroDivisionError
# print("Result:", result)
from functools import wraps

# def validate(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         message = '_"Function call is not valid!"_ '
#         for i in args:
#             if type(i) is not int or i > 256:
#                 return message
#         for i in kwargs.values():
#             if type(i) is not int or i > 256:
#                 return message
#         try:
#             return fn(*args, **kwargs)
#         except TypeError:
#             return message
#     return wrapper


# @validate
# def set_pixel(x: int, y: int, z: int) -> str:
#     return "Pixel created!"
#
# print(set_pixel((1, 2), 300, 1))
