from textblob import TextBlob
import re


def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_sentiment(tweet):

    blob = TextBlob(clean_tweet(tweet))
    print(clean_tweet(tweet))
    polarity = blob.sentiment.polarity

    if polarity > 0.0:
        return 'positive'
    elif polarity < 0.0:
        return 'negative'
    else:
        return 'neutral'
