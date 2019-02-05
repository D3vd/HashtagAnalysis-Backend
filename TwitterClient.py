import tweepy
from tweepy import OAuthHandler

import os


class TwitterClient():

    def __init__(self):

        try:

            consumer_key = os.getenv('API_KEY')
            consumer_secret = os.getenv('API_SECRET_KEY')
            access_token = os.getenv('ACCESS_TOKEN')
            access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

            try:
                self.auth = OAuthHandler(consumer_key, consumer_secret)
                self.auth.set_access_token(access_token, access_token_secret)

                self.api = tweepy.API(self.auth)

            except:
                print("Error: Authentication Failed")

        except:
            print("Error: Unable to retrieve API keys")

    def get_tweets(self, query, count):

        tweets = []

        fetched_tweets = [status for status in tweepy.Cursor(
            self.api.search, q=query, tweet_mode="extended", lang='en').items(count)]

        for tweet in fetched_tweets:

            parsed_tweet = {}

            parsed_tweet['text'] = tweet._json['full_text']
            parsed_tweet['retweet_count'] = tweet._json['retweet_count']
            parsed_tweet['favorite_count'] = tweet._json['favorite_count']

            tweets.append(parsed_tweet)

        return tweets
