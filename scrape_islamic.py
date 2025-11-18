from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://jamiat.org.za/monthly-islamic-calendar/")
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

islamic_el = soup.find("div", class_="value islamic hd-out")
islamic_date = islamic_el.get_text(strip=True) if islamic_el else None

# Load local index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

span = soup.find("span", id="prayer-islamic-date")
if span and islamic_date:
    span.string = islamic_date

with open("index.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
