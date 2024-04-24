"""
Задание 2
Модифицируйте предыдущий сценарий, чтобы получить данные из таблицы.

Требования:
- Создайте пустой список, который будет хранить словари с данными
из каждой строки
- Извлеките соответствующие данные из каждой строки таблицы
и сохраните их в словаре.
- Добавьте каждый словарь к списку данных.
- Выведите полученный список в консоль.
"""
import requests
from lxml import html

url = ('https://worldathletics.org/records/toplists/sprints/'
       '60-metres/indoor/women/senior/2023?page=1')
response = requests.get(url)
tree = html.fromstring(response.content)
column_names = tree.xpath("//table[@class='records-table']/thead/tr/th/text()")
rows = tree.xpath("//table[@class='records-table']/tbody/tr")
# row_data = rows.xpath(".//td/text()")
# for name in column_names:
#     print(name.strip())
# rows = tree.xpath("//table[@class='records-table']/tbody/tr")

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

for record in result_list:
    print(record)
