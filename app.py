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

    highest_rt = 0
    biggest_tweet = {}

    for tweet in tweets:
        sentiment = get_sentiment(tweet['text'])
        if sentiment == 1:
            tweet['sentiment'] = 'positive'
            positive += 1
        elif sentiment == -1:
            tweet['sentiment'] = 'negative'
            negative += 1
        else:
            tweet['sentiment'] = 'neutral'
            neutral += 1

        if tweet['retweet_count'] > highest_rt:
            biggest_tweet = tweet

    total = positive + negative + neutral

    positive = (positive / total) * 100
    negative = (negative / total) * 100
    neutral = (neutral / total) * 100

    return jsonify({
        'results': {
            'positive': positive,
            'negative': negative,
            'neutral': neutral
        },
        'biggest_tweet': biggest_tweet
    })
