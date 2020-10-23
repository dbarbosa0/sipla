import csv
import os
import re


arr = os.listdir('.')
fuselinkDir = {}
curveList = []
tipos = []

items = []
types = []
maxlen = 0
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

    fuselinkDir[fuse.split('.')[0]] = maxCurve +  list(reversed(minCurve))

    if len(maxCurve) + len(minCurve) > maxlen:
        maxlen = len(maxCurve) + len(minCurve)


def exportCSV():
    with open('../FuseLink_CooperMcGraw.csv', 'w' , newline='') as csvfile:

        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        rowText = []
        for nameCurve in fuselinkDir:
            rowText.append(nameCurve)

        writer.writerow(rowText)

        for ctdPoints in range(0, maxlen):

            rowText.clear()

            for data in fuselinkDir:
                try:

                    rowText.append(fuselinkDir[data][ctdPoints])
                except IndexError:
                    rowText.append('')
            writer.writerow(rowText)

exportCSV()

# print(list(fuselinkDir.keys()))
# print(fuselinkDir)



