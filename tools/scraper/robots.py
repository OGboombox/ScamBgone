# tools/scraper/robots.py
from urllib.parse import urlparse
from urllib import robotparser

def allowed_by_robots(url: str, user_agent: str) -> bool:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(base)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        # If robots.txt can’t be fetched, default to deny to be safe; 
        # change to True if the site policy explicitly allows scraping.
        return False