from flask import Flask, jsonify, redirect
from flask_cors import CORS, cross_origin
import os

from TwitterClient import TwitterClient
from SentimentAnalysis import get_sentiment

from tweepy.error import TweepError

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return redirect('https://hashtaganalysis.netlify.com')


@app.route('/api/<query>')
@cross_origin()
def api(query):

    query_limit = int(os.getenv('QUERY_LIMIT'))

    api = TwitterClient()

    try:
        tweets = api.get_tweets(query, query_limit)

    except TweepError as e:
        return jsonify({
            "status_code": 429,
            "message": "Too many requests. Try again later"
        })

    if len(tweets) == 0:
        return jsonify({
            "status_code": 400,
            "message": "Not a valid query"
        })

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

    if abs(positive_mean - negative_mean) < 10.0:
        sentiment = 'Controversial'
    elif positive_mean > negative_mean:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'

    INDIA_WOE_ID = 23424848
    trending = api.get_trending(INDIA_WOE_ID)

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
        'biggest_tweet': biggest_tweet,
        'status_code': 200,
        'message': 'Request Successful!',
        'trending': trending[:10]
    })
