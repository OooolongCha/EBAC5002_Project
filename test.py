import pandas as pd
import os
import string
import re

os.chdir("S:/NUS/EBAC5002/Project/Data")
data = pd.read_csv('data_final.csv')
del data['Unnamed: 0']
del data['Unnamed: 0.1']
del data['index']

auto = data[data["category"] == 'Comedy'] #get a sub-dataframe with only one category
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
auto_description_pro = [t for t in auto_description if type(t) != float]

from sklearn.feature_extraction.text import CountVectorizer
c_vec = CountVectorizer(stop_words = stop, ngram_range= (1,2))
ngrams = c_vec.fit_transform(auto_description_pro)

count_values=ngrams.toarray().sum(axis=0)
vocab=c_vec.vocabulary_

df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
            ).rename(columns={0: 'Freq', 1:'Phrase'})[0:10]


#pip install wordcloud
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

font_path = 'Font/JumperPERSONALUSEONLY-Extra-Bold.ttf'

wc_fd = WordCloud(background_color="white", font_path = font_path, max_words=500, random_state=42, width=500, height=500)
wc_fd.generate_from_frequencies(vocab)
plt.imshow(wc_fd, interpolation='bilinear')
plt.axis("off")
plt.show()
