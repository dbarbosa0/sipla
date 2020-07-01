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
import opendss.storage.class_select_dispatch_curve
import opendss.storage.class_select_price_curve
import opendss.storage.class_config_storagecontroller
import opendss.storage.class_dispatchmode_default
import opendss.storage.class_dispatchmode_follow
import opendss.storage.class_dispatchmode_loadlevel
import opendss.storage.class_dispatchmode_price
import opendss.storage.class_storagecontroller_dispatchmode_loadshape
import config as cfg
import unidecode

class C_Active_Pow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.DialogActPowDefault = opendss.storage.class_dispatchmode_default.C_ActPow_Default_DispMode_Dialog()
        self.DialogActPowFollow = opendss.storage.class_dispatchmode_follow.C_ActPow_Follow_DispMode_Dialog()
        self.DialogActPowLoadLevel = opendss.storage.class_dispatchmode_loadlevel.C_ActPow_LoadLevel_DispMode_Dialog()
        self.DialogActPowPrice = opendss.storage.class_dispatchmode_price.C_ActPow_Price_DispMode_Dialog()
        self.DialogActPowLoadShape = opendss.storage.class_storagecontroller_dispatchmode_loadshape.C_ActPow_LoadShape_DispMode_Dialog()

        self.ConfigStorageController = opendss.storage.class_config_storagecontroller.C_ActPow_Config_StorageController_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()

        self.Disp_BtnGroup = QButtonGroup() # Button Group para os RadioBtn fora da GroupBox

        self.None_Radio_Btn = QRadioButton('Nenhum modo selecionado')
        self.None_Radio_Btn.setChecked(True)
        self.None_Radio_Btn.clicked.connect(self.disableGroupBoxes)
        self.Disp_BtnGroup.addButton(self.None_Radio_Btn)
        self.Dialog_Layout.addWidget(self.None_Radio_Btn, 0, 1, 1, 2)

        self.DispSinc_Radio_Btn = QRadioButton("Carga e Descarga Sincronizados")
        self.DispSinc_Radio_Btn.setChecked(False)
        self.DispSinc_Radio_Btn.clicked.connect(self.disableDispIndep)
        self.Disp_BtnGroup.addButton(self.DispSinc_Radio_Btn)
        self.Dialog_Layout.addWidget(self.DispSinc_Radio_Btn, 1, 1, 1, 2)

        ### GroupBox Despacho Sincroninzado
        self.DispSinc_GroupBox = QGroupBox()
        self.DispSinc_GroupBox.setEnabled(False)
        self.DispSinc_GroupBox_Layout = QVBoxLayout()

        self.DispSinc_BtnGroup = QButtonGroup()

        ## GroupBox AutoDespacho
        self.DispSinc_GroupBox_AutoDespacho_GroupBox = QGroupBox("Auto Despacho")
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout = QGridLayout()
        # Radio Btn "Default"
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn = QRadioButton("Default")
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.setChecked(False)
        #self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.clicked.connect(self.ActPowDefault)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn, 1, 1, 1, 1)
        self.DispSinc_BtnGroup.addButton(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn)
        # Radio Btn "Follow"
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn = QRadioButton("Follow")
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        #self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.clicked.connect(self.ActPowFollow)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn, 2, 1, 1, 1)
        self.DispSinc_BtnGroup.addButton(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn)
        # Radio Btn "LoadLevel"
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn = QRadioButton("LoadLevel")
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.setChecked(False)
        #self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.clicked.connect(self.ActPowLoadLevel)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn, 1, 2, 1, 1)
        self.DispSinc_BtnGroup.addButton(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn)
        # Radio Btn "Price"
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn = QRadioButton("Price")
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.setChecked(False)
        #self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.clicked.connect(self.ActPowPrice)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn, 2, 2, 1, 1)
        self.DispSinc_BtnGroup.addButton(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn)

        self.DispSinc_GroupBox_AutoDespacho_GroupBox.setLayout(self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout)

        ## GroupBox AutoDespacho
        self.DispSinc_GroupBox_StorageCont_GroupBox = QGroupBox("Storage Controller")
        self.DispSinc_GroupBox_StorageCont_GroupBox_Layout = QVBoxLayout()
        # Radio Btn "LoadShape"
        self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn = QRadioButton("LoadShape")
        self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.setChecked(False)
        #self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.clicked.connect(self.ActPowLoadShape)
        self.DispSinc_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn)
        self.DispSinc_BtnGroup.addButton(self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn)

        self.DispSinc_GroupBox_StorageCont_GroupBox.setLayout(self.DispSinc_GroupBox_StorageCont_GroupBox_Layout)

        self.DispSinc_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_AutoDespacho_GroupBox)
        self.DispSinc_GroupBox_Layout.addWidget(self.DispSinc_GroupBox_StorageCont_GroupBox)

        self.DispSinc_GroupBox.setLayout(self.DispSinc_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.DispSinc_GroupBox, 2, 1, 1, 2)

        self.DispIndep_Radio_Btn = QRadioButton("Carga e Descarga Independentes")
        self.DispIndep_Radio_Btn.setChecked(False)
        self.DispIndep_Radio_Btn.clicked.connect(self.disableDispSinc)
        self.Disp_BtnGroup.addButton(self.DispIndep_Radio_Btn)
        self.Dialog_Layout.addWidget(self.DispIndep_Radio_Btn, 3, 1, 1, 2)

        ### GroupBox Despacho Independente
        self.DispIndep_GroupBox = QGroupBox()   # GroupBox do Despacho de carga e descarga independentes
        self.DispIndep_GroupBox.setEnabled(False)
        self.DispIndep_GroupBox_Layout = QGridLayout()

        self.DispIndep_GroupBox_Label = QLabel("Selecione um Modo de Carga e um Modo de Descarga")
        self.DispIndep_GroupBox_Layout.addWidget(self.DispIndep_GroupBox_Label, 1, 1, 1, 2)

        ## GroupBox Modo de Carga
        self.ModoCarga_GroupBox = QGroupBox("Modo de Carga")
        #self.ModoCarga_GroupBox.setFixedWidth(175)
        self.ModoCarga_GroupBox_Layout = QGridLayout()

        self.ModoCarga_BtnGroup = QButtonGroup()

        self.ModoCarga_GroupBox_StorageCont_GroupBox = QGroupBox("Storage Controller")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout = QGridLayout()

        # Radio Btn "PeakShaveLow"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn = QRadioButton("PeakShaveLow")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.setChecked(False)
        #self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.clicked.connect(self.ActPowPeakShaveLow)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn)
        # Radio Btn "I-PeakShaveLow"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn = QRadioButton("I-PeakShaveLow")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.setChecked(False)
        #self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.clicked.connect(self.ActPowIPeakShaveLow)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn)
        # Radio Btn "Time"
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = QRadioButton("Time")
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(False)
        #self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.clicked.connect(self.ActPowChargeTime)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)
        self.ModoCarga_BtnGroup.addButton(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)

        self.ModoCarga_GroupBox_StorageCont_GroupBox.setLayout(self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout)

        self.ModoCarga_GroupBox_Layout.addWidget(self.ModoCarga_GroupBox_StorageCont_GroupBox, 2, 1, 1, 1)

        self.ModoCarga_GroupBox.setLayout(self.ModoCarga_GroupBox_Layout)
        self.DispIndep_GroupBox_Layout.addWidget(self.ModoCarga_GroupBox, 2, 1, 1, 1)

        ## GroupBox Modo de Descarga
        self.ModoDescarga_GroupBox = QGroupBox("Modo de Descarga")
        self.ModoDescarga_GroupBox.setFixedWidth(175)
        self.ModoDescarga_GroupBox_Layout = QGridLayout()

        self.ModoDescarga_BtnGroup = QButtonGroup()

        self.ModoDescarga_GroupBox_StorageCont_GroupBox = QGroupBox("Storage Controller")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout = QGridLayout()

        # Radio Btn "PeakShaveLow"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn = QRadioButton("PeakShave")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.setChecked(False)
        #self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.clicked.connect(self.ActPowPeakShave)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn)
        # Radio Btn "I-PeakShaveLow"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn = QRadioButton("I-PeakShave")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.setChecked(False)
        #self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.clicked.connect(self.ActPowIPeakShave)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn)
        # Radio Btn "Follow"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn = QRadioButton("Follow")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        #self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.clicked.connect(self.ActPowStorageContFollow)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn)
        # Radio Btn "Support"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn = QRadioButton("Support")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.setChecked(False)
        #self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.clicked.connect(self.ActPowSupport)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn)
        # Radio Btn "Schedule"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn = QRadioButton("Schedule")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.setChecked(False)
        #self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.clicked.connect(self.ActPowSchedule)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(
            self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn)
        # Radio Btn "Time"
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = QRadioButton("Time")
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(False)
        #self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.clicked.connect(self.ActPowDischargeTime)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)
        self.ModoDescarga_BtnGroup.addButton(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn)

        self.ModoDescarga_GroupBox_StorageCont_GroupBox.setLayout(self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout)

        self.ModoDescarga_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox_StorageCont_GroupBox, 2, 1, 1, 1)

        self.ModoDescarga_GroupBox.setLayout(self.ModoDescarga_GroupBox_Layout)
        self.DispIndep_GroupBox_Layout.addWidget(self.ModoDescarga_GroupBox, 2, 2, 1, 1)

        self.DispIndep_GroupBox.setLayout(self.DispIndep_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.DispIndep_GroupBox, 4, 1, 1, 2)

        #### Botões do Dialog
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptDespachoPotAtiva)
        self.Dialog_Layout.addWidget(self.OK_Btn, 5, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelDespachoPotAtiva)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 5, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def acceptDespachoPotAtiva(self):
        if self.DispSinc_Radio_Btn.isChecked():
            for i in [[self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn, self.DialogActPowDefault],
                      [self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn, self.DialogActPowFollow],
                      [self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn, self.DialogActPowLoadLevel],
                      [self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn, self.DialogActPowPrice],
                      [self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn, self.DialogActPowLoadShape]]:
                if i[0].isChecked():
                    i[1].show()
                    if i[0] == self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn:
                        self.DialogActPowLoadShape.updateDialog()
                        self.NumComboBox = self.DialogActPowLoadShape.StorControl_GroupBox_Selection_ComboBox.count()  # Número de elementos iniciais no ComboBox
                        self.DialogActPowLoadShape.NumComboBox = self.NumComboBox

                    self.close()
        if self.DispIndep_Radio_Btn.isChecked():
            self.ConfigStorageController.show()
            self.ConfigStorageController.updateDialog()

            self.NumComboBox = self.ConfigStorageController.StorControl_GroupBox_Selection_ComboBox.count() #Número de elementos iniciais no ComboBox
            self.ConfigStorageController.NumComboBox = self.NumComboBox

            self.close()
            self.ConfigStorageController.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn = self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn
            self.ConfigStorageController.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn = self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn
            self.ConfigStorageController.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn
            self.ConfigStorageController.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn = self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn
            self.ConfigStorageController.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn = self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn
            self.ConfigStorageController.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn = self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn
            self.ConfigStorageController.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn = self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn
            self.ConfigStorageController.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn = self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn
            self.ConfigStorageController.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn

    def cancelDespachoPotAtiva(self):
        self.clearRadioBtns()
        self.close()

    def clearRadioBtns(self):
        self.DispSinc_BtnGroup.setExclusive(False)
        self.ModoCarga_BtnGroup.setExclusive(False)
        self.ModoDescarga_BtnGroup.setExclusive(False)

        self.None_Radio_Btn.setChecked(True)

        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.setChecked(False)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.setChecked(False)
        self.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.setChecked(False)
        self.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.setChecked(False)
        self.DispSinc_GroupBox.setEnabled(False)

        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.setChecked(False)
        self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.setChecked(False)
        self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(False)
        self.DispIndep_GroupBox.setEnabled(False)

        self.DispSinc_BtnGroup.setExclusive(True)
        self.ModoCarga_BtnGroup.setExclusive(True)
        self.ModoDescarga_BtnGroup.setExclusive(True)

    def disableGroupBoxes(self):
        self.DispIndep_GroupBox.setEnabled(False)
        self.DispSinc_GroupBox.setEnabled(False)

    def disableDispIndep(self):
        self.DispIndep_GroupBox.setEnabled(False)
        self.DispSinc_GroupBox.setEnabled(True)

    def disableDispSinc(self):
        self.DispSinc_GroupBox.setEnabled(False)
        self.DispIndep_GroupBox.setEnabled(True)
