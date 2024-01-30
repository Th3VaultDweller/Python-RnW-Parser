import random
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager

# делаем опцию для запуска браузера в режиме инкогнито
option = Options()
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--disable-infobars")
option.add_argument("--start-maximized")

# берём драйвер для работы Selenium и запускаем Chrome на странице поиска в режиме инкогнито
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser = webdriver.Chrome(options=option)
browser.get("https://www.google.com/")

# определяем URL сайта
url = "https://krasnoeibeloe.ru/"
browser.get(url)

# ждём появления кнопки и проходим проверку на возраст
element_to_be_clicked = "/html/body/div[7]/div/div/div/div/div/div[2]/div[2]/a[1]"

if element_to_be_clicked:
    age_popup = (
        wait(browser, 60)
        .until(EC.visibility_of_element_located((By.XPATH, element_to_be_clicked)))
        .click()
    )
else:
    pass
    time.sleep(random.randrange(2, 5))


# переходим в каталог
catalogue = browser.find_element(
    By.XPATH, "/html/body/div[1]/div/header/div/div[2]/div[3]/nav/ul/li[1]/a"
).click()

time.sleep(random.randrange(2, 5))

# и пробуем собрать все товары из одной категории
category = browser.find_element(
    By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/a"
)
category.click()

time.sleep(random.randrange(5, 15))

all_product_links = browser.find_element(
    By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[6]"
).find_elements("catalog_product_item").text()
for link in all_product_links:
    link_text = all_product_links.get_attribute("text")  # название товара
    link_href = all_product_links.get_attribute("href")  # ccылка на товар
    # print(i)  # нумерация товаров начинается с нуля
    print(f"{link_text.strip()}: {link_href}")


browser.quit()
