import tweepy, re, requests, bs4, json
from tweepy import OAuthHandler
import pandas as pd
from nlp_toolkit import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)'
}

creds = json.load(open('E:/API-Credentials/Twitter.json'))

URL_REGEX = re.compile(r'''((http[s]?://)[^ <>'"{}|\\^`[\]]*)''')
TOKENIZE_REGEX = re.compile(r"[A-Z][a-z]+|[0-9]+[a-z]*|[A-Z]+?|[a-z]+")

auth = OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
auth.set_access_token(creds["access_token"], creds["access_secret"])
api = tweepy.API(auth, timeout=10, wait_on_rate_limit=True)

def extract_info(status):
    tweet = {
        'text': status.text,
        'followers': status.user.followers_count,
        'retweets': status.retweet_count,
        'favorites': status.favorite_count,
        'publish_url': f'https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/{status.id_str}',
        'user': (status.user.name, status.entities['urls'][0]['url']) if status.user.verified else None
    }
    tweet_hashtags = []
    for _ in status.entities['hashtags']:
        tweet_hashtags.append(_['text'])
    tweet['hashtags'] = ' '.join(tweet_hashtags)
    return tweet

def fetch_tweets(n, query=''):
    try:
        list_tweets = []
        for status in tweepy.Cursor(api.search, q=query+" -filter:retweets", lang='en', result_type='trending').items(n):
            list_tweets.append(extract_info(status))
        list_tweets = pd.DataFrame(list_tweets)
        list_tweets['followers'] /= list_tweets['followers'].max()
        list_tweets['retweets'] /= list_tweets['retweets'].max()
        list_tweets['favorites'] /= list_tweets['favorites'].max()
        return list_tweets
    except Exception as e:
        print(e)
        
def hashtag_trends(id):
    try:
        trends = api.trends_place(id) [0]['trends']
        names = [(trend['name'], trend['tweet_volume']) for trend in trends]
        return names
    except Exception as e:
        print(e)
        return []

def tokenize_hashtag(hashtag):
    if len(hashtag.split()) == 1:
        return TOKENIZE_REGEX.findall(hashtag)
    return hashtag.split()    
    
def filter_tags(news_tags):
    news_tags = [tag for tag in news_tags if tag[1] is not None]
    news_tags = [tag for tag in news_tags if (97 <= ord(tag[0][1]) <= 122) or (65 <= ord(tag[0][1]) <= 90) or (48 <= ord(tag[0][1]) <= 57)]
    for tag in news_tags:
        for char in tag[0]:
            if char not in '#QWERTYUIOPASDFGHJKLZXCVBNM qwertyuiopasdfghjklzxcvbnm1234567890.-_"\'':
                news_tags.remove(tag)
                break    
    news_tags_copy = news_tags[:]
    news_tags = []
    news_tags_clean = []
    for t in news_tags_copy:
        clean_t = ''.join(x.lower() for x in tokenize_hashtag(t[0]))
        if clean_t != '' and clean_t not in news_tags_clean:
            news_tags_clean.append(clean_t)
            news_tags.append(t)
    return news_tags    

def fix_tweets(url):
    res = requests.get(url, headers=headers, timeout=60)
    if res.status_code == requests.codes.ok:
        return (json.loads(res.text)['html'])
    return None
