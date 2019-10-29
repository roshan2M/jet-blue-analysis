import tweepy
from datetime import datetime
from google.cloud import bigquery
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.api_core.exceptions import InvalidArgument
from nlp import nlp
import os

# apis and connectors
bigquery_client = bigquery.Client()
nlp_client = language_v1.LanguageServiceClient()

# bigquery 
dataset_id = 'jetblue'
table_id = 'reviews'
table_ref = bigquery_client.dataset(dataset_id).table(table_id)
table = bigquery_client.get_table(table_ref)


# twitter shit
ckey = os.environ.get("twitter_api_key")
csecret = os.environ.get("twitter_api_secret_key")
atoken = os.environ.get("twitter_access_token")
asecret = os.environ.get("twitter_access_token_secret")

OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,
 'access_token_key':atoken, 'access_token_secret':asecret}
 
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])

api = tweepy.API(auth)

cricTweet = tweepy.Cursor(api.search, q='jetblue -filter:retweets').items(69)

ROWS_TO_INSERT = []

counter = 1
for tweet in cricTweet:

    print("## Processing tweet#{}".format(counter))

    if (tweet.place is None):
        place = ""
    else:
        place = tweet.place.country
    
    # running nlp
    review = nlp(tweet.text)
    review.analyze_sentiment(nlp_client)
    review.analyze_entity_sentiment(nlp_client)
    review.analyze_syntax(nlp_client)
    review.analyze_context(nlp_client)


    new_row = {
        'review_title': tweet.text, 
        'source': 'twitter',
        'date_created': datetime.date(tweet.created_at),
        'author': tweet.user.id,
        'likes': tweet.favorite_count,
        'location': place,
        'sentiment': review.sentiment,
        'sentiment_magnitude': review.sentiment_magnitude,
        'adjectives': str(review.adjs),
        'adverbs': str(review.advs),
        # 'entity_1_salience': review.entities['cost'][0],
        # 'entity_1_sentiment': review.entities['cost'][1],
        # 'entity_2_salience': review.entities['food'][0],
        # 'entity_2_sentiment': review.entities['food'][1],
        # 'entity_3_salience': review.entities['service'][0],
        # 'entity_3_sentiment': review.entities['service'][1],
        # 'entity_4_salience': review.entities['entertainment'][0],
        # 'entity_4_sentiment': review.entities['entertainment'][1]
    }

    ROWS_TO_INSERT.append(new_row)
    print("Appended tweet #{}".format(counter))
    counter+=1


errors = bigquery_client.insert_rows(table, ROWS_TO_INSERT)

print(errors)
assert errors == []