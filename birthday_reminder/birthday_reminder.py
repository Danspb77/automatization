file= open ('./birthdays.txt', mode='r',encoding='UTF-8')
birth_file=(file.read().splitlines())
linesMas=[]
dateDictionary={}

for line in birth_file:
    linesMas.append(line.split(' '))
print(linesMas)
for elem in linesMas:
    dateDictionary[elem[0]]=elem[1]
print(dateDictionary)
