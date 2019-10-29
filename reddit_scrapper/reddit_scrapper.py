from psaw import PushshiftAPI
import datetime as dt

api = PushshiftAPI()

gen = api.search_submissions(
    after=start_epoch,
    subreddit='jetblue',
    limit=1000)

results = list(gen)

with open('reddit_reviews.csv','w') as output_csv:
    for result in results:
        print(result.title)
        print(result.selftext)
        print(result.author)
        print(result.created)
        print(result.url)
        print(result.score)
