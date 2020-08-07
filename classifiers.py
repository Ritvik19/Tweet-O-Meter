from nlp_toolkit import *
import json, pickle

vectorizer_spam = pickle.load(open('Vectorizer-spam.pkl', 'rb'))
classifier_spam = pickle.load(open('SpamClassifier.pkl', 'rb'))

def classify_spam(text):
    text = [cleanText(str(text))]
    vector = vectorizer_spam.transform(text)
    return classifier_spam.predict(vector)[0]

association_rules = json.load(open('association-rules.json'))

def classify_tag(query, category=None):
    query = cleanText(str(query))
    if category is not None:
        if category in association_rules.keys():
            for kw in association_rules[category]:
                if kw in query:
                    return 1
            return 0
        return None
    tags = []
    for cat in association_rules.keys():
        for kw in association_rules[cat]:
            if kw in query.split():
                tags.append(cat)
                break
    return tags
