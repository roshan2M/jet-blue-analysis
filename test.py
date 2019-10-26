from SentimentAnalyzer import SentimentAnalyzer

import copy, datetime, json, math, os, re, requests, sys
import facebook, tweepy

FB_AUTH = "https://graph.facebook.com/oauth/access_token"

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
        except Exception as e:
            print("Error Authenticating: {}".format(str(e)))
            sys.exit(1)
    
    def clean_text(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    
    def get_tweets(self, query):
        try:
            tweets = tweepy.Cursor(self.api.search, q=query).items(200)
            for x in tweets:
                self.tweets.append({
                    "created_at": x._json["created_at"],
                    "text": x._json["text"],
                    "user": {
                        "id": x._json["user"]["id"],
                        "location": x._json["user"]["location"],
                        "followers_count": x._json["user"]["followers_count"],
                        "friends_count": x._json["user"]["friends_count"]
                    },
                    "geo": x._json["geo"],
                    "sentiment": self.analyzer.get_sentiment(self.clean_text(x._json["text"]))
                })
        except Exception as e:
            print("Error Searching Tweets: {}".format(str(e)))
            sys.exit(1)
        return self.tweets
    
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

def get_access_token():
    result = requests.get(FB_AUTH, params={"client_id": os.environ.get("app_id"), "client_secret": os.environ.get("app_secret"), "grant_type": "client_credentials"})
    access_token = result.json()["access_token"]
    access_type = result.json()["token_type"]
    return access_token, access_type

if __name__ == "__main__":
    # graph = facebook.GraphAPI(access_token = "EAAklsgB5SzYBANtf0c3gZBb89EJq6tsrRVj8OG8OxM5WungdztBkrIM9fMYKQ5CRSm3M5bIuyj7646LjgpYCjMx4tNkJpvWE40Al9SIaiTeLX97U2q7RT6bXqby3NyZClXUZCbZAZBItxecgmbdy3SG6jUDZAUkb3hGZCmZBqUMvpAZDZD")
    # page_ids = ["JetBlue"]
    # pages = graph.get_objects(page_ids, fields="created_time")
    # print(pages)
    # requests.get("https://graph.facebook.com/JetBlue", params={
    #     "access_token": ""
    # })
    scraper = TwitterScraper()
    tweets = scraper.get_tweets('JetBlue')
    # print([tweets[i]["created_at"] for i in range(len(tweets))])
    print(scraper.get_time_weighted_sentiments())