from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg


class C_Insert_InvControl_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Controle do Inversor de Frequência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.resize(600, 600)

        ##Layout principal
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        self.TabWidget = QTabWidget()
        self.TabVoltvar = VoltvarTab()  # QWidget
        self.TabVoltwatt = VoltwattTab()  # QWidget
        self.TabWidget.addTab(self.TabVoltvar, "VOLT-VAR")
        self.TabWidget.addTab(self.TabVoltwatt, "VOLT-WATT")
        self.Dialog_Layout.addWidget(self.TabWidget)

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Dialog_Btns_Save_Btn = QPushButton("Save")
        self.Dialog_Btns_Save_Btn.setIcon(QIcon('img/icon_save.png'))
        self.Dialog_Btns_Save_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Save_Btn.clicked.connect(self.saveDefaultParameters)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Save_Btn)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancel")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 0)

        self.setLayout(self.Dialog_Layout)
        self.loadDefaultParameters()

    def saveDefaultParameters(self):
        pass

    def get_lineedit(self, lineedit):
        self.lineedit = lineedit.text()
        return self.lineedit

    def get_combobox(self, combobox):
        ## itemData corresponde à tag do item selecionado no combobox. "None" aparece quando não há nada no combobox
        ## currentIndex indica o índice do item selecionado
        self.combobox = str(combobox.itemData(combobox.currentIndex()))
        return self.combobox

    def loadParameters(self):
        pass

    def loadDefaultParameters(self):  # Só carrega quando abre a janela pela primeira vez
        pass

    def Accept(self):
        pass

    def updateDialog(self):
        pass


class VoltvarTab(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIVoltvarTab()

    def InitUIVoltvarTab(self):
        self.Select_PVSystem_GroupBox = QGroupBox("PVSystem")
        self.Select_PVSystem_GroupBox_Layout = QHBoxLayout()
        self.Select_PVSystem_GroupBox_ComboBox = QComboBox()
        self.Select_PVSystem_GroupBox_ComboBox.setMaximumWidth(150)
        self.Select_PVSystem_GroupBox_Layout.addWidget(self.Select_PVSystem_GroupBox_ComboBox)
        self.Select_PVSystem_GroupBox.setLayout(self.Select_PVSystem_GroupBox_Layout)
        #Adicionando itens ao combobox com suas respectivas tags(data)

        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.Select_PVSystem_GroupBox)
        self.setLayout(self.Tab_layout)

class VoltwattTab(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUIVoltwattTab()

    def InitUIVoltwattTab(self):
        self.Select_PVSystem_GroupBox = QGroupBox("PVSystem")
        self.Select_PVSystem_GroupBox_Layout = QHBoxLayout()
        self.Select_PVSystem_GroupBox_ComboBox = QComboBox()
        self.Select_PVSystem_GroupBox_ComboBox.setMaximumWidth(150)
        self.Select_PVSystem_GroupBox_Layout.addWidget(self.Select_PVSystem_GroupBox_ComboBox)
        self.Select_PVSystem_GroupBox.setLayout(self.Select_PVSystem_GroupBox_Layout)
        # Adicionando itens ao combobox com suas respectivas tags(data)

        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.Select_PVSystem_GroupBox)
        self.setLayout(self.Tab_layout)

