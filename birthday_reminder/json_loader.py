import json
import os

import re
from datetime import datetime


data = {'name': 'Larry',
    'website': 'pythonist.ru',
    'from': 'Michigan'}
# with open('data.json', 'w') as outfile:
#     json.dump(data, outfile)

with open("data.json", "r") as read_file:
    data = json.load(read_file)

print((data))
# today=datetime.datetime.today()
# today=today.strftime("%d/%m/%Y")

date_string = "24/07/2020"
date_object = datetime.strptime(date_string, "%d/%m/%Y")

year = date_object.year
print(year)
# today2=datetime.datetime.today()
# print(today2.year-today[5:])
# print(today[6:])
for key, value in data.items():
    if '24/07' in value:
        print(f"{key}: {value}")

def age_calculation(value):
    date_string = str(value)
    date_object = datetime.strptime(date_string, "%d/%m/%Y")
    date_object=date_object.year
    now = datetime.now()
    now=now.year

    delta = now - date_object

    return( delta)
age_calculation(date_string)




