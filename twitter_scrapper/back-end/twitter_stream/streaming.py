import json, os, re, sys
import tweepy

from textblob import TextBlob
from google.cloud import bigquery

class SentimentAnalyzer(object):
    def __init__(self):
        pass
    
    def get_sentiment(self, text):
        return TextBlob(text).sentiment.polarity

class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.client = bigquery.Client(project = "smart-inn-257104")
        self.table = self.client.get_table(self.client.dataset("twitter").table("messages"))
    
    def clean_text(self, text):
        return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

    def on_data(self, tweet):
        tweet = json.loads(tweet)
        message = self.clean_text(tweet["text"])
        sentiment = self.analyzer.get_sentiment(message)
        location = tweet["user"]["location"] if tweet["user"]["location"] is not None else 'Null'
        row = [ (
            tweet["id_str"],
            True,
            tweet["created_at"],
            message,
            sentiment,
            tweet["user"]["friends_count"],
            tweet["user"]["followers_count"],
            location
        ) ]
        self.client.insert_rows(self.table, row)

    def on_status(self, status):
        status = json.loads(status)
        message = self.clean_text(status["text"])
        sentiment = self.analyzer.get_sentiment(message)
        location = status["user"]["location"] if status["user"]["location"] is not None else 'Null'
        row = [ (
            status["id_str"],
            True,
            status["created_at"],
            message,
            sentiment,
            status["user"]["friends_count"],
            status["user"]["followers_count"],
            location
        ) ]
        self.client.insert_rows(self.table, row)
    
    def on_error(self, status_code):
        print(status_code)

class TwitterStream(object):
    def __init__(self):
        consumer_key = os.environ.get("twitter_api_key")
        consumer_secret = os.environ.get("twitter_api_secret_key")
        access_token = os.environ.get("twitter_access_token")
        access_secret = os.environ.get("twitter_access_token_secret")
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_secret)
            self.api = tweepy.API(self.auth)
        except Exception as e:
            print("Error Authenticating: {}".format(str(e)))
            sys.exit(1)
        streamListener = MyStreamListener()
        self.stream = tweepy.Stream(auth = self.api.auth, listener = streamListener)
    
    def run(self):
        self.stream.filter(track=['JetBlue'])

twitter_stream = TwitterStream()
print("Twitter streaming service is running.")
twitter_stream.run()