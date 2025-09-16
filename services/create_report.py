import json
import requests
from utils.extract_response import extract_response
from utils.write_file import write_in_file


def create_report():
    print("---------------------------------------------------------------------------")
    print("Calling gov....")
    search_response = requests.get(
        "https://www.in.gov.br/consulta/-/buscar/dou?q=%22Tipo+de+Produto%3A+Alimento%22&s=do1&exactDate=dia&sortType=0"
    )
    pattern = r"({\"jsonArray\"\s*:.*\[.*\]})"
    found = extract_response(pattern, search_response.text)
    if not found:
        print("No reports generated")
        return
    json_response = json.loads(found[0])
    for resolution in json_response["jsonArray"]:
        print(
            "---------------------------------------------------------------------------"
        )
        extracted_paragraphs = []
        url_title = resolution["urlTitle"]
        print(f"Searching for {url_title}....")
        resolution_found = requests.get(f"https://www.in.gov.br/web/dou/-/{url_title}")
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

    print("---------------------------------------------------------------------------")
    if len(json_response["jsonArray"]) > 0:
        print(f"Generated {len(json_response['jsonArray'])} reports")
    else:
        print("No reports generated")
