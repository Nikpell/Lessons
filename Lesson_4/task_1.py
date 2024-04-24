"""
Напишите сценарий на языке Python, который выполняет следующие задачи:

- отправляет HTTP GET-запрос на целевой URL и
получает содержимое веб-страницы.
- выполняет парсинг HTML-содержимого ответа с
помощью библиотеки lxml.
- используя выражения XPath, извлеките данные из
первой строки таблицы.
- выведите извлеченные данные из первой строки таблицы в консоль.
"""
import requests
from lxml import html

url = ('https://worldathletics.org/records/toplists/sprints/'
       '60-metres/indoor/women/senior/2023?page=1')
response = requests.get(url)
tree = html.fromstring(response.content)
rows = tree.xpath("//table[@class='records-table']/tbody/tr")
column_name = rows[0].xpath(".//td/text()")
for column in column_name:
    print(column.strip())




