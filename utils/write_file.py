import os
import sys
from datetime import datetime
from typing import List


def write_in_file(txt: List[str]):
    filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    if getattr(sys, "frozen", False):
        app_dir = os.path.dirname(sys.executable)
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))

    report_path = os.path.join(app_dir, f"relatorio_{filename}.txt")

    print(f"Generated {report_path}")
    with open(report_path, "w") as file:
        for line in txt:
            file.write(line + "\n")
