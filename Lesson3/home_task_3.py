"""
Загрузите данные который вы получили на предыдущем уроке путем
скрейпинга сайта с помощью Buautiful Soup в MongoDB и создайте базу
данных и коллекции для их хранения.
Поэкспериментируйте с различными методами запросов.
Зарегистрируйтесь в ClickHouse.
Загрузите данные в ClickHouse и создайте таблицу для их хранения
"""
from clickhouse_driver import Client
import json

client = Client('localhost')


def update_database():
    client.execute('CREATE DATABASE IF NOT EXISTS book')
    client.execute('''
    CREATE TABLE IF NOT EXISTS book.info (
        id UInt64,
        name String,
        price Float,
        availability Int32,
        description String
    ) ENGINE = MergeTree()
    ORDER BY id
    ''')
    with open('books_data_new.json', 'r') as file:
        data = json.load(file)
    id = 0
    for i in range(len(data)):
        id = i + 1
        name = data[i]['Name']
        price = data[i]['Price']
        availability = data[i]['Availability']
        description = data[i]['Description']
        client.execute("""
            INSERT INTO book.info (
                id, name, price, availability,
                description
            ) VALUES""",
                       [(id,
                         name or "",
                         price or "",
                         availability or "",
                         description or "",
                         )])


def write_to_file(file_name, query, data):
    with open(file_name, 'w+') as file:
        print(query, file=file)
        print(data, file=file)


def query_to_database(query):
    return client.execute(query)


query_1 = "SELECT * FROM book.info"

query_2 = "SELECT count(*) FROM book.info"

# 2. Фильтрация записей на основе критериев
# 2.1. Равенство: Получение записей с "Availability", равным '10'
query_3 = "SELECT * FROM book.info WHERE availability = 1"

# 2.2. Диапазон: Выборка записей с ценой между 10 и 30
query_4 = ("SELECT name, price, availability "
           "FROM book.info "
           "WHERE price BETWEEN 10 and 30")

# 3. Сортировка записей на основе одного или нескольких полей
# 3.1. Сортировка записей по цене в порядке убывания
query_5 = ("SELECT name, price, availability "
           "FROM book.info "
           "ORDER BY price DESC "
           "LIMIT 5"
           )
# 3.2. Сортировка записей по цене в порядке возрастания и по количеству в порядке убывания
query_6 = ("SELECT name, price, availability "
           "FROM book.info "
           "ORDER BY price ASC, availability DESC "
           "LIMIT 5"
           )
# 4. Агрегирование записей с помощью таких функций, как count, sum и avg.
# 4.1. Подсчет количества книг с ценой между 10 и 30
query_7 = ("SELECT count(*)"
           " FROM book.info"
           " WHERE price BETWEEN 10 AND 30"
           )
# 4.2. Рассчитайте среднюю цену книг с доступным количеством между 10 и 15
query_8 = ("SELECT avg(price)"
           " FROM book.info"
           " WHERE availability BETWEEN 10 AND 15"
           )


data = query_to_database(query_8)
write_to_file('8.txt', query_8, data)
