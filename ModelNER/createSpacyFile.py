import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.load("ru_core_news_lg")
with open("ModelNER/test_train_data.json", "r", encoding="utf-8") as file:
    training_data = json.load(file)

db = DocBin()

for text, annotation in training_data["annotations"]:
    doc = nlp(text)
    ents = []
    for start, end, label in annotation["entities"]:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

db.to_disk("./dev.spacy")
