import requests
from bs4 import BeautifulSoup

from src.TenisNike import TenisNike

urls = [
    "https://www.nike.com.br/tenis-nike-dunk-high-retro-masculino-026963.html?cor=51",
    "https://www.nike.com.br/tenis-nike-renew-ride-3-012944.html?cor=IM",
]

options = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

for url in urls:
    response = requests.get(url, headers=options)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        TenisNike(soup, url).print()

        print("============================================================")
        print('\n')

