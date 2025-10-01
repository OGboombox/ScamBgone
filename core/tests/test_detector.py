import json, sys
from core.src.detector import Rulepack, decide
def test_allows_normal_message():
    rp = Rulepack.default()
    assert decide("Your code is 123456. Do not share.", rp).startswith("ALLOW")

def test_blocks_bad_domain_exact_or_subdomain():
    rp = Rulepack.default()
    assert decide("http://bit.ly/win", rp).startswith("JUNK")
    assert decide("http://x.bit.ly/win", rp).startswith("JUNK")