from SentimentAnalyzer import SentimentAnalyzer
from TwitterScraper import TwitterScraper

import os, requests

FB_AUTH = "https://graph.facebook.com/oauth/access_token"

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
    tweets = scraper.write_tweets('JetBlue')