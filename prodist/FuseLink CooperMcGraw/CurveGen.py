import csv
import os
import re

from PyQt5.QtWidgets import QFileDialog

arr = os.listdir('.')
fuselinkDir = {}
curveList = []
tipos = []

items = []
types = []

for file in arr:
    if file.split('.')[1] == 'csv':
        match = re.match(r"([0-9]+)([a-z]+)", file.split('.')[0], re.I)
        if match:
            auxNum = int(list(match.groups())[0])
            auxType = list(match.groups())[1]
            aux = [auxNum,auxType]
            items.append(aux)
            for a in list(match.groups())[1]:
                if a not in types:
                    types.append(a)

items = sorted(items)
types = sorted(types)

for tipo in types:
    for item in items:
        if item[1] == tipo:
            tipos.append(item)

for item in tipos:
    a = str(item[0]) + str(item[1]) + '.csv'
    curveList.append(a)

# print(curveList)

for fuse in curveList:
    # print(fuse)

    with open(fuse, 'r', newline='') as file:
        dataCSV = {}
        csv_reader_object = csv.reader(file)
        name_col = next(csv_reader_object)

        for row in name_col:
            dataCSV[row] = []

        for row in csv_reader_object:  ##Varendo todas as linhas
            for ndata in range(0, len(name_col)):  ## Varendo todas as colunas
                dataCSV[name_col[ndata]].append(row[ndata])

    [minAmp,minTime,maxAmp,maxTime] = list(dataCSV.values())

    minCurve = []
    maxCurve = []

    for i in range(0,len(minAmp)):
        if minAmp[i] and minTime[i]:
            minCurve.append(minAmp[i] + ';' + minTime[i])

    for i in range(0,len(maxAmp)):
        if maxAmp[i] and maxTime[i]:
            maxCurve.append(maxAmp[i] + ';' + maxTime[i])

    # print(minCurve)
    # print(maxCurve)

    fuselinkDir[fuse.split('.')[0]] =  [minCurve,maxCurve].copy()

    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    rowText = []
    for nameCurve in fuselinkDir.keys():
        rowText.append(nameCurve)

    writer.writerow(rowText)

    for ctdPoints in range(0, len(fuselinkDir)):
        rowText.clear()
        for dataShape in self.dataDispCurve:
            rowText.append(self.dataDispCurve[dataShape][ctdPoints])
        writer.writerow(rowText)

print(fuselinkDir.keys())
print(fuselinkDir)


