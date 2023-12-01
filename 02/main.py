from flask import Flask
from pypdf import PdfReader


app = Flask(__name__)


@app.route("/")
def index():
    return "PDF reader"


@app.route("/read")
def read():
    reader = PdfReader("data/faq.pdf")
    number_of_pages = len(reader.pages)
    text_pdf = ""
    for i in range(0, number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        text_pdf = text_pdf + "\n" + text
    return {
        "pages": number_of_pages,
        "text": text_pdf,
    }


@app.route("/read/<int:page_number>")
def read_page_number(page_number):
    reader = PdfReader("data/faq.pdf")
    page = reader.pages[page_number - 1]
    text = page.extract_text()
    return {
        "page": page_number,
        "text": text,
    }