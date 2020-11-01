import os
import fpdf
from utils.util import calculateAge
from docx import Document
from docx.text.paragraph import Paragraph
import pandas as pd


def read_and_interpolate_file(route, person, ext):
    try:
        with open(route) as f:
            content = f.read()
            content = content.replace("[NAME]", person["givenNames"].title()).replace("[LAST_NAME_1]", person["lastName1"].title()).replace("[LAST_NAME_2]", person["lastName2"].title()).replace("[COMPANY]", person["company"].title()).replace("[POSITION]", person["position"].upper()).replace("[BIRTH_DATE]", person["birthDate"]).replace("[PHONE]", person["phoneNumber"]).replace("[EMAIL]", person["email"]).replace("[ADDRESS]", person["address"].title()).replace("[AGE]", str(calculateAge(person["birthDate"])))            
        cwd = os.getcwd()
        lines = content.split('\n')
        if ext == 'pdf':
            pdf = fpdf.FPDF(format='letter') #pdf format
            pdf.add_page() #create new page
            pdf.set_font("Arial", size=12) # font and textsize
            for index, line in enumerate(lines):
                pdf.cell(200, 10, txt=line, ln=(index+1), align='L')
            pdf.output("{}/static/{}.{}".format(cwd,person["id"],ext))
            return
        if ext == 'docx':
            document = Document()
            for index, line in enumerate(lines):
                if index == 0:
                    document.add_heading(line, 0)
                else:
                    document.add_paragraph(line)
            document.save("{}/static/{}.{}".format(cwd,person["id"],ext))
            return
        with open('{}/static/{}.txt'.format(cwd,person["id"]), 'w') as file:
            file.write(content)

    except FileNotFoundError as fne:
        raise fne
    except FileExistsError as fee:
        raise fne