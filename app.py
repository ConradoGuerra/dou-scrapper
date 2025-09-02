from typing import List
from flask import Flask, json
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    from infra.client import get
    from service.extract_response import extract_response

    search_response = get(
        "https://www.in.gov.br/consulta/-/buscar/dou?q=%22Tipo+de+Produto%3A+Alimento%22&s=do1&exactDate=dia&sortType=0"
    )
    pattern = r"({\"jsonArray\"\s*:\[.*\]})"
    found = extract_response(pattern, search_response.text)
    json_response = json.loads(found[0])
    for resolution in json_response["jsonArray"]:
        extracted_paragraphs = []
        url_title = resolution["urlTitle"]
        resolution_found = get(f"https://www.in.gov.br/web/dou/-/{url_title}")
        pattern = r"(Empresa: .+)</p>"
        found = extract_response(pattern, resolution_found.text)
        extracted_paragraphs.append(found[0])
        pattern = r"(Produto .+)</p>"
        found = extract_response(pattern, resolution_found.text)
        extracted_paragraphs.append(found[0])
        pattern = r"(Ações de fiscalização: .+)</p>"
        found = extract_response(pattern, resolution_found.text)
        extracted_paragraphs.append(found[0])
        pattern = r"(Suspensão .*|Proibição .*)</p>"
        found = extract_response(pattern, resolution_found.text)
        extracted_paragraphs.append(found[0])
        pattern = r"(Motivação: .+)</p>"
        found = extract_response(pattern, resolution_found.text)
        extracted_paragraphs.append(found[0])
        write_in_file(extracted_paragraphs)

    if len(json_response["jsonArray"]) > 0:
        return f"Generated {len(json_response['jsonArray'])} reports"
    return "No reports generated"


def write_in_file(txt: List[str]):
    filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open(f"relatorio_{filename}.txt", "w") as file:
        for line in txt:
            file.write(line + "\n")


if __name__ == "__main__":
    app.run(debug=True)
