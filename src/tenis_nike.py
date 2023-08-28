from bs4 import BeautifulSoup


class TenisNike:
    def __init__(self, soup: BeautifulSoup, url: str):
        self.url = url
        self.name = soup.find("h1", {"data-testid": "product-name"})
        self.cor = soup.find("li", {"data-testid": "color-description"})

        if soup.find_all("img", {"data-testid": True}):
            self.img = [
                img["src"] for img in soup.find_all("img", {"data-testid": True})
            ][:3]
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

    def to_dict(self):
        result = {
            "Nome": self.name.text,
            "Cor": self.cor.text.replace("Cor: ", ""),
            "Avaliação": self.rating
            if isinstance(self.rating, str)
            else f"{self.rating.text}/5.0",
            "Tamanhos Disponíveis": ", ".join(self.sizes),
            "Imagens": self.img,
            "URL": self.url,
        }

        if self.haves_discount:
            self.saving = f'R$ {float(self.price_without_discount.text.replace("R$ ", "").replace(",", ".")) - float(self.price_with_discount.text.replace("R$ ", "").replace(",", ".")):.2f}'.replace(
                ".", ","
            )

            result.update({"Preço sem desconto": self.price_without_discount.text})
            result.update({"Preço com desconto": self.price_with_discount.text})
            result.update({"Economia": self.saving})
            result.update({"Desconto": f"{self.discount.text}"})
        else:
            result.update({"Preço": self.price.text})

        return result
