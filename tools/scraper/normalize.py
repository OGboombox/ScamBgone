# tools/scraper/normalize.py
import re

URL = re.compile(r'https?://\S+', re.I)

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.strip()
    s = URL.sub(" <url> ", s)
    s = re.sub(r"\s+", " ", s)
    return s