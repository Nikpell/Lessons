"""
Задание 1
- установите библиотеку Beautiful Soup.

- создайте новый сценарий Python и импортируйте библиотеку Beautiful Soup.

- напишите код для запроса веб-страницы
https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab с помощью библиотеки requests.

- выведите HTML-содержимое веб-страницы в консоль.
"""
import requests
from bs4 import BeautifulSoup

url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify())
