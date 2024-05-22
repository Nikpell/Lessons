"""
Выберите веб-сайт, который содержит информацию, представляющую
интерес для извлечения данных. Это может быть новостной сайт,
платформа для электронной коммерции или любой другой сайт,
который позволяет осуществлять скрейпинг (убедитесь в соблюдении
условий обслуживания сайта).
Используя Selenium, напишите сценарий для автоматизации процесса
перехода на нужную страницу сайта.
Определите элементы HTML, содержащие информацию, которую вы хотите
извлечь (например, заголовки статей, названия продуктов, цены и т.д.).
Используйте BeautifulSoup для парсинга содержимого HTML и извлечения
нужной информации из идентифицированных элементов.
Обработайте любые ошибки или исключения, которые могут возникнуть в
процессе скрейпинга.
Протестируйте свой скрипт на различных сценариях, чтобы убедиться,
что он точно извлекает нужные данные.
Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1
страницы), который включает следующее: URL сайта. Укажите URL сайта,
который вы выбрали для анализа. Описание. Предоставьте краткое
описание информации, которую вы хотели извлечь из сайта. Подход.
Объясните подход, который вы использовали для навигации по сайту,
определения соответствующих элементов и извлечения нужных данных.
Трудности. Опишите все проблемы и препятствия, с которыми вы
столкнулись в ходе реализации проекта, и как вы их преодолели.
Результаты. Включите образец извлеченных данных в выбранном вами
структурированном формате (например, CSV или JSON).
Примечание: Обязательно соблюдайте условия обслуживания сайта и
избегайте чрезмерного скрейпинга, который может нарушить нормальную
работу сайта.

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json


teacher_chose = input('If you don`t want spend a lot of time press 2, if you don`t mind, press "ENTER": ')
if teacher_chose == '2':
    teacher_chose = int(teacher_chose)
else:
    teacher_chose = True
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
              " like Gecko) Chrome/58.0.3029.110 Safari/537.36")
link = "https://clinmarket.ru/studies"
chrome_option = Options()
chrome_option.add_argument(f'{user_agent=}')
driver = webdriver.Chrome(options=chrome_option)
try:
    driver.get(link)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME,
                                                                   'body')))
    time.sleep(2)
    size_length = driver.execute_script("return document.documentElement.scrollHeight")
    while(teacher_chose):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);"
                              "")
        driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);"
                              "")
        size_new = driver.execute_script("return document.documentElement.scrollHeight")
        if size_new == size_length:
            break
        size_length = size_new
        if isinstance(teacher_chose, int):
            teacher_chose -= 1
    url_part = driver.find_elements_by_tag_name('a')
    urls = []
    for i in range(len(url_part)):
        urls.append(url_part[i].get_attribute("href"))
    driver.quit()
    list_name = ['title', 'status', 'protocol', 'description', 'area', 'registration',
                 'organisation', 'remedy_name', 'towns', 'country_developer', 'developer', 'phase', 'patients_q']
    data_dict = {}
    data = []
    for url in urls:
        if url.split('/')[-1].isdigit():
            driver = webdriver.Chrome(options=chrome_option)
            driver.get(url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME,
                                                                           'body')))
            time.sleep(5)
            list_data = driver.find_element_by_class_name("flex-column").text.split('\n')
            for i in range(len(list_data) - 2, 0, -2):
                list_data.pop(i)

            data.append(dict(zip(list_name, list_data)))
            driver.quit()

except Exception as er:
    print(f'Произошла ошибка: {er}')
finally:
    with open('clinmarket.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    driver.quit()
