from bs4 import BeautifulSoup
import sys
import json

mosque_map = {
    "kgn": "kgn.html",
    "fr": "fr.html",
    "j": "j.html",
    "cm": "cm.html"
}

mosque_key = sys.argv[1]
data = json.loads(sys.argv[2])
filename = mosque_map.get(mosque_key)

with open(filename, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

rows = soup.select("table tbody tr")
for i, row in enumerate(rows):
    cells = row.find_all("td")
    if len(cells) == 3:
        label = cells[0].text.strip()
        cells[1].string = data[label]["Adhan"]
        cells[2].string = data[label]["Iqamah"]

with open(filename, "w", encoding="utf-8") as f:
    f.write(str(soup))