from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

import re

from collections import Counter


def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_sentiment(tweet):

    blob = TextBlob(clean_tweet(tweet))
    polarity = blob.sentiment.polarity

    if polarity > 0.0:
        return 1
    elif polarity < 0.0:
        return -1
    else:
        return 0


def get_word_count(tweets):

    raw_text = ''

    for tweet in tweets:
        cleaned_tweet = clean_tweet(tweet['text'])
        raw_text += cleaned_tweet.lower()

    stop = stopwords.words('english')

    words = nltk.word_tokenize(raw_text)
    stopwordsfree_words = [word for word in words if word not in stop]

    counter = Counter(stopwordsfree_words)

    most_occur = counter.most_common(20)

    most_occur_list = []

    for word in most_occur:
        temp = {}
        temp['word'] = word[0]
        temp['count'] = word[1]

        most_occur_list.append(temp)

    return most_occur_list
