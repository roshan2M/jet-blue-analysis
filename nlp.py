from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.api_core.exceptions import InvalidArgument

SALIENCE_THRESHOLD = 0.0005

class nlp:
    def __init__(self, review_text):
        self.review_text =  review_text
        self.type_ = enums.Document.Type.PLAIN_TEXT 
        self.encoding_type = enums.EncodingType.UTF8
        self.entities = {
            'cost':[0,0], 
            'food': [0.0],
            'service': [0,0],
            'entertainment': [0,0] 
            }

        # language = "en"
        # document = {"content": review_text, "type": type_, "language": language}

        ''' 
        Creates the attributes releated to sentiment, context and syntax analysis thorugh
        google's nlp cloud service API. The attributes are
        - self.category
        - self.category_conf
        - self.language
        - self.sentiment
        - self.sentiment_magnitude
        - self.entities = []
        each entity in the array has the following 
        name, salience, sentiment.score, sentiment.magnitude        
        - self.adjs = []
        - self.advs = [] 
        '''

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

    def analyze_context(self, client):
        try:
            document = {"content": self.review_text, "type": self.type_}
            classify = client.classify_text(document)

            if (not self.language == "en"):
                self.category = None
                self.category_conf =  None

            # Loop through classified categories returned from the API
            for category in classify.categories:
                self.category = category.name
                self.category_conf = category.confidence 
        except InvalidArgument as e:
            pass

    def analyze_sentiment(self, client):
        # SENTIMENT ANALYSIS
        try:
            document = {"content": self.review_text, "type": self.type_}
            response = client.analyze_sentiment(document, encoding_type=self.encoding_type)

            # document language
            self.language = response.language
            # overall message sentiment
            self.sentiment = response.document_sentiment.score 
            # sentiment magnitude
            self.sentiment_magnitude = response.document_sentiment.magnitude
        
        except InvalidArgument as e:
            pass


    def analyze_entity_sentiment(self, client):
        # ENTITY SENTIMENT ANALSYS
        try:
            document = {"content": self.review_text, "type": self.type_}
            response = client.analyze_entity_sentiment(document, encoding_type=self.encoding_type)

            # Loop through entitites returned from the API
            for entity in response.entities:
                print("\n", entity)
                if (entity == "cost"):
                    self.entities['cost'] = [entity.salience, entity.sentiment.score]
                if (entity == "food"):
                    self.entities['food'] = [entity.salience, entity.sentiment.score]
                if (entity == "service"):
                    self.entities['service'] = [entity.salience, entity.sentiment.score]
                if (entity == "entertainment"):
                    self.entities['entertainment'] = [entity.salience, entity.sentiment.score]

                # if (entity.salience > SALIENCE_THRESHOLD):
                #     self.entities.append(entity)
        except InvalidArgument as e:
            pass

    def analyze_syntax(self, client):
        # SYNTAX ANALYSIS FOR ADJECTIVES
        try:
            document = {"content": self.review_text, "type": self.type_}
            response = client.analyze_syntax(document, encoding_type=self.encoding_type)

            self.adjs = []
            self.advs = []

            # Loop through tokens returned from the API
            for token in response.tokens:
                pos = token.part_of_speech
                pos_name = enums.PartOfSpeech.Tag(pos.tag).name
                text = token.text
                if (pos_name == "ADJ"):
                    self.adjs.append(text.content)
                if (pos_name == "ADV"):
                    self.advs.append(text.content)
        except InvalidArgument as e:
            pass