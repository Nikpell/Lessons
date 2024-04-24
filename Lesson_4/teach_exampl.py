import requests
from lxml import html

url = "https://www.worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page=1"
headers = {
'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)
tree = html.fromstring(response.content)
table_rows = tree.xpath("//div[@class='records-table']/tbody/tr")

rows_html_list = []

for row in table_rows:
    row_html = html.tostring(row, pretty_print=True, encoding='unicode')
    rows_html_list.append(row_html)

for row_html in rows_html_list:
    print(row_html)