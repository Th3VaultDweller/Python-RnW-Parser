import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}
# получаем код страницы товаров
html = requests.get("https://vkusvill.ru/goods/").text
print(html)

soup = BeautifulSoup(html, "lxml")  # lxml - самый быстрый парсер
