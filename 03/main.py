from flask import Flask
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route("/")
def index():
    r = requests.get('https://cuantoestaeldolar.pe/')
    raw_html = r.text
    soup = BeautifulSoup(raw_html, 'html.parser')
    elements = soup.find_all("p", class_="ValueQuotation_text___mR_0")
    exchangeCompra = float(elements[2].text)
    exchangeVenta = float(elements[3].text)
    return {
        "compra": exchangeCompra,
        "venta": exchangeVenta
    }