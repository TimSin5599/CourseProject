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
    phones = re.search(r"(?:(?:8|\+7|7)[\-\s]?)+(?:\(?\d{3}\)?[\-\s]?)+[\d\-\s]{7,10}", text)
    if phones is None:
        return "-"
    text_ = phones.group()
    text_ = re.sub("[^\d\+\(\)]+", " ", text_)
    return text_

def get_experience(text):
    match = re.search(r'Опыт\s*работы[^\d\w]*([\u0401\u0451\u0410-\u044f\d]+\s+'
                       r'[\u0401\u0451\u0410-\u044f\d]+\s+[\u0401\u0451\u0410-\u044f\d]+\s+[\u0401\u0451\u0410-\u044f\d]+)', text)
    if match is not None:
        return match.group()
    return "-"

def get_salary(text):
    match = re.search(r'[\d{1,} ]{2,}(руб|\$|\₽|\€)\.?', text)

    if match is not None:
        return match.group()
    return "-"

def get_email(text):
    emails = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if emails is None:
        return "-"
    return emails.group()

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

    if len(name) == 0:
        name = "-"

    name = re.sub("[^\w\.]+", " ", name)
    name = re.sub("(\B \B|\B | \B)+", "", name)

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
        "PER": set(),
        "DEGREE": set()
    }

    for ent in doc.ents:
        ent_text = re.sub("[^\w\.]+", " ", ent.text)
        ent_text = re.sub("(\B \B|\B | \B)+", "", ent_text)
        ent_text = ent_text.lower()

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
            if len(ent_text.split(" ")) >= 3 and len(dictionary["DATA"]) == 0:
                dictionary["DATA"].add(ent_text.lower())
        elif ent.label_ == "PER":
            dictionary["PER"].add(ent_text)

    enum = {"Среднее", "Высшее", "Магистр", "Бакалавр", "Аспирант",
            "Бакалавриат", "Магистратура", "Аспирантура"}

    for i in dictionary["EDU"]:
        for j in enum:
            i_text = i.lower()
            j_text = j.lower()
            if j_text in i_text:
                dictionary["DEGREE"].add(i)
                break

    for i in dictionary["DEGREE"]:
        dictionary["EDU"].remove(i)

    return dictionary