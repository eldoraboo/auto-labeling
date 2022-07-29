import spacy
import classy_classification
from itertools import groupby
from transformers import pipeline
from pathlib import Path

nlp_trf = spacy.load("en_core_web_trf")
nlp_sm = spacy.load("en_core_web_sm")
nlp_md = spacy.load("en_core_web_md")
nlp_lg = spacy.load("en_core_web_lg")
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
nlp_fs = spacy.load(Path('model/model/'))


candidate_labels = ['Chemicals', 'Construction Materials', 'Containers and Packaging', 'Metals and Mining', 'Paper and Forest Products']

def doc_to_spans(doc):
    tokens = [(tok.text, tok.idx, tok.ent_type_) for tok in doc]
    results = []
    entities = set()
    for entity, group in groupby(tokens, key=lambda t: t[-1]):
        if not entity:
            continue
        group = list(group)
        _, start, _ = group[0]
        word, last, _ = group[-1]
        text = ' '.join(item[0] for item in group)
        end = last + len(word)
        results.append({"label": entity, "start_offset": start, "end_offset": end})
        entities.add(entity)
    return results, entities

# ==================Spacy====================#

def ner_spacy_trf(text):
    doc1 = nlp_trf(text)
    spans, ents = doc_to_spans(doc1)
    return spans

def ner_spacy_sm(text):
    doc1 = nlp_sm(text)
    spans, ents = doc_to_spans(doc1)
    return spans

def ner_spacy_md(text):
    doc1 = nlp_md(text)
    spans, ents = doc_to_spans(doc1)
    return spans
        
def ner_spacy_lg(text):
    doc1 = nlp_lg(text)
    spans, ents = doc_to_spans(doc1)
    return spans

def textcat_bart_lg(text):
    classified = classifier(text, candidate_labels)
    label = classified['labels'][0]
    return [{ "label": label }]

def textcat_fewshot(text):
    categories = nlp_fs(text)._.cats
    max_category = max(categories, key=categories.get)
    return [{ "label": max_category }]
