import uvicorn
from fastapi import FastAPI,Request
from model import ner_main

app = FastAPI(
    title = "NLP API",
    description = "NLP API for Named Entity Recognition and Text Classification"
    )

@ app.post('/ner_spacy_trf')
def ner_spacy_trf_text(text: str):
    output_spacy = list(ner_main.ner_spacy_trf(text))
    result = output_spacy
    return result

@ app.post('/ner_spacy_sm')
def ner_spacy_sm_text(text: str):
    output_spacy = list(ner_main.ner_spacy_sm(text))
    result = output_spacy
    return result

@ app.post('/ner_spacy_md')
def ner_spacy_md_text(text: str):
    output_spacy = list(ner_main.ner_spacy_md(text))
    result = output_spacy
    return result

@ app.post('/ner_spacy_lg')
def ner_spacy_lg_text(text: str):
    output_spacy = list(ner_main.ner_spacy_lg(text))
    result = output_spacy
    return result

@ app.post('/textcat_bart_lg')
def textcat_bart_lg_text(text: str):
    output_bart = list(ner_main.textcat_bart_lg(text))
    result = output_bart
    return result


@ app.post('/textcat_fewshot')
def textcat_fewshot_text(text: str):
    output_fewshot = list(ner_main.textcat_fewshot(text))
    result = output_fewshot
    return result
