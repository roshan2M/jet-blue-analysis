from textblob import TextBlob

class SentimentAnalyzer(object):
    def __init__(self):
        pass
    
    def get_sentiment(self, text):
        return TextBlob(text).sentiment.polarity 