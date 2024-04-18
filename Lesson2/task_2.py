"""
Ваша задача - создать Python-сценарий, который извлекает данные
по каждому фильму ( по каждой ссылке, сохраненной в url_joined)
 и сохраняет их в JSON-файл.
на релизы фильмов со страницы "International Box Office" на сайте
Box Office Mojo.
- Для каждого фильма извлеките следующую информацию:
Distributor
Opening (в формате int)
Release Date
MPAAы.
Running Time (в секундах)о веб-страницы.
Genres (в виде списка)
In Releaseлок с базовым URL.
Widest Release (в формате int)
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd

url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
base_url = "https://www.boxofficemojo.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
link = []
for x in soup.find_all('td', {'class', "a-text-left mojo-field-type-release mojo-cell-wide"}):
    href = x.find('a')
    if href:
        link.append(href.get('href'))
# print(link)
url_join = [urllib.parse.urljoin(base_url, x) for x in link]
table = soup.find('table', {'class', 'a-bordered'})
headers = [header.text.strip() for header in table.find_all('th') if header.text]
data = []
for row in table.find_all('tr'):
    row_dict = {}
    cell = row.find_all('td')
    if cell:
        row_dict[headers[0]] = cell[0].find('a').text if cell[0].find('a') else ''
        row_dict[headers[1]] = cell[1].find('a').text if cell[1].find('a') else ''
        row_dict[headers[2]] = cell[2].text
        row_dict[headers[3]] = cell[3].find('a').text if cell[3].find('a') else ''
        row_dict[headers[4]] = cell[4].text.strip()
        row_dict[headers[5]] = cell[5].text.replace('$', '').replace(',', '')
        data.append(row_dict)
df = pd.DataFrame(data)
pd.set_option("display.max.columns", None)
print(df.head())
