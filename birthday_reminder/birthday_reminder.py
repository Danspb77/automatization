import datetime
from datetime import *


file= open ('./birthdays.txt', mode='r',encoding='UTF-8')
birth_file=(file.read().splitlines())
linesMas=[]


dateDictionary={}
dateDictionaryValues=dateDictionary.values()
dateDictionaryKeys=dateDictionary.keys()

def datetimeStr(data):
    devidingSymb=data[2]
    data=data.split(devidingSymb)
    day=int(data[0])
    month=int(data[1])
    year=int(data[2])
    return [year,month,day]

for line in birth_file:
    linesMas.append(line.split())
print(linesMas)

for elem in linesMas:
    year=datetimeStr(elem[1])[0]
    month=datetimeStr(elem[1])[1]
    day=datetimeStr(elem[1])[2]
    
    dateDictionary[elem[0]]=date(year,month,day)
    
print(type(dateDictionary['Папа']))
print(str(datetime.today())[0:10])
print (dateDictionaryValues)


for key in dateDictionaryKeys:
    print(str(datetime.today())[5:10])
    if str(dateDictionary[key])[5:]==(str(datetime.today())[5:10]):
        print(print(key,' have a bithday'))







