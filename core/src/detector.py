#Work In Progess - not ready for production

import re
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Rulepack:
    version: int
    bad_domains: List[str]
    keywords: Dict[str, float]
    model: Dict  # placeholder for later ML export
    thresholds: Dict[str, float]


    @staticmethod
    def default():
        return Rulepack(
            version=1,
            bad_domains=["bit.ly", "tiny.cc", "t.co", ".wang", ".top", ".xyz", ".buzz", ".live"],
            keywords={"urgent": 1.0, "refund": 0.8, "verify": 0.7, "congratulations": 0.6},
            model={"type": "none"},  # we’ll plug ML here later
            thresholds={"autoBlock": 1.5, "cloud": 0.8}
        )

def extract_urls(text: str):
    return re.findall(r'https?://([^\s/]+)', text, flags=re.I)

def keyword_score(text: str, keywords: Dict[str, float]) -> float:
    score = 0.0
    words = re.findall(r"[A-Za-z']+", text.lower())
    for w in words:
        score += keywords.get(w, 0.0)
    return score

def domain_score(text: str, bad_domains: List[str]) -> float:
    hosts = [h.lower() for h in extract_urls(text)]
    return 1.0 if any(bad in h for h in hosts for bad in bad_domains) else 0.0

def score_text(text: str, rp: Rulepack) -> float:
    return keyword_score(text, rp.keywords) + domain_score(text, rp.bad_domains)

def decide(text: str, rp: Rulepack) -> str:
    s = score_text(text, rp)
    if s >= rp.thresholds["autoBlock"]:
        return f"JUNK (score={s:.2f})"
    elif s >= rp.thresholds["cloud"]:
        return f"UNSURE—CLOUD (score={s:.2f})"
    else:
        return f"ALLOW (score={s:.2f})"

