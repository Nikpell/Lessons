"""
адание 2
Напишите сценарий на языке Python, чтобы получить ссылки на релизы фильмов со страницы "International Box Office" на сайте Box Office Mojo.
Сохраните ссылки в списке и выведите список на консоль.

Требования:

- Используйте библиотеку requests для запроса веб-страницы.
- Используйте Beautiful Soup для парсинга HTML-содержимого веб-страницы.
- Найдите все ссылки в колонке #1 Release веб-страницы.
- Используйте библиотеку urllib.parse для объединения ссылок с базовым URL.
- Сохраните ссылки в списке и выведите список на консоль.

https://www.mongodb.com/try/download/community
https://www.mongodb.com/try/download/compass
yandex/clickhouse-server:latest
"""

import requests  # Используется для отправки HTTP-запросов
from bs4 import BeautifulSoup  # Для парсинга HTML и XML документов
import urllib.parse  # Для склейки URL
from datetime import datetime  # Для работы с датами и временем
import time  # Для работы со временем
import re  # Для работы с регулярными выражениями
import json  # Для работы с форматом данных JSON


def get_box_office_data():
    """
    Функция для получения данных о кассовых сборах
    :return:
    """
    # URL страницы, с которой будут собираться данные
    url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
    # Заголовки запроса для имитации запроса от браузера
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    # Отправка GET-запроса на URL
    response = requests.get(url, headers=headers)
    # Разбор HTML-кода страницы
    soup = BeautifulSoup(response.content, 'html.parser')

    # Список для хранения ссылок на страницы с детальной информацией о фильмах
    release_links = []
    # Поиск всех элементов td с определенным классом, содержащих ссылки на фильмы
    for link in soup.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide'):
        a_tag = link.find('a')  # Поиск тега <a> внутри элемента
    if a_tag:
        release_links.append(a_tag.get('href'))  # Добавление ссылки на фильм в список

    # Преобразование относительных ссылок в абсолютные
    url_joined = [urllib.parse.urljoin('https://www.boxofficemojo.com', link) for link in release_links]

    # Список для хранения собранных данных
    data = []
    # Перебор всех ссылок для получения детальной информации о каждом фильме
    for url in url_joined:
        response = requests.get(url, headers=headers)  # Отправка запроса
        soup = BeautifulSoup(response.content, 'html.parser')  # Разбор HTML
        # Поиск таблицы с основной информацией о фильме
        table = soup.find('div', class_='a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile')
        print("1")
        if not table:
            continue

        # Сбор данных из таблицы
        rows = table.find_all('div', class_='a-section a-spacing-none')

        row_data = {}  # Словарь для хранения данных о фильме
        for row in rows:
            key = row.find('span').text.strip()  # Ключ (название поля)
            spans = row.find_all('span')
            if len(spans) > 1:
                value = spans[1].text.strip()  # Значение поля
            # Преобразование данных в соответствии с их типом
            if key == 'Opening':
                value = int(re.sub('[^0-9]', '', value))  # Преобразование строки в число
            elif key == 'Release Date':
                value = value  # Дата без изменений
            elif key == 'Running Time':
                try:
                    time_parts = re.findall(r'\d+', value)  # Разбиение времени на части
                    hours, minutes = map(int, time_parts)  # Преобразование в часы и минуты
                    value = hours * 3600 + minutes * 60  # Перевод в секунды
                except ValueError:
                    continue
            elif key == 'Genres':
                value = [genre.strip() for genre in value.split(',') if genre.strip()]  # Разбиение жанров на список
            elif key == 'In Release':
                value = re.sub(r'[^\d]', '', value)  # Удаление нечисловых символов
            elif key == 'Widest Release':
                value = int(re.sub('[^0-9]', '', value))  # Преобразование строки в число

            row_data[key] = value  # Добавление пары ключ-значение в словарь

            if row_data:
                data.append(row_data)  # Добавление данных о фильме в общий список
                time.sleep(1)  # Задержка для предотвращения блокировки (закомментировано)

    return data  # Возврат собранных данных


# Функция для сохранения данных в формате JSON
def save_data_to_json(data, filename='box_office_data.json'):
    with open(filename, 'w') as f:  # Открытие файла для записи
        json.dump(data, f, indent=4)  # Сохранение данных в формате JSON с отступами


# Главная функция
def main():
    data = get_box_office_data()  # Получение данных о кассовых сборах
    save_data_to_json(data)  # Сохранение данных в файл


if __name__ == "__main__":
    main()
