import sys
import tkinter as tk
from tkinter import messagebox
from docx import Document
import spacy
import re
import fitz
from spacy.matcher import Matcher


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
        return text
    elif extension == "pdf":
        with fitz.open(path) as pdf_doc:
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                text += page.get_text()
        return text
    elif extension == "docx":
        doc = Document(path)

        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Данный формат файлов не поддерживается")

        root.destroy()
        root.quit()
        exit(0)


def get_phone_number(text):
    phones = re.findall(r"(?:(?:8|\+7)[\- ]?)?(?:\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", text)
    if len(phones) == 0:
        return ""
    return phones[0]


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
        elif matches[i][0] == matches[i-1][0]:
            span = nlp_text[start:end]
            break
        else:
            break
    if span is not None:
        return span.text
    else:
        return ""

def get_experience(text):
    return ""


if __name__ == '__main__':
    nlp = spacy.load("ru_core_news_sm")

    path_ = build_path()
    text_ = open_file(path_)

    print("FIO - ", get_name(text_))
    print("Phone number - ", get_phone_number(text_))
    print("Email - ", get_email(text_))
    print("Experience - ")
