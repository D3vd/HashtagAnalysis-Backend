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
    tweets = api.get_tweets(query, 200)

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

    total_per = positive + negative + neutral

    positive_per = round(((positive / total_per) * 100), 2)
    negative_per = round(((negative / total_per) * 100), 2)
    neutral_per = round(((neutral / total_per) * 100), 2)

    mean_total = positive + negative

    positive_mean = round(((positive / mean_total) * 100), 2)
    negative_mean = round(((negative / mean_total) * 100), 2)

    sentiment = ''

    if abs(positive_mean - negative_mean) < 5.0:
        sentiment = 'Controversial'
    elif positive_mean - negative_mean:
        sentiment = 'Positive'
    else:
        sentiment = 'negative'

    return jsonify({
        'sentiment': sentiment,
        'count': {
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'total': total_per
        },
        'mean': {
            'positive': positive_mean,
            'negative': negative_mean
        },
        'results': {
            'positive': positive_per,
            'negative': negative_per,
            'neutral': neutral_per
        },
        'biggest_tweet': biggest_tweet
    })
