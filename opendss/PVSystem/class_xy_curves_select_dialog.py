from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, QRadioButton, \
    QPushButton, QHBoxLayout, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QSizePolicy, QLineEdit, QLabel, \
    QWidget
from PyQt5.QtCore import Qt, QEvent

import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception


class C_XY_Curve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Modo de Seleção de Curva"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.InitUI()
        self.curve_name = ''
        self.x_axys = ''
        self.y_axys = ''

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        # Select mode groupbox
        self.XY_Curve_Select_GroupBox = QGroupBox("Inserindo Curva")
        self.XY_Curve_Select_GroupBox_Layout = QHBoxLayout()
        self.Dialog_Layout.addWidget(self.XY_Curve_Select_GroupBox)

        # Confirm Buttons groupbox
        self.XY_Curve_Confirm_Btns_Layout = QHBoxLayout()
        self.XY_Curve_Confirm_Btns_Layout.setAlignment(Qt.AlignRight)

        # Manual mode groupbox
        self.XY_Curve_Manual_Mode_GroupBox = QGroupBox("Modo Manual")
        self.XY_Curve_Manual_Mode_GroupBox_Layout = QGridLayout()
        # self.Manual_Mode_GroupBox.setFixedWidth(450)
        self.Dialog_Layout.addWidget(self.XY_Curve_Manual_Mode_GroupBox)
        self.XY_Curve_Manual_Mode_GroupBox.setVisible(False)

        # Csv mode groupbox
        self.XY_Curve_Csv_Mode_GroupBox = QGroupBox("Modo Csv")
        self.XY_Curve_Csv_Mode_GroupBox_Layout = QGridLayout()
        # self.Csv_Mode_GroupBox.setFixedWidth(450)
        self.Dialog_Layout.addWidget(self.XY_Curve_Csv_Mode_GroupBox)
        self.XY_Curve_Csv_Mode_GroupBox.setVisible(False)

        # Creating and Adding Labels / Variables
        self.XY_Curve_Csv_Name_Label = QLabel("Nome da Curva:")
        self.XY_Curve_Csv_Name = QLineEdit()
        self.XY_Curve_Manual_Name_Label = QLabel("Nome da Curva:")
        self.XY_Curve_Manual_Name = QLineEdit()
        self.XY_Curve_Xdata_Label = QLabel("Pontos do eixo X:")
        self.XY_Curve_Xdata = QLineEdit()
        self.XY_Curve_Xdata.setToolTip('Preencha este campo somente com números, usando ponto (.) para \n'
                                    'determinar as casas decimais e separando cada valor com vírgula (,) \n'
                                    'EX: 0.6 0.7 0.8 0.9 1')
        self.XY_Curve_Ydata_Label = QLabel("Pontos do eixo Y:")
        self.XY_Curve_Ydata = QLineEdit()
        self.XY_Curve_Ydata.setToolTip('Preencha este campo somente com números, usando ponto (.) para \n'
                                    'determinar as casas decimais e separando cada valor com vírgula (,) \n'
                                    'EX: 0.6 0.7 0.8 0.9 1')

        self.XY_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Manual_Name_Label, 0, 0, 1, 1)
        self.XY_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Xdata_Label, 1, 0, 1, 1)
        self.XY_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Ydata_Label, 2, 0, 1, 1)
        self.XY_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Manual_Name, 0, 1, 1, 1)
        self.XY_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Xdata, 1, 1, 1, 1)
        self.XY_Curve_Manual_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Ydata, 2, 1, 1, 1)
        self.XY_Curve_Csv_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Csv_Name_Label, 0, 0, 1, 1)
        self.XY_Curve_Csv_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Csv_Name, 0, 1, 1, 1)

        # Creating Buttons and Adding Buttons in Groupbox
        self.XY_Curve_Select_Default_Btn = QRadioButton("Default")
        self.XY_Curve_Select_Manual_Btn = QRadioButton("Inserção Manual")
        self.XY_Curve_Select_Csv_Btn = QRadioButton("Buscar CSV")
        self.XY_Curve_Csv_Mode_File_Btn = QPushButton("Escolha o arquivo CSV")

        self.XY_Curve_Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.XY_Curve_Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.XY_Curve_Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.XY_Curve_Dialog_Btns_Cancel_Btn.clicked.connect(self.reject)

        self.XY_Curve_Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.XY_Curve_Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.XY_Curve_Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.XY_Curve_Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)

        self.XY_Curve_Select_GroupBox_Layout.addWidget(self.XY_Curve_Select_Default_Btn)
        self.XY_Curve_Select_GroupBox_Layout.addWidget(self.XY_Curve_Select_Manual_Btn)
        self.XY_Curve_Select_GroupBox_Layout.addWidget(self.XY_Curve_Select_Csv_Btn)
        self.XY_Curve_Csv_Mode_GroupBox_Layout.addWidget(self.XY_Curve_Csv_Mode_File_Btn, 1, 1, 1, 1)
        self.XY_Curve_Confirm_Btns_Layout.addWidget(self.XY_Curve_Dialog_Btns_Ok_Btn)
        self.XY_Curve_Confirm_Btns_Layout.addWidget(self.XY_Curve_Dialog_Btns_Cancel_Btn)

        # Set and Add Layouts
        self.XY_Curve_Select_GroupBox.setLayout(self.XY_Curve_Select_GroupBox_Layout)
        self.XY_Curve_Manual_Mode_GroupBox.setLayout(self.XY_Curve_Manual_Mode_GroupBox_Layout)
        self.XY_Curve_Csv_Mode_GroupBox.setLayout(self.XY_Curve_Csv_Mode_GroupBox_Layout)
        self.Dialog_Layout.addLayout(self.XY_Curve_Select_GroupBox_Layout, 0)
        self.Dialog_Layout.addLayout(self.XY_Curve_Confirm_Btns_Layout)
        self.setLayout(self.Dialog_Layout)

        # Define Radio Buttons Actions
        self.XY_Curve_Select_Default_Btn.toggled.connect(lambda: self.Default_Mode_On())
        self.XY_Curve_Select_Manual_Btn.toggled.connect(lambda: self.Manual_Mode_On())
        self.XY_Curve_Select_Csv_Btn.toggled.connect(lambda: self.Csv_Mode_On())

    def Manual_Mode_On(self):  # Como será apresentada a janela Manual
        self.XY_Curve_Manual_Name.clear()
        self.XY_Curve_Xdata.clear()
        self.XY_Curve_Ydata.clear()
        self.XY_Curve_Manual_Mode_GroupBox.setVisible(True)
        self.XY_Curve_Csv_Mode_GroupBox.setVisible(False)
        self.adjustSize()

    def Default_Mode_On(self):  # Como será apresentada a janela Default
        self.XY_Curve_Manual_Mode_GroupBox.setVisible(False)
        self.XY_Curve_Csv_Mode_GroupBox.setVisible(False)
        self.adjustSize()

    def Csv_Mode_On(self):  # Como será apresentada a janela Csv
        self.XY_Curve_Csv_Name.clear()
        self.XY_Curve_Csv_Mode_GroupBox.setVisible(True)
        self.XY_Curve_Manual_Mode_GroupBox.setVisible(False)
        self.adjustSize()

    def define_default_entries(self):
        self.curve_name = 'Default'
        self.x_axys = str([0.1, 0.2, 0.4, 1.0]).strip('[]').replace("'", "")
        self.y_axys = str([0.86, 0.9, 0.93, 0.97]).strip('[]').replace("'", "")

        return self.curve_name, self.x_axys, self.y_axys

    def verify_manual_entries(self):  # Validando as entradas manuais
        aux1 = self.XY_Curve_Xdata.text().split(',')
        aux2 = self.XY_Curve_Ydata.text().split(',')

        if self.XY_Curve_Manual_Name.text().isspace() or self.XY_Curve_Xdata.text().isspace() or \
                self.XY_Curve_Ydata.text().isspace() or self.XY_Curve_Manual_Name.text() == '' or \
                self.XY_Curve_Xdata.text() == '' or self.XY_Curve_Ydata.text() == '':  # Verifica se há campos vazios
            msg = QMessageBox()
            msg.information(self, 'Campos Vazios ',
                            "Por favor preencha todos os campos")

        elif len(aux1) != len(aux2):  # Verifica se X tem a mesma qtd de pontos que Y
            msg = QMessageBox()
            msg.information(self, 'Vetores não coincidem ',
                            "Verifique se X tem a mesma quantidade de pontos que Y")

        else:
            self.curve_name = self.XY_Curve_Manual_Name.text()
            self.x_axys = self.XY_Curve_Xdata.text()
            self.y_axys = self.XY_Curve_Ydata.text()

        return self.curve_name, self.x_axys, self.y_axys

    def verify_Csv_entries(self):  # Validando as entradas do arquivo Csv

        if self.XY_Curve_Csv_Name.text().isspace() or self.XY_Curve_Csv_Name.text() == '':  # Verifica se há campos vazios
            msg = QMessageBox()
            msg.information(self, 'Campos Vazios ',
                            "Por favor preencha o nome da curva")

        else:
            self.curve_name = self.XY_Curve_Csv_Name.text()

    def Accept(self):
        if self.XY_Curve_Select_Default_Btn.isChecked():
            self.curve_name = ''
            self.x_axys = ''
            self.y_axys = ''
            self.define_default_entries()
            print('modo default')
            print(self.curve_name)

        elif self.XY_Curve_Select_Manual_Btn.isChecked():
            self.curve_name = ''
            self.x_axys = ''
            self.y_axys = ''
            self.verify_manual_entries()
            print('modo manual')
            print(self.curve_name)

        elif self.XY_Curve_Select_Csv_Btn.isChecked():
            self.curve_name = ''
            self.x_axys = ''
            self.y_axys = ''
            self.verify_Csv_entries()
            print('modo csv')
            print(self.curve_name)

        self.close()
