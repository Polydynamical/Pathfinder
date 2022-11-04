import json
import pandas as pd
import numpy as np


distancefile = json.loads(open("100distance.txt").read())

li = []

for parent, adj_li in dict(distancefile).items():
    for adj in adj_li:
        li.append(adj[1])

df = pd.DataFrame(li)
print(df.describe())
