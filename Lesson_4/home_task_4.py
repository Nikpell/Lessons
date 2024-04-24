"""
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки
HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml,
чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

Строку агента пользователя в заголовке HTTP-запроса,
чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и
извлечения их содержимого.
Обработка ошибок для случаев,
когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические
и юридические нормы при веб-скреппинге.
"""
import requests
from lxml import html
import csv
import urllib.parse
import random
import time

LIST_TO_CSV = []


def one_page_scrape(url):
    """
    get page from url
    :param url:
    :return:
    """
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    })
    print(response.status_code)
    return html.fromstring(response.content)


def parce_page(tree):
    """
    get data from page table and write it to list of dictionary,
     redundant columns handled
    :param tree:
    :return:
    """
    def filter_elemet(elements):
        if elements[0] in list_name:
            return True
        return False

    list_name = ['Статус КИ', 'Фаза КИ', 'Города', 'Название ЛП', 'Название организации, проводящей КИ',
                 'Номер и дата РКИ', 'Дата начала и окончания КИ', 'Терапевтическая область', 'Название протокола']
    protocol_name = tree.xpath("//span[@class='']/a/text()")
    name = tree.xpath("//span[@class='name']/text()")
    value = tree.xpath("//div[@class='row-info']/span[@class='value']/text()")
    new_list = list(zip(name, value))
    new_list = list(filter(filter_elemet, new_list))

    while (len(new_list)):
        row = {}
        for i in range(1, 10):
            row.update({new_list.pop()})
        row.update({'протокол_номер': protocol_name.pop()})
        LIST_TO_CSV.append(row)


def page_to_csv(list_row):
    """
    write general list of dictionary to csv file
    :param list_row:
    :return:
    """
    with open('hometask.csv', 'w', newline='') as csvfile:
        fieldnames = [x for x in list_row[0].keys()]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in list_row:
            writer.writerow(row)


def is_new_page_available(tree):
    """
    get a address of new page in list or empty list
    :param tree:
    :return:
    """
    url_new = tree.xpath("/html/body/div[1]/div/div[8]/ul/li[14]/a/@href")
    return url_new


def teacher_chose():
    """
    for convenience to check working
    :return:
    """
    print('For your convenience, you can select the number of pages '
          'required for processing')
    number = input('Enter number of pages or all pages will process : ')
    return number


def do_one_circle(url):
    """
    full parse of one`s page
    :param url:
    :return:
    """
    tree = one_page_scrape(url)
    parce_page(tree)
    return is_new_page_available(tree)


def main():
    """
    parse of pick out pages and write to csv file
    :return:
    """
    number = teacher_chose()
    url = ('https://clinline.ru/reestr-klinicheskih-issledovanij.html'
           '?show-all=&per_page=50&search=&fio=&name=&status%5B0%5D=%D0%9F%'
           'D1%80%D0%BE%D0%B2%D0%BE%D0%B4%D0%B8%D1%82%D1%81%D1%8F&rki_begin=&rki_end=')
    if number.strip().isdigit():
        for i in range(int(number)):
            if url == 'https://clinline.ru':
                break
            else:
                url_new = do_one_circle(url)
                if url_new:
                    url_end = url_new[0]
                else:
                    url_end = ''
                print(f'open {i + 1}`th page')
                url = urllib.parse.urljoin('https://clinline.ru', url_end)
                time.sleep(random.randint(20, 60) / 10)
    else:
        i = 1
        while (url != 'https://clinline.ru'):
            new_url = do_one_circle(url)
            if new_url:
                url_end = new_url[0]
            else:
                url_end = ''
            print(f'open {i}`th page')
            url = urllib.parse.urljoin('https://clinline.ru', url_end)
            time.sleep(random.randint(20, 60) / 10)
            i += 1

    page_to_csv(LIST_TO_CSV)


if __name__ == "__main__":
    main()
