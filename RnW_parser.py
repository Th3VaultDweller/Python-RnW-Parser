import random
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager

# прописываем опции для запуска браузера
option = Options()
option = webdriver.ChromeOptions()
option.add_argument("--incognito")  # режим инкогнито
option.add_argument("--disable-infobars")  # отключение всплывающих окон
option.add_argument("--start-maximized")  # включение полноэкранного режима

# берём драйвер для работы Selenium и запускаем Chrome на странице поиска в режиме инкогнито
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser = webdriver.Chrome(options=option)

# определяем URL сайта
url = "https://krasnoeibeloe.ru/"
browser.get(url)
print(f"Перехожу на сайт {url}...\n")

# ждём появления кнопки и проходим проверку на возраст
element_to_be_clicked = "/html/body/div[7]/div/div/div/div/div/div[2]/div[2]/a[1]"
print("Жду появления окна с подтверждением возраста...\n")

if element_to_be_clicked:
    age_popup = (
        wait(browser, 60)
        .until(EC.visibility_of_element_located((By.XPATH, element_to_be_clicked)))
        .click()
    )
    print("Проверка на возраст прошла успешно.\n")
else:
    pass
    time.sleep(random.randrange(2, 5))

print("Перехожу в каталог товаров...")

# переходим в каталог
catalogue = browser.find_element(
    By.XPATH, "/html/body/div[1]/div/header/div/div[2]/div[3]/nav/ul/li[1]/a"
).click()

time.sleep(random.randrange(2, 5))

# кликаем на нужную категорию товаров
category = browser.find_element(
    By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/a"
)
category.click()
print("Выбираю категорию товара...\n")

time.sleep(random.randrange(5, 15))
print("Начинаю парсинг информации...\n")

# и пробуем собрать все товары из одной категории
all_product_links = browser.find_element(
    By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[6]"
).find_elements(By.CLASS_NAME, "catalog_product_item_cont")

for i, link in enumerate(all_product_links):

    link_text = (
        link.find_element(By.CLASS_NAME, "product_item_name")
        .find_element(By.TAG_NAME, "a")
        .text
    )  # название товара

    link_href = (
        link.find_element(By.CLASS_NAME, "product_item_name")
        .find_element(By.TAG_NAME, "a")
        .get_property("href")
    )  # ccылка на товар

    link_subtitle = (
        link.find_element(By.CLASS_NAME, "product_item_name")
        .find_element(By.CLASS_NAME, "product-subtitle")
        .text
    )  # сопутствующая информация о товаре

    link_rating = (
        link.find_element(By.CLASS_NAME, "product_item_bottom")
        .find_element(By.CLASS_NAME, "rate_votes")
        .text
    )  # количество оценок товара

    print(i)  # нумерация товаров начинается с нуля

    link_price = link.find_element(
        By.CLASS_NAME, "product_item_bottom-btns"
    )  # цена на товар

    if link_price.find_element(By.TAG_NAME, "a").text:
        print(f"Цену товара можно уточнить в магазине.")
    else:
        product_price = link_price.find_elements(
            By.CLASS_NAME, "i_price"
        )  # цена товара
        for price in product_price:
            if product_price:
                link_price = price.find_element(By.TAG_NAME, "div").text

    print(
        f"Название: {link_text}\nСтрана, объём и процент алкоголя: {link_subtitle}\nКоличество оценок: {link_rating}\nЦена: {link_price}\nСсылка: {link_href}\n"
    )
    time.sleep(random.randrange(2, 5))

print(f"Парсинг сайта {url} завершён!\n")

browser.quit()
