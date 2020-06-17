from PyQt5.QtGui import QColor, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QRadioButton, QButtonGroup, QSpinBox
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
import opendss.storage.class_active_pow_dispmode_dialog
import opendss.storage.class_insert_storage_dialog
import config as cfg
import unidecode


class C_ActPow_Config_StorageController_Dialog(QDialog): ## Classe Dialog configurações gerais do Storage Controller
    def __init__(self):
        super().__init__()

        self.titleWindow = "Configurar Storage Controller"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.DialogActPowPeakShaveLow = C_ActPow_Charge_PeakShaveLow_DispMode_Dialog()
        self.DialogActPowIPeakShaveLow = C_ActPow_Charge_IPeakShaveLow_DispMode_Dialog()
        self.DialogActPowChargeTime = C_ActPow_Charge_Time_DispMode_Dialog()
        self.DialogActPowPeakShave = C_ActPow_Discharge_PeakShave_DispMode_Dialog()
        self.DialogActPowIPeakShave = C_ActPow_Discharge_IPeakShave_DispMode_Dialog()
        self.DialogActPowStorageContFollow = C_ActPow_Discharge_Follow_DispMode_Dialog()
        self.DialogActPowSupport = C_ActPow_Discharge_Support_DispMode_Dialog()
        self.DialogActPowSchedule = C_ActPow_Discharge_Schedule_DispMode_Dialog()
        self.DialogActPowDischargeTime = C_ActPow_Discharge_Time_DispMode_Dialog()

        self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn = 0
        self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn = 0
        self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = 0
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn = 0
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn = 0
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn = 0
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn = 0
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn = 0
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = 0

        self._StorageConfig_GroupBox_Nome_LineEdit = 0
        self._StorageConfig_GroupBox_PercentageReserve_LineEdit = 0

        self._NumComboBox = 0

        # self._StorageControllers = []

        self.StorageControllersTemporario = []

        self.InitUI()

    @property
    def ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn(self):
        return self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn

    @ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.setter
    def ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn(self, value):
        self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn = value

    @property
    def ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn(self):
        return self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn

    @ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.setter
    def ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn(self, value):
        self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn = value

    @property
    def ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn(self):
        return self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn

    @ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setter
    def ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn(self, value):
        self._ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = value

    @property
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn(self):
        return self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn

    @ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.setter
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn(self, value):
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn = value

    @property
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn(self):
        return self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn

    @ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.setter
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn(self, value):
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn = value

    @property
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn(self):
        return self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn

    @ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.setter
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn(self, value):
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn = value

    @property
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn(self):
        return self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn

    @ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.setter
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn(self, value):
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn = value

    @property
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn(self):
        return self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn

    @ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.setter
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn(self, value):
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn = value

    @property
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn(self):
        return self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn

    @ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setter
    def ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn(self, value):
        self._ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn = value

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

    @property
    def NumComboBox(self):
        return self._NumComboBox

    @NumComboBox.setter
    def NumComboBox(self, value):
        self._NumComboBox = value

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
        #self.StorControl_Reserve.setText(str(self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()))
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

        ###### Botões Dialogs para configurar os modos de carga de descarga
        self.Dialog_Btns_ChargeDischarge_Layout = QHBoxLayout()
        # self.Dialog_Btns_ChargeDischarge_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Charge_Btn = QPushButton("Configurar Modo de Carga")
        self.Dialog_Btns_Charge_Btn.clicked.connect(self.configChargeDialog)
        self.Dialog_Btns_ChargeDischarge_Layout.addWidget(self.Dialog_Btns_Charge_Btn)

        self.Dialog_Btns_Discharge_Btn = QPushButton("Configurar Modo de Descarga")
        self.Dialog_Btns_Discharge_Btn.clicked.connect(self.configDischargeDialog)
        self.Dialog_Btns_ChargeDischarge_Layout.addWidget(self.Dialog_Btns_Discharge_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_ChargeDischarge_Layout)

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

    def get_StorControl_Name(self):
        return self.StorControl_Name.text()

    def get_ElementStorControl(self):
        return self.StorControl_Element_ComboBox.currentText()

    def get_TerminalStorControl(self):
        return self.StorControl_Terminal_ComboBox.currentText()

    def get_ReserveStorControl(self):
        return self.StorControl_Reserve.text()

    def get_WeightStorControl(self):
        return self.StorControl_Weight.text()

    def getStorage_Name(self):
        return self.StorageConfig_GroupBox_Nome_LineEdit.text()

    def getStorage_PercentageReserve(self):
        return self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()

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
            self.Dialog_Btns_Charge_Btn.setEnabled(False)
            self.Dialog_Btns_Discharge_Btn.setEnabled(False)
        else:
            self.StorControl_GroupBox.setVisible(False)
            self.StorControl_GroupBox_Selection.setEnabled(True)
            self.Dialog_Btns_Ok_Btn.setEnabled(True)
            self.Dialog_Btns_Cancel_Btn.setEnabled(True)
            self.Dialog_Btns_Charge_Btn.setEnabled(True)
            self.Dialog_Btns_Discharge_Btn.setEnabled(True)

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
        StorageController["StorageControllerName"] = unidecode.unidecode(self.get_StorControl_Name().replace(" ", "_"))
        StorageController["ElementList"] = []
        StorageController["Element"] = self.get_ElementStorControl()
        StorageController["Terminal"] = self.get_TerminalStorControl()
        StorageController["Reserve"] = self.get_ReserveStorControl()
        StorageController["Weight"] = {self.getStorage_Name(): self.get_WeightStorControl()}
        StorageController["ChargeMode"] = self.ChargeMode()
        StorageController["DischargeMode"] = self.DischargeMode()

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
                    ctd["ChargeMode"] = StorageController["ChargeMode"]
                    ctd["DischargeMode"] = StorageController["DischargeMode"]
                    QMessageBox(QMessageBox.Information, "Storage Controller",
                                "Storage Controller" + ctd["StorageControllerName"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()
        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def configChargeDialog(self):
        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            for i in [[self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn, self.DialogActPowPeakShaveLow],
                      [self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn, self.DialogActPowIPeakShaveLow],
                      [self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn, self.DialogActPowChargeTime]]:
                if i[0].isChecked():
                    i[1].StorageControllersTemporario = self.StorageControllersTemporario
                    i[1].StorControl_GroupBox_Selection_ComboBox = self.StorControl_GroupBox_Selection_ComboBox
                    i[1].updateDialog()
                    i[1].show()

    def configDischargeDialog(self):
        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            for i in [[self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn, self.DialogActPowPeakShave],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn, self.DialogActPowIPeakShave],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn, self.DialogActPowStorageContFollow],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn, self.DialogActPowSupport],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn, self.DialogActPowSchedule],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn, self.DialogActPowDischargeTime]]:
                if i[0].isChecked():
                    i[1].StorageControllersTemporario = self.StorageControllersTemporario
                    i[1].StorControl_GroupBox_Selection_ComboBox = self.StorControl_GroupBox_Selection_ComboBox
                    i[1].updateDialog()
                    i[1].show()

    def acceptStorageControlSelection(self):
        ChargeModeOK = False
        DischargeModeOK = False
        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            for i in [[self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn, self.DialogActPowPeakShaveLow],
                      [self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn, self.DialogActPowIPeakShaveLow],
                      [self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn, self.DialogActPowChargeTime]]:
                if i[0].isChecked():
                    if i[1].ChargeMode == {}:
                        QMessageBox(QMessageBox.Warning, "Storage Controller",
                                    "Selecione um Modo de Carga!",
                                    QMessageBox.Ok).exec()
                    else:
                        ChargeModeOK = True
                        for ctd in self.StorageControllersTemporario:
                            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                                ctd.update(i[1].ChargeMode)
            for i in [[self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn, self.DialogActPowPeakShave],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn, self.DialogActPowIPeakShave],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn, self.DialogActPowStorageContFollow],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn, self.DialogActPowSupport],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn, self.DialogActPowSchedule],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn, self.DialogActPowDischargeTime]]:
                if i[0].isChecked():
                    if i[1].DischargeMode == {}:
                        QMessageBox(QMessageBox.Warning, "Storage Controller",
                                    "Selecione um Modo de Descarga!",
                                    QMessageBox.Ok).exec()
                    else:
                        DischargeModeOK = True
                        for ctd in self.StorageControllersTemporario:
                            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                                ctd.update(i[1].DischargeMode)
                                ctd["ElementList"].append(self.getStorage_Name())
            if ChargeModeOK and DischargeModeOK:
                self.close()

    def cancelStorageControlSelection(self):
        self.clearStorControlParameters()
        self.close()

    def ChargeMode(self):
        for i in [[self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn, "PeakShaveLow"],
                  [self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn, "I-PeakShaveLow"],
                  [self.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn, "Time"]]:
            if i[0].isChecked():
                ChargeMode = i[1]
        return ChargeMode

    def DischargeMode(self):
         for i in [[self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn, "PeakShave"],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn, "I-PeakShave"],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn, "Follow"],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn, "Support"],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn, "Schedule"],
                      [self.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn, "Time"]]:
            if i[0].isChecked():
                DischargeMode = i[1]
         return DischargeMode

    def updateDialog(self):
        print("lloadshape")
        self.StorControl_GroupBox_Selection_ComboBox.clear()
        if not self.StorageControllersTemporario == []:
            for ctd in self.StorageControllersTemporario:
                if "ChargeMode" in ctd and "DischargeMode" in ctd:
                    if ctd["ChargeMode"] == self.ChargeMode() and ctd["DischargeMode"] == self.DischargeMode():
                        self.StorControl_GroupBox_Selection_ComboBox.addItem(ctd["StorageControllerName"])

        self.StorControl_Element_ComboBox.clear()
        self.StorControl_Element_ComboBox.addItems(self.OpenDSS.getElementList())

class C_ActPow_Charge_PeakShaveLow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Charge PeakShaveLow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho PeakShaveLow da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()

        self.ChargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kWTargetLow_Label = QLabel("Pot. alvo (kW):")
        self.Dialog_Layout.addWidget(self.kWTargetLow_Label, 2, 1, 1, 1)
        self.kWTargetLow_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.kWTargetLow_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kWTargetLow_LineEdit, 2, 2, 1, 2)
        self.BandLow_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.BandLow_Label, 3, 1, 1, 1)
        self.BandLow_LineEdit = QLineEdit()
        self.BandLow_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.BandLow_LineEdit, 3, 2, 1, 1)
        self.BandLow_Unit_ComboBox = QComboBox()
        self.BandLow_Unit_ComboBox.addItems(["kW", "% kW"])
        self.Dialog_Layout.addWidget(self.BandLow_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelPeakShaveLow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptPeakShaveLow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)

        self.setLayout(self.Dialog_Layout)

    def getkWTargetLow(self):
        return self.kWTargetLow_LineEdit.text()
    def getBandLowUnit(self):
        return self.BandLow_Unit_ComboBox.currentText
    def getBandWidthLow(self):
        return self.BandLow_LineEdit.text()

    def verificaLineEdits(self):
        if not self.kWTargetLow_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Potência alvo (kW) não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.BandLow_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptPeakShaveLow(self):
        if self.verificaLineEdits():
            self.ChargeMode["ChargeMode"] = "PeakShaveLow"
            self.ChargeMode["kWTargetLow"] = self.getkWTargetLow()
            if self.getBandLowUnit() == "kW":
                self.ChargeMode["kWBandLow"] = self.getBandWidthLow()
            else:
                self.ChargeMode["%kWBandLow"] = self.getBandWidthLow()
            self.close()
    def cancelPeakShaveLow(self):
        self.close()

    def clearParameters(self):
        self.kWTargetLow_LineEdit.setText("")
        self.BandLow_LineEdit.setText("")
        self.BandLow_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTargetLow" in ctd:
                    self.kWTargetLow_LineEdit.setText(ctd["kWTargetLow"])
                if "kWBandLow" in ctd:
                    self.BandLow_LineEdit.setText(ctd["kWBandLow"])
                    self.BandLow_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.BandLow_LineEdit.setText(ctd["%kWBandLow"])
                    self.BandLow_Unit_ComboBox.setCurrentIndex(1)

class C_ActPow_Charge_IPeakShaveLow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Charge IPeakShaveLow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho I-PeakShaveLow da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()
        self.ChargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kampsTargetLow_Label = QLabel("Corrente alvo (kAmps):")
        self.Dialog_Layout.addWidget(self.kampsTargetLow_Label, 2, 1, 1, 1)
        self.kampsTargetLow_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.kampsTargetLow_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kampsTargetLow_LineEdit, 2, 2, 1, 2)
        self.BandLow_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.BandLow_Label, 3, 1, 1, 1)
        self.BandLow_LineEdit = QLineEdit()
        self.BandLow_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.BandLow_LineEdit, 3, 2, 1, 1)
        self.BandLow_Unit_ComboBox = QComboBox()
        self.BandLow_Unit_ComboBox.addItems(["kAmps", "% kAmps"])
        self.Dialog_Layout.addWidget(self.BandLow_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelIPeakShaveLow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptIPeakShaveLow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def getkampsTargetLow(self):
        return self.kampsTargetLow_LineEdit.text()
    def getBandLowUnit(self):
        return self.BandLow_Unit_ComboBox.currentText
    def getBandWidthLow(self):
        return self.BandLow_LineEdit.text()

    def verificaLineEdits(self):
        if not self.kampsTargetLow_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a corrente alvo (kAmps) não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.BandLow_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptIPeakShaveLow(self):
        if self.verificaLineEdits():
            self.ChargeMode["ChargeMode"] = "I-PeakShaveLow"
            self.ChargeMode["kWTargetLow"] = self.getkampsTargetLow()
            if self.getBandLowUnit() == "kW":
                self.ChargeMode["kWBandLow"] = self.getBandWidthLow()
            else:
                self.ChargeMode["%kWBandLow"] = self.getBandWidthLow()
            self.close()
    def cancelIPeakShaveLow(self):
        self.close()

    def clearParameters(self):
        self.kampsTargetLow_LineEdit.setText("")
        self.BandLow_LineEdit.setText("")
        self.BandLow_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTargetLow" in ctd:
                    self.kampsTargetLow_LineEdit.setText(ctd["kWTargetLow"])
                if "kWBandLow" in ctd:
                    self.BandLow_LineEdit.setText(ctd["kWBandLow"])
                    self.BandLow_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.BandLow_LineEdit.setText(ctd["%kWBandLow"])
                    self.BandLow_Unit_ComboBox.setCurrentIndex(1)

class C_ActPow_Charge_Time_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Charge Time da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Time da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()

        self.ChargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeChargeTrigger = QLabel("Charge Trigger:")
        self.Dialog_Layout.addWidget(self.timeChargeTrigger, 2, 1, 1, 1)
        self.timeChargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeChargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeChargeTrigger_LineEdit, 2, 2, 1, 1)
        self.RateCharge_Label = QLabel("Taxa de carregamento (%):")
        self.Dialog_Layout.addWidget(self.RateCharge_Label, 3, 1, 1, 1)
        self.RateCharge_LineEdit = QLineEdit()
        self.RateCharge_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.RateCharge_LineEdit, 3, 2, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelTime)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptTime)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def gettimeChargeTrigger(self):
        return self.timeChargeTrigger_LineEdit.text()
    def getRateCharge(self):
        return self.RateCharge_LineEdit.text()

    def verificaLineEdits(self):
        if not self.timeChargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para o Charge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.RateCharge_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Taxa de carregamento não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptTime(self):
        if self.verificaLineEdits():
            self.ChargeMode["ChargeMode"] = "Time"
            self.ChargeMode["timeChargeTrigger"] = self.gettimeChargeTrigger()
            self.ChargeMode["%RateCharge"] = self.getRateCharge()
            self.close()
    def cancelTime(self):
        self.close()

    def clearParameters(self):
        self.timeChargeTrigger_LineEdit.setText("")
        self.RateCharge_LineEdit.setText("")

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeChargeTrigger" in ctd:
                    self.timeChargeTrigger_LineEdit.setText(ctd["timeChargeTrigger"])
                    self.RateCharge_LineEdit.setText(ctd["%RateCharge"])

class C_ActPow_Discharge_PeakShave_DispMode_Dialog(QDialog):# Classe Dialog Despacho Discharge PeakShave da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho PeakShave da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()

        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kWTarget_Label = QLabel("Pot. alvo (kW):")
        self.Dialog_Layout.addWidget(self.kWTarget_Label, 2, 1, 1, 1)
        self.kWTarget_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.kWTarget_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kWTarget_LineEdit, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_LineEdit = QLineEdit()
        self.Band_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Band_LineEdit, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["kW", "% kW"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def getkWTarget(self):
        return self.kWTarget_LineEdit.text()
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText
    def getBandWidth(self):
        return self.Band_LineEdit.text()

    def verificaLineEdits(self):
        if not self.kWTarget_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Potência alvo (kW) não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Band_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptPeakShave(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "PeakShave"
            self.DischargeMode["kWTarget"] = self.getkWTarget()
            if self.getBandUnit() == "kW":
                self.DischargeMode["kWBand"] = self.getBandWidth()
            else:
                self.DischargeMode["%kWBand"] = self.getBandWidth()
            self.close()
    def cancelPeakShave(self):
        self.close()

    def clearParameters(self):
        self.kWTarget_LineEdit.setText("")
        self.Band_LineEdit.setText("")
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTarget" in ctd:
                    self.kWTarget_LineEdit.setText(ctd["kWTarget"])
                if "kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["%kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

class C_ActPow_Discharge_IPeakShave_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge IPeakShave da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho I-PeakShave da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()
        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kampsTarget_Label = QLabel("Corrente alvo (kAmps):")
        self.Dialog_Layout.addWidget(self.kampsTarget_Label, 2, 1, 1, 1)
        self.kampsTarget_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.kampsTarget_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kampsTarget_LineEdit, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_LineEdit = QLineEdit()
        self.Band_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Band_LineEdit, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["kAmps", "% kAmps"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelIPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptIPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def getkampsTarget(self):
        return self.kampsTarget_LineEdit.text()
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText
    def getBandWidth(self):
        return self.Band_LineEdit.text()

    def verificaLineEdits(self):
        if not self.kampsTarget_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a corrente alvo (kAmps) não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Band_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptIPeakShave(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "I-PeakShave"
            self.DischargeMode["kWTarget"] = self.getkampsTarget()
            if self.getBandUnit() == "kW":
                self.DischargeMode["kWBand"] = self.getBandWidth()
            else:
                self.DischargeMode["%kWBand"] = self.getBandWidth()
            self.close()
    def cancelIPeakShave(self):
        self.close()

    def clearParameters(self):
        self.kampsTarget_LineEdit.setText("")
        self.Band_LineEdit.setText("")
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTarget" in ctd:
                    self.kampsTarget_LineEdit.setText(ctd["kWTarget"])
                if "kWBandLow" in ctd:
                    self.Band_LineEdit.setText(ctd["kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.Band_LineEdit.setText(ctd["%kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

class C_ActPow_Discharge_Follow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge Follow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Follow da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()

        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeDischargeTrigger_Label = QLabel("Discharge Trigger:")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_Label, 2, 1, 1, 1)
        self.timeDischargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeDischargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_LineEdit, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_LineEdit = QLineEdit()
        self.Band_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Band_LineEdit, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["kW", "% kW"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        self.kWThreshold_CheckBox = QCheckBox("Carga mínima para ativar\ndescarregamento:")
        self.kWThreshold_CheckBox.clicked.connect(self.EnableDisablekWThreshold)
        self.Dialog_Layout.addWidget(self.kWThreshold_CheckBox, 4, 1, 1, 1)
        self.kWThreshold_LineEdit = QLineEdit()
        self.kWThreshold_LineEdit.setEnabled(False)
        self.kWThreshold_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kWThreshold_LineEdit, 4, 2, 1, 2)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelFollow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptFollow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 5, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_LineEdit.text()
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText
    def getBandWidth(self):
        return self.Band_LineEdit.text()
    def getkWThreshold(self):
        return self.kWThreshold_LineEdit.text()

    def EnableDisablekWThreshold(self):
        if self.kWThreshold_CheckBox.isChecked():
            self.kWThreshold_LineEdit.setEnabled(True)
        else:
            self.kWThreshold_LineEdit.setEnabled(False)

    def verificaLineEdits(self):
        if not self.timeDischargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para o Discharge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Band_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor da Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif self.kWThreshold_CheckBox.isChecked():
                if not self.kWThreshold_LineEdit.hasAcceptableInput():
                    QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Carga mínima não é um valor válido!",
                                QMessageBox.Ok).exec()
                    return False
        else:
            return True

    def acceptFollow(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "Follow"
            self.DischargeMode["timeDischargeTrigger"] = self.gettimeDischargeTrigger()
            if self.getBandUnit() == "kW":
                self.DischargeMode["kWBand"] = self.getBandWidth()
            else:
                self.DischargeMode["%kWBand"] = self.getBandWidth()
            if self.kWThreshold_CheckBox.isChecked():
                self.DischargeMode["kWThreshold"] = self.getkWThreshold()
            self.close()
    def cancelFollow(self):
        self.close()

    def clearParameters(self):
        self.timeDischargeTrigger_LineEdit.setText("")
        self.kWThreshold_LineEdit.setText("")
        self.kWThreshold_CheckBox.setChecked(False)
        self.Band_LineEdit.setText("")
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_LineEdit.setText(ctd["timeDischargeTrigger"])
                if "kWThreshold" in ctd:
                    self.kWThreshold_LineEdit.setText(ctd["kWThreshold"])
                if "kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["kWBandLow"])
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.Band_LineEdit.setText(ctd["%kWBandLow"])
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

class C_ActPow_Discharge_Support_DispMode_Dialog(QDialog):# Classe Dialog Despacho Discharge Support da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Support da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()

        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kWTarget_Label = QLabel("Pot. alvo (kW):")
        self.Dialog_Layout.addWidget(self.kWTarget_Label, 2, 1, 1, 1)
        self.kWTarget_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.kWTarget_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kWTarget_LineEdit, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_LineEdit = QLineEdit()
        self.Band_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Band_LineEdit, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["kW", "% kW"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelSupport)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptSupport)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def getkWTarget(self):
        return self.kWTarget_LineEdit.text()
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText
    def getBandWidth(self):
        return self.Band_LineEdit.text()

    def verificaLineEdits(self):
        if not self.kWTarget_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Potência alvo (kW) não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Band_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptSupport(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "Support"
            self.DischargeMode["kWTarget"] = self.getkWTarget()
            if self.getBandUnit() == "kW":
                self.DischargeMode["kWBand"] = self.getBandWidth()
            else:
                self.DischargeMode["%kWBand"] = self.getBandWidth()
            self.close()
    def cancelSupport(self):
        self.close()

    def clearParameters(self):
        self.kWTarget_LineEdit.setText("")
        self.Band_LineEdit.setText("")
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTarget" in ctd:
                    self.kWTarget_LineEdit.setText(ctd["kWTarget"])
                if "kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["%kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

class C_ActPow_Discharge_Schedule_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge Schedule da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Schedule da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()
        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeDischargeTrigger = QLabel("Discharge Trigger:")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger, 2, 1, 1, 1)
        self.timeDischargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeDischargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_LineEdit, 2, 2, 1, 1)
        self.Tup_Label = QLabel("Duração da subida da rampa:")
        self.Dialog_Layout.addWidget(self.Tup_Label, 3, 1, 1, 1)
        self.Tup_LineEdit = QLineEdit()
        self.Tup_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Tup_LineEdit, 3, 2, 1, 1)
        self.Tflat_Label = QLabel("Duração do platô:")
        self.Dialog_Layout.addWidget(self.Tflat_Label, 4, 1, 1, 1)
        self.Tflat_LineEdit = QLineEdit()
        self.Tflat_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Tflat_LineEdit, 4, 2, 1, 1)
        self.Tdn_Label = QLabel("Duração da descida da rampa:")
        self.Dialog_Layout.addWidget(self.Tdn_Label, 5, 1, 1, 1)
        self.Tdn_LineEdit = QLineEdit()
        self.Tdn_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Tdn_LineEdit, 5, 2, 1, 1)
        self.RateDischarge_Label = QLabel("Taxa de descarregamento (%):")
        self.Dialog_Layout.addWidget(self.RateDischarge_Label, 6, 1, 1, 1)
        self.RateDischarge_LineEdit = QLineEdit()
        self.RateDischarge_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.RateDischarge_LineEdit, 6, 2, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelSchedule)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptSchedule)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 7, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_LineEdit.text()
    def getTup(self):
        return self.Tup_LineEdit.text()
    def getTflat(self):
        return self.Tflat_LineEdit.text()
    def getTdn(self):
        return self.Tdn_LineEdit.text()
    def getRateDischarge(self):
        return self.RateDischarge_LineEdit.text()

    def verificaLineEdits(self):
        if not self.timeDischargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para o Discharge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Tup_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Duração da subida da rampa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Tflat_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Duração do platô não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Tdn_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da Duração da descida da rampa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.RateDischarge_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Taxa de descarregamento não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptSchedule(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "Schedule"
            self.DischargeMode["timeDischargeTrigger"] = self.gettimeDischargeTrigger()
            self.DischargeMode["Tup"] = self.getTup()
            self.DischargeMode["Tflat"] = self.getTflat()
            self.DischargeMode["Tdn"] = self.getTdn()
            self.DischargeMode["%RatekW"] = self.getRateDischarge()
            self.close()
    def cancelSchedule(self):
        self.close()

    def clearParameters(self):
        self.timeDischargeTrigger_LineEdit.setText("")
        self.Tup_LineEdit.setText("")
        self.Tflat_LineEdit.setText("")
        self.Tdn_LineEdit.setText("")
        self.RateDischarge_LineEdit.setText("")

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_LineEdit.setText(ctd["timeDischargeTrigger"])
                    self.Tup_LineEdit.setText(ctd["Tup"])
                    self.Tflat_LineEdit.setText(ctd["Tflat"])
                    self.Tdn_LineEdit.setText(ctd["Tdn"])
                    self.RateDischarge_LineEdit.setText(ctd["%RatekW"])

class C_ActPow_Discharge_Time_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge Time da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Time da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()
        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeDischargeTrigger = QLabel("Discharge Trigger:")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger, 2, 1, 1, 1)
        self.timeDischargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeDischargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_LineEdit, 2, 2, 1, 1)
        self.RateDischarge_Label = QLabel("Taxa de descarregamento (%):")
        self.Dialog_Layout.addWidget(self.RateDischarge_Label, 3, 1, 1, 1)
        self.RateDischarge_LineEdit = QLineEdit()
        self.RateDischarge_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.RateDischarge_LineEdit, 3, 2, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelTime)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptTime)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_LineEdit.text()
    def getRateDischarge(self):
        return self.RateDischarge_LineEdit.text()

    def verificaLineEdits(self):
        if not self.timeDischargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para o Discharge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.RateDischarge_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Taxa de descarregamento não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptTime(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "Time"
            self.DischargeMode["timeDischargeTrigger"] = self.gettimeDischargeTrigger()
            self.DischargeMode["%RatekW"] = self.getRateDischarge()
            self.close()
    def cancelTime(self):
        self.close()

    def clearParameters(self):
        self.timeDischargeTrigger_LineEdit.setText("")
        self.RateDischarge_LineEdit.setText("")

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_LineEdit.setText(ctd["timeDischargeTrigger"])
                    self.RateDischarge_LineEdit.setText(ctd["%RatekW"])