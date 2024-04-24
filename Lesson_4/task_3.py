"""
Задание 3
- Определите базовый URL для страниц записей, включая параметр
номера страницы.
- Создайте функцию для скрейпинга данных таблицы из одной страницы.
- Создайте функцию для сохранения полученных данных в базе данных
MongoDB.
- Создайте главную функцию, которая выполняет итерации по всем
страницам записей и сохраняет данные для каждой страницы.
- Ваш скрипт Python должен быть модульным, с отдельными функциями
для скрейпинга и сохранения данных, чтобы его можно было легко
модифицировать и расширять. Он также должен включать задержку между
запросами не менее 5 секунд, чтобы не перегружать сервер.
- Используйте функцию time.sleep() для добавления задержки между
запросами. Это важно для того, чтобы не перегружать сервер и не быть
заблокированным.

- Используйте User Agent, чтобы избежать блокировки сервером.

- Протестируйте свой код на небольшом количестве страниц, прежде чем
запускать его на всем наборе. Это поможет вам выявить ошибки и
отладить функции скрейпинга и сохранения данных.
"""
import requests
from lxml import html
from pymongo import MongoClient
import pandas as pd



def one_page_scrape(url):
    responce = requests.get(url, headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    })

    tree = html.fromstring(responce.content)

    rows = tree.xpath("//table[@class='records-table']/tbody/tr")

    result_list = list()
    for row in rows:
        row_data = row.xpath(".//td/text()")
        record = {}
        record['Rank'] = int(row_data[0].strip())
        record['Mark'] = float(row_data[1].strip())
        record['WIND'] = float(row_data[2].strip() if row_data[2].strip() else "0")
        record['Competitor'] = row.xpath(".//td[4]/a/text()")[0].strip()
        record['DOB'] = row_data[5].strip()
        record['Nat'] = row_data[7].strip()
        record['Pos'] = row_data[8].strip()
        record['Venue'] = row_data[9].strip()
        record['Date'] = row_data[10].strip()
        record['ResultScore'] = int(row_data[11].strip())

        result_list.append(record)
    return result_list

def persist_to_mongo(result_list):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sixteen_metres"]
    sport = db["women"]
    sport.insert_many(result_list)
    # df = pd.DataFrame()

def main_function():
    for i in range(1,3):
        persist_to_mongo(one_page_scrape(f'https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page={i}'))
        print(f"page {i} processed")


if __name__ == "__main__":
    main_function()
