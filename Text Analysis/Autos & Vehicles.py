import pandas as pd
import os
import string
import re

os.chdir("S:/NUS/EBAC5002/Project/Data")
data = pd.read_csv('data_final.csv')
del data['Unnamed: 0']
del data['Unnamed: 0.1']
del data['index']

auto = data[data["category"] == 'Autos & Vehicles'] #get a sub-dataframe with only one category
auto = auto.reset_index() # re-index
del auto['index']

auto_tags = auto['tags']
auto_description = auto['description']

## Define a function of pro-processing 
# Stop word preparation
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english') + ['one', 'become', 'get', 'make', 'take', '|', '...', "''"]

WNlemma = nltk.WordNetLemmatizer()

# define a function to convert text into tokens 
def pre_process(text):
    tokens = nltk.word_tokenize(text)  #first tokenize the text
    tokens=[ WNlemma.lemmatize(t.lower()) for t in tokens] # convert the text into lower case and lemmatized
    tokens=[ t for t in tokens if t not in stop] # Remove the stopwords and some meaningless words
    tokens = [ t for t in tokens if t not in string.punctuation ]
    tokens = [ t for t in tokens if len(t) >= 2 ]
    tokens = [ t for t in tokens if not t.isnumeric() ] # And remove the numbers
    text_after_process = list(set(tokens)) # put the unique words into a list
    return(text_after_process)

# tokenize the tags
auto_tags_pro = []
for rows in auto_tags:
    rows_pro = pre_process(rows)
    auto_tags_pro.append(rows_pro)

# tokenize the description
auto_description_pro = []

for rows in auto_description:
    rows_pro = pre_process(rows)
    auto_description_pro.append(rows_pro)
    
# combine tags and descritpion
auto_full = []
i = 0 # loop variable
while i < len(auto_description_pro):
    full_token = list(auto_tags_pro[i] + auto_description_pro[i])
    auto_full.append(full_token)
    i = i + 1

#further clean the tokens
i = 0
while i < len(auto_full):
    j = 0
    while j < len(auto_full[i]):
        if auto_full[i][j].endswith('|'):\
            auto_full[i][j] = auto_full[i][j][0:-1]
        j = j + 1
    i = i + 1


## seperate auto category into some sub_categories
# build a dictionary for commerical demand
from nltk.corpus import wordnet as wn
nltk.download('wordnet')

commerical = ['commerical', 'advertisement', 'ad']
bike = ['bike', 'bicycle','motorcycle', 'cycle']

brand = ['dodge', 'toyota', 'tesla', 'doug', 'demuro', 'dodge', 
              'hyundai', 'marvel', 'mercedes-benz', 'honda', 'chevrolet', 'ford',
              'jeep', 'bmw', 'porsche', 'subaru', 'nissan', 'cadilac', 'volkswagen',
              'lexus', 'audi', 'ferrari', 'f1', 'volvo', 'jaguar', 'gmc', 'buick',
              'acura', 'bentley', 'lincoln', 'mazda', 'rover', 'trucks', 'kia', 'chrysler',
              'pontiac', 'infiniti', 'mitsubishi', 'oldsmobile', 'maserati', 'martin', 'bugatti',
              'mini', 'alfa', 'romeo', 'saab', 'suzuki', 'studebaker', 'renault', 'peugeot',
              'daewoo', 'hudson', 'citroen', 'mg', 'lamborghini', 'mercedes']
# the words extract from USA top 50 popular cars brand

wn.synsets('accident')
ss = wn.synsets('accident', pos = wn.NOUN)[0]
accident_hypo = ss.hyponyms()
accident = ['accident', 'extreme', 'rain', 'wind', 'storm']

for item in accident_hypo:
    item1 = str(item)
    word = re.search(r"'[a-z]+.", item1)[0]
    word = word[1:-1]
    accident.append(word)

    t = item.hyponyms()
    for sub_item in t:
        sub_item = str(sub_item)
        word = re.search(r"'[a-z]+.", sub_item)[0]
        word = word[1:-1]
        accident.append(word)

# Add sub_category to the data
i = 0 # loop variable
auto['sub_category'] = ''

while i < len(auto):
    for ele in auto_full[i]:
        if ele in commerical:
            auto['sub_category'][i] = 'commerical'
        elif ele in accident:
            auto['sub_category'][i] = 'accident'
        elif ele in bike:
             auto['sub_category'][i] = 'bike/motorcycle'
        elif ele in brand:
            auto['sub_category'][i] = 'great cars series'
    i = i + 1

# write the sub_dataframe
#auto.to_csv('auto.csv')


