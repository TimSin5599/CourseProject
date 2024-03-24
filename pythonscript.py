from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import sys

from extractingAttributes import (
    build_path,
    open_file,
    get_name,
    get_organization,
    get_email,
    get_phone_number,
    get_attributes_from_model)

def get_text_from_array(array):
    text = ""
    for i in range(len(array)):
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
    pdf.add_font("AcromRegular", style="", fname=sys.argv[0].split("pythonscript.py")[0] + 'AcromRegular.ttf', uni=True)
    pdf.set_font('AcromRegular', '', 18)
    pdf.multi_cell(0,5,'Ключевые данные из резюме:\n\n')
    pdf.set_font('AcromRegular', '', 12)
    pdf.multi_cell(0,5, text)
    pdf.output(path)

if __name__ == '__main__':
    path_ = build_path()
    text_ = open_file(path_)

    skills, edu, org, languages, self_summary, speciality, faculty = get_attributes_from_model(text_)
    text = ""
    text += get_name(text_) + "\n"
    text += "Номер телефона: " + get_phone_number(text_) + "\n"
    text += "Email: " + get_email(text_) + "\n"
    text += "Образовательные учреждения: " + "\n" + get_text_from_array(edu) + "\n"
    text += "Факультеты: " + get_text_from_array(faculty) + "\n"
    text += "Специальности: " + get_text_from_array(speciality) + "\n"
    text += "Организации: " + "\n" + get_text_from_array(org) + "\n"
    text += "Языки: " + get_text_from_array(languages) + "\n"
    text += "Навыки: " + "\n" + get_text_from_array(skills) + "\n"
    text += "Личная информация: " + "\n" + get_text_from_array(self_summary) + "\n"

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
