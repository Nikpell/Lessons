"""
Задание 1
- Установите пакет PyMongo и импортируйте MongoClient и json.
- Установите Compass MongoDB
- Подключитесь к серверу MongoDB по адресу
'mongodb://localhost:27017/'.
- Создайте базу данных 'town_cary' и коллекцию 'crashes'.
- Выполните чтение файла JSON 'crash-data.json'.
- Напишите функцию chunk_data, которая принимает два аргумента:
список данных и размер фрагмента. Функция должна разделить данные
на более мелкие фрагменты указанного размера и вернуть генератор.
- Разделите данные JSON на фрагменты по 5000 записей в каждом.
- Переберите все фрагменты и вставьте каждый фрагмент в коллекцию
MongoDB с помощью функции insert_many().
- Выведите финальное сообщение, указывающее на то, что данные были
успешно вставлены.
"""

from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['town_cary']
collection = db['crashes']

with open('crash-data.json', 'r') as f:
    data = json.load(f)

data_ = data['features']
chunk = 5000


def chung_size(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]


for data_chunk in chung_size(data_, chunk):
    collection.insert_many(data_chunk)
