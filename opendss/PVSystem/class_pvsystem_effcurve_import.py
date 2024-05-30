from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, QRadioButton, \
    QPushButton, QHBoxLayout, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QSizePolicy, QLineEdit, QLabel, \
    QWidget
from PyQt5.QtCore import Qt, QStringListModel

import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception


class C_Eff_Curve_Import(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Modo de Seleção de Curva"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.InitUI()

        self.curve_name = ''
        self.npts = ''
        self.x_axys = ''
        self.y_axys = ''

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        # Select mode groupbox
        self.Eff_Curve_Select_GroupBox = QGroupBox("Inserindo Curva")
        self.Eff_Curve_Select_GroupBox_Layout = QHBoxLayout()
        self.Dialog_Layout.addWidget(self.Eff_Curve_Select_GroupBox)

        # Confirm Buttons groupbox
        self.Eff_Curve_Confirm_Btns_Layout = QHBoxLayout()
        self.Eff_Curve_Confirm_Btns_Layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Manual mode groupbox
        self.Eff_Curve_Manual_Mode_GroupBox = QGroupBox("Modo Manual")
        self.Eff_Curve_Manual_Mode_GroupBox_Layout = QGridLayout()
        # self.Manual_Mode_GroupBox.setFixedWidth(450)
        self.Dialog_Layout.addWidget(self.Eff_Curve_Manual_Mode_GroupBox)
        self.Eff_Curve_Manual_Mode_GroupBox.setVisible(False)

        # Csv mode groupbox
        self.Eff_Curve_Csv_Mode_GroupBox = QGroupBox("Modo Csv")
        self.Eff_Curve_Csv_Mode_GroupBox_Layout = QGridLayout()
        # self.Csv_Mode_GroupBox.setFixedWidth(450)
        self.Dialog_Layout.addWidget(self.Eff_Curve_Csv_Mode_GroupBox)
        self.Eff_Curve_Csv_Mode_GroupBox.setVisible(False)

        # Creating and Adding Labels / Variables
        self.Eff_Curve_Csv_Name_Label = QLabel("Nome da Curva:")
        self.Eff_Curve_Csv_Name = QLineEdit()
        self.Eff_Curve_Manual_Name_Label = QLabel("Nome da Curva:")
        self.Eff_Curve_Manual_Name = QLineEdit()
        self.Eff_Curve_Xdata_Label = QLabel("Pontos do eixo X:")
        self.Eff_Curve_Xdata = QLineEdit()
        self.Eff_Curve_Xdata.setToolTip('Preencha este campo somente com números, usando ponto (.) para \n'
                                       'determinar as casas decimais e separando cada valor com vírgula (,) \n'
                                       'EX: 0.6, 0.7, 0.8, 0.9, 1')
        self.Eff_Curve_Ydata_Label = QLabel("Pontos do eixo Y:")
        self.Eff_Curve_Ydata = QLineEdit()
        self.Eff_Curve_Ydata.setToolTip('Preencha este campo somente com números, usando ponto (.) para \n'
                                       'determinar as casas decimais e separando cada valor com vírgula (,) \n'
                                       'EX: 0.6, 0.7, 0.8, 0.9, 1')

        self.Eff_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Manual_Name_Label, 0, 0, 1, 1)
        self.Eff_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Xdata_Label, 1, 0, 1, 1)
        self.Eff_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Ydata_Label, 2, 0, 1, 1)
        self.Eff_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Manual_Name, 0, 1, 1, 1)
        self.Eff_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Xdata, 1, 1, 1, 1)
        self.Eff_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Ydata, 2, 1, 1, 1)
        self.Eff_Curve_Csv_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Csv_Name_Label, 0, 0, 1, 1)
        self.Eff_Curve_Csv_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Csv_Name, 0, 1, 1, 1)

        # Creating Buttons and Adding Buttons in Groupbox
        self.Eff_Curve_Select_Default_Btn = QRadioButton("Default")
        self.Eff_Curve_Select_Manual_Btn = QRadioButton("Inserção Manual")
        self.Eff_Curve_Select_Csv_Btn = QRadioButton("Buscar CSV")

        self.Eff_Curve_Csv_Mode_File_Btn = QPushButton("Escolha o arquivo CSV")
        self.Eff_Curve_Csv_Mode_File_Btn.setIcon(QIcon('Imagens/Text-csv-text.svg'))
        self.Eff_Curve_Csv_Mode_File_Btn.clicked.connect(self.csv_select)

        self.Eff_Curve_Btns_Dialog_Cancel_Btn = QPushButton("Cancelar")
        self.Eff_Curve_Btns_Dialog_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Eff_Curve_Btns_Dialog_Cancel_Btn.setFixedWidth(100)
        self.Eff_Curve_Btns_Dialog_Cancel_Btn.clicked.connect(self.reject)

        self.Eff_Curve_Btns_Dialog_Ok_Btn = QPushButton("OK")
        self.Eff_Curve_Btns_Dialog_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Eff_Curve_Btns_Dialog_Ok_Btn.setFixedWidth(100)
        self.Eff_Curve_Btns_Dialog_Ok_Btn.clicked.connect(self.Accept)

        self.Eff_Curve_Select_GroupBox_Layout.addWidget(self.Eff_Curve_Select_Default_Btn)
        self.Eff_Curve_Select_GroupBox_Layout.addWidget(self.Eff_Curve_Select_Manual_Btn)
        self.Eff_Curve_Select_GroupBox_Layout.addWidget(self.Eff_Curve_Select_Csv_Btn)
        self.Eff_Curve_Csv_Mode_GroupBox_Layout.addWidget(self.Eff_Curve_Csv_Mode_File_Btn, 1, 1, 1, 1)
        self.Eff_Curve_Confirm_Btns_Layout.addWidget(self.Eff_Curve_Btns_Dialog_Ok_Btn)
        self.Eff_Curve_Confirm_Btns_Layout.addWidget(self.Eff_Curve_Btns_Dialog_Cancel_Btn)

        # Set and Add Layouts
        self.Eff_Curve_Select_GroupBox.setLayout(self.Eff_Curve_Select_GroupBox_Layout)
        self.Eff_Curve_Manual_Mode_GroupBox.setLayout(self.Eff_Curve_Manual_Mode_GroupBox_Layout)
        self.Eff_Curve_Csv_Mode_GroupBox.setLayout(self.Eff_Curve_Csv_Mode_GroupBox_Layout)
        self.Dialog_Layout.addLayout(self.Eff_Curve_Select_GroupBox_Layout, 0)
        self.Dialog_Layout.addLayout(self.Eff_Curve_Confirm_Btns_Layout)
        self.setLayout(self.Dialog_Layout)

        # Define Radio Buttons Actions
        self.Eff_Curve_Select_Default_Btn.toggled.connect(lambda: self.Default_Mode_On())
        self.Eff_Curve_Select_Manual_Btn.toggled.connect(lambda: self.Manual_Mode_On())
        self.Eff_Curve_Select_Csv_Btn.toggled.connect(lambda: self.Csv_Mode_On())

    def Default_Mode_On(self):  # Como será apresentada a janela Default
        self.Eff_Curve_Manual_Mode_GroupBox.setVisible(False)
        self.Eff_Curve_Csv_Mode_GroupBox.setVisible(False)
        self.adjustSize()

    def Manual_Mode_On(self):  # Como será apresentada a janela Manual
        self.Eff_Curve_Manual_Name.clear()
        self.Eff_Curve_Xdata.clear()
        self.Eff_Curve_Ydata.clear()
        self.Eff_Curve_Manual_Mode_GroupBox.setVisible(True)
        self.Eff_Curve_Csv_Mode_GroupBox.setVisible(False)
        self.adjustSize()

    def Csv_Mode_On(self):  # Como será apresentada a janela Csv
        self.Eff_Curve_Csv_Name.clear()
        self.Eff_Curve_Csv_Mode_GroupBox.setVisible(True)
        self.Eff_Curve_Manual_Mode_GroupBox.setVisible(False)
        self.adjustSize()

    def define_default_entries(self):
        self.curve_name = 'Eff_Default'
        self.npts = '4'
        self.x_axys = str([0.1, 0.2, 0.4, 1.0]).strip('[]').replace("'", "")
        self.y_axys = str([0.86, 0.9, 0.93, 0.97]).strip('[]').replace("'", "")

    def verify_manual_entries(self):  # Validando as entradas manuais
        aux1 = self.Eff_Curve_Xdata.text().split(',')
        aux2 = self.Eff_Curve_Ydata.text().split(',')

        if self.Eff_Curve_Manual_Name.text().isspace() or self.Eff_Curve_Xdata.text().isspace() or \
                self.Eff_Curve_Ydata.text().isspace() or self.Eff_Curve_Manual_Name.text() == '' or \
                self.Eff_Curve_Xdata.text() == '' or self.Eff_Curve_Ydata.text() == '':  # Verifica se há campos vazios
            msg = QMessageBox()
            msg.information(self, 'Campos Vazios ',
                            "Por favor preencha todos os campos")

        elif len(aux1) != len(aux2):  # Verifica se X tem a mesma qtd de pontos que Y
            msg = QMessageBox()
            msg.information(self, 'Vetores não coincidem ',
                            "Verifique se X tem a mesma quantidade de pontos que Y")

        else:
            self.curve_name = self.Eff_Curve_Manual_Name.text()
            self.x_axys = self.Eff_Curve_Xdata.text()
            self.y_axys = self.Eff_Curve_Ydata.text()

        return self.curve_name, self.x_axys, self.y_axys

    def csv_select(self):  # Pegando o arquivo csv pra tratar
        global fname, dataCSV
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open CSV file',
                                                "LoadShapes", "CSV files (*.csv)")

            if platform.system() == "Windows":
                fname = fname[0].replace('/', '\\')
            else:
                fname = fname[0]

            dataCSV = {}

            with open(str(fname), 'r', newline='') as file:
                csv_reader_object = csv.reader(file)

                name_col = next(csv_reader_object)

                for row in name_col:
                    dataCSV[row] = []

                for row in csv_reader_object:  ##Varendo todas as linhas
                    for ndata in range(0, len(name_col)):  ## Varendo todas as colunas
                        dataCSV[name_col[ndata]].append(row[ndata])

        except:
            class_exception.ExecConfigOpenDSS("Erro ao importar a(s) Curva(s) de Carga!", "Verifique o arquivo CSV!")
        print(dataCSV)
        print(len(dataCSV.values()))
        return dataCSV

    def verify_Csv_entries(self):  # Validando as entradas do arquivo Csv
        if self.Eff_Curve_Csv_Name.text().isspace() or self.Eff_Curve_Csv_Name.text() == '':  # Verifica se há campos vazios
            msg = QMessageBox()
            msg.information(self, 'Campos Vazios ',
                            "Por favor preencha o nome da curva")
        else:
            self.curve_name = self.Eff_Curve_Csv_Name.text()

    def Accept(self):
        if self.Eff_Curve_Select_Default_Btn.isChecked():
            self.curve_name = ''
            self.x_axys = ''
            self.y_axys = ''
            self.define_default_entries()

        elif self.Eff_Curve_Select_Manual_Btn.isChecked():
            self.curve_name = ''
            self.x_axys = ''
            self.y_axys = ''
            self.verify_manual_entries()

        elif self.Eff_Curve_Select_Csv_Btn.isChecked():
            self.curve_name = ''
            self.x_axys = ''
            self.y_axys = ''
            self.verify_Csv_entries()

        self.close()
        self.cleareffcurveParameters()

    def cleareffcurveParameters(self):
        self.Eff_Curve_Csv_Name.setText("")
        self.Eff_Curve_Manual_Name.setText("")
        self.Eff_Curve_Xdata.setText("")
        self.Eff_Curve_Ydata.setText("")
