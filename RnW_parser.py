import json
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

# берём драйвер для работы Selenium
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
        wait(browser, 120)
        .until(EC.visibility_of_element_located((By.XPATH, element_to_be_clicked)))
        .click()
    )
    print("Проверка на возраст прошла успешно.\n")
else:
    pass
    time.sleep(random.randrange(2, 5))

print("Перехожу в каталог товаров...\n")

# # находим каталог товаров на странице
# all_categories = browser.find_element(By.CLASS_NAME, "left_catalog_c").find_elements(
#     By.TAG_NAME, "a"
# )  # все категории товаров на сайте

# # берём каждую ссылку и каталога товаров
# print(f"Вывожу на экран все категории товаров и сохраняю их в файл...\n")
# all_categories_links_dict = {}
# for link in all_categories:
#     link_text = link.text
#     link_href = link.get_attribute("href")
#     print(f"{link_text}: {link_href}")
#     time.sleep(random.randrange(2, 5))

#     all_categories_links_dict[link_text] = link_href

#     # сохраняем каждую ссылку из каталога товаров в отдельный json-файл
#     with open("all_categories_links.json", "w") as file:
#         json.dump(all_categories_links_dict, file, indent=4, ensure_ascii=False)

# открываем сохранённый файл
with open("all_categories_links.json") as file:
    all_links = json.load(file)  # преобразование json в обычный словарь Python
    print(f"\n{all_links}\n")

# и считываем ссылки из файла
for category in list(all_links.values()):
    if category == "Идеи для подарков":
        pass
    time.sleep(25)
    category_url = browser.get(category)
    print(f"Перехожу по адресу категории {str(category_url)}\n")

    time.sleep(random.randrange(2, 5))
    category_inner_name = browser.find_element(By.TAG_NAME, "h1").text
    time.sleep(random.randrange(2, 5))
    print(f"Выбираю категорию товара <<{category_inner_name}>>\n")

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
        time.sleep(random.randrange(5, 10))

print(f"Парсинг сайта {url} завершён!\n")

browser.quit()
