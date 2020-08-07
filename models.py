from tweetometer import db
from datetime import datetime

class Post(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Hashtag = db.Column(db.String(100), nullable=False)
    Tweet1 = db.Column(db.Text(), nullable=False)
    Tweet2 = db.Column(db.Text(), nullable=False)
    Tweet3 = db.Column(db.Text(), nullable=False)
    Tweet4 = db.Column(db.Text(), nullable=False)
    Timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Hotness = db.Column(db.Integer(), nullable=False)
    Sentiment = db.Column(db.Integer(), nullable=False)
    Trend = db.Column(db.String(100), nullable=False)
    FullStory = db.Column(db.Text(), nullable=False)
    VerificationScore = db.Column(db.Integer(), nullable=False)
    Users = db.Column(db.Text())
    ANI = db.Column(db.Text())
    HindustanTimes = db.Column(db.Text())
    IndiaToday = db.Column(db.Text())
    IndianExpress = db.Column(db.Text())
    NDTV = db.Column(db.Text())
    TheHindu = db.Column(db.Text())
    National = db.Column(db.Integer(), nullable=False)
    Sports = db.Column(db.Integer(), nullable=False)
    World = db.Column(db.Integer(), nullable=False)
    Politics = db.Column(db.Integer(), nullable=False)
    Technology = db.Column(db.Integer(), nullable=False)
    Entertainment = db.Column(db.Integer(), nullable=False)
    Hatke = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.Id}', '{self.Hashtag}')"