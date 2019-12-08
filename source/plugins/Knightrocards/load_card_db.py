import pandas as pd
from pymongo import MongoClient

import math

# Distributions 
FIVE_STARS = 0.01
FOUR_STARS = 0.04
THREE_STARS = 0.2
TWO_STARS = 0.5
ONE_STAR = 0.5

client = MongoClient()
db = client['Knightrocards']

db["Characters"].drop()
characters = db['Characters']

df = pd.read_csv("chars.csv", delimiter=",")
total = df.shape[0]


for ind, row in df.iterrows():
    new_entry = {}
    new_entry['ID'] = row['id']
    new_entry['Rank'] = row['rank']
    new_entry['Name'] = row['name']
    new_entry['Picture'] = row['pic']
    x = (42470 - row['rank'])
    new_entry['PP'] = int(1000 + math.exp(x / 3478))

    rel_rank = row['rank'] / total
    if rel_rank <= FIVE_STARS:
        new_entry['Stars'] = 5
    elif rel_rank <= FOUR_STARS:
        new_entry['Stars'] = 4
    elif rel_rank <= THREE_STARS:
        new_entry['Stars'] = 3
    elif rel_rank <= TWO_STARS:
        new_entry['Stars'] = 2
    else:
        new_entry['Stars'] = 1
    
    print(new_entry)
    characters.insert_one(new_entry)

characters = db['Characters']
for item in characters.find({"Stars" : 3}):
    print(item)
