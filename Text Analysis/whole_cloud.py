'''

Please put this file with function.py under the same path!

'''
from function import text_analysis
import pandas as pd
import os

os.chdir("S:/NUS/EBAC5002/Project/Data") 
data = pd.read_csv('data_final.csv')

category= data['category']
cate_set = set()

for ele in category:
    cate_set.add(ele)
    

for ele in cate_set:
    print("Operating Category:", ele)
    text_analysis(data, ele)

text_analysis(data, 'Comedy')
text_analysis(data, 'Entertainment')
text_analysis(data, 'Film & Animation')
text_analysis(data, 'Gaming')
text_analysis(data, 'Howto & Style')
text_analysis(data, 'Music')
text_analysis(data, 'News & Politics')
text_analysis(data, 'Nonprofits & Activism')
text_analysis(data, 'People & Blogs')
text_analysis(data, 'Pets & Animals')
text_analysis(data, 'Science & Technology')
text_analysis(data, 'Shows')
text_analysis(data, 'Sports')
text_analysis(data, 'Travel & Events')
text_analysis(data, 'Autos & Vehicles')
