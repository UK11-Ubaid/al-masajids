from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# -------------------------------
# SETUP HEADLESS CHROME
# -------------------------------
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# -------------------------------
# SCRAPE ENGLISH DATE + PRAYER TIMES
# -------------------------------
driver.get("https://salaahtimes.co.za/johannesburg")
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

english_data = {}

table = soup.find('table', class_='table table-bordered pull center visible-xs')

if table:
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 1:
            # English date
            english_data['Date'] = cols[0].get_text(strip=True)
        elif len(cols) >= 2:
            label = cols[0].get_text(strip=True)
            time_value = cols[-1].get_text(strip=True)
            english_data[label] = time_value

# -------------------------------
# SCRAPE ISLAMIC DATE
# -------------------------------
driver.get("https://jamiat.org.za/monthly-islamic-calendar/")
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

islamic_el = soup.find("div", class_="value islamic hd-out")
islamic_date = islamic_el.get_text(strip=True) if islamic_el else None

driver.quit()

print("English Date:", english_data.get("Date"))
print("Islamic Date:", islamic_date)

# -------------------------------
# LOAD LOCAL HTML
# -------------------------------
with open("index.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# -------------------------------
# UPDATE PRAYER TIMES IN TABLE
# -------------------------------
for row in soup.select("table tbody tr"):
    cols = row.find_all("td")
    if len(cols) == 2:
        name = cols[0].get_text(strip=True)
        if name in english_data:
            cols[1].string = english_data[name]

# -------------------------------
# UPDATE ENGLISH DATE
# -------------------------------
date_span = soup.find("span", id="prayer-date")
if date_span and 'Date' in english_data:
    date_span.string = english_data['Date']

# -------------------------------
# UPDATE ISLAMIC DATE
# -------------------------------
islamic_span = soup.find("span", id="prayer-islamic-date")
if islamic_span and islamic_date:
    islamic_span.string = islamic_date

# -------------------------------
# SAVE UPDATED HTML
# -------------------------------
with open("index.html", "w", encoding="utf-8") as file:
    file.write(str(soup))

print("index.html updated successfully.")
