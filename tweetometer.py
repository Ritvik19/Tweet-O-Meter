from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

import logging
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.jinja_env.globals.update(eval=eval)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
admin = Admin(app)

from routes import *
from models import Post

from verify import *
from sentiment_analysis import *
from twitter_toolkit import *
from nlp_toolkit import *
from classifiers import *
from core import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

file_handler = logging.FileHandler('site.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def fetchAllTweets(news):
    liveTweets = {}
    
    logger.info('Fetching News...')
    for i, k in enumerate(news):
        logger.info(f"{i+1:{2}} / {len(news):{2}} : {k[0]:{35}}")
        temp = fetch_tweets(180, k[0])
        if temp is not None:
            logger.info(len(temp))
            if len(temp) >= 30:
                liveTweets[k] = temp 
                
    logger.info('\n\nTweets Fetched')
    return liveTweets

def tweet_id(tweeturls):
    hash_ = 0
    for tweeturl in tweeturls:
        hash_ += int(tweeturl.split('/')[-1])
    return str(hash_)


def createContent():
    ind = hashtag_trends(23424848)
    gbl = hashtag_trends(1)
    news_tags = filter_tags(list(set(ind+gbl)))
    liveTweets = fetchAllTweets(news_tags)
    for i,k in enumerate(liveTweets.keys()):
        logger.debug(k[0])
        score, results = verification_score(' '.join(tokenize_hashtag(k[0])))
        if results[0] != '' and score >= 42:
            summary = buildStory(4, liveTweets[k])
            if len(summary[0]) == 4:
                print(f"{i+1:{2}} {k[0]:{35}}")
                liveTweets[k]['sentiment'] = liveTweets[k]['text'].apply(sentiment_intensity)
                new_post = Post(
                    Hashtag=k[0], Hotness=int(k[1]), Tweet1=fix_tweets(summary[0][2]),
                    Tweet2=fix_tweets(summary[0][3]), Tweet3=fix_tweets(summary[0][0]), Tweet4=fix_tweets(summary[0][1]),
                    VerificationScore=score, Sentiment=sentiment_analysis(summary[1]), FullStory=results[0],
                    Trend=hashtags_sentiments(liveTweets[k], tweet_id(summary[0])),
                    ANI=results[1], HindustanTimes=results[2], IndiaToday=results[3], IndianExpress=results[4],
                    NDTV=results[5], TheHindu=results[6], 
                    National=classify_tag('\n'.join(summary[1]), 'national'),
                    Sports=classify_tag('\n'.join(summary[1]), 'sports'),
                    World=classify_tag('\n'.join(summary[1]), 'world'),
                    Politics=classify_tag('\n'.join(summary[1]), 'politics'),
                    Technology=classify_tag('\n'.join(summary[1]), 'technology'),
                    Entertainment=classify_tag('\n'.join(summary[1]), 'entertainment'),
                    Hatke=classify_tag('\n'.join(summary[1]), 'hatke'),
                    Users=str(getUsers(liveTweets[k]))
                )
                logger.debug(new_post)
                db.session.add(new_post)
                db.session.commit()
                logger.debig('New Post Created')
    logger.info('Content Created')

sched = BackgroundScheduler(daemon=True)
sched.add_job(createContent,'interval',minutes=480)
sched.start()