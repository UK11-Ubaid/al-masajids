from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Setup headless Chrome for GitHub Actions
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://salaahtimes.co.za/johannesburg")
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Extract prayer times
table = soup.find('table', class_='table table-bordered pull center visible-xs')
prayer_times = {}

if table:
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 1:
            prayer_times['Date'] = cols[0].get_text(strip=True)
        elif len(cols) >= 2:
            label = cols[0].get_text(strip=True).strip()
            time_value = cols[-1].get_text(strip=True).strip()
            prayer_times[label] = time_value

# Load local HTML
with open("index.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# Update prayer times
for row in soup.select("table tbody tr"):
    cols = row.find_all("td")
    if len(cols) == 2:
        name = cols[0].get_text(strip=True)
        if name in prayer_times:
            cols[1].string = prayer_times[name]

# Update date display
date_span = soup.find('span', id='prayer-date')
if date_span and 'Date' in prayer_times:
    date_span.string = prayer_times['Date']

# Save updated HTML
with open("index.html", "w", encoding="utf-8") as file:
    file.write(str(soup))
