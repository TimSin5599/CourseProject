import sys
import tkinter as tk
from tkinter import messagebox

import fitz
from docx import Document
import spacy
import re
from spacy.matcher import Matcher
from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, Doc, NewsNERTagger

nlp = spacy.load("ru_core_news_lg")
pathModel = sys.argv[0].split("pythonscript.py")[0] + "ModelNER\\output\\model-best"
nlp_model = spacy.load(pathModel)

def build_path():
    length = len(sys.argv)
    if length == 0:
        return ""

    path = ""
    for i in range(1, length - 1):
        path += sys.argv[i] + " "
    path += sys.argv[length - 1]
    return path


def open_file(path):
    text = ""
    extension = path.split('.')[-1]

    if extension == "txt":
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.replace("\n", " ")
        return text
    elif extension == "pdf":
        with fitz.open(path) as pdf_doc:
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                text += page.get_text().replace("\n", " ")
        return text
    elif extension == "docx":
        doc = Document(path)

        for paragraph in doc.paragraphs:
            text += paragraph.text.replace("\n", " ")
        return text
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Данный формат файлов не поддерживается")

        root.destroy()
        root.quit()
        exit(0)


def get_phone_number(text):
    phones = re.findall(r"(?:(?:8|\+7)[\-\s]?)?(?:\(?\d{3}\)?[\-\s]?)?[\d\-\s]{7,10}", text)
    if len(phones) == 0:
        return ""
    text_ = str(phones[0])
    text_ = text_[::-1].replace(" ", "", 1)[::-1]
    text_ = text_.replace(" ", "-")
    # text_ = text_.replace("\t", "-")
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
    nlp_text = nlp(text)
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN', 'OP': '?'}]
    matcher.add('NAME', [pattern])
    matches = matcher(nlp_text)

    span = None
    for i in range(len(matches)):
        match, start, end = matches[i]
        if span is None:
            span = nlp_text[start:end]
        elif matches[i][0] == matches[i-1][0] and matches[i-1][1] == matches[i][1]:
            span = nlp_text[start:end]
            break
        else:
            break
    if span is not None:
        return span.text
    else:
        return ""

def get_organization(text):
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    organization = [i.text for i in doc.spans if i.type == "ORG"]
    return organization

def get_attributes_from_model(text):
    doc = nlp_model(text)
    skills = []
    edu = []
    org = []
    languages = []
    self_summary = []
    speciality = []
    faculty = []

    for ents in doc.ents:
        if ents.label_ == "SKILLS":
            skills.append(ents.text)
        elif ents.label_ == "EDU":
            edu.append(ents.text)
        elif ents.label_ == "ORG":
            org.append(ents.text)
        elif ents.label_ == "LANGUAGES":
            languages.append(ents.text)
        elif ents.label_ == "SELF_SUMMARY":
            self_summary.append(ents.text)
        elif ents.label_ == "SPECIALITY":
            speciality.append(ents.text)
        elif ents.label_ == "FACULTY":
            faculty.append(ents.text)

    return skills, edu, org, languages, self_summary, speciality, faculty