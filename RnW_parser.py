import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


# получаем код страницы товаров
html = requests.get("https://krasnoeibeloe.ru/catalog/").text

with open("data/catalog.html", "w") as file:
    file.write(html)  # запишем код страницы в отдельный файл на всякий случай

soup = BeautifulSoup(html, "lxml")  # lxml - самый быстрый парсер

# получаем все ссылки со страницы товаров
