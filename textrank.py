from nlp_toolkit import *
from classifiers import *
import json, pickle
from twitter_toolkit import *
from nltk import pos_tag

def rankTweets(n, tweet):
    text = tweet['text']
    clean_text = df2str(text)     

    sentences = text.values
    word2count ={}

    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 0
            word2count[word] += 1

    for key in word2count.keys():
        word2count[key] = word2count[key]/max(word2count.values())
        
    word2idf = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2idf.keys():
                word2idf[word] = idf(word, text)
            if pos_tag(word) in ['JJ', 'JJR', 'JJS', 'NNP', 'NNPS']:
                word2idf[word] *= 2

    sent2score = {}

    for sentence in sentences:
        if sentence not in sent2score.keys():
            sent2score[sentence] = 0
        for word in nltk.word_tokenize(str(sentence).lower()):
            if word in word2count.keys():
                sent2score[sentence] += word2count[word]*word2idf[word]
        try:        
            sent2score[sentence] *= len(nlp(sentence).ents)/(len(cleanText(sentence).split()))
        except ZeroDivisionError:
            pass
        
        
    sorted_sentences = [(k, sent2score[k]) for k in sorted(sent2score, key=sent2score.get, reverse=True)]

    summary = []
    summary_clean = []
    i = 1
    for k, v in sorted_sentences:
        try :
            dl = langdetect.detect(str(k))
        except:
            dl = '--'
        if dl == 'en' and classify_spam(k) == 0 and jaccard_iterator(lambda x: cleanText(x).split(), k, summary_clean) < 60 and v > 0:
            summary.append(tweet[tweet['text'] == str(k)]['publish_url'].values[0])
            summary_clean.append(tweet[tweet['text'] == str(k)]['text'].values[0])
            i += 1
            if i > n:
                break
    return summary, summary_clean

