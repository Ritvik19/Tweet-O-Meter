import nltk, re, langdetect, spacy
nlp = spacy.load("en")
from math import log, exp
from nltk.tokenize import sent_tokenize

def jaccard_similarity(t1, t2):
    t1, t2 = set(t1),  set(t2)
    return len(t1&t2)*100/len(t1|t2)

def jaccard_iterator(tokenizer, item, array):
    item = tokenizer(item)
    array = list(map(tokenizer, array))
    try:
        return max([jaccard_similarity(item, a) for a in array])
    except ValueError:
        return 0

def expand_contractions(text):
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)  
    return text

def remove_url(text):
    URL_REGEX = re.compile(r'''((http[s]?://)[^ <>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r' ', text)

def remove_handles(text):
    HANDLES_REGEX = re.compile(r'@\S+')
    return HANDLES_REGEX.sub(r' ', text)

def remove_incomplete_last_word(text):
    INCOMPLETE_LAST_WORD_REGEX = re.compile(r'\S+…')
    return INCOMPLETE_LAST_WORD_REGEX.sub(r' ', text )
    
def remove_hashtags(text):
    HASHTAGS_REGEX = re.compile(r'#\S+')
    return HASHTAGS_REGEX.sub(r' ', text)

remove_punc = lambda x : re.sub(r"\W", ' ', x)

remove_num = lambda x : re.sub(r"\d", ' ', x)

remove_extra_spaces = lambda x : re.sub(r"\s+", ' ', x)

lower_case = lambda x : x.lower()

remove_shortwords = lambda x: ' '.join(word for word in x.split() if len(word) > 2)

with open('stopwords.txt') as f:
    sw = map(lambda x : x.strip(), f.readlines())
stop_words = set(nltk.corpus.stopwords.words('english'))|set(sw)
remove_stopwords = lambda x: ' '.join(word for word in x.split() if word not in stop_words)

def cleanText(x):
    x = str(x)
    x = remove_url(x)
    x = remove_handles(x)
    x = remove_incomplete_last_word(x)
    x = remove_hashtags(x)
    x = lower_case(x)
    x = expand_contractions(x)
    x = remove_punc(x)
    x = remove_num(x)
    x = remove_extra_spaces(x)
    x = remove_shortwords(x)
    x = remove_stopwords(x)
    return x

def df2str(df):
    corpus = ''
    for x in df.unique():
        corpus += cleanText(str(x)) + '\n'
    return str(corpus)

def idf(word, text):
    sentences = list(map(lambda x : cleanText(str(x)), text))
    N = len(sentences)
    ni = 0
    for sent in sentences:
        if word in sent:
            ni += 1
    return log(N/ni)