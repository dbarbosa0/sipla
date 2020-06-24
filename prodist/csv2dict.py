import csv
from sys import platform

class c2d:
    def csv2dict(self,csv_path):
        fname = csv_path
        dataCSV = {}
        # if platform.system() == "Windows":
        fname = csv_path.replace("/", "\\")

        with open(fname, 'r', newline='') as file:
            csv_reader_object = csv.reader(file)

            name_col = next(csv_reader_object)

            for row in name_col:
                dataCSV[row] = []

            for row in csv_reader_object:  ##Varendo todas as linhas
                for ndata in range(0, len(name_col)):  ## Varendo todas as colunas
                    dataCSV[name_col[ndata]].append(row[ndata])

            return dataCSV