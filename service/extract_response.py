import re
from typing import List


def extract_response(pattern: str, response: str) -> List[str]:
    return re.findall(pattern, response)
