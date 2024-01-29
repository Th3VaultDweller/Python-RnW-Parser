import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# берём драйвер для работы Selenium и запускаем Chrome на странице поиска
browser = webdriver.Chrome()
browser.get("https://www.google.com/")

# определяем URL сайта
url = "https://krasnoeibeloe.ru/"
browser.get(url)
time.sleep(15)

# ждём появления кнопки и проходим проверку на возраст
element = wait(browser, 15).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[2]/div[2]/a[1]")
    )
)
element.click()

time.sleep(15)

browser.quit()
