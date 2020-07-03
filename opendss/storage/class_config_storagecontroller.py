from PyQt5.QtGui import QColor, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QRadioButton, QButtonGroup, QSpinBox
from PyQt5.QtCore import Qt

import opendss.class_opendss
import opendss.storage.class_select_dispatch_curve
import opendss.storage.class_select_price_curve
import opendss.storage.class_active_pow_dispmode_dialog
import opendss.storage.class_insert_storage_dialog
import opendss.storage.class_storagecontroller_chargemode_peakshavelow
import opendss.storage.class_storagecontroller_chargemode_ipeakshavelow
import opendss.storage.class_storagecontroller_chargemode_time
import opendss.storage.class_storagecontroller_dischargemode_peakshave
import opendss.storage.class_storagecontroller_dischargemode_ipeakshave
import opendss.storage.class_storagecontroller_dischargemode_follow
import opendss.storage.class_storagecontroller_dischargemode_support
import opendss.storage.class_storagecontroller_dischargemode_schedule
import opendss.storage.class_storagecontroller_dischargemode_time

import config as cfg
import unidecode


class C_ActPow_Config_StorageController_Dialog(QDialog): ## Classe Dialog configurações gerais do Storage Controller
    def __init__(self):
        super().__init__()

        self.titleWindow = "Configurar Storage Controller"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.DialogActPowPeakShaveLow = opendss.storage.class_storagecontroller_chargemode_peakshavelow.C_ActPow_Charge_PeakShaveLow_DispMode_Dialog()
        self.DialogActPowIPeakShaveLow = opendss.storage.class_storagecontroller_chargemode_ipeakshavelow.C_ActPow_Charge_IPeakShaveLow_DispMode_Dialog()
        self.DialogActPowChargeTime = opendss.storage.class_storagecontroller_chargemode_time.C_ActPow_Charge_Time_DispMode_Dialog()
        self.DialogActPowPeakShave = opendss.storage.class_storagecontroller_dischargemode_peakshave.C_ActPow_Discharge_PeakShave_DispMode_Dialog()
        self.DialogActPowIPeakShave = opendss.storage.class_storagecontroller_dischargemode_ipeakshave.C_ActPow_Discharge_IPeakShave_DispMode_Dialog()
        self.DialogActPowStorageContFollow = opendss.storage.class_storagecontroller_dischargemode_follow.C_ActPow_Discharge_Follow_DispMode_Dialog()
        self.DialogActPowSupport = opendss.storage.class_storagecontroller_dischargemode_support.C_ActPow_Discharge_Support_DispMode_Dialog()
        self.DialogActPowSchedule = opendss.storage.class_storagecontroller_dischargemode_schedule.C_ActPow_Discharge_Schedule_DispMode_Dialog()
        self.DialogActPowDischargeTime = opendss.storage.class_storagecontroller_dischargemode_time.C_ActPow_Discharge_Time_DispMode_Dialog()

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

        ### LineEdits
        self.StorControl_Name = QLineEdit()
        self.StorControl_Reserve = QLineEdit()
        #self.StorControl_Reserve.setText(str(self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()))

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

        self.StorControl_Layout.addWidget(self.StorControl_Name, 0, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Element_ComboBox, 1, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Terminal_ComboBox, 2, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Reserve, 3, 1, 1, 1)

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
        self.StorControl_Layout.addItem(self.StorControl_Btns_Layout, 4, 0, 1, 2)
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

    def getStorage_Name(self):
        return unidecode.unidecode(self.StorageConfig_GroupBox_Nome_LineEdit.text().replace(" ", "_"))

    def getStorage_PercentageReserve(self):
        return self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()

    def clearStorControlParameters(self):
        self.StorControl_Name.setText("")
        self.StorControl_Element_ComboBox.setCurrentIndex(0)
        self.StorControl_Terminal_ComboBox.setCurrentIndex(0)
        self.StorControl_Reserve.setText(self.getStorage_PercentageReserve())

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
            if ChargeModeOK and DischargeModeOK:
                for ctd in self.StorageControllersTemporario:  # Garante que dois StorageController não controlem um mesmo Storage
                    if self.getStorage_Name() in ctd["ElementList"] and (not ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText()):
                        self.StorageControllersTemporario.remove(ctd)

                for ctd in self.StorageControllersTemporario:
                    if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                        ctd["ElementList"].append(self.getStorage_Name())

                for ctd in self.StorageControllersTemporario:  # Garante que nao haja StorController que não controle nenhum Storage
                    if not ctd["ElementList"]:
                        self.StorageControllersTemporario.remove(ctd)
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
        self.StorControl_GroupBox_Selection_ComboBox.clear()
        if not self.StorageControllersTemporario == []:
            for ctd in self.StorageControllersTemporario:
                if "ChargeMode" in ctd and "DischargeMode" in ctd:
                    if ctd["ChargeMode"] == self.ChargeMode() and ctd["DischargeMode"] == self.DischargeMode():
                        self.StorControl_GroupBox_Selection_ComboBox.addItem(ctd["StorageControllerName"])

        self.StorControl_Element_ComboBox.clear()
        self.StorControl_Element_ComboBox.addItems(self.OpenDSS.getElementList())