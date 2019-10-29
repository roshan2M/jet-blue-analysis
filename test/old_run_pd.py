from nlp import nlp
import pandas as pd

df = pd.read_csv('sample_reviews.csv', delimiter=',')

for index, row  in df.iterrows():
    
    row = next(df.iterrows())[i]
    print(row)

test = nlp(sample_text)
test.analyze()

print(test.response)
for entity in test.entities:
    print(entity.name)
    print(entity.salience)