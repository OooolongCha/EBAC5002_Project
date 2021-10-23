import string
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
import re

def information_extract(data, aimcategory):
    '''
    This is a function to extract information from 'tags' and 'description' of some specific category (aimcategory) 

    Parameters
    ----------
    data : pandas dataframe
        DESCRIPTION.
    aimcategory : string
        Such as: 'Comedy' or 'Gaming'

    Returns
    -------
    aimcategory_tags : pandas.core.series.Series
        
    aimcategory_description : pandas.core.series.Series
        
    Example
    -------
    comedy_tags, comedy_description = information_extract(data, 'Comedy')
    
    '''
    try: del data['Unnamed: 0']
    except KeyError: pass

    try: del data['Unnamed: 0.1']
    except KeyError: pass
    
    try: del data['index']
    except KeyError: pass
    
    aimcategory = data[data["category"] == aimcategory] #get a sub-dataframe with only one category
    aimcategory = aimcategory.reset_index() # re-index
    
    try: del aimcategory['index']
    except KeyError: pass

    aimcategory_tags = aimcategory['tags']
    aimcategory_description = aimcategory['description']
    
    return aimcategory_tags, aimcategory_description



def pre_process(text):

    stop = stopwords.words('english') + ['one', 'become', 'get', 'make', 'take', '|', '...', "''", "--",
                                         'http', 'youtube', 'subscribe', 'channel', 'twitter', 'instagram', 'facebook', 'video', 
                                         'patreon', 'patron','game', 'gameplay', 'play']
    # Stop words need to be ajusted for different cateogries
    WNlemma = nltk.WordNetLemmatizer()
    
    tokens = nltk.word_tokenize(text)  #first tokenize the text
    tokens=[ WNlemma.lemmatize(t.lower()) for t in tokens] # convert the text into lower case and lemmatized
    tokens=[ t for t in tokens if t not in stop] # Remove the stopwords and some meaningless words
    tokens = [ t for t in tokens if t not in string.punctuation ]
    tokens = [ t for t in tokens if len(t) >= 2 ]
    
    for t in tokens:
        if bool(re.search(r'\d',t)) == True:
            tokens.remove(t)
    
    tokens = [ t for t in tokens if not t.isnumeric() ] #remove the numbers
    text_after_process = list(set(tokens)) # put the unique words into a list

    return text_after_process


def tokenize(text_after_process):
    text_tokenized = []
    for rows in text_after_process:
        if type(rows) != str:
            rows = str(rows)
        
        rows_pro = pre_process(rows)
        text_tokenized.append(rows_pro)
    return text_tokenized



def further_process(pro_tags, pro_descriptions):  #further clean, combine tag and des
    
    # combine tags and descritpion    
    text_full = []
    i = 0 # loop variable
    while i < len(pro_descriptions):
        text_full_tokenized = list(pro_tags[i] + pro_descriptions[i])
        text_full.append(text_full_tokenized)
        i = i + 1

    #further clean the tokens: exclude the symbol '/'
    i = 0
    while i < len(text_full):
        j = 0
        while j < len(text_full[i]):
            if  text_full[i][j].endswith('|'):
                del text_full[i][j]
                #text_full[i][j] = text_full[i][j][0:-1]
                
            j = j + 1
        i = i + 1

    #further clean the tokens: exclude the symbol '\n'
    i = 0
    while i < len(text_full):
        j = 0
        while j < len(text_full[i]):
            if  text_full[i][j].startswith('\\n') or text_full[i][j].startswith('//'):
                del text_full[i][j]
                # text_full[i][j] = text_full[i][j][2:]
            j = j + 1
        i = i + 1
    return text_full

def automatic_clean(data, aimcategory):
    pre_tags, pre_descriptions = information_extract(data, aimcategory)
    after_tags = tokenize(pre_tags)
    after_descriptions = tokenize(pre_descriptions)
    full_text = further_process(after_tags, after_descriptions)
    
    full_list = []
    for lst in full_text:
        for ele in lst:
           full_list.append(ele)
    
    return full_list
#-------------------------Extract the nouns------------------------------------

def lemmaNVAR_noun(wpos):
    wnl = nltk.WordNetLemmatizer()
    i = 0 #loop variable
    lemmas = []
    while i < len(wpos):
        for w, pos in wpos[i]:
            if pos == 'NOUN':
                    lemmas.append(wnl.lemmatize(w.lower(), pos = pos[0].lower()))

        i = i + 1
    return lemmas

def automatic_noun(textlist):
    pos = []
    for t in textlist:
        t = pos_tag(word_tokenize(t), tagset='universal')
        t = list(set(t))
        pos.append(t)
   
    noun = lemmaNVAR_noun(pos)
    return noun

#----------------------Draw word cloud-----------------------------------------
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def draw_wordcloud(input_word):
    font_path = 'Font/JumperPERSONALUSEONLY-Extra-Bold.ttf'

    wc_fd = WordCloud(background_color="white", font_path = font_path, max_words=2000, random_state=42, width=500, height=500)
    wc_fd.generate_from_frequencies(input_word)
    plt.imshow(wc_fd, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    

#-------------------Whole function--------------------------------------------
from nltk import FreqDist
def text_analysis(data, category):
    full_list = automatic_clean(data, category)
    noun = automatic_noun(full_list)
    wordcloud = FreqDist(noun)
    draw_wordcloud(wordcloud)