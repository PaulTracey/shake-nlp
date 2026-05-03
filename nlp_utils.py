from collections import Counter
from pathlib import Path

from flask import abort
import spacy
from spacy.pipeline import EntityRuler


DATA_DIR = Path(__file__).parent / "data"


WORKS = {
    "hamlet": {
        "slug": "hamlet",
        "title": "Hamlet",
        "author": "William Shakespeare",
        "year": "c. 1600",
        "description": "A tragedy of grief, revenge, uncertainty, and political decay.",
        "source": "Public-domain excerpt for portfolio exploration.",
        "text_path": DATA_DIR / "hamlet.txt",
    }
}


def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        nlp = spacy.blank("en")
        nlp.add_pipe("sentencizer")
        ruler = nlp.add_pipe("entity_ruler")
        add_hamlet_entities(ruler)
        return nlp


def add_hamlet_entities(ruler: EntityRuler):
    names = [
        "Hamlet",
        "Claudius",
        "Gertrude",
        "Ophelia",
        "Polonius",
        "Laertes",
        "Horatio",
        "Denmark",
        "Elsinore",
        "King",
        "Queen",
    ]
    ruler.add_patterns([{"label": "HAMLET_TERM", "pattern": name} for name in names])


NLP = load_nlp()


def get_work(slug):
    work = WORKS.get(slug)
    if work is None:
        abort(404)

    text = work["text_path"].read_text(encoding="utf-8")
    return {**work, "text": text}


def parse(text):
    return NLP(text)


def word_frequencies(text, limit=25):
    doc = parse(text)
    words = [
        token.lemma_.lower() if token.lemma_ else token.text.lower()
        for token in doc
        if token.is_alpha and not token.is_stop and len(token.text) > 2
    ]
    return Counter(words).most_common(max(1, min(limit, 100)))


def get_named_entities(text):
    doc = parse(text)
    return [
        {"text": ent.text, "label": ent.label_, "sentence": ent.sent.text.strip()}
        for ent in doc.ents
    ]


def get_pos_counts(text):
    doc = parse(text)
    counts = Counter(token.pos_ or "UNKNOWN" for token in doc if token.is_alpha)
    return counts.most_common()


def search_work(text, query):
    if not query:
        return []

    doc = parse(text)
    query_lower = query.lower()
    matches = []

    for sent in doc.sents:
        sentence = sent.text.strip()
        if query_lower in sentence.lower():
            matches.append(sentence)

    return matches
