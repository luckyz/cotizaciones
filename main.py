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

    def transformar(self, valor):
        return "${:.2f}".format(float((valor.text.replace(",", ".")))).replace(".", ",")

    def cotizacion_compra(self):
        row = self.soup.select_one(urls[self.id]["compra"])
        return self.transformar(row)

    def cotizacion_venta(self):
        row = self.soup.select_one(urls[self.id]["venta"])
        return self.transformar(row)


def main():
    # ejemplo
    c = Cotizacion("bna")
    print(c.url)
    print(c.cotizacion_compra())

if __name__ == '__main__':
    main()
