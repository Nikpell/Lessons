from selenium import webdriver # класс управления браузером
from selenium.webdriver.chrome.options import Options # Настройки
from selenium.webdriver.common.by import By # селекторы
from selenium.webdriver.support.ui import WebDriverWait # класс для ожидания
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
              " like Gecko) Chrome/58.0.3029.110 Safari/537.36")
link = "https://clinmarket.ru/studies/11667"
chrome_option = Options()
chrome_option.add_argument(f'{user_agent=}')
driver = webdriver.Chrome(options=chrome_option)
driver.get(link)
WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME,
                                                                    'body')))
list_name = ['title', 'status', 'protocol', 'description', 'area', 'registration',
             'organisation', 'remedy_name', 'towns', 'country_developer', 'developer', 'phase', 'patients_q']
time.sleep(10)
smths = driver.find_element_by_class_name("flex-column").text.split('\n')
for i in range(len(smths) - 2, 0, -2):
    smths.pop(i)
table = dict(zip(list_name, smths))
print(table)
# driver.find_elements_by_class_name())

driver.quit()

