import sys
import tkinter as tk
from tkinter import messagebox
from docx import Document
# import spacy
import re
import fitz

path = ""
length = len(sys.argv)

"""Сборка пути файла"""
for i in range(1, length - 1):
    path += sys.argv[i] + " "
path += sys.argv[length - 1]

extension = path.split('.')[-1]
text = ''

"""Поиск формата файла"""
if extension == "txt":
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
elif extension == "pdf":
    with fitz.open(path) as pdf_doc:
        for page_num in range(pdf_doc.page_count):
            page = pdf_doc[page_num]
            text += page.get_text()
elif extension == "docx":
    doc = Document(path)

    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
else:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", "Данный формат файлов не поддерживается")

    root.destroy()
    root.quit()
    exit(0)

print(text)

print("email - ", re.findall(r'\S+@\S+', text))

# print(path + " " + extension)
