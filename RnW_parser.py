import csv
import datetime
import json
import random
import time
from timeit import default_timer as timer

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager

# прописываем опции для запуска браузера
option = Options()
option = webdriver.ChromeOptions()
option.add_argument("--incognito")  # режим инкогнито
option.add_argument("--disable-infobars")  # отключение всплывающих окон
option.add_argument("--start-maximized")  # включение полноэкранного режима
option.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
# берём драйвер для работы Selenium
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser = webdriver.Chrome(options=option)

start_app_time = timer()  # отсчёт с перехода на страницу сайта

# создаём csv-таблицу для записи собранной информации
current_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
with open(
    f"parsed_data_csv\Krasnoe_n_Beloe_{current_time}.csv", "w", encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            "Название товара",
            "Сопутствующая информация о товаре",
            "Изображение",
            "Количество оценок",
            "Цена",
            "Ссылка на товар",
        )
    )

# определяем URL сайта
url = "https://krasnoeibeloe.ru/"
browser.get(url)
print(f"[INFO] Перехожу на сайт {url}...\n")

# ждём появления кнопки и проходим проверку на возраст
element_to_be_clicked = "/html/body/div[7]/div/div/div/div/div/div[2]/div[2]/a[1]"
print("[INFO] Жду появления окна с подтверждением возраста...\n")

if element_to_be_clicked:
    age_popup = (
        wait(browser, 120)
        .until(EC.visibility_of_element_located((By.XPATH, element_to_be_clicked)))
        .click()
    )
    print("[INFO] Проверка на возраст прошла успешно.\n")
else:
    pass
    time.sleep(random.randrange(2, 5))

print("[INFO] Перехожу в каталог товаров...\n")

# находим каталог товаров на странице
all_categories = browser.find_element(By.CLASS_NAME, "left_catalog_c").find_elements(
    By.TAG_NAME, "a"
)  # все категории товаров на сайте

# берём каждую ссылку из каталога товаров
print(f"[INFO] Вывожу на экран все категории товаров и сохраняю их в файл...\n")
all_categories_links_dict = {}
for link in all_categories:
    link_text = link.text
    link_href = link.get_attribute("href")
    print(f"{link_text}: {link_href}")
    time.sleep(random.randrange(2, 5))

    all_categories_links_dict[link_text] = link_href

    # сохраняем каждую ссылку из каталога товаров в отдельный json-файл
    with open("all_categories_links.json", "w") as file:
        json.dump(all_categories_links_dict, file, indent=4, ensure_ascii=False)

# открываем сохранённый файл
with open("all_categories_links.json") as file:
    all_links = json.load(file)  # преобразование json в обычный словарь Python

# и считываем ссылки из файла
for category in list(all_links.values()):
    time.sleep(random.randrange(5, 10))
    category_url = browser.get(category)
    time.sleep(random.randrange(2, 5))
    category_inner_name = browser.find_element(By.TAG_NAME, "h1").text
    time.sleep(random.randrange(2, 5))
    print(f"\n[INFO] Выбираю категорию товара <<{category_inner_name}>>\n")

    # создаём пустой список, куда будем складывать всю инфу
    all_data = []

    if category_inner_name == "Идеи для подарков":
        print(f"[INFO] Скрипт для <<{category_inner_name}>> в процессе написания!\n")
        pass

    else:
        # пробуем собрать все товары из одной категории
        all_product_links = browser.find_elements(
            By.CLASS_NAME, "catalog_product_item_cont"
        )
        
        if all_product_links:
            time.sleep(random.randrange(5, 10))
            print("[INFO] Начинаю парсинг информации...\n")

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

                link_image = link.find_element(By.TAG_NAME, "img").get_property(
                    "src"
                )  # изображение товара

                print(i)  # нумерация товаров начинается с нуля

                try:
                    link_price = (
                        link.find_element(By.CLASS_NAME, "product_item_bottom-btns")
                        .find_element(By.CLASS_NAME, "i_price")
                        .text
                    )  # цена на товар

                except:
                    link_price = "не указана, можно уточнить в магазине"

                print(
                    f"Название: {link_text}\nСопутствующая информация: {link_subtitle}\nИзображение: {link_image}\nКоличество оценок: {link_rating}\nЦена: {link_price}\nСсылка: {link_href}\n"
                )

                all_data.append(
                    {
                        category_inner_name: (
                            {
                                "link_text": link_text,
                                "link_subtitle": link_subtitle,
                                "link_image": link_image,
                                "link_rating": link_rating,
                                "link_price": link_price,
                                "link_href": link_href,
                            }
                        )
                    }
                )

                # запись данных в json-словарь
                with open(
                    f"parsed_data_json\Krasnoe_n_Beloe_{current_time}.json",
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(all_data, file, indent=4, ensure_ascii=False)

                # запись данных в csv-таблицу
                with open(
                    f"parsed_data_csv\Krasnoe_n_Beloe_{current_time}.csv",
                    "a",
                    encoding="utf-8",
                ) as file:
                    writer = csv.writer(file)

                    writer.writerow(
                        (
                            link_text,
                            link_subtitle,
                            link_image,
                            link_rating,
                            link_price,
                            link_href,
                        )
                    )

                time.sleep(10)

        else:
            # на случай, если в существующей категории вообще ничего нет
            print(
                f"[INFO] В категории <<{category_inner_name}>> нет информации для парсинга :(\n"
            )
            pass


overall_app_time = timer() - start_app_time  # общий подсчёт времени

print(f"[INFO] Парсинг сайта {url} завершён!\n")
print(f"[INFO] Количество наименований: {len(all_data)}\n")
print(f"[INFO] Общее время парсинга: {round(overall_app_time)} секунд(а).\n")

browser.quit()
