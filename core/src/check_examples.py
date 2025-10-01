import json, sys
from core.src.detector import Rulepack, decide
rp = Rulepack.default()
cases = json.load(open("core/data/examples.json","r",encoding="utf-8"))
ok = 0
for c in cases:
    got = decide(c["text"], rp).split()[0]
    print(f"{c['text']}\n  want={c['want']} got={got}\n")
    ok += int(got == c["want"])
print(f"Passed {ok}/{len(cases)}")
sys.exit(0 if ok == len(cases) else 1)