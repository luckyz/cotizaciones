# -*- coding: utf-8 -*-
#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

urls = {
    "iol": {
        "url": "https://dolariol.com/",
        "compra": ".precio-compra",
        "venta": ".precio-venta"
    },
    "bna": {
        "url": "https://bna.com.ar/Personas",
        "compra": "#billetes > table > tbody > tr:nth-child(1) > td:nth-child(2)",
        "venta": "#billetes > table > tbody > tr:nth-child(1) > td:nth-child(3)"
    }
}



class Cotizacion(object):
    def __init__(self, id):
        super(Cotizacion, self).__init__()
        self.id = id
        self.url = urls[self.id]["url"]
        self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")

    def compra(self):
        return urls[self.id]["compra"]

    def venta(self):
        return urls[self.id]["venta"]

    def cotizacion(self, selector):
        row = self.soup.select_one(selector)
        precio = "${:.2f}".format(float((row.text.replace(",", "."))))

        return precio.replace(".", ",")


def main():
    # ejemplo
    c = Cotizacion("bna")
    print(c.url)
    print(c.cotizacion(c.compra()))

if __name__ == '__main__':
    main()
