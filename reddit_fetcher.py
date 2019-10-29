from psaw import PushshiftAPI
from datetime import date
from google.cloud import bigquery
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.api_core.exceptions import InvalidArgument
from nlp import nlp


# apis and connectors
api = PushshiftAPI()
bigquery_client = bigquery.Client()
nlp_client = language_v1.LanguageServiceClient()

# bigquery 
dataset_id = 'jetblue'
table_id = 'reviews_test'
table_ref = bigquery_client.dataset(dataset_id).table(table_id)
table = bigquery_client.get_table(table_ref)


# fetch reddit data
reddit_data_gen = api.search_submissions(
    subreddit='jetblue',
    filter=['title','selftext', 'created', 'author', 'score', 'url'],
    limit=1000)

reddit_gen = list(reddit_data_gen)

ROWS_TO_INSERT = []

counter = 1

for review in reddit_gen:
    
    print("## Processing review#{}".format(counter))

    review_title = review.title
    review_details = review.selftext
    author = review.author
    date_created = date.fromtimestamp(review.created)
    likes = int(review.score)
    url = review.url
    source = 'reddit'

    # nlp
    if (review_details == ''):
        review_text = review_title
    else:
        review_text = review_details
    
    print("review text: {}".format(review_text))

    review = nlp(review_text)
    review.analyze_sentiment(nlp_client)
    review.analyze_entity_sentiment(nlp_client)
    review.analyze_syntax(nlp_client)
    review.analyze_context(nlp_client)


    new_row = {
        'review_title': review_title, 
        'review_details': review_details,
        'source': source,
        'date_created': date_created,
        'author': author,
        'likes': likes,
        'url': url,
        'sentiment': review.sentiment,
        'sentiment_magnitude': review.sentiment_magnitude,
        'adjectives': str(review.adjs),
        'adverbs': str(review.advs),
        'entity_1_salience': review.entities['cost'][0],
        'entity_1_sentiment': review.entities['cost'][1],
        'entity_2_salience': review.entities['food'][0],
        'entity_2_sentiment': review.entities['food'][1],
        'entity_3_salience': review.entities['service'][0],
        'entity_3_sentiment': review.entities['service'][1],
        'entity_4_salience': review.entities['entertainment'][0],
        'entity_4_sentiment': review.entities['entertainment'][1]
    }

    ROWS_TO_INSERT.append(new_row)
    


    print("Appended review #{}".format(counter))
    counter+=1

    
errors = bigquery_client.insert_rows(table, ROWS_TO_INSERT)

print(errors)
assert errors == []