from datetime import datetime
from typing import List


def write_in_file(txt: List[str]):
    filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open(f"relatorio_{filename}.txt", "w") as file:
        for line in txt:
            file.write(line + "\n")
