from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt

import csv
import random
import pathlib
import platform
import pyqtgraph
import class_exception

import opendss.class_opendss
import config as cfg

class C_Active_Pow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

        # self.OpenDSS = opendss.class_opendss.C_OpenDSS()


    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()

        self.Dialog_Label = QLabel("Selecione um Modo de Carga e um Modo de Descarga")
        self.Dialog_Layout.addWidget(self.Dialog_Label, 1, 1, 1, 2)

        ################# GroupBox Modo de Carga #########################
        self.ModoCarga_GroupBox = QGroupBox("Modo de Carga")
        self.ModoCarga_GroupBox.setFixedWidth(175)
        self.ModoCarga_GroupBox_Layout = QGridLayout()

        self.ModoCarga_BtnGroup = QButtonGroup()

        self.ModoCarga_GroupBox_AutoDespacho_GroupBox = QGroupBox("Auto Despacho")
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout = QGridLayout()

        # Radio Btn "Default"
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn = QRadioButton("Default")
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.clicked.connect(self.ActPowChargeDefault)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn)
        # Radio Btn "Follow"
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn = QRadioButton("Follow")
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.clicked.connect(self.ActPowChargeFollow)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn)
        # Radio Btn "LoadLevel"
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn = QRadioButton("LoadLevel")
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.clicked.connect(self.ActPowChargeLoadLevel)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn)
        # Radio Btn "Price"
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn = QRadioButton("Price")
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.clicked.connect(self.ActPowChargePrice)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn)

        self.ModoCarga_GroupBox_AutoDespacho_GroupBox.setLayout(self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout)

        self.ModoCarga_GroupBox_StorageCont_GroupBox = QGroupBox("Storage Controller")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout = QGridLayout()

        # Radio Btn "PeakShaveLow"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn = QRadioButton("PeakShaveLow")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.clicked.connect(self.ActPowChargePeakShaveLow)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn)
        # Radio Btn "I-PeakShaveLow"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn = QRadioButton("I-PeakShaveLow")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.clicked.connect(self.ActPowChargeIPeakShaveLow)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn)
        # Radio Btn "Time"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = QRadioButton("Time")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.clicked.connect(self.ActPowChargeTime)
        self.ModoCarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)
        # Radio Btn "LoadShape"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn = QRadioButton("LoadShape")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.clicked.connect(self.ActPowChargeLoadShape)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn)

        self.ModoCarga_GroupBox_StorageCont_GroupBox.setLayout(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout)

        self.ModoCarga_GroupBox_Layout.addWidget(self.ModoCarga_GroupBox_AutoDespacho_GroupBox, 1, 1, 1, 1)
        self.ModoCarga_GroupBox_Layout.addWidget(self.ModoCarga_GroupBox_StorageCont_GroupBox, 2, 1, 1, 1)

        self.ModoCarga_GroupBox.setLayout(self.ModoCarga_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.ModoCarga_GroupBox, 2, 1, 1, 1)

        ################# GroupBox Modo de Descarga #########################
        self.ModoDescarga_GroupBox = QGroupBox("Modo de Descarga")
        self.ModoDescarga_GroupBox.setFixedWidth(175)
        self.ModoDescarga_GroupBox_Layout = QGridLayout()

        self.ModoDescarga_BtnGroup = QButtonGroup()

        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox = QGroupBox("Auto Despacho")
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout = QGridLayout()

        # Radio Btn "Default"
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn = QRadioButton("Default")
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.clicked.connect(self.ActPowDischargeDefault)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn)
        # Radio Btn "Follow"
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn = QRadioButton("Follow")
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.clicked.connect(self.ActPowDischargeFollow)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn)
        # Radio Btn "LoadLevel"
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn = QRadioButton("LoadLevel")
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.clicked.connect(self.ActPowDischargeLoadLevel)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn)
        # Radio Btn "Price"
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn = QRadioButton("Price")
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.clicked.connect(self.ActPowDischargePrice)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn)

        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox.setLayout(self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout)

        self.ModoDescarga_GroupBox_StorageCont_GroupBox = QGroupBox("Storage Controller")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout = QGridLayout()

        # Radio Btn "PeakShaveLow"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn = QRadioButton("PeakShave")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.clicked.connect(self.ActPowDischargePeakShave)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn)
        # Radio Btn "I-PeakShaveLow"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn = QRadioButton("I-PeakShave")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.clicked.connect(self.ActPowDischargeIPeakShave)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn)
        # Radio Btn "Follow"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn = QRadioButton("Follow")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.clicked.connect(self.ActPowDischargeStorageContFollow)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn)
        # Radio Btn "Support"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn = QRadioButton("Support")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.clicked.connect(self.ActPowDischargeSupport)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn)
        # Radio Btn "Schedule"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn = QRadioButton("Schedule")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.clicked.connect(self.ActPowDischargeSchedule)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn)
        # Radio Btn "Time"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = QRadioButton("Time")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.clicked.connect(self.ActPowDischargeTime)
        self.ModoDescarga_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)
        # Radio Btn "LoadShape"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn = QRadioButton("LoadShape")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.clicked.connect(self.ActPowDischargeLoadShape)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn)

        self.ModoDescarga_GroupBox_StorageCont_GroupBox.setLayout(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout)

        self.ModoDescarga_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_AutoDespacho_GroupBox, 1, 1, 1, 1)
        self.ModoDescarga_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox, 2, 1, 1, 1)

        self.ModoDescarga_GroupBox.setLayout(self.ModoDescarga_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.ModoDescarga_GroupBox, 2, 2, 1, 1)

        #### Botões do Dialog
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptDespachoPotAtiva)
        self.Dialog_Layout.addWidget(self.OK_Btn, 3, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelDespachoPotAtiva)
        self.Dialog_Layout.addWidget(self.Cancel_Btn)


        self.setLayout(self.Dialog_Layout)



    def acceptDespachoPotAtiva(self):
        pass

    def cancelDespachoPotAtiva(self):
        pass

    def ActPowChargeDefault(self):
        print("ActPowChargeDefault")

    def ActPowChargeFollow(self):
        print("ActPowChargeDefault")

    def ActPowChargeLoadLevel(self):
        print("LoadLevel")

    def ActPowChargePrice(self):
        print("Price")

    def ActPowChargePeakShaveLow(self):
        print("PeakShaveLow")

    def ActPowChargeIPeakShaveLow(self):
        print("I-PeakShaveLow")

    def ActPowChargeTime(self):
        print("Time")

    def ActPowChargeLoadShape(self):
        print("LoadShape")

    def ActPowDischargeDefault(self):
        print("ActPowChargeDefault")

    def ActPowDischargeFollow(self):
        print("ActPowChargeDefault")

    def ActPowDischargeLoadLevel(self):
        print("LoadLevel")

    def ActPowDischargePrice(self):
        print("Price")

    def ActPowDischargePeakShave(self):
        print("PeakShaveLow")

    def ActPowDischargeIPeakShave(self):
        print("I-PeakShaveLow")

    def ActPowDischargeStorageContFollow(self):
        print("Follow Storage Cont Descarga")

    def ActPowDischargeSupport(self):
        print("Support Descarga")

    def ActPowDischargeSchedule(self):
        print("Schedule Descarga")

    def ActPowDischargeTime(self):
        print("Time")

    def ActPowDischargeLoadShape(self):
        print("LoadShape")
