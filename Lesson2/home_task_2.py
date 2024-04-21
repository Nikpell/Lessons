"""
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию
о всех книгах на сайте во всех категориях: название, цену, количество товара в наличии
(In stock (19 available)) в формате integer, описание.

Затем сохранить эту информацию в JSON-файле.
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import json


def get_soup_for_page(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; '
                      'Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_links_for_book(soup):
    book_links = []
    for link in soup.find_all('div', class_='image_container'):
        a_tag = link.find('a')
        if a_tag:
            book_links.append(a_tag.get('href').replace('catalogue/', ''))
    return book_links


def get_links_for_pages(soup):
    for link in soup.find_all('li', class_="next"):
        a_tag = link.find('a')
        return a_tag.get('href').replace('catalogue/', '')


def join_url(link):
    return urllib.parse.urljoin('http://books.toscrape.com/catalogue/', link)


def get_data_from_page(soup):
    name = soup.find('div', class_='col-sm-6 product_main').find('h1').text
    price = soup.find('p', class_='price_color').text
    available = soup.find('p', class_='instock availability').text.strip()
    available = int(available.replace('In stock (', '').replace(' available)', ''))
    product_description = set(soup.find_all('p', attrs=False)) - set(soup.find_all('p', attrs=True))
    product_description = f'{product_description}'
    product_description = product_description.replace('{<p>', '').replace('</p>}', '')
    data = {'Name': name,
            'Price': price,
            'Availability': available,
            'Description': product_description
            }
    return data


def save_data_to_json(data, filename='books_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    list_links_to_books = []
    soup = get_soup_for_page('http://books.toscrape.com/')
    book_list = get_links_for_book(soup)
    link = get_links_for_pages(soup)
    list_pages = ['http://books.toscrape.com/']
    list_links_to_books.extend(book_list)
    while (link):
        url = join_url(link)
        soup = get_soup_for_page(url)
        book_list = get_links_for_book(soup)
        list_pages.append(url)
        list_links_to_books.extend(book_list)
        link = get_links_for_pages(soup)
    list_links_to_books = [join_url(x) for x in list_links_to_books]
    common_list = []
    for url in list_links_to_books:
        soup = get_soup_for_page(url)
        common_list.append(get_data_from_page(soup))
    save_data_to_json(common_list)


if __name__ == "__main__":
    main()
