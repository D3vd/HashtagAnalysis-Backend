from textblob import TextBlob
import nltk

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


def get_word_count(tweets, query):

    raw_text = ''

    for tweet in tweets:
        cleaned_tweet = clean_tweet(tweet['text'])
        raw_text += cleaned_tweet.lower()

    stop = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own',
            'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 'amp']

    words = nltk.word_tokenize(raw_text)
    stopwordsfree_words = [word for word in words if word not in stop]

    counter = Counter(stopwordsfree_words)

    most_occur = counter.most_common(15)

    most_occur_list = []

    for word in most_occur:

        if word[0] == query:
            continue

        temp = {}
        temp['word'] = word[0]
        temp['count'] = word[1]

        most_occur_list.append(temp)

    return most_occur_list
