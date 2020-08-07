import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
sia_obj = SentimentIntensityAnalyzer()

def sentiment_intensity(x):
    return sia_obj.polarity_scores(x)['compound']


def sentiment_analysis(tweets):
    total = 0
    pos = 0
    for t in tweets:
        intensity = sentiment_intensity(t)
        if intensity > 0:
            pos += intensity
        total += abs(intensity)
    try:
        return (pos*100)//total
    except ZeroDivisionError:
        return 50
        

def hashtags_sentiments(tweets, uid):
    data = tweets.explode('hashtags')
    data = data.dropna(subset=['hashtags'])
    hashtags = []
    positive = []
    negative = []

    for _ in pd.Series(' '.join(data['hashtags']).split()).value_counts()[:10].index:
        negative.append(data[(data['hashtags'] == _) & (data['sentiment'] <= 0)]['sentiment'].sum())
        positive.append(data[(data['hashtags'] == _) & (data['sentiment'] >  0)]['sentiment'].sum())
        hashtags.append(_)

    y = np.arange(len(hashtags))

    fig, ax = plt.subplots()
    ax.plot(negative, 'r-o')
    ax.plot(positive, 'g-o')
    ax.legend(['Negative', 'Positive'])
    ax.grid()
    ax.set_xlabel('Hashtag')
    ax.set_ylabel('Sentiment Intensity')
    ax.set_xticks(y)
    ax.set_xticklabels(hashtags, rotation=45)

    fig.tight_layout()
    fig.subplots_adjust()
    plt.savefig('static/'+str(uid)+'.png')      
        
    return str(uid)+'.png'