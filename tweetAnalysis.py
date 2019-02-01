import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler

import re
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


if __name__ == '__main__':

    api = TwitterClient()
