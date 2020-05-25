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
    def __init__(self, entidad=None):
        super(Cotizacion, self).__init__()
        self.entidad = entidad
        if self.entidad != None:
            self.url = urls[self.id]["url"]
            self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        else:
            self.url = None
            self.soup = None
        self.urls = urls

    def transformar(self, valor):
        return "${:.2f}".format(float((valor.text.replace(",", ".")))).replace(".", ",")

    def cotizacion_compra(self, entidad):
        self.url = urls[entidad]["url"]
        self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        row = self.soup.select_one(urls[entidad]["compra"])
        return self.transformar(row)

    def cotizacion_venta(self, entidad):
        self.url = urls[entidad]["url"]
        self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        row = self.soup.select_one(urls[entidad]["venta"])
        return self.transformar(row)

    def cotizar(self):
        e, c, v = [], [], []
        for entidad in urls.keys():
            e.append("=== {} ===".format(entidad.upper()))
            c.append("Compra: {}".format(self.cotizacion_compra(entidad)))
            v.append("Venta: {}".format(self.cotizacion_venta(entidad)))

        return e, c, v


def main():
    # ejemplo
    c = Cotizacion()
    print("Entidades soportadas: {}".format(", ".join([x for x in urls.keys()])))
    # c.cotizar()
    entidad = str(input(">> Ingrese el nombre de una entidad para consultar: " ))
    if entidad != "*":
        compra = c.cotizacion_compra(entidad)
        venta = c.cotizacion_venta(entidad)
        print("=== {} ===".format(entidad.upper()))
        print("Compra: {}".format(compra))
        print("Venta: {}".format(venta))
    else:
        for entidad in urls:
            print("=== {} ===".format(entidad.upper()))
            print(c.cotizacion_compra(entidad))
            print(c.cotizacion_venta(entidad))
            print("")

if __name__ == '__main__':
    main()
