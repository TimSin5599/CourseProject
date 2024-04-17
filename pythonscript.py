import os
import sys
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from docx import Document
from PIL import Image
import fitz

from extractingAttributes import (
    open_file,
    get_name,
    get_experience,
    get_email,
    get_phone_number,
    get_salary,
    get_attributes_from_model)

path_ = sys.argv[1]
pathDir = sys.argv[0].split("pythonscript.py")[0]
pathFont = pathDir + 'fonts\\AcromRegular.ttf'

def get_text_from_array(array):
    text = ""

    for i in range(len(array)):
        if i == 0:
            word = array[i].split(" ")[0]
            word = word.title()
            array[i] = array[i].replace(array[i].split(" ")[0], word)
        if i == len(array) - 1:
            text += array[i]
            break
        text += array[i] + ", "

    if len(array) == 0:
        text = "-"
    return text

def createPDF(text, path):
    text.replace('\n','<br />\n')
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.add_font("AcromRegular", style="", fname=pathFont, uni=True)
    pdf.set_font('AcromRegular', '', 18)


    if path_.split(".")[-1] == "pdf":
        doc = fitz.open(path_)
        check = False
        for i in range(len(doc)):
            for img in doc.get_page_images(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                if (pix1.w >= 100 and pix1.h >= 100):
                    weight = pix1.w
                    height = pix1.h
                    while (weight > 75 or height > 75):
                        weight = weight * 0.8
                        height = height * 0.8
                    pix1.save(pathDir + "image.png")
                    pdf.image(pathDir + "image.png", w=weight, h=height)
                    os.remove(pathDir + "image.png")
                    check = True
                    break
            if check:
                break
    elif path_.split(".")[-1] == "docx":
        doc = Document(path_)

        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                image = rel.target_part.blob
                with open(pathDir + "image.png", "wb") as image_file:
                    image_file.write(image)
                image = Image.open(pathDir+"image.png")
                if (image.width >= 100 and image.height >= 100):
                    weight = image.width
                    height = image.height
                    while (weight > 75 or height > 75):
                        weight = weight * 0.8
                        height = height * 0.8
                    image.save(pathDir + "image.png")
                    pdf.image(pathDir + "image.png", w=weight, h=height)
                    os.remove(pathDir + "image.png")
                    break

    pdf.multi_cell(0,5,'\nКлючевые данные из резюме:\n\n')
    pdf.set_font('AcromRegular', '', 12)
    pdf.multi_cell(0,5, text)
    pdf.output(path)

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Статус", "Файл с извлеченными данными успешно создан")
    root.destroy()
    root.quit()

if __name__ == '__main__':
    text_ = open_file(path_)
    dictionary = get_attributes_from_model(text_)

    person = get_name(text_)
    text = ""
    text += "ФИО: " + person + "\n"
    text += "Дата рождения: " + get_text_from_array(list(dictionary["DATA"])) + "\n"
    text += "Номер телефона: " + get_phone_number(text_) + "\n"
    text += "Email: " + get_email(text_) + "\n"
    text += "Адрес: " + get_text_from_array(list(dictionary["ADR"])) + "\n"
    text += "Желаемая зарплата: " + get_salary(text_) + "\n"
    text += "Образование: " + get_text_from_array(list(dictionary["DEGREE"])) + "\n"
    text += "Образовательные учреждения: " + "\n" + get_text_from_array(list(dictionary["EDU"])) + "\n"
    text += "Факультеты: " + get_text_from_array(list(dictionary["FACULTY"])) + "\n"
    text += "Специальности: " + get_text_from_array(list(dictionary["SPECIALTY"])) + "\n"
    text += "Организации: " + "\n" + get_text_from_array(list(dictionary["ORG"])) + "\n"
    text += "Опыт работы: " + "\n" + get_experience(text_) + "\n"
    text += "Языки: " + get_text_from_array(list(dictionary["LANGUAGES"])) + "\n"
    text += "Ключевые навыки: " + "\n" + get_text_from_array(list(dictionary["SKILLS"])) + "\n"
    text += "Личная информация: " + "\n" + get_text_from_array(list(dictionary["SELF_SUMMARY"])) + "\n"

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Сохранение файла", "Пожалуйста, сохраните файл в нужную вам директорию")
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("pdf files", "*.pdf"), ("All files", "*.*")])
    root.destroy()
    root.quit()

    if file_path:
        createPDF(text, file_path)
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Не удалось сохранить файл")
        root.destroy()
        root.quit()
