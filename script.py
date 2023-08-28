import requests
from bs4 import BeautifulSoup

url = "https://www.nike.com.br/tenis-nike-dunk-high-retro-masculino-026963.html?cor=51"
# url = "https://www.nike.com.br/tenis-nike-renew-ride-3-012944.html?cor=IM"
options = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=options)


class TenisNike:
    def __init__(self, soup: BeautifulSoup):
        self.name = soup.find("h1", {"data-testid": "product-name"})
        self.cor = soup.find("li", {"data-testid": "color-description"})

        if soup.find_all("img", {"data-testid": True}):
            self.img = [
                img["src"] for img in soup.find_all("img", {"data-testid": True})
            ][:2]
        if soup.find("span", {"aria-label": "preço antigo"}) != None:
            self.haves_discount = True
            self.price_with_discount = soup.find("span", {"data-testid": "pricebox"})
            self.price_without_discount = soup.find(
                "span", {"aria-label": "preço antigo"}
            )
            self.discount = self.price_without_discount.find_next()
        else:
            self.haves_discount = False
            self.price = soup.find("span", {"data-testid": "pricebox"})

        if soup.find("span", {"data-testid": "snippet-rating-label"}):
            self.rating = soup.find("span", {"data-testid": "snippet-rating-label"})
        else:
            self.rating = "Sem avaliação"

        self.sizes = [
            label.text
            for label in soup.find_all("label")
            if "disabled" not in label.contents[0].attrs
        ]

    def print(self):
        for key, value in self.to_dict().items():
            print(f"{key}: {value}")
        # if tenis.haves_discount:
        #     print("Nome:", self.name.text)
        #     print("Preco sem desconto:", self.price_without_discount.text)
        #     print("Preco com desconto:", self.price_with_discount.text)
        #     print(f"Desconto: {self.discount.text}")
        # else:
        #     print("Nome:", self.name.text)
        #     print("Preço:", self.price.text)

        # if isinstance(self.rating, str):
        #     print(f"Avaliação: {self.rating}")
        # else:
        #     print(f"Avaliação: {self.rating.text}/5.0")

        # print("Tamanhos Disponiveis:", ", ".join(self.sizes))

    def to_dict(self):
        result = {
            "Nome": self.name.text,
            "Cor": self.cor.text.replace("Cor: ", ""),
            "Avaliação": self.rating
            if isinstance(self.rating, str)
            else f"{self.rating.text}/5.0",
            "Tamanhos Disponíveis": ", ".join(self.sizes),
            "Imagens": self.img,
            "URL": url,
        }

        if self.haves_discount:
            result.update({"Preço sem desconto": self.price_without_discount.text})
            result.update({"Preço com desconto": self.price_with_discount.text})
        else:
            result.update({"Preço": self.price.text})

        return result


if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    tenis = TenisNike(soup)

    tenis.print()

    # print(tenis.to_dict())
