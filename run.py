from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud import translate_v3beta1 as translate
from nlp import nlp

def test_language_sentiment(input_file, client):
    with open('lang_sent.txt', 'w') as output_file:
        for line in input_file:
            line = line.strip("RT").strip()
            review = nlp(line)
            review.analyze_sentiment(client) 
            output = review.language + ',' + str(review.sentiment) + '\n'
            print(output)
            output_file.write(output)

def test_entity_sent(input_file, client):
    with open('entities.csv', 'w') as output_file:
        for line in input_file:
            line = line.strip("RT").strip()
            review = nlp(line)
            review.analyze_sentiment(client)
            # do entity analysis if only in 'en' 
            if ((review.language) and (review.language == "en")):
                print(review)
                print(review.language)
                review.analyze_entity_sentiment(client)
                for entity in review.entities:
                    output = entity.name + '\n'
                    print(output)
                    output_file.write(output)
            print(review)


# nlp client
nlp_client = language_v1.LanguageServiceClient()

input_file = open('sample_reviews.csv', 'r')
test_entity_sent(input_file, nlp_client)
input_file.close()
