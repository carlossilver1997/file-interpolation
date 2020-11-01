from datetime import date
import smtplib

def calculateAge(birthDate):
    dia, mes, anio = [int(v) for v in birthDate.split("/")] 
    born = date(anio, mes, dia)
    hoy = date.today()    
    try:
       cumpleanios = born.replace(year=hoy.year) 
    except ValueError: 
       cumpleanios = born.replace(year=hoy.year, day=born.day - 1) 
    if cumpleanios > hoy:          
       return hoy.year - born.year - 1 
    else: 
       return hoy.year - born.year 