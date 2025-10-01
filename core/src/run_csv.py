# sms_sample reader

import pandas as pd
from core.src.detector import Rulepack, decide

df = pd.read_csv("core/data/sms_sample.csv")
rp = Rulepack.default()

df['decision'] = df['text'].apply(lambda t: decide(t, rp))
print(df[["label", "text", "decision"]].to_string(index=False))