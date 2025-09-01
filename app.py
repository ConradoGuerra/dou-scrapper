from typing import List
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    from infra.client import get
    from service.extract_response import extract_response

    texto = []
    response = get(
        "https://www.in.gov.br/consulta/-/buscar/dou?q=%22Tipo+de+Produto%3A+Alimento%22&s=do1&exactDate=all&sortType=0"
    )
    pattern = r"urlTitle\"\:\"([a-z-0-9.*]+)"
    found = extract_response(pattern, response.text)
    response = get(f"https://www.in.gov.br/web/dou/-/{found[0]}")
    pattern = r"(Empresa: [A-Z\s]+ - CNPJ: [0-9]+)"
    found = extract_response(pattern, response.text)
    print(found)
    texto.append(found[0])
    pattern = r"(Produto - \(Lote\):[íáçãéóàâêA-Za-z0-9\,\s\(\)\-\º\/\.\;\:\°]+)"
    found = extract_response(pattern, response.text)
    print(found)
    texto.append(found[0])
    pattern = r"(Ações de fiscalização: [íáçãéA-Za-z0-9]+)"
    found = extract_response(pattern, response.text)
    print(found)
    texto.append(found[0])
    pattern = r"(Suspensão - [íáçãéA-Za-z0-9\,\s]+)"
    found = extract_response(pattern, response.text)
    print(found)
    texto.append(found[0])
    pattern = r"(Motivação: [íáçãéóàâêA-Za-z0-9\,\s\(\)\-\º\/\.\;\:\°]+)"
    found = extract_response(pattern, response.text)
    print(found)
    texto.append(found[0])
    write_in_file(texto)

    return response.text


def write_in_file(txt: List[str]):
    with open("test.txt", "w") as file:
        for line in txt:
            file.write(line + "\n")


if __name__ == "__main__":
    app.run(debug=True)
