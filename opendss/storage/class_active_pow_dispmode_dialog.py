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
        self.DialogActPowDefault = C_ActPow_Default_DispMode_Dialog()
        self.DialogActPowFollow = C_ActPow_Follow_DispMode_Dialog()
        self.DialogActPowLoadLevel = C_ActPow_LoadLevel_DispMode_Dialog()
        self.DialogActPowPrice = C_ActPow_Price_DispMode_Dialog()
        self.DialogActPowLoadShape = C_ActPow_LoadShape_DispMode_Dialog()

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

class C_ActPow_Default_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Deafult da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Default da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.DefaultParameters = {}

        self.Select_DispCurve = opendss.storage.class_select_dispatch_curve.C_Config_DispCurve_Dialog()
        self.Select_DispCurveFile = opendss.storage.class_select_dispatch_curve

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.ChargeTrigger_Label = QLabel("Charge Trigger")
        self.Dialog_Layout.addWidget(self.ChargeTrigger_Label, 2, 1, 1, 1)
        self.ChargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.ChargeTrigger_LineEdit, 2, 2, 1, 1)
        self.DischargeTrigger_Label = QLabel("Discharge Trigger")
        self.Dialog_Layout.addWidget(self.DischargeTrigger_Label, 3, 1, 1, 1)
        self.DischargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.DischargeTrigger_LineEdit, 3, 2, 1, 1)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 4, 1, 1, 1)
        self.TimeTrigger_LineEdit = QLineEdit()
        self.TimeTrigger_LineEdit.setText("2.00")
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_LineEdit, 4, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de despacho")
        self.DispatchCurve_Btn.clicked.connect(self.selectDispCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 5, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptDefault)
        self.Dialog_Layout.addWidget(self.OK_Btn, 6, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelDefault)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 6, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_LineEdit.setEnabled(True)
        else:
            self.TimeTrigger_LineEdit.setEnabled(False)

    def selectDispCurve(self):
        self.Select_DispCurve.show()

    def acceptDefault(self):
        self.DefaultParameters = {}
        self.DefaultParameters["ChargeTrigger"] = self.ChargeTrigger_LineEdit.text()
        self.DefaultParameters["DischargeTrigger"] = self.DischargeTrigger_LineEdit.text()
        if self.TimeTrigger_LineEdit.isEnabled():
            self.DefaultParameters["TimeChargeTrigger"] = self.TimeTrigger_LineEdit.text()
        self.DefaultParameters.update(self.Select_DispCurve.dataDispCurve)
        self.close()

    def cancelDefault(self):
        self.close()

class C_ActPow_Follow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Follow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Follow da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.FollowParameters = {}

        self.InitUI()

        self.Select_DispCurve = opendss.storage.class_select_dispatch_curve.C_Config_DispCurve_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira o parâmetro")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 2, 1, 1, 1)
        self.TimeTrigger_LineEdit = QLineEdit()
        self.TimeTrigger_LineEdit.setText("2.00")
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_LineEdit, 2, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de despacho")
        self.DispatchCurve_Btn.clicked.connect(self.selectDispCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 3, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptFollow)
        self.Dialog_Layout.addWidget(self.OK_Btn, 4, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelFollow)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 4, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_LineEdit.setEnabled(True)
        else:
            self.TimeTrigger_LineEdit.setEnabled(False)

    def selectDispCurve(self):
        self.Select_DispCurve.show()

    def acceptFollow(self):
        self.FollowParameters = {}
        self.FollowParameters.update(self.Select_DispCurve.dataDispCurve)
        if self.TimeTrigger_LineEdit.isEnabled():
            self.FollowParameters["TimeChargeTrigger"] = self.TimeTrigger_LineEdit.text()
        self.close()

    def cancelFollow(self):
        self.close()

class C_ActPow_LoadLevel_DispMode_Dialog(QDialog): ## Classe Dialog Despacho LoadLevel da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho LoadLevel da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.LoadLevelParameters = {}

        self.InitUI()

        self.Select_PriceCurve = opendss.storage.class_select_price_curve.C_Config_PriceCurve_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.ChargeTrigger_Label = QLabel("Charge Trigger")
        self.Dialog_Layout.addWidget(self.ChargeTrigger_Label, 2, 1, 1, 1)
        self.ChargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.ChargeTrigger_LineEdit, 2, 2, 1, 1)
        self.DischargeTrigger_Label = QLabel("Discharge Trigger")
        self.Dialog_Layout.addWidget(self.DischargeTrigger_Label, 3, 1, 1, 1)
        self.DischargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.DischargeTrigger_LineEdit, 3, 2, 1, 1)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 4, 1, 1, 1)
        self.TimeTrigger_LineEdit = QLineEdit()
        self.TimeTrigger_LineEdit.setText("2.00")
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_LineEdit, 4, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de preço")
        self.DispatchCurve_Btn.clicked.connect(self.selectPriceCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 5, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptLoadLevel)
        self.Dialog_Layout.addWidget(self.OK_Btn, 6, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelLoadLevel)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 6, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_LineEdit.setEnabled(True)
        else:
            self.TimeTrigger_LineEdit.setEnabled(False)

    def selectPriceCurve(self):
        self.Select_PriceCurve.show()

    def acceptLoadLevel(self):
        self.LoadLevelParameters = {}
        self.LoadLevelParameters["ChargeTrigger"] = self.ChargeTrigger_LineEdit.text()
        self.LoadLevelParameters["DischargeTrigger"] = self.DischargeTrigger_LineEdit.text()
        if self.TimeTrigger_LineEdit.isEnabled():
            self.LoadLevelParameters["TimeChargeTrigger"] = self.TimeTrigger_LineEdit.text()
        self.LoadLevelParameters.update(self.Select_PriceCurve.dataPriceCurve)
        self.close()

    def cancelLoadLevel(self):
        self.close()

class C_ActPow_Price_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Price da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Price da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.PriceParameters = {}

        self.InitUI()

        self.Select_PriceCurve = opendss.storage.class_select_price_curve.C_Config_PriceCurve_Dialog()
        self.Select_PriceCurveFile = opendss.storage.class_select_price_curve

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.ChargeTrigger_Label = QLabel("Charge Trigger")
        self.Dialog_Layout.addWidget(self.ChargeTrigger_Label, 2, 1, 1, 1)
        self.ChargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.ChargeTrigger_LineEdit, 2, 2, 1, 1)
        self.DischargeTrigger_Label = QLabel("Discharge Trigger")
        self.Dialog_Layout.addWidget(self.DischargeTrigger_Label, 3, 1, 1, 1)
        self.DischargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.DischargeTrigger_LineEdit, 3, 2, 1, 1)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 4, 1, 1, 1)
        self.TimeTrigger_LineEdit = QLineEdit()
        self.TimeTrigger_LineEdit.setText("2.00")
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_LineEdit, 4, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de preço")
        self.DispatchCurve_Btn.clicked.connect(self.selectPriceCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 5, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptPrice)
        self.Dialog_Layout.addWidget(self.OK_Btn, 6, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelPrice)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 6, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_LineEdit.setEnabled(True)
        else:
            self.TimeTrigger_LineEdit.setEnabled(False)

    def selectPriceCurve(self):
        self.Select_PriceCurve.show()

    def acceptPrice(self):
        self.PriceParameters = {}
        self.PriceParameters["ChargeTrigger"] = self.ChargeTrigger_LineEdit.text()
        self.PriceParameters["DischargeTrigger"] = self.DischargeTrigger_LineEdit.text()
        if self.TimeTrigger_LineEdit.isEnabled():
            self.PriceParameters["TimeChargeTrigger"] = self.TimeTrigger_LineEdit.text()
        self.PriceParameters.update(self.Select_PriceCurve.dataPriceCurve)
        self.close()

    def cancelPrice(self):
        self.clearParameters()
        self.close()

    def clearParameters(self):
        self.ChargeTrigger_LineEdit.setText("")
        self.DischargeTrigger_LineEdit.setText("")
        self.TimeTrigger_CheckBox.setChecked(False)
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.TimeTrigger_LineEdit.setText("2.00")

class C_ActPow_LoadShape_DispMode_Dialog(QDialog): ## Classe Dialog Despacho LoadShape da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho LoadShape da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Select_DispCurve = opendss.storage.class_select_dispatch_curve.C_Config_DispCurve_Dialog()

        self.StorageControllersTemporario = []

        self._NumComboBox = 0
        self._StorageConfig_GroupBox_Nome_LineEdit = 0
        self._StorageConfig_GroupBox_PercentageReserve_LineEdit = 0

        self.InitUI()

    @property
    def NumComboBox(self):
        return self._NumComboBox

    @NumComboBox.setter
    def NumComboBox(self, value):
        self._NumComboBox = value

    @property
    def StorageConfig_GroupBox_Nome_LineEdit(self):
        return self._StorageConfig_GroupBox_Nome_LineEdit

    @StorageConfig_GroupBox_Nome_LineEdit.setter
    def StorageConfig_GroupBox_Nome_LineEdit(self, value):
        self._StorageConfig_GroupBox_Nome_LineEdit = value

    @property
    def StorageConfig_GroupBox_PercentageReserve_LineEdit(self):
        return self._StorageConfig_GroupBox_PercentageReserve_LineEdit

    @StorageConfig_GroupBox_PercentageReserve_LineEdit.setter
    def StorageConfig_GroupBox_PercentageReserve_LineEdit(self, value):
        self._StorageConfig_GroupBox_PercentageReserve_LineEdit = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog


        ## GroupBox Seleção do Storage Controller
        self.StorControl_GroupBox_Selection = QGroupBox("Storage Controllers")
        self.StorControl_GroupBox_Selection_Label = QLabel("Selecione um dos Storage Controllers Existentes")
        self.StorControl_GroupBox_Selection_ComboBox = QComboBox()

        # Layout do GroupBox Seleção do Storage Controller
        self.StorControl_GroupBox_Selection_Layout = QGridLayout()
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Label, 0, 0, 1, 3)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_ComboBox, 1, 0, 1, 3)
        self.StorControl_GroupBox_Selection.setLayout(self.StorControl_GroupBox_Selection_Layout)

        self.Dialog_Layout.addWidget(self.StorControl_GroupBox_Selection)

        ##### Btns
        self.StorControl_GroupBox_Selection_Remover_Btn = QPushButton("Remover")
        self.StorControl_GroupBox_Selection_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.StorControl_GroupBox_Selection_Remover_Btn.clicked.connect(self.removeStorControl)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Remover_Btn, 2, 0, 1, 1)

        self.StorControl_GroupBox_Selection_Edit_Btn = QPushButton("Editar")
        self.StorControl_GroupBox_Selection_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.StorControl_GroupBox_Selection_Edit_Btn.clicked.connect(self.editStorControl)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Edit_Btn, 2, 1, 1, 1)

        self.StorControl_GroupBox_Selection_Adicionar_Btn = QPushButton("Adicionar")
        self.StorControl_GroupBox_Selection_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        self.StorControl_GroupBox_Selection_Adicionar_Btn.clicked.connect(self.addStorControl)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Adicionar_Btn, 2, 2, 1, 1)

        self.StorControl_GroupBox = QGroupBox("Configurações Gerais do Storage Controller")
        self.StorControl_GroupBox.setVisible(False)
        ## GroupBox opções
        ### Labels New StorControl.Sourcebus
        self.StorControl_Name_Label = QLabel("Nome:")
        self.StorControl_Element_Label = QLabel("Elemento:")
        self.StorControl_Terminal_Label = QLabel("Terminal:")
        self.StorControl_Reserve_Label = QLabel("Energia reserva:")
        self.StorControl_Weight_Label = QLabel("Peso do Storage\nna frota:")

        ### LineEdits
        self.StorControl_Name = QLineEdit()
        self.StorControl_Reserve = QLineEdit()
        self.StorControl_Weight = QLineEdit()
        self.StorControl_Weight.setText("1.0")

        ### Comboboxs
        self.StorControl_Element_ComboBox = QComboBox()
        self.StorControl_Element_ComboBox.clear()
        self.StorControl_Terminal_ComboBox = QComboBox()
        self.StorControl_Terminal_ComboBox.addItems(["1", "2"])

        ### Layout
        self.StorControl_Layout = QGridLayout()
        self.StorControl_Layout.addWidget(self.StorControl_Name_Label, 0, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Element_Label, 1, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Terminal_Label, 2, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Reserve_Label, 3, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Weight_Label, 4, 0, 1, 1)

        self.StorControl_Layout.addWidget(self.StorControl_Name, 0, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Element_ComboBox, 1, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Terminal_ComboBox, 2, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Reserve, 3, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Weight, 4, 1, 1, 1)

        ###### Botões dos Parâmetros
        self.StorControl_Btns_Layout = QHBoxLayout()
        self.StorControl_Btns_Layout.setAlignment(Qt.AlignRight)

        self.StorControl_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.StorControl_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.StorControl_Btns_Cancel_Btn.clicked.connect(self.CancelAddEdit)
        self.StorControl_Btns_Layout.addWidget(self.StorControl_Btns_Cancel_Btn)

        self.StorControl_Btns_Ok_Btn = QPushButton("OK")
        self.StorControl_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.StorControl_Btns_Ok_Btn.clicked.connect(self.AcceptAddEditStorControl)
        self.StorControl_Btns_Layout.addWidget(self.StorControl_Btns_Ok_Btn)
        self.StorControl_Layout.addItem(self.StorControl_Btns_Layout, 5, 0, 1, 2)
        ####

        self.StorControl_GroupBox.setLayout(self.StorControl_Layout)

        self.Dialog_Layout.addWidget(self.StorControl_GroupBox)

        ##############################################################################################

        ###### Botão Dialog para configurar a curva de despacho
        self.DispCurve_Btn_Layout = QHBoxLayout()
        self.DispCurve_Btn = QPushButton("Configurar curva de despacho")
        self.DispCurve_Btn.clicked.connect(self.selectDispCurve)
        self.DispCurve_Btn_Layout.addWidget(self.DispCurve_Btn)

        self.Dialog_Layout.addLayout(self.DispCurve_Btn_Layout)

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelStorageControlSelection)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptStorageControlSelection)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout)

        self.setLayout(self.Dialog_Layout)

    def getStorage_Name(self):
        return unidecode.unidecode(self.StorageConfig_GroupBox_Nome_LineEdit.text().replace(" ", "_"))

    def getStorage_PercentageReserve(self):
        return self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()

    def get_StorControl_Name(self):
        return unidecode.unidecode(self.StorControl_Name.text().replace(" ", "_"))

    def get_ElementStorControl(self):
        return self.StorControl_Element_ComboBox.currentText()

    def get_TerminalStorControl(self):
        return self.StorControl_Terminal_ComboBox.currentText()

    def get_ReserveStorControl(self):
        return self.StorControl_Reserve.text()

    def get_WeightStorControl(self):
        return self.StorControl_Weight.text()

    def clearStorControlParameters(self):
        self.StorControl_Name.setText("")
        self.StorControl_Element_ComboBox.setCurrentIndex(0)
        self.StorControl_Terminal_ComboBox.setCurrentIndex(0)
        self.StorControl_Reserve.setText(self.getStorage_PercentageReserve())
        self.StorControl_Weight.setText("1.0")

    def addStorControl(self):
        if self.StorControl_GroupBox_Selection_ComboBox.count() + 1 - self.NumComboBox <= 1: # Para garantir que só adicione um controlador por Storage
            self.clearStorControlParameters()
            self.StorControl_Name.setEnabled(True)
            self.EnableDisableParameters(True)
        else:
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "Só é possível adicionar um Storage Controller por Storage.\nEdite ou remova algum dos existentes!",
                        QMessageBox.Ok).exec()

    def editStorControl(self):
        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            self.clearStorControlParameters()
            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                    self.StorControl_Name.setText(ctd["StorageControllerName"])
                    self.StorControl_Element_ComboBox.setCurrentText(ctd["Element"])
                    self.StorControl_Terminal_ComboBox.setCurrentText(ctd["Terminal"])
                    self.StorControl_Reserve.setText(ctd["Reserve"])
                    self.StorControl_Weight.setText(ctd["Weight"][self.getStorage_Name()])
            self.StorControl_Name.setEnabled(False)
            self.EnableDisableParameters(True)

    def CancelAddEdit(self):
        self.clearStorControlParameters()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):
        if bool:
            self.StorControl_GroupBox.setVisible(True)
            self.StorControl_GroupBox_Selection.setEnabled(False)
            self.Dialog_Btns_Ok_Btn.setEnabled(False)
            self.Dialog_Btns_Cancel_Btn.setEnabled(False)
            self.DispCurve_Btn.setEnabled(False)
        else:
            self.StorControl_GroupBox.setVisible(False)
            self.StorControl_GroupBox_Selection.setEnabled(True)
            self.Dialog_Btns_Ok_Btn.setEnabled(True)
            self.Dialog_Btns_Cancel_Btn.setEnabled(True)
            self.DispCurve_Btn.setEnabled(True)

    def removeStorControl(self):
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                self.StorageControllersTemporario.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Storage Controller",
                            "Storage Controller " + ctd["StorageControllerName"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
        self.updateDialog()

    def AcceptAddEditStorControl(self):
        StorageController = {}
        StorageController["StorageControllerName"] = self.get_StorControl_Name()
        StorageController["ElementList"] = []
        StorageController["Element"] = self.get_ElementStorControl()
        StorageController["Terminal"] = self.get_TerminalStorControl()
        StorageController["Reserve"] = self.get_ReserveStorControl()
        StorageController["Weight"] = {self.getStorage_Name(): self.get_WeightStorControl()}
        StorageController["DispatchMode"] = "LoadShape"

        if self.StorControl_Name.isEnabled():
            ctdExist = False
            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == StorageController["StorageControllerName"]:
                    ctdExist = True
            if not ctdExist:
                self.StorageControllersTemporario.append(StorageController)
                QMessageBox(QMessageBox.Information, "Storage Controller",
                            "Storage Controller " + StorageController["StorageControllerName"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Storage Controller",
                            "Storage Controller" + StorageController["StorageControllerName"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == StorageController["StorageControllerName"]:
                    ctd["Element"] = StorageController["Element"]
                    ctd["Terminal"] = StorageController["Terminal"]
                    ctd["Reserve"] = StorageController["Reserve"]
                    ctd["Weight"][self.getStorage_Name()] = self.get_WeightStorControl()
                    QMessageBox(QMessageBox.Information, "Storage Controller",
                                "Storage Controller" + ctd["StorageControllerName"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()
        print("Controller tempo:", self.StorageControllersTemporario)

        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def acceptStorageControlSelection(self):
        DispatchCurveOK = False

        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            if self.Select_DispCurve.dataDispCurve == {}:
                QMessageBox(QMessageBox.Warning, "Storage Controller", "Selecione uma curva de despacho!", QMessageBox.Ok).exec()
            else:
                DispatchCurveOK = True
                for ctd in self.StorageControllersTemporario:
                    if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                        ctd.update(self.Select_DispCurve.dataDispCurve)

        if DispatchCurveOK:
            for ctd in self.StorageControllersTemporario: # Garante que dois StorageController não controlem um mesmo Storage
                if self.getStorage_Name() in ctd["ElementList"] and (not ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText()):
                    self.StorageControllersTemporario.remove(ctd)

            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                    ctd["ElementList"].append(self.getStorage_Name())

            for ctd in self.StorageControllersTemporario: # Garante que nao haja StorController que não controle nenhum Storage
                if not ctd["ElementList"]:
                    self.StorageControllersTemporario.remove(ctd)

            print(self.StorageControllersTemporario)
            self.close()

    def cancelStorageControlSelection(self):
        self.close()

    def updateDialog(self):
        self.StorControl_GroupBox_Selection_ComboBox.clear()
        if not self.StorageControllersTemporario == []:
            for ctd in self.StorageControllersTemporario:
                if "DispatchMode" in ctd:
                    self.StorControl_GroupBox_Selection_ComboBox.addItem(ctd["StorageControllerName"])

        self.StorControl_Element_ComboBox.clear()
        self.StorControl_Element_ComboBox.addItems(self.OpenDSS.getElementList())

    def selectDispCurve(self):
        self.Select_DispCurve.show()









