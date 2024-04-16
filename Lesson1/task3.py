import json

import pandas as pd

with open('../Prev_HT/dict.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(list(data.items()), columns=['name','address'])
print(df.info)