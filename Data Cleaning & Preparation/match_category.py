import json
import csv
import os
import pandas as pd

os.chdir("S:/NUS/EBAC5002/Project/Data")

data = pd.read_csv('data_clean.csv')
# extract Id and title from the json file
#cate = open('US_category_id.json', 'r')
#cateId = json.load(cate)
#with open('US_category_id.csv', 'w', newline = '') as f:
#    csvWriter = csv.writer(f)
#    csvWriter.writerow(['id', 'category'])
#    for i in cateId['items']:
#        csvWriter.writerow([i['id'], i['snippet']['title']])
        
# match Id and title with the data file
id_to_category = {}
with open(r"US_category_id.json") as f:
    cate = json.load(f)
    for category in cate["items"]:
        id_to_category[category["id"]] = category['snippet']['title']
data['category_id'] = data['category_id'].astype(str)
data['category'] = data['category_id'].map(id_to_category)
data.to_csv('test5.csv')
