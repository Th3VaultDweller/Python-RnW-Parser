import requests
from bs4 import BeautifulSoup

# headers = {
#     "Accept": "application/json",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
# }

proxy = {"https": "https://91.25.93.174:3128"}

# получаем код страницы товаров
url = "http://ident.me/"
response = requests.get(url, proxies=proxy)
ip_adress = response.text
print("Your IP is:", ip_adress)


# soup = BeautifulSoup(html, "lxml")  # lxml - самый быстрый парсер
