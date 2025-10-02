# tools/scraper/scrape.py
import time, os, sys, json
from pathlib import Path
from urllib.parse import urlparse
import yaml
import requests
import requests_cache
import pandas as pd
from bs4 import BeautifulSoup
from readability import Document
from tqdm import tqdm

from .robots import allowed_by_robots
from .normalize import normalize_text

ROOT = Path(__file__).resolve().parents[2]     # project root
SCRAPED_DIR = ROOT / "scraped"
SCRAPED_DIR.mkdir(exist_ok=True)

def session_with_headers(ua: str, timeout: int):
    requests_cache.install_cache(
        cache_name=str(SCRAPED_DIR / "http_cache"),
        expire_after=60*60*24  # 1 day
    )
    s = requests.Session()
    s.headers.update({"User-Agent": ua})
    s.request_timeout = timeout
    return s

def fetch(s: requests.Session, url: str, timeout: int):
    resp = s.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp

def scrape_table(s, src, timeout):
    resp = fetch(s, src["url"], timeout)
    tables = pd.read_html(resp.text)
    idx = src.get("table_index", 0)
    col = src.get("text_column", 0)
    if idx >= len(tables):
        raise IndexError(f"No table index {idx} at {src['url']}")
    df = tables[idx]
    if col >= len(df.columns):
        raise IndexError(f"No column {col} in table {idx} at {src['url']}")
    texts = df.iloc[:, col].astype(str).tolist()
    return [normalize_text(t) for t in texts if isinstance(t, str)]

def scrape_list(s, src, timeout):
    resp = fetch(s, src["url"], timeout)
    soup = BeautifulSoup(resp.text, "lxml")
    items = soup.select(src["selector"])
    return [normalize_text(i.get_text(" ", strip=True)) for i in items]

def scrape_article(s, src, timeout):
    resp = fetch(s, src["url"], timeout)
    doc = Document(resp.text)
    html = doc.summary(html_partial=True)
    soup = BeautifulSoup(html, "lxml")
    text = normalize_text(soup.get_text(" ", strip=True))
    return [text] if text else []

def main():
    cfg_path = ROOT / "tools" / "scraper" / "config.yaml"
    cfg = yaml.safe_load(open(cfg_path, "r", encoding="utf-8"))
    out_csv = ROOT / cfg.get("out_csv", "scraped/scam_texts.csv")
    ua = cfg.get("user_agent", "ScamawayBot/0.1")
    delay = cfg.get("delay_seconds", 2)
    timeout = cfg.get("timeout_seconds", 15)

    s = session_with_headers(ua, timeout)
    rows = []

    for src in tqdm(cfg["sources"], desc="Sources"):
        url = src["url"]
        # robots.txt check
        if not allowed_by_robots(url, ua):
            print(f"[SKIP robots.txt] {url}")
            continue

        label = src.get("label", "spam").lower()
        stype = src["type"]

        try:
            if stype == "table":
                texts = scrape_table(s, src, timeout)
            elif stype == "list":
                texts = scrape_list(s, src, timeout)
            elif stype == "article":
                texts = scrape_article(s, src, timeout)
            else:
                print(f"[WARN] Unknown type '{stype}' for {url}")
                continue
        except Exception as e:
            print(f"[ERR] {url}: {e}")
            continue

        # de-duplicate & filter empties
        seen = set()
        for t in texts:
            t = t.strip()
            if t and t not in seen:
                rows.append({"text": t, "label": label, "source_url": url, "source_name": src.get("name","")})
                seen.add(t)

        time.sleep(delay)  # be gentle

    if not rows:
        print("No rows collected. Check your selectors/table config.")
        sys.exit(1)

    df = pd.DataFrame(rows)
    # final cleanup: drop very short rows (optional)
    df = df[df["text"].str.len() >= 10]
    df = df.drop_duplicates(subset=["text"])
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"Wrote {len(df)} rows → {out_csv}")

if __name__ == "__main__":
    main()
