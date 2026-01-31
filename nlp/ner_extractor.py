import spacy
from spacy.cli import download

MODEL = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL)
except:
    download(MODEL)
    nlp = spacy.load(MODEL)


def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
