import sys
import tkinter as tk
from tkinter import messagebox

import fitz
from docx import Document
import spacy
import re
from natasha import (
    Doc,
    Segmenter,
    MorphVocab,
    NamesExtractor,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER
)


pathModel = sys.argv[0].split("\\pythonscript.py")[0]
nlp_model = spacy.load(pathModel + "\\ModelNER\\output\\model-best")
nlp = spacy.load("ru_core_news_lg")

def open_file(path):
    text = ""
    extension = path.split('.')[-1]

    if extension == "txt":
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
    elif extension == "pdf":
        with fitz.open(path) as pdf_doc:
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                text += page.get_text() + " "
    elif extension == "docx":
        doc = Document(path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + " "
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Данный формат файлов не поддерживается")

        root.destroy()
        root.quit()
        exit(0)

    return text


def get_phone_number(text):
    phones = re.findall(r"(?:(?:8|\+7|7)[\-\s]?)+(?:\(?\d{3}\)?[\-\s]?)+[\d\-\s]{7,10}", text)
    if len(phones) == 0:
        return ""
    text_ = str(phones[0])
    text_ = text_[::-1].replace(" ", "", 1)[::-1]
    text_ = text_.replace(" ", "-")
    text_ = text_.replace("\n", " ")
    return text_

def get_experience(text):
    match = re.findall(r'Опыт\s*работы[^\d\w]*([\u0401\u0451\u0410-\u044f\d]+\s+'
                       r'[\u0401\u0451\u0410-\u044f\d]+\s+[\u0401\u0451\u0410-\u044f\d]+\s+[\u0401\u0451\u0410-\u044f\d]+)', text)
    if len(match) != 0:
        return match
    return ""

def get_email(text):
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if len(emails) == 0:
        return ""
    return emails[0]


def get_name(text):
    emb = NewsEmbedding()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()

    names_extractor = NamesExtractor(morph_vocab)
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)

    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)

    name = ""
    for i in doc.spans:
        if i.fact:
            obj = i.fact.as_dict
            if ('first' in obj and
                    'last' in obj and
                        'middle' in obj):
                name = i.text
                break
            elif (len(name) == 0 and
                'first' in obj and
                 'last' in obj):
                name = i.text
    return name
def get_attributes_from_model(text):
    doc = nlp_model(text)
    dictionary = {
        "SKILLS": set(),
        "EDU": set(),
        "ORG": set(),
        "LANGUAGES": set(),
        "SELF_SUMMARY": set(),
        "SPECIALTY": set(),
        "FACULTY": set(),
        "ADR": set(),
        "DATA": set(),
        "PER": set()
    }

    for ent in doc.ents:
        ent_text = re.sub("[^\w\.]+", " ", ent.text)
        ent_text = re.sub("(\B \B|\B | \B)+", "", ent_text)
        # print(ent.text, ent.label_, ent_text)
        if ent.label_ == "SKILLS":
            dictionary["SKILLS"].add(ent_text.lower())
        elif ent.label_ == "EDU":
            dictionary["EDU"].add(ent_text)
        elif ent.label_ == "ORG":
            dictionary["ORG"].add(ent_text)
        elif ent.label_ == "LANGUAGES":
            dictionary["LANGUAGES"].add(ent_text.lower())
        elif ent.label_ == "SELF_SUMMARY":
            dictionary["SELF_SUMMARY"].add(ent_text.lower())
        elif ent.label_ == "SPECIALTY":
            dictionary["SPECIALTY"].add(ent_text.lower())
        elif ent.label_ == "FACULTY":
            dictionary["FACULTY"].add(ent_text)
        elif ent.label_ == "ADR":
            dictionary["ADR"].add(ent_text)
        elif ent.label_ == "DATA":
            dictionary["DATA"].add(ent_text.lower())
        elif ent.label_ == "PER":
            dictionary["PER"].add(ent_text)

    return dictionary