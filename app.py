from flask import Flask, jsonify

from TwitterClient import TwitterClient
from SentimentAnalysis import get_sentiment

app = Flask(__name__)


@app.route('/')
def index():
    return 'Home'


@app.route('/api/<query>')
def api(query):

    api = TwitterClient()
    tweets = api.get_tweets(query, 500)

    positive = 0
    negative = 0
    neutral = 0

    for tweet in tweets:
        sentiment = get_sentiment(tweet['text'])
        if sentiment == 1:
            positive += 1
        elif sentiment == -1:
            negative += 1
        else:
            neutral += 1

    total = positive + negative + neutral

    positive = (positive / total) * 100
    negative = (negative / total) * 100
    neutral = (neutral / total) * 100

    return jsonify(
        {
            'positive': positive,
            'negative': negative,
            'neutral': neutral
        }
    )
