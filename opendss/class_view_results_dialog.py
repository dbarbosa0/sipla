from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QTableWidget, \
    QCheckBox,QTableWidgetItem

import cmath

from PyQt5.QtCore import Qt

import opendss.class_opendss
import opendss.class_data
import config as cfg
import unidecode

class C_View_Results_Dialog(QDialog): ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Fluxo de Potência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.dataOpenDSS = opendss.class_data.C_Data() #Acesso ao Banco de Dados

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()

        self.Dialog_Layout = QHBoxLayout() #Layout da Dialog

        ###
        ## GroupBox View
        self.View_GroupBox = QGroupBox("Configure")
        self.View_GroupBox.setFixedWidth(250)
        self.View_GroupBox.setFixedHeight(200)

        ## ComboBOX
        self.View_GroupBox_Element_ComboBox = QComboBox()
        self.View_GroupBox_Terminal_ComboBox = QComboBox()
        self.View_GroupBox_Terminal_ComboBox.addItems(["1","2"])

        self.View_GroupBox_Element_ComboBox.setMaximumWidth(170)
        self.View_GroupBox_Terminal_ComboBox.setMaximumWidth(70)

        ##Label
        self.View_GroupBox_Terminal_Label = QLabel("Terminal:")
        self.View_GroupBox_Elemento_Label = QLabel("Elemento:")
        self.View_GroupBox_PushButton_Label = QLabel("Confirmar:")

        ##Pushbutton
        self.View_GroupBox_PushButton = QPushButton("Ok")
        self.View_GroupBox_PushButton.setIcon(QIcon('img/icon_ok.png'))
        self.View_GroupBox_PushButton.setMaximumWidth(70)
        self.View_GroupBox_PushButton.clicked.connect(self.set_TableViewsResults)

        # Layout do GroupBox Medidores
        self.View_GroupBox_Layout = QGridLayout()
        self.View_GroupBox_Layout.addWidget(self.View_GroupBox_Element_ComboBox, 0, 1, 1, 1)
        self.View_GroupBox_Layout.addWidget(self.View_GroupBox_Terminal_ComboBox, 1, 1, 1, 1)
        self.View_GroupBox_Layout.addWidget(self.View_GroupBox_PushButton, 2, 1, 1, 1)
        self.View_GroupBox_Layout.addWidget(self.View_GroupBox_Elemento_Label, 0, 0, 1, 1)
        self.View_GroupBox_Layout.addWidget(self.View_GroupBox_Terminal_Label, 1, 0, 1, 1)
        self.View_GroupBox_Layout.addWidget(self.View_GroupBox_PushButton_Label, 2, 0, 1, 1)
        self.View_GroupBox.setLayout(self.View_GroupBox_Layout)
        ###
        ## GroupBox ViewLoadFlow
        self.ViewLoadFlow_GroupBox = QGroupBox("Fluxo de Potência")
        self.ViewLoadFlow_GroupBox.setFixedWidth(650)
        self.ViewLoadFlow_GroupBox.setFixedHeight(200)

        ## Tab View Results
        self.ViewLoadFlow_TabWidget = QTabWidget()

        self.TableResults = TableViewsResults()  # QWidget
        self.ViewLoadFlow_TabWidget.addTab(self.TableResults, "View")

        # Layout do GroupBox Medidores
        self.ViewLoadFlow_GroupBox_Layout = QGridLayout()
        self.ViewLoadFlow_GroupBox_Layout.addWidget(self.ViewLoadFlow_TabWidget, 0, 2, 2, 2)
        self.ViewLoadFlow_GroupBox.setLayout(self.ViewLoadFlow_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.View_GroupBox)
        self.Dialog_Layout.addWidget(self.ViewLoadFlow_GroupBox)

        self.setLayout(self.Dialog_Layout)



    def updateDialog(self):
        self.View_GroupBox_Element_ComboBox.addItems(self.OpenDSS.getAllNamesElements())

    def set_TableViewsResults(self):
        self.OpenDSS.SetActiveElement(self.View_GroupBox_Element_ComboBox.currentText())
        self.OpenDSS.get_Voltages_TableViewsResults()
        if self.View_GroupBox_Terminal_ComboBox.currentText() == "1" and self.View_GroupBox_Element_ComboBox.currentText()[1] == "i" or "w" or "s" or "o":
            ##Tensão VLL
            self.TableResults.setItem(0, 0, QTableWidgetItem(str(round(self.OpenDSS.get_Voltages_TableViewsResults()[0]/1000,3))))
            self.TableResults.setItem(1, 0, QTableWidgetItem(str(round(self.OpenDSS.get_Voltages_TableViewsResults()[2]/1000,3))))
            self.TableResults.setItem(2, 0, QTableWidgetItem(str(round(self.OpenDSS.get_Voltages_TableViewsResults()[4]/1000,3))))
            ##Tensão VLLN
            self.TableResults.setItem(0, 1, QTableWidgetItem(str(round((self.OpenDSS.get_Voltages_TableViewsResults()[0]/1.73205080757)/1000,3))))
            self.TableResults.setItem(1, 1, QTableWidgetItem(str(round((self.OpenDSS.get_Voltages_TableViewsResults()[2]/1.73205080757)/1000,3))))
            self.TableResults.setItem(2, 1 , QTableWidgetItem(str(round((self.OpenDSS.get_Voltages_TableViewsResults()[4]/1.73205080757)/1000,3))))
            ##Corrente
            self.TableResults.setItem(0, 2, QTableWidgetItem(str(round(self.OpenDSS.get_Currents_TableViewsResults()[0],3))))
            self.TableResults.setItem(1, 2, QTableWidgetItem(str(round(self.OpenDSS.get_Currents_TableViewsResults()[2],3))))
            self.TableResults.setItem(2, 2, QTableWidgetItem(str(round(self.OpenDSS.get_Currents_TableViewsResults()[4],3))))
            ##PW
            self.TableResults.setItem(0, 4, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[0],3))))
            self.TableResults.setItem(1, 4, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[2],3))))
            self.TableResults.setItem(2, 4, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[4],3))))
            ##PQ
            self.TableResults.setItem(0, 5, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[1],3))))
            self.TableResults.setItem(1, 5, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[3],3))))
            self.TableResults.setItem(2, 5, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[5],3))))
            ##SKVA
            self.TableResults.setItem(0, 3, QTableWidgetItem(str(round((self.OpenDSS.get_Powers_TableViewsResults()[0] ** 2 + self.OpenDSS.get_Powers_TableViewsResults()[1] ** 2) ** (0.5),3))))
            self.TableResults.setItem(1, 3, QTableWidgetItem(str(round((self.OpenDSS.get_Powers_TableViewsResults()[2] ** 2 + self.OpenDSS.get_Powers_TableViewsResults()[3] ** 2) ** (0.5),3))))
            self.TableResults.setItem(2, 3, QTableWidgetItem(str(round((self.OpenDSS.get_Powers_TableViewsResults()[4] ** 2 + self.OpenDSS.get_Powers_TableViewsResults()[5] ** 2) ** (0.5),3))))
        #else:
            #QMessageBox(QMessageBox.Information, "ERROR", " Equipamento ainda não disponível", QMessageBox.Ok).exec()


        if self.View_GroupBox_Terminal_ComboBox.currentText() == "2" and self.View_GroupBox_Element_ComboBox.currentText()[1] == "i" or "w" or "s":
            ##Tensão VLL
            self.TableResults.setItem(0, 0, QTableWidgetItem(str(round(self.OpenDSS.get_Voltages_TableViewsResults()[6]/1000,3))))
            self.TableResults.setItem(1, 0, QTableWidgetItem(str(round(self.OpenDSS.get_Voltages_TableViewsResults()[8]/1000,3))))
            self.TableResults.setItem(2, 0, QTableWidgetItem(str(round(self.OpenDSS.get_Voltages_TableViewsResults()[10]/1000,3))))

            ##Tensão VLLN
            self.TableResults.setItem(0, 1, QTableWidgetItem(str(round((self.OpenDSS.get_Voltages_TableViewsResults()[6]/1.73205080757)/1000,3))))
            self.TableResults.setItem(1, 1, QTableWidgetItem(str(round((self.OpenDSS.get_Voltages_TableViewsResults()[8]/1.73205080757)/1000,3))))
            self.TableResults.setItem(2, 1, QTableWidgetItem(str(round((self.OpenDSS.get_Voltages_TableViewsResults()[10]/1.73205080757)/1000,3))))

            ##Corrente
            self.TableResults.setItem(0, 2, QTableWidgetItem(str(round(self.OpenDSS.get_Currents_TableViewsResults()[6],3))))
            self.TableResults.setItem(1, 2, QTableWidgetItem(str(round(self.OpenDSS.get_Currents_TableViewsResults()[8],3))))
            self.TableResults.setItem(2, 2, QTableWidgetItem(str(round(self.OpenDSS.get_Currents_TableViewsResults()[10],3))))

            ##PW
            self.TableResults.setItem(0, 4, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[6],3))))
            self.TableResults.setItem(1, 4, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[8],3))))
            self.TableResults.setItem(2, 4, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[10],3))))
            ##PQ
            self.TableResults.setItem(0, 5, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[7],3))))
            self.TableResults.setItem(1, 5, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[9],3))))
            self.TableResults.setItem(2, 5, QTableWidgetItem(str(round(self.OpenDSS.get_Powers_TableViewsResults()[11],3))))
            ##SKVA
            self.TableResults.setItem(0, 3, QTableWidgetItem(str(round((self.OpenDSS.get_Powers_TableViewsResults()[6]**2 + self.OpenDSS.get_Powers_TableViewsResults()[7]**2) ** 0.5 ,3))))
            self.TableResults.setItem(1, 3, QTableWidgetItem(str(round((self.OpenDSS.get_Powers_TableViewsResults()[8]**2 + self.OpenDSS.get_Powers_TableViewsResults()[9]**2) ** 0.5 ,3))))
            self.TableResults.setItem(2, 3, QTableWidgetItem(str(round((self.OpenDSS.get_Powers_TableViewsResults()[10]**2 + self.OpenDSS.get_Powers_TableViewsResults()[11]**2) ** 0.5 ,3))))
        #else:
            #QMessageBox(QMessageBox.Information, "ERROR", " Equipamento ainda não disponível", QMessageBox.Ok).exec()


class TableViewsResults(QTableWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):

        columnsTable = ('kVLL', 'kVLN', 'i (A)', 'kVA', 'kW', 'kVAR')
        rowTable = ('A', 'B', 'C')

        self.setColumnCount(len(columnsTable))
        self.setRowCount(len(rowTable))

        self.setHorizontalHeaderLabels(columnsTable)
        self.setVerticalHeaderLabels(rowTable)

        self.setEditTriggers(QTableWidget.NoEditTriggers)