from SentimentAnalyzer import SentimentAnalyzer
from BigQuery import BigQuery

import datetime, math, os, re, sys
import tweepy

class TwitterScraper(object):
    def __init__(self):
        consumer_key = os.environ.get("twitter_api_key")
        consumer_secret = os.environ.get("twitter_api_secret_key")
        access_token = os.environ.get("twitter_access_token")
        access_secret = os.environ.get("twitter_access_token_secret")
        self.analyzer = SentimentAnalyzer()
        self.tweets = []
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_secret)
            self.api = tweepy.API(self.auth)
            self.bigquery = BigQuery("twitter", "messages")
        except Exception as e:
            print("Error Authenticating: {}".format(str(e)))
            sys.exit(1)
    
    def clean_text(self, text):
        return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    
    def write_tweets(self, query):
        try:
            iterations = 0
            max_id = 0
            while iterations < 150:
                print("Iteration: {}".format(iterations))
                # current_date = datetime.date.today().strftime("%Y-%m-%d")
                # last_five_days = (datetime.date.today() - datetime.timedelta(days = 5)).strftime("%Y-%m-%d")
                if iterations > 0:
                    tickets = tweepy.Cursor(
                        self.api.search,
                        q = query,
                        max_id = max_id
                    ).items(100)
                else:
                    tickets = tweepy.Cursor(
                        self.api.search,
                        q = query
                    ).items(100)
                rows = []
                for i, x in enumerate(tickets):
                    if i == 0:
                        max_id = x._json["id"]
                    cleanText = self.clean_text(x._json["text"])
                    location = x._json["user"]["location"] if x._json["user"]["location"] is not None else 'Null'
                    createDatetime = x._json["created_at"].split(" ")
                    createDatetime = datetime.datetime.strptime(" ".join([createDatetime[i] for i in [1, 2, 5, 3]]), "%b %d %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    r = (
                        x._json["user"]["id"],
                        True,
                        createDatetime,
                        cleanText,
                        self.analyzer.get_sentiment(cleanText),
                        x._json["user"]["friends_count"],
                        x._json["user"]["followers_count"],
                        location
                    )
                    rows += [r]
                iterations += 1
                self.bigquery.write_to_bigquery(rows)
                self.bigquery.write_to_bigquery(rows)
                self.bigquery.write_to_bigquery(rows)
                self.bigquery.write_to_bigquery(rows)
        except Exception as e:
            print("Error Searching Tweets: {}".format(str(e)))
            sys.exit(1)
    
    def weight(self, days):
        if days < 0:
            return 0
        return math.exp(-(2.0/365)*days)
    
    def get_create_date(self, tweet):
        create_date = tweet["created_at"].split(" ")
        return datetime.datetime.strptime(" ".join([create_date[i] for i in [1, 2, 5]]), "%b %d %Y").date()
    
    def get_time_weighted_sentiments(self):
        idx = 0
        moving_ave = []
        while idx < 365:
            end_date = datetime.date.today() - datetime.timedelta(days = idx)
            weights = [self.weight((end_date - self.get_create_date(t)).days) for t in self.tweets]
            exp_ave = sum([weights[i] * self.tweets[i]["sentiment"] for i in range(len(weights))]) / max(0.1, sum(weights))
            moving_ave.append(exp_ave)
            idx += 1
        return moving_ave