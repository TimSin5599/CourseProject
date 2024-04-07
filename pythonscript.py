import os
import sys
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import fitz

from extractingAttributes import (
    open_file,
    get_name,
    get_experience,
    get_email,
    get_phone_number,
    get_attributes_from_model)

path_ = sys.argv[1]
pathDir = sys.argv[0].split("pythonscript.py")[0]
pathFont = pathDir + 'fonts\\AcromRegular.ttf'

def get_text_from_array(array):
    text = ""

    for i in range(len(array)):
        if i == 0:
            array[i] = array[i].capitalize()
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

    doc = fitz.open(path_)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            if (pix1.w >= 200 and pix1.h >= 200):
                pix1.save(pathDir + "image.png")
                pdf.image(pathDir + "image.png", w=40, h=40)
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
    # print(text_)
    dictionary = get_attributes_from_model(text_)

    person = get_name(text_)
    text = ""
    text += "ФИО: " + person + "\n"
    text += "Дата рождения: " + get_text_from_array(list(dictionary["DATA"])) + "\n"
    text += "Номер телефона: " + get_phone_number(text_) + "\n"
    text += "Email: " + get_email(text_) + "\n"
    text += "Адрес: " + get_text_from_array(list(dictionary["ADR"])) + "\n"
    text += "Образовательные учреждения: " + "\n" + get_text_from_array(list(dictionary["EDU"])) + "\n"
    text += "Факультеты: " + get_text_from_array(list(dictionary["FACULTY"])) + "\n"
    text += "Специальности: " + get_text_from_array(list(dictionary["SPECIALTY"])) + "\n"
    text += "Организации: " + "\n" + get_text_from_array(list(dictionary["ORG"])) + "\n"
    text += "Опыт работы: " + "\n" + get_text_from_array(get_experience(text_)) + "\n"
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
