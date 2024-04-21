"""
Задание 2
- Импортируйте MongoClient и json.
- Cоздайте экземпляр клиента для подключения к MongoDB.
- Подключитесь к базе данных 'town_cary' и коллекции 'crashes'.
- Найдите первый документ в коллекции и распечатайте его в формате
JSON.
- Используйте функцию count_documents(), чтобы получить общее
количество документов в коллекции.
- Отфильтруйте документы по критерию "properties.fatalities",
равному "Yes", и подсчитайте количество совпадающих документов.
- Используйте проекцию для отображения только полей
"properties.lightcond" и "properties.weather" для документов с
"properties.fatalities" равным "Yes".
- Используйте операторы $lt и $gte для подсчета количества документов
 с "properties.month" меньше 6 и больше или равно 6, соответственно.
- Используйте оператор $regex для подсчета количества документов,
содержащих слово "rain" в поле "properties.weather", игнорируя регистр.
- Используйте оператор $in для подсчета количества документов,
в которых "properties.rdclass" является либо "US ROUTE",
либо "STATE SECONDARY ROUTE".
- Используйте оператор $all для подсчета количества документов,
в которых "properties.rdconfigur" содержит как "TWO-WAY",
так и "DIVIDED".
- Используйте оператор $ne для подсчета количества документов,
у которых "properties.rdcondition" не равно "DRY".
1^15
"""
from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['town_cary']
collection = db['crashes']

li = collection.find()
element = li[0]
element_json = json.dumps(element, indent=4, default=str)


def count_documents(collection):
    return collection.count_documents({})


def count_documents_from_query(collection, query):
    return collection.count_documents(query)


query = {"properties.fatalities": 'Yes'}

# print(count_documents_from_query(collection, query))

# - Используйте проекцию для отображения только полей
# "properties.lightcond" и "properties.weather" для документов с
# "properties.fatalities" равным "Yes".
projection = {"properties.lightcond": 1, "properties.weather": 1, "_id": 0}
fatalities_documents = collection.find({"properties.fatalities": "Yes"}, projection)
# print("Документы с фатальными случаями:")
# for doc in fatalities_documents:
#     print(doc)

# Используйте операторы $lt и $gte для подсчета количества документов
#  с "properties.month" меньше 6 и больше или равно 6, соответственно.
month_lt_6_count = collection.count_documents({"properties.month": {"$lt": '6'}})
month_gte_6_count = collection.count_documents({"properties.month": {"$gte": '6'}})
print("Количество документов с месяцем меньше 6:", month_lt_6_count)
print("Количество документов с месяцем больше или равным 6:", month_gte_6_count)
