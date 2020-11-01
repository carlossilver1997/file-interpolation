from utils.util import calculateAge
import os

def read_and_interpolate_file(route, person, ext):
    try:
        with open(route) as f:
            content = f.read()
            content = content.replace("[NAME]", person["givenNames"].title()).replace("[LAST_NAME_1]", person["lastName1"].title()).replace("[LAST_NAME_2]", person["lastName2"].title()).replace("[COMPANY]", person["company"].title()).replace("[POSITION]", person["position"].upper()).replace("[BIRTH_DATE]", person["birthDate"]).replace("[PHONE]", person["phoneNumber"]).replace("[EMAIL]", person["email"]).replace("[ADDRESS]", person["address"].title()).replace("[AGE]", str(calculateAge(person["birthDate"])))
            print(content)
        if ext is 'pdf':
            pass
        if ext is 'word':
            pass
        cwd = os.getcwd()  # Get the current working directory (cwd)
        with open('{}/static/{}.txt'.format(cwd,person["id"]), 'w') as file:
            file.write(content)

    except FileNotFoundError as fne:
        raise fne
    except FileExistsError as fee:
        raise fne