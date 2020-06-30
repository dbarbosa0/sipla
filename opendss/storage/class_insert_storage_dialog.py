from PyQt5.QtGui import QColor, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

import csv
import random
import pathlib
import platform
import pyqtgraph
import class_exception

import opendss.class_opendss
import opendss.storage.class_active_pow_dispmode_dialog
import opendss.storage.class_reactive_pow_dispmode_dialog
import opendss.storage.class_config_eff_curve
import opendss.storage.class_config_storagecontroller
import config as cfg
import unidecode


class C_Insert_Storage_Dialog(QDialog):  ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Storage Insert"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.Storages = []
        self.StorageControllers = []

        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        # self.EffCurve = opendss.storage.class_config_eff_curve.C_Config_EffCurve_Dialog()
        # self.EffCurveFile = opendss.storage.class_config_eff_curve
        self.DispModeActPowDialog = opendss.storage.class_active_pow_dispmode_dialog.C_Active_Pow_DispMode_Dialog()
        self.DispModeReactPowDialog = opendss.storage.class_reactive_pow_dispmode_dialog.C_Reactive_Pow_DispMode_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QHBoxLayout()  # Layout da Dialog

        ####################### GroupBox Storages ############################################################
        self.Storages_GroupBox = QGroupBox("Storages")  # Criando a GroupBox Storages
        self.Storages_GroupBox.setFixedWidth(400)
        self.Storages_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do Storages é em Grid

        # Tree Widget
        self.Storages_GroupBox_TreeWidget = QTreeWidget()
        self.Storages_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Barra', 'Modo de Despacho'])
        self.Storages_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_TreeWidget, 1, 1, 1, 3)
        # Botao Adicionar
        self.Storages_GroupBox_Add_Btn = QPushButton("Adicionar")  # Botão de Adicionar dentro do GroupBox
        self.Storages_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.Storages_GroupBox_Add_Btn.clicked.connect(self.addStorages)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_Add_Btn, 3, 1, 1, 1)
        # Botao Excluir
        self.Storages_GroupBox_Excluir_Btn = QPushButton("Excluir")  # Botão de Excluir dentro do GroupBox
        self.Storages_GroupBox_Excluir_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Storages_GroupBox_Excluir_Btn.clicked.connect(self.removeStorages)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_Excluir_Btn, 3, 2, 1, 1)
        # Botão Editar
        self.Storages_GroupBox_Edit_Btn = QPushButton("Editar")  # Botão de editar dentro do GroupBox
        self.Storages_GroupBox_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.Storages_GroupBox_Edit_Btn.clicked.connect(self.editStorages)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_Edit_Btn, 3, 3, 1, 1)
        # Botao OK
        self.Storages_GroupBox_OK_Btn = QPushButton("OK")  # Botão OK dentro do GroupBox
        self.Storages_GroupBox_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Storages_GroupBox_OK_Btn.clicked.connect(self.acceptInsertStorage)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_OK_Btn, 4, 1, 1, 2)
        # Botao Cancelar
        self.Storages_GroupBox_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Storages_GroupBox_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Storages_GroupBox_Cancel_Btn.clicked.connect(self.cancelInsertStorage)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_Cancel_Btn, 4, 3, 1, 1)

        ############################ GroupBox Modos de Despacho ########################################################
        self.ModoDespacho_GroupBox = QGroupBox("Modos de Despacho")  # Criando a GroupBox Modos de Desapacho
        self.ModoDespacho_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do Modos de Despacho é em Grid

        # Botão Modo de Despacho da Potencia Ativa
        self.ModoDespacho_GroupBox_PotAtiv_Btn = QPushButton("Modo de Despacho da Pot. Ativa")
        self.ModoDespacho_GroupBox_PotAtiv_Btn.clicked.connect(self.DispModeActPow)
        self.ModoDespacho_GroupBox_Layout.addWidget(self.ModoDespacho_GroupBox_PotAtiv_Btn, 0, 0, 1, 1)
        # Botão Modo de Despacho da Potencia Reativa
        self.ModoDespacho_GroupBox_PotReat_Btn = QPushButton("Modo de Despacho da Pot. Reativa")
        self.ModoDespacho_GroupBox_PotReat_Btn.clicked.connect(self.DispModeReactPow)
        self.ModoDespacho_GroupBox_Layout.addWidget(self.ModoDespacho_GroupBox_PotReat_Btn, 0, 1, 1, 1)

        self.Storages_GroupBox.setLayout(self.Storages_GroupBox_Layout)  # define o Layout do GroupBox Storages
        self.ModoDespacho_GroupBox.setLayout(self.ModoDespacho_GroupBox_Layout)  # define o Layout do GroupBox ModoDespacho

        self.Dialog_Layout.addWidget(self.Storages_GroupBox)  # adiciona o GroupBox Storages ao Dialog

        ##################################### Tabs #####################################################################
        self.TabWidget = QTabWidget()
        self.TabConfig = StorageConfig()  # Tab das configurações gerais
        self.TabInversorConfig = InversorConfig()  # Tab das configurações do inversor
        self.TabWidget.addTab(self.TabConfig, "Configurações Gerais")
        self.TabWidget.addTab(self.TabInversorConfig, "Configurações do Inversor")

        ### Botões das Configurações
        self.Config_Btns_Layout = QHBoxLayout()
        self.Config_Btns_Layout.setAlignment(Qt.AlignRight)
        # Botao Restaurar Default
        self.Config_Btns_Default_Btn = QPushButton("Restaurar Default")  # Botão Default dentro do GroupBox
        self.Config_Btns_Default_Btn.setFixedHeight(30)
        self.Config_Btns_Default_Btn.setFixedWidth(200)
        self.Config_Btns_Default_Btn.clicked.connect(self.DefaultConfigParameters)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Default_Btn)
        # Botão OK
        self.Config_Btns_OK_Btn = QPushButton("OK")
        self.Config_Btns_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Config_Btns_OK_Btn.setFixedHeight(30)
        self.Config_Btns_OK_Btn.clicked.connect(self.AcceptAddEditStorage)
        self.Config_Btns_OK_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_OK_Btn)
        # Botao Cancelar
        self.Config_Btns_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Config_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Config_Btns_Cancel_Btn.setFixedHeight(30)
        self.Config_Btns_Cancel_Btn.clicked.connect(self.CancelAddEditStorage)
        self.Config_Btns_Cancel_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Cancel_Btn)

        ################################### GroupBox das Configurações #################################################
        self.StorageEInvConfig_GroupBox = QGroupBox()  # GroupBox que engloba as Tabs e Modo de Despacho
        self.StorageEInvConfig_GroupBox_Layout = QVBoxLayout()
        self.StorageEInvConfig_GroupBox.setVisible(False)

        self.StorageEInvConfig_GroupBox_Layout.addWidget(self.TabWidget)
        self.StorageEInvConfig_GroupBox_Layout.addWidget(self.ModoDespacho_GroupBox)  # adiciona o GroupBox ModoDespacho ao GroupBox superior
        self.StorageEInvConfig_GroupBox_Layout.addItem(self.Config_Btns_Layout)  # adiciona o Layout dos Botões das Configurações ao GroupBox superior

        self.StorageEInvConfig_GroupBox.setLayout(self.StorageEInvConfig_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.StorageEInvConfig_GroupBox)  # adiciona a GroupBox das Configurações ao Dialog

        self.setLayout(self.Dialog_Layout)

    def get_StorageName(self):
        return unidecode.unidecode(self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.text().replace(" ", "_"))

    def removeStorages(self):
        for ctd in range(self.Storages_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
            Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                self.Storages_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                for i in self.Storages:
                    if i["StorageName"] == Item.text(0):
                        self.Storages.remove(i)
                for i in self.StorageControllers:
                    if Item.text(0) in i['ElementList']:
                        i['ElementList'].remove(Item.text(0))
                    if i['ElementList'] == []:
                        self.StorageControllers.remove(i)

        self.updateDialog()

    def addStorages(self):
        self.DispModeActPowDialog.clearRadioBtns()
        self.EnableDisableParameters(True)
        self.DefaultConfigParameters()
        self.adjustSize()

    def editStorages(self):
        checkCont = 0
        try:
            for ctd in range(self.Storages_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
                if self.Storages_GroupBox_TreeWidget.topLevelItem(ctd).checkState(0) == Qt.Checked:
                    checkCont += 1
                    Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)

            if checkCont == 1:
                self.clearStorageParameters()
                for i in self.Storages:
                    if i["StorageName"] == Item.text(0):
                        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setText(i["StorageName"])
                        self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.setCurrentText(i["Conn"])
                        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.setCurrentText(i["Bus"])
                        self.TabConfig.StorageConfig_GroupBox_kW_LineEdit.setText(i["kW"])
                        self.TabConfig.StorageConfig_GroupBox_kv_LineEdit.setText(i["kV"])
                        self.TabConfig.StorageConfig_GroupBox_kWhrated_LineEdit.setText(i["kWhrated"])
                        self.TabConfig.StorageConfig_GroupBox_kWhstored_LineEdit.setText(i["kWhstored"])
                        self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit.setText(i["%reserve"])
                        self.TabConfig.StorageConfig_GroupBox_IdlingkW_LineEdit.setText(i["%IdlingkW"])
                        self.TabConfig.StorageConfig_GroupBox_Per100Charge_LineEdit.setText(i["%Charge"])
                        self.TabConfig.StorageConfig_GroupBox_Per100Discharge_LineEdit.setText(i["%Discharge"])
                        self.TabConfig.StorageConfig_GroupBox_EffCharge_LineEdit.setText(i["%EffCharge"])
                        self.TabConfig.StorageConfig_GroupBox_EffDischarge_LineEdit.setText(i["%EffDischarge"])
                        if i["state"] == "Idling":
                            self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Ocioso")
                        elif i["state"] == "Charging":
                            self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Carregando")
                        else:
                            self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Descarregando")
                        self.TabConfig.StorageConfig_GroupBox_vMinPu_LineEdit.setText(i["vMinpu"])
                        self.TabConfig.StorageConfig_GroupBox_vMaxPu_LineEdit.setText(i["vMaxpu"])
                        self.TabConfig.StorageConfig_GroupBox_R_LineEdit.setText(i["%R"])
                        self.TabConfig.StorageConfig_GroupBox_X_LineEdit.setText(i["%X"])

                        self.TabInversorConfig.InversorConfig_GroupBox_kVA_LineEdit.setText(i["kVA"])
                        self.TabInversorConfig.InversorConfig_GroupBox_kWrated_LineEdit.setText(i["kWrated"])
                        if i["varFollowInverter"] == "Yes":
                            self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText("Ativa CutIn/CutOut")
                        else:
                            self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText("Desativa CutIn/CutOut")
                        self.TabInversorConfig.InversorConfig_GroupBox_CutIn_LineEdit.setText(i["%CutIn"])
                        self.TabInversorConfig.InversorConfig_GroupBox_CutOut_LineEdit.setText(i["%CutOut"])
                        self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_LineEdit.setText(i["kvarMax"])
                        self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_LineEdit.setText(i["kvarMaxAbs"])
                        self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_LineEdit.setText(i["%PminNoVars"])
                        self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_LineEdit.setText(i["%PminkvarMax"])
                        if i["PFPriority"] == "True":
                            self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.setCurrentText("Sim")
                        else:
                            self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.setCurrentText("Não")
                        if i["WattPriority"] == "True":
                            self.TabInversorConfig.InversorConfig_GroupBox_WattPriority_ComboBox.setCurrentText("Sim")
                        else:
                            self.TabInversorConfig.InversorConfig_GroupBox_WattPriority_ComboBox.setCurrentText("Não")

                        if 'FP' in i['ReactPow']:
                            self.DispModeReactPowDialog.FPConst_RadioBtn.setChecked(True)
                            self.DispModeReactPowDialog.FPConst_LineEdit.setEnabled(True)
                            self.DispModeReactPowDialog.FPConst_LineEdit.setText(i['ReactPow']['FP'])
                        elif 'kvar' in i['ReactPow']:
                            self.DispModeReactPowDialog.kvarConst_RadioBtn.setChecked(True)
                            self.DispModeReactPowDialog.kvarConst_LineEdit.setEnabled(True)
                            self.DispModeReactPowDialog.kvarConst_LineEdit.setText(i['ReactPow']['kvar'])

                        ptsX = str(i["EffCurve"]["Xarray"]).strip('[]').replace("'", "")
                        ptsY = str(i["EffCurve"]["Yarray"]).strip('[]').replace("'", "")
                        self.TabInversorConfig.EffCurveFile.Config_EffCurve_GroupBox_TreeWidget_Item(self.TabInversorConfig.EffCurve.EffCurve_GroupBox_TreeWidget,
                                                                                                     i["EffCurve"]["EffCurveName"],
                                                                                                     ptsX,
                                                                                                     ptsY,
                                                                                                     cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])

                        if i["Carga/Descarga"] == "Sincronizados":
                            self.DispModeActPowDialog.DispSinc_Radio_Btn.setChecked(True)
                            self.DispModeActPowDialog.DispSinc_GroupBox.setEnabled(True)

                            if i['ModoCarga/Descarga'] == 'Default':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.setChecked(True)
                                self.DispModeActPowDialog.DialogActPowDefault.ChargeTrigger_LineEdit.setText(i["ActPow"]["ChargeTrigger"])
                                self.DispModeActPowDialog.DialogActPowDefault.DischargeTrigger_LineEdit.setText(i["ActPow"]["DischargeTrigger"])
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.TimeTrigger_LineEdit.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowDefault.TimeTrigger_LineEdit.setText(i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowDefault.TimeTrigger_CheckBox.setChecked(True)
                            elif i['ModoCarga/Descarga'] == 'Follow':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.setChecked(True)
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowFollow.TimeTrigger_LineEdit.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowFollow.TimeTrigger_LineEdit.setText(i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowFollow.TimeTrigger_CheckBox.setChecked(True)
                            elif i['ModoCarga/Descarga'] == 'LoadLevel':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.setChecked(True)
                                self.DispModeActPowDialog.DialogActPowLoadLevel.ChargeTrigger_LineEdit.setText(i["ActPow"]["ChargeTrigger"])
                                self.DispModeActPowDialog.DialogActPowLoadLevel.DischargeTrigger_LineEdit.setText(i["ActPow"]["DischargeTrigger"])
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowLoadLevel.TimeTrigger_LineEdit.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowLoadLevel.TimeTrigger_LineEdit.setText(i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowLoadLevel.TimeTrigger_CheckBox.setChecked(True)
                            elif i['ModoCarga/Descarga'] == 'Price':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.setChecked(True)
                                self.DispModeActPowDialog.DialogActPowPrice.ChargeTrigger_LineEdit.setText(i["ActPow"]["ChargeTrigger"])
                                self.DispModeActPowDialog.DialogActPowPrice.DischargeTrigger_LineEdit.setText(i["ActPow"]["DischargeTrigger"])
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.TimeTrigger_LineEdit.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowPrice.TimeTrigger_LineEdit.setText(i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowPrice.TimeTrigger_CheckBox.setChecked(True)
                            elif i['ModoCarga/Descarga'] == 'LoadShape':
                                self.DispModeActPowDialog.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.setChecked(True)

                        if i["Carga/Descarga"] == "Independentes":
                            self.DispModeActPowDialog.DispIndep_Radio_Btn.setChecked(True)
                            self.DispModeActPowDialog.DispIndep_GroupBox.setEnabled(True)

                            if i['ModoCarga'] == 'PeakShaveLow':
                                self.DispModeActPowDialog.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.setChecked(True)
                            elif i['ModoCarga'] == 'I-PeakShaveLow':
                                self.DispModeActPowDialog.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.setChecked(True)
                            elif i['ModoCarga'] == 'Time':
                                self.DispModeActPowDialog.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(True)

                            if i['ModoDescarga'] == 'PeakShave':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.setChecked(True)
                            elif i['ModoDescarga'] == 'I-PeakShave':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.setChecked(True)
                            elif i['ModoDescarga'] == 'Follow':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.setChecked(True)
                            elif i['ModoDescarga'] == 'Support':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.setChecked(True)
                            elif i['ModoDescarga'] == 'Schedule':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.setChecked(True)
                            elif i['ModoDescarga'] == 'Time':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(True)

                self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setEnabled(False)
                self.EnableDisableParameters(True)

            if checkCont > 1:
                raise class_exception.ExecConfigOpenDSS("Insert Storage",
                                                        "Selecione somente um Storage para editar!")
            elif checkCont == 0:
                raise class_exception.ExecConfigOpenDSS("Insert Storage",
                                                        "Selecione pelo menos um Storage para editar!")
        except:
            pass

    def DispModeActPow(self):
        if self.get_StorageName() == "":
            QMessageBox(QMessageBox.Information, "Storage",
                        "Antes de configurar o Despacho da Potência Ativa, escolha\num nome para o Storage!",
                        QMessageBox.Ok).exec()
        else:
            self.DispModeActPowDialog.ConfigStorageController.StorageConfig_GroupBox_Nome_LineEdit = self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit
            self.DispModeActPowDialog.DialogActPowLoadShape.StorageConfig_GroupBox_Nome_LineEdit = self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit
            self.DispModeActPowDialog.ConfigStorageController.StorageConfig_GroupBox_PercentageReserve_LineEdit = self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit
            self.DispModeActPowDialog.DialogActPowLoadShape.StorageConfig_GroupBox_PercentageReserve_LineEdit = self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit

            # self.TabConfig.ConfigStorageController.StorageControllers = self.StorageControllers
            # self.DispModeActPowDialog.DialogActPowLoadShape.StorageControllersTemporario = self.StorageControllers
            # self.TabConfig.ConfigStorageController.StorageControllersTemporario = self.StorageControllers
            self.DispModeActPowDialog.exec()

            self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setReadOnly(True)

            print("Controller :", self.StorageControllers)

    def DispModeReactPow(self):
        if self.get_StorageName() == "":
            QMessageBox(QMessageBox.Information, "Storage",
                        "Antes de configurar o Despacho da Potência Reativa, escolha\num nome para o Storage!",
                        QMessageBox.Ok).exec()
        else:
            self.DispModeReactPowDialog.show()

    def AcceptAddEditStorage(self):

        if self.TabConfig.verificaLineEdits() and self.TabInversorConfig.verificaLineEdits():

            if self.TabInversorConfig.EffCurve.dataEffCurve == {}:
                QMessageBox(QMessageBox.Information, "Insert Storage",
                            "Selecione uma curva de eficiência do Inversor!",
                            QMessageBox.Ok).exec()

            elif self.DispModeActPowDialog.None_Radio_Btn.isChecked():
                QMessageBox(QMessageBox.Information, "Insert Storage",
                            "Configure algum Modo de Despacho!",
                            QMessageBox.Ok).exec()

            else:
                countName = 0
                Storage = {}

                for e in self.StorageControllers: # Garante que dois StorageController não controlem um mesmo Storage
                    while self.get_StorageName() in e["ElementList"]:
                        e["ElementList"].remove(self.get_StorageName())

                ############# seta data das configurações gerais
                Storage["StorageName"] = self.get_StorageName()
                Storage["Conn"] = self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.currentText()
                Storage["Bus"] = self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText()
                Storage["kW"] = self.TabConfig.StorageConfig_GroupBox_kW_LineEdit.text()
                Storage["kV"] = self.TabConfig.StorageConfig_GroupBox_kv_LineEdit.text()
                Storage["kWhrated"] = self.TabConfig.StorageConfig_GroupBox_kWhrated_LineEdit.text()
                Storage["kWhstored"] = self.TabConfig.StorageConfig_GroupBox_kWhstored_LineEdit.text()
                Storage["%reserve"] = self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()
                Storage["%IdlingkW"] = self.TabConfig.StorageConfig_GroupBox_IdlingkW_LineEdit.text()
                Storage["%Charge"] = self.TabConfig.StorageConfig_GroupBox_Per100Charge_LineEdit.text()
                Storage["%Discharge"] = self.TabConfig.StorageConfig_GroupBox_Per100Discharge_LineEdit.text()
                Storage["%EffCharge"] = self.TabConfig.StorageConfig_GroupBox_EffCharge_LineEdit.text()
                Storage["%EffDischarge"] = self.TabConfig.StorageConfig_GroupBox_EffDischarge_LineEdit.text()
                if self.TabConfig.StorageConfig_GroupBox_state_ComboBox.currentText() == "Ocioso":
                    Storage["state"] = "Idling"
                if self.TabConfig.StorageConfig_GroupBox_state_ComboBox.currentText() == "Carregando":
                    Storage["state"] = "Charging"
                if self.TabConfig.StorageConfig_GroupBox_state_ComboBox.currentText() == "Descarregando":
                    Storage["state"] = "Discharging"
                Storage["vMinpu"] = self.TabConfig.StorageConfig_GroupBox_vMinPu_LineEdit.text()
                Storage["vMaxpu"] = self.TabConfig.StorageConfig_GroupBox_vMaxPu_LineEdit.text()
                Storage["%R"] = self.TabConfig.StorageConfig_GroupBox_R_LineEdit.text()
                Storage["%X"] = self.TabConfig.StorageConfig_GroupBox_X_LineEdit.text()
                ############# seta data das configurações do inversor
                Storage["kVA"] = self.TabInversorConfig.InversorConfig_GroupBox_kVA_LineEdit.text()
                Storage["kWrated"] = self.TabInversorConfig.InversorConfig_GroupBox_kWrated_LineEdit.text()
                if self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.currentText() == "Ativa CutIn/CutOut":
                    Storage["varFollowInverter"] = "Yes"
                else:
                    Storage["varFollowInverter"] = "No"
                Storage["%CutIn"] = self.TabInversorConfig.InversorConfig_GroupBox_CutIn_LineEdit.text()
                Storage["%CutOut"] = self.TabInversorConfig.InversorConfig_GroupBox_CutOut_LineEdit.text()
                Storage["kvarMax"] = self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_LineEdit.text()
                Storage["kvarMaxAbs"] = self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_LineEdit.text()
                Storage["%PminNoVars"] = self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_LineEdit.text()
                Storage["%PminkvarMax"] = self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_LineEdit.text()
                if self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.currentText() == "Sim":
                    Storage["PFPriority"] = "True"
                else:
                    Storage["PFPriority"] = "False"
                if self.TabInversorConfig.InversorConfig_GroupBox_WattPriority_ComboBox.currentText() == "Sim":
                    Storage["WattPriority"] = "True"
                else:
                    Storage["WattPriority"] = "False"
                Storage.update({"EffCurve": self.TabInversorConfig.EffCurve.dataEffCurve})
                Storage.update({"ReactPow": self.DispModeReactPowDialog.ReactPow})

                if self.DispModeActPowDialog.DispSinc_Radio_Btn.isChecked():
                    Storage["Carga/Descarga"] = "Sincronizados"
                    for i in [[self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn, "Default"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn, "Follow"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn,"LoadLevel"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn, "Price"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn,"LoadShape"]]:
                        if i[0].isChecked():
                            Storage["ModoCarga/Descarga"] = i[1]

                elif self.DispModeActPowDialog.DispIndep_Radio_Btn.isChecked():
                    Storage["Carga/Descarga"] = "Independentes"
                    Storage["ModoCarga"] = self.DispModeActPowDialog.ConfigStorageController.ChargeMode()
                    Storage["ModoDescarga"] = self.DispModeActPowDialog.ConfigStorageController.DischargeMode()

                if self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.isEnabled():  # Se estiver adicionando um Storage
                    for ctd in range(0, self.Storages_GroupBox_TreeWidget.topLevelItemCount()):
                        Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)

                        if Item.text(0) == self.get_StorageName():
                            countName += 1

                    if countName == 0:
                        if Storage["Carga/Descarga"] == "Sincronizados":

                            Storage_TreeWidget_Item(self.Storages_GroupBox_TreeWidget,
                                                    self.get_StorageName(),
                                                    self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText(),
                                                    Storage["ModoCarga/Descarga"])

                            if Storage["ModoCarga/Descarga"] == "Default":
                                Storage.update({"ActPow": self.DispModeActPowDialog.DialogActPowDefault.DefaultParameters})
                            elif Storage["ModoCarga/Descarga"] == "Follow":
                                Storage.update({"ActPow": self.DispModeActPowDialog.DialogActPowFollow.FollowParameters})
                            elif Storage["ModoCarga/Descarga"] == "LoadLevel":
                                Storage.update({"ActPow": self.DispModeActPowDialog.DialogActPowLoadLevel.LoadLevelParameters})
                            elif Storage["ModoCarga/Descarga"] == "Price":
                                Storage.update({"ActPow": self.DispModeActPowDialog.DialogActPowPrice.PriceParameters})
                            elif Storage["ModoCarga/Descarga"] == "LoadShape":
                                Storage.update({"ActPow": None})
                                StorageCont = 0
                                for i in self.StorageControllers:
                                    if self.get_StorageName() in i["ElementList"]:
                                        StorageCont += 1
                                if StorageCont == 0:
                                    for ctd in self.DispModeActPowDialog.DialogActPowLoadShape.StorageControllersTemporario:
                                        if self.get_StorageName() in ctd["ElementList"]:
                                            self.StorageControllers.append(ctd.copy())

                        if Storage["Carga/Descarga"] == "Independentes":
                            Storage.update({"ActPow": None})
                            StorageCont = 0
                            for i in self.StorageControllers:
                                if self.get_StorageName() in i["ElementList"]:
                                    StorageCont += 1
                            if StorageCont == 0:
                                for ctd in self.DispModeActPowDialog.ConfigStorageController.StorageControllersTemporario:
                                    if self.get_StorageName() in ctd["ElementList"]:
                                        self.StorageControllers.append(ctd.copy())

                            Storage_TreeWidget_Item(self.Storages_GroupBox_TreeWidget,
                                                    self.get_StorageName(),
                                                    self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText(),
                                                    Storage["ModoCarga"] + "/" + Storage["ModoDescarga"])

                        self.Storages.append(Storage)

                    else:
                        QMessageBox(QMessageBox.Warning, "Insert Storage",
                                    "Não foi possível adicionar, pois já existe um Storage com esse nome.",
                                    QMessageBox.Ok).exec()

                else:  # Se estiver editando um Storage
                    for ctd in self.Storages:
                        if ctd["StorageName"] == Storage["StorageName"]:

                            ctd["Conn"] = Storage["Conn"]
                            ctd["Bus"] = Storage["Bus"]
                            ctd["kW"] = Storage["kW"]
                            ctd["kV"] = Storage["kV"]
                            ctd["kWhrated"] = Storage["kWhrated"]
                            ctd["kWhstored"] = Storage["kWhstored"]
                            ctd["%reserve"] = Storage["%reserve"]
                            ctd["%IdlingkW"] = Storage["%IdlingkW"]
                            ctd["%Charge"] = Storage["%Charge"]
                            ctd["%Discharge"] = Storage["%Discharge"]
                            ctd["%EffCharge"] = Storage["%EffCharge"]
                            ctd["%EffDischarge"] = Storage["%EffDischarge"]
                            ctd["state"] = Storage["state"]
                            ctd["vMinpu"] = Storage["vMinpu"]
                            ctd["vMaxpu"] = Storage["vMaxpu"]
                            ctd["%R"] = Storage["%R"]
                            ctd["%X"] = Storage["%X"]

                            ctd["kVA"] = Storage["kVA"]
                            ctd["kWrated"] = Storage["kWrated"]
                            ctd["%CutIn"] = Storage["%CutIn"]
                            ctd["%CutOut"] = Storage["%CutOut"]
                            ctd["kvarMax"] = Storage["kvarMax"]
                            ctd["kvarMaxAbs"] = Storage["kvarMaxAbs"]
                            ctd["%PminNoVars"] = Storage["%PminNoVars"]
                            ctd["%PminkvarMax"] = Storage["%PminkvarMax"]
                            ctd["PFPriority"] = Storage["PFPriority"]
                            ctd["WattPriority"] = Storage["WattPriority"]

                            if Storage["Carga/Descarga"] == "Sincronizados":
                                ctd["Carga/Descarga"] = Storage["Carga/Descarga"]

                                for i in [["Default", self.DispModeActPowDialog.DialogActPowDefault.DefaultParameters],
                                          ["Follow", self.DispModeActPowDialog.DialogActPowFollow.FollowParameters],
                                          ["LoadLevel", self.DispModeActPowDialog.DialogActPowLoadLevel.LoadLevelParameters],
                                          ["Price", self.DispModeActPowDialog.DialogActPowPrice.PriceParameters]]:
                                    if Storage["ModoCarga/Descarga"] == i[0]:
                                        ctd["ModoCarga/Descarga"] = Storage["ModoCarga/Descarga"]
                                        ctd.update({"ActPow": i[1]})

                                if Storage["ModoCarga/Descarga"] == "LoadShape":
                                    ctd["ModoCarga/Descarga"] = Storage["ModoCarga/Descarga"]
                                    ctd.update({"ActPow": None})

                                    if not self.DispModeActPowDialog.DialogActPowLoadShape.StorageControllersTemporario == []:
                                        # for i in self.StorageControllers:
                                        #     while self.get_StorageName() in i["ElementList"]:
                                        #         i["ElementList"].remove(self.get_StorageName())
                                        for i in self.DispModeActPowDialog.DialogActPowLoadShape.StorageControllersTemporario:
                                            if self.get_StorageName() in i["ElementList"]:
                                                self.StorageControllers.append(i.copy())

                                for ctd in range(self.Storages_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
                                    Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)
                                    if Item.text(0) == self.get_StorageName():
                                        self.Storages_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                                        Storage_TreeWidget_Item(self.Storages_GroupBox_TreeWidget,
                                                        self.get_StorageName(),
                                                        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText(),
                                                        Storage["ModoCarga/Descarga"])

                            elif Storage["Carga/Descarga"] == "Independentes":
                                ctd["Carga/Descarga"] = Storage["Carga/Descarga"]
                                ctd['ModoCarga'] = Storage['ModoCarga']
                                ctd['ModoDescarga'] = Storage['ModoDescarga']
                                ctd.update({"ActPow": None})

                                if not self.DispModeActPowDialog.ConfigStorageController.StorageControllersTemporario == []:
                                    # for i in self.StorageControllers:
                                    #     while self.get_StorageName() in i["ElementList"]:
                                    #         i["ElementList"].remove(self.get_StorageName())
                                    for i in self.DispModeActPowDialog.ConfigStorageController.StorageControllersTemporario:
                                        if self.get_StorageName() in i["ElementList"]:
                                            self.StorageControllers.append(i.copy())

                                for ctd in range(0, self.Storages_GroupBox_TreeWidget.topLevelItemCount()):
                                    Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)
                                    if Item.text(0) == self.get_StorageName():
                                        self.Storages_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                                        Storage_TreeWidget_Item(self.Storages_GroupBox_TreeWidget,
                                                                self.get_StorageName(),
                                                                self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText(),
                                                                Storage["ModoCarga"] + "/" + Storage["ModoDescarga"])

                self.updateDialog()
                self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setEnabled(True)
                self.clearStorageParameters()
                self.DefaultConfigParameters()
                self.EnableDisableParameters(False)
                self.adjustSize()

    def CancelAddEditStorage(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setEnabled(True)
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setReadOnly(False)
        self.EnableDisableParameters(False)
        self.adjustSize()

    def acceptInsertStorage(self):
        if not self.StorageControllers == []:
            for ctd in self.StorageControllers:
                if not ctd["ElementList"]: # Garante que nao haja StorageController que não controle nenhum Storage
                    self.StorageControllers.remove(ctd)
                ctd["ElementList"] = list(set(ctd["ElementList"]))
        self.OpenDSS.Storages = self.Storages
        self.OpenDSS.StorageControllers = self.StorageControllers
        print("insert:")
        print(self.Storages)
        print(self.StorageControllers)

        self.clearStorageParameters()
        self.DefaultConfigParameters()
        self.close()

    def cancelInsertStorage(self):
        self.clearStorageParameters()
        self.DefaultConfigParameters()
        self.close()

    def EnableDisableParameters(self, bool):
        if bool:
            self.StorageEInvConfig_GroupBox.setVisible(True)
            self.Storages_GroupBox.setVisible(False)
        else:
            self.StorageEInvConfig_GroupBox.setVisible(False)
            self.Storages_GroupBox.setVisible(True)

    def updateDialog(self):
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.clear()
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.addItems(self.OpenDSS.getBusList())

    def DefaultConfigParameters(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.setCurrentText("Y")
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_kW_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kv_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kWhrated_LineEdit.setText("50")
        self.TabConfig.StorageConfig_GroupBox_kWhstored_LineEdit.setText("50")
        self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit.setText("20")
        self.TabConfig.StorageConfig_GroupBox_IdlingkW_LineEdit.setText("1")
        self.TabConfig.StorageConfig_GroupBox_Per100Charge_LineEdit.setText("100")
        self.TabConfig.StorageConfig_GroupBox_Per100Discharge_LineEdit.setText("100")
        self.TabConfig.StorageConfig_GroupBox_EffCharge_LineEdit.setText("90")
        self.TabConfig.StorageConfig_GroupBox_EffDischarge_LineEdit.setText("90")
        self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Ocioso")
        self.TabConfig.StorageConfig_GroupBox_vMinPu_LineEdit.setText("0.9")
        self.TabConfig.StorageConfig_GroupBox_vMaxPu_LineEdit.setText("1.1")
        self.TabConfig.StorageConfig_GroupBox_R_LineEdit.setText("0")
        self.TabConfig.StorageConfig_GroupBox_X_LineEdit.setText("50")

        self.TabInversorConfig.InversorConfig_GroupBox_kVA_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_kWrated_LineEdit.setText("25")
        self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText("Desativa CutIn/CutOut")
        self.TabInversorConfig.InversorConfig_GroupBox_CutIn_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_CutOut_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_LineEdit.setText("999999")
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_LineEdit.setText("999999")
        self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.setCurrentText("Não")
        self.TabInversorConfig.InversorConfig_GroupBox_WattPriority_ComboBox.setCurrentText("Pot. Reativa")

    def clearStorageParameters(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setReadOnly(False)

        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_kW_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kv_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kWhrated_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kWhstored_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_IdlingkW_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_Per100Charge_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_Per100Discharge_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_EffCharge_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_EffDischarge_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_vMinPu_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_vMaxPu_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_R_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_X_LineEdit.setText("")

        self.TabInversorConfig.InversorConfig_GroupBox_kVA_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_kWrated_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentIndex(0)
        self.TabInversorConfig.InversorConfig_GroupBox_CutIn_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_CutOut_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.setCurrentIndex(0)

        self.TabInversorConfig.EffCurve.EffCurve_GroupBox_TreeWidget.clear() #Limpa o TreeWidget e o plot da Curva de Eficiencia
        self.TabInversorConfig.EffCurve.graphWidget.clear()
        self.TabInversorConfig.EffCurve.dataEffCurve = {}

        self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.restoreParameters()
        self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.restoreParameters()


class StorageConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIStorageConfig()


    def InitUIStorageConfig(self):

        self.ConfigStorageController = opendss.storage.class_config_storagecontroller.C_ActPow_Config_StorageController_Dialog()
        ### Valida as entradas dos LineEdits
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.LineEditsValidos0 = QDoubleValidator()
        self.LineEditsValidos0.setBottom(0.0)

        ###################### GroupBox StorageConfig #######################################################
        self.StorageConfig_GroupBox = QGroupBox()  # Criando a GroupBox StorageConfig
        self.StorageConfig_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do StorageConfig é em Grid
        # Configurar nome do elemento Storage
        self.StorageConfig_GroupBox_Nome_Label = QLabel("Nome")
        self.StorageConfig_GroupBox_Nome_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Nome_Label, 0, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Nome_LineEdit, 0, 1, 1, 1)
        # Configurar propriedade "conn"
        self.StorageConfig_GroupBox_conn_Label = QLabel("Tipo de conexão")
        self.StorageConfig_GroupBox_conn_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_conn_ComboBox.addItems(["Y", "LN", "Delta", "LN"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_conn_Label, 0, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_conn_ComboBox, 0, 3, 1, 1)
        # Configurar propriedade "Bus"
        self.StorageConfig_GroupBox_Bus_Label = QLabel("Barra de conexão")
        self.StorageConfig_GroupBox_Bus_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Bus_Label, 1, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Bus_ComboBox, 1, 1, 1, 1)
        # Configurar propriedade "kW" (potência de saída)
        self.StorageConfig_GroupBox_kW_Label = QLabel("Potência nominal de saída (kW)")
        self.StorageConfig_GroupBox_kW_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_kW_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kW_Label, 2, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kW_LineEdit, 2, 1, 1, 1)
        # Configurar propriedade "kv" (tensão de saída)
        self.StorageConfig_GroupBox_kv_Label = QLabel("Tensão de saída (kV)")
        self.StorageConfig_GroupBox_kv_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_kv_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kv_Label, 1, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kv_LineEdit, 1, 3, 1, 1)
         # Configurar propriedade "kWhrated" (capacidade nominal do Storage em kWh)
        self.StorageConfig_GroupBox_kWhrated_Label = QLabel("Capacidade Nominal (kWh)")
        self.StorageConfig_GroupBox_kWhrated_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_kWhrated_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhrated_Label, 2, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhrated_LineEdit, 2, 3, 1, 1)
        # Configurar propriedade "kWhstored" (quantidade atual de energia armazenada em kWh)
        self.StorageConfig_GroupBox_kWhstored_Label = QLabel("Energia armazenada atual (kWh)")
        self.StorageConfig_GroupBox_kWhstored_Label.setToolTip("Energia Armazenada atual em kWh")
        self.StorageConfig_GroupBox_kWhstored_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_kWhstored_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhstored_Label, 3, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhstored_LineEdit, 3, 3, 1, 1)
        # Configurar propriedade "%reserve" (quantidade de energia para ser deixada como reserva em %)
        self.StorageConfig_GroupBox_PercentageReserve_Label = QLabel("Energia reserva (%)")
        self.StorageConfig_GroupBox_PercentageReserve_Label.setToolTip(
            "Percentual da capacidade de armazenamento nominal (kWh)\npara ser mantida em reserva. É tratado como nível mínimo de\ndescarregamento, em situações normais")
        self.StorageConfig_GroupBox_PercentageReserve_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_PercentageReserve_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_PercentageReserve_Label, 3, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_PercentageReserve_LineEdit, 3, 1, 1, 1)
        # Configurar propriedade "%IdlingkW" (kW consumida por perdas por inatividade)
        self.StorageConfig_GroupBox_IdlingkW_Label = QLabel("Perdas por inatividade (%)")
        self.StorageConfig_GroupBox_IdlingkW_Label.setToolTip(
            "Percentual de potência ativa nominal (kW)\nconsumida por perdas por inatividade.")
        self.StorageConfig_GroupBox_IdlingkW_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_IdlingkW_LineEdit.setValidator(self.LineEditsValidos0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_IdlingkW_Label, 4, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_IdlingkW_LineEdit, 4, 3, 1, 1)
        # Configurar propriedade "%Charge" (Taxa de carregamento em % da potencia nominal)
        self.StorageConfig_GroupBox_Per100Charge_Label = QLabel("Taxa de carregamento (%)")
        self.StorageConfig_GroupBox_Per100Charge_Label.setToolTip(
            "Taxa de carregamento em percentual da\npotência ativa nominal (kW).")
        self.StorageConfig_GroupBox_Per100Charge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Per100Charge_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Charge_Label, 4, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Charge_LineEdit, 4, 1, 1, 1)
        # Configurar propriedade "%Discharge" (Taxa de descarregamento em % da potencia nominal)
        self.StorageConfig_GroupBox_Per100Discharge_Label = QLabel("Taxa de descarregamento (%)")
        self.StorageConfig_GroupBox_Per100Discharge_Label.setToolTip(
            "Taxa de descarregamento em percentual da\npotência ativa nominal (kW).")
        self.StorageConfig_GroupBox_Per100Discharge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Per100Discharge_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Discharge_Label, 5, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Discharge_LineEdit, 5, 3, 1, 1)
        # Configurar propriedade "%EffCharge" (% de eficiencia ao carregar o Storage)
        self.StorageConfig_GroupBox_EffCharge_Label = QLabel("Eficiência do carregamento (%) ")
        self.StorageConfig_GroupBox_EffCharge_Label.setToolTip("Percentual de eficiência para o carregamento")
        self.StorageConfig_GroupBox_EffCharge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_EffCharge_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffCharge_Label, 5, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffCharge_LineEdit, 5, 1, 1, 1)
        # Configurar propriedade "%EffDischarge" (% de eficiencia ao descarregar o Storage)
        self.StorageConfig_GroupBox_EffDischarge_Label = QLabel("Eficiência do descarregamento (%)")
        self.StorageConfig_GroupBox_EffDischarge_Label.setToolTip("Percentual de eficiência para o carregamento")
        self.StorageConfig_GroupBox_EffDischarge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_EffDischarge_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffDischarge_Label, 6, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffDischarge_LineEdit, 6, 3, 1, 1)
        # Configurar propriedade "state" (seta o estado de operação)
        self.StorageConfig_GroupBox_state_Label = QLabel("Estado de operação")
        self.StorageConfig_GroupBox_state_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_state_ComboBox.addItems(["Ocioso", "Carregando", "Descarregando"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_state_Label, 6, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_state_ComboBox, 6, 1, 1, 1)
        # Configurar propriedade "vminpu" (tensão minima, em pu, para a qual o modelo se aplica)
        self.StorageConfig_GroupBox_vMinPu_Label = QLabel("Tensão mínima (p.u.)")
        self.StorageConfig_GroupBox_vMinPu_Label.setToolTip(
            "Tensão mínima em p.u. para a qual o modelo se aplica. Abaixo\ndesse valor,o modelo da carga se torna um modelo de impedância constante.")
        self.StorageConfig_GroupBox_vMinPu_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_vMinPu_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMinPu_Label, 7, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMinPu_LineEdit, 7, 1, 1, 1)
        # Configurar propriedade "vmaxpu" (tensão maxima, em pu, para a qual o modelo se aplica)
        self.StorageConfig_GroupBox_vMaxPu_Label = QLabel("Tensão máxima (p.u.)")
        self.StorageConfig_GroupBox_vMaxPu_Label.setToolTip(
            "Tensão máxima em p.u. para a qual o modelo se aplica. Abaixo\ndesse valor,o modelo da carga se torna um modelo de impedância constante.")
        self.StorageConfig_GroupBox_vMaxPu_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_vMaxPu_LineEdit.setValidator(self.LineEditsValidos)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMaxPu_Label, 7, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMaxPu_LineEdit, 7, 3, 1, 1)
        # Configurar propriedade "%R" (resistência interna equivalente percentual)
        self.StorageConfig_GroupBox_R_Label = QLabel("Resistência interna (%)")
        self.StorageConfig_GroupBox_R_Label.setToolTip("Percentual da resistência interna equivalente")
        self.StorageConfig_GroupBox_R_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_R_LineEdit.setValidator(self.LineEditsValidos0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_R_Label, 8, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_R_LineEdit, 8, 1, 1, 1)
        # Configurar propriedade "%X" (reatância interna equivalente percentual)
        self.StorageConfig_GroupBox_X_Label = QLabel("Reatância interna (%)")
        self.StorageConfig_GroupBox_X_Label.setToolTip("Percentual da reatância interna equivalente")
        self.StorageConfig_GroupBox_X_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_X_LineEdit.setValidator(self.LineEditsValidos0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_X_Label, 8, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_X_LineEdit, 8, 3, 1, 1)

        self.StorageConfig_GroupBox.setLayout(
            self.StorageConfig_GroupBox_Layout)  # define o Layout do GroupBox StoragesConfig

        self.Tab_layout = QGridLayout()
        self.Tab_layout.addWidget(self.StorageConfig_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Tab_layout)

    def verificaLineEdits(self):
        for i in [
            self.StorageConfig_GroupBox_kW_LineEdit,
            self.StorageConfig_GroupBox_kv_LineEdit,
            self.StorageConfig_GroupBox_kWhrated_LineEdit,
            self.StorageConfig_GroupBox_kWhstored_LineEdit,
            self.StorageConfig_GroupBox_PercentageReserve_LineEdit,
            self.StorageConfig_GroupBox_Per100Charge_LineEdit,
            self.StorageConfig_GroupBox_IdlingkW_LineEdit,
            self.StorageConfig_GroupBox_Per100Discharge_LineEdit,
            self.StorageConfig_GroupBox_EffCharge_LineEdit,
            self.StorageConfig_GroupBox_EffDischarge_LineEdit,
            self.StorageConfig_GroupBox_vMinPu_LineEdit,
            self.StorageConfig_GroupBox_vMaxPu_LineEdit,
            self.StorageConfig_GroupBox_R_LineEdit,
            self.StorageConfig_GroupBox_X_LineEdit,
        ]:
            if not i.hasAcceptableInput():
                QMessageBox(QMessageBox.Warning, "Insert Storage","Algum valor inserido nas Configurações Gerais não é válido!\n Verifique os valores inseridos!",
                        QMessageBox.Ok).exec()
                return False
            else:
                return True

class InversorConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIInversorConfig()

        self.EffCurve = opendss.storage.class_config_eff_curve.C_Config_EffCurve_Dialog()
        self.EffCurveFile = opendss.storage.class_config_eff_curve

    def InitUIInversorConfig(self):

        ### Valida as entradas dos LineEdits
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.LineEditsValidos0 = QDoubleValidator()
        self.LineEditsValidos0.setBottom(0.0)
        ############################ GroupBox Configuracoes do Inversor ################################################
        self.InversorConfig_GroupBox = QGroupBox(
            "Configurações do Inversor")  # Criando a GroupBox Configurações do Inversor
        self.InversorConfig_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InversorConfig é em Grid
        # Configurar propriedade "kVA"
        self.InversorConfig_GroupBox_kVA_Label = QLabel("Pot. aparente máxima (kVA)")
        self.InversorConfig_GroupBox_kVA_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_kVA_LineEdit.setValidator(self.LineEditsValidos)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kVA_Label, 0, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kVA_LineEdit, 0, 1, 1, 1)
        # Configurar propriedade "kWrated" (Pot. ativa máxima de saída do inversor)
        self.InversorConfig_GroupBox_kWrated_Label = QLabel("Pot. ativa máxima (kW)")
        self.InversorConfig_GroupBox_kWrated_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_kWrated_LineEdit.setValidator(self.LineEditsValidos)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kWrated_Label, 0, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kWrated_LineEdit, 0, 3, 1, 1)
        # Configurar propriedade "%varFollowInverter" (True ativa %CutIn %CutOut False desativa %CutIn %CutOut)
        self.InversorConfig_GroupBox_varFollowInverter_Label = QLabel("Seta status do CutIn/CutOut")
        self.InversorConfig_GroupBox_varFollowInverter_Label.setToolTip("Quando desativado, o inversor gera/absorve \
potência reativa independentemente\ndo status do inversor. Quando ativado, a geração/absorção de potência reativa\nirá \
cessar quando o inversor estiver desligado devido a queda da potência DC\nabaixo do CutOut. A geração/absorção vai \
começar novamente quando a potência\nDC estiver acima de CutIn")
        self.InversorConfig_GroupBox_varFollowInverter_ComboBox = QComboBox()
        self.InversorConfig_GroupBox_varFollowInverter_ComboBox.addItems(["Ativa CutIn/CutOut", "Desativa CutIn/CutOut"])
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_varFollowInverter_Label, 1, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_varFollowInverter_ComboBox, 1, 1, 1, 1)
        # Configurar propriedade "EffCurve" (True ativa %CutIn %CutOut False desativa %CutIn %CutOut)
        self.InversorConfig_GroupBox_EffCurve_Btn = QPushButton("Selecionar curva de Eficiência")
        self.InversorConfig_GroupBox_EffCurve_Btn.clicked.connect(self.EffCurveConfig)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_EffCurve_Btn, 1, 2, 1, 2)
        # Configurar propriedade "%CutIn"
        self.InversorConfig_GroupBox_CutIn_Label = QLabel("CutIn (%)")
        self.InversorConfig_GroupBox_CutIn_Label.setToolTip("Potência CutIn em percentual da potência aparente (kVA) do\
 inversor.\nÉ a potência DC mínima para ligar o inversor quando ele está desligado.\nPrecisa ser igual ou maior que CutOut")
        self.InversorConfig_GroupBox_CutIn_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_CutIn_LineEdit.setValidator(self.LineEditsValidos0)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutIn_Label, 2, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutIn_LineEdit, 2, 1, 1, 1)
        # Configurar propriedade "CutOut" (Pot. ativa máxima de saída do inversor)
        self.InversorConfig_GroupBox_CutOut_Label = QLabel("CutOut (%)")
        self.InversorConfig_GroupBox_CutOut_Label.setToolTip("Potência CutOut em percentual da potência aparente (kVA) do\
inversor.\nÉ a potência DC mínima para manter o inversor ligado. Precisa ser\nigual ou menor que CutIn")
        self.InversorConfig_GroupBox_CutOut_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_CutOut_LineEdit.setValidator(self.LineEditsValidos0)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutOut_Label, 2, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutOut_LineEdit, 2, 3, 1, 1)
        # Configurar propriedade "kvarMax" (máximo geração de kvar aceita pelo inversor)
        self.InversorConfig_GroupBox_kvarMax_Label = QLabel("Máxima Geração de kvar")
        self.InversorConfig_GroupBox_kvarMax_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_kvarMax_LineEdit.setValidator(self.LineEditsValidos)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMax_Label, 3, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMax_LineEdit, 3, 1, 1, 1)
        # Configurar propriedade "kvarMaxAbs" (máximo absorção de kvar aceita pelo inversor)
        self.InversorConfig_GroupBox_kvarMaxAbs_Label = QLabel("Máxima Absorção de kvar")
        self.InversorConfig_GroupBox_kvarMaxAbs_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_kvarMaxAbs_LineEdit.setValidator(self.LineEditsValidos)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMaxAbs_Label, 3, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMaxAbs_LineEdit, 3, 3, 1, 1)
        # Configurar propriedade "%PminNoVars" (pot. ativa mínima na qual o inversor nao produz/absorve pot. reativa)
        self.InversorConfig_GroupBox_PminNoVars_Label = QLabel("Pot. mín. s/ despacho de reativo (%)")
        self.InversorConfig_GroupBox_PminNoVars_Label.setToolTip("Potência ativa mínima, em percentual da potência ativa \
máxima (kW),\nna qual não há produção/absorção de reativo")
        self.InversorConfig_GroupBox_PminNoVars_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_PminNoVars_LineEdit.setValidator(self.LineEditsValidos0)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminNoVars_Label, 4, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminNoVars_LineEdit, 4, 1, 1, 1)
        # Configurar propriedade "%PminkvarMax" (pot. ativa mínima que permite o inversor produzir/absorver pot. reativa)
        self.InversorConfig_GroupBox_PminkvarMax_Label = QLabel("Pot. mín. c/ despacho de reativo (%)")
        self.InversorConfig_GroupBox_PminkvarMax_Label.setToolTip("Potência ativa mínima, em percentual da potência ativa \
máxima (kW), que permite\no inversor produzir/absorver potencia reativa até um valor máximo")
        self.InversorConfig_GroupBox_PminkvarMax_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_PminkvarMax_LineEdit.setValidator(self.LineEditsValidos0)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminkvarMax_Label, 4, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminkvarMax_LineEdit, 4, 3, 1, 1)
        # Configurar propriedade "PFPriority" (True: seta PF para seu valor quando kVA excedido)
        self.InversorConfig_GroupBox_PFPriority_Label = QLabel("FP prioridade")
        self.InversorConfig_GroupBox_PFPriority_Label.setToolTip("Se ativada, é dada prioridade ao fator de potência e \
a prioridade\nda potência é negligenciada. Só funciona se estiver operando nos\nmodos de despacho PF ou Kvar constantes")
        self.InversorConfig_GroupBox_PFPriority_ComboBox = QComboBox()
        self.InversorConfig_GroupBox_PFPriority_ComboBox.addItems(["Sim", "Não"])
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PFPriority_Label, 5, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PFPriority_ComboBox, 5, 1, 1, 1)
        # Configurar propriedade "WattPriority:" (True: prioriza pot. ativa)
        self.InversorConfig_GroupBox_WattPriority_Label = QLabel("Prioridade de Potência")
        self.InversorConfig_GroupBox_WattPriority_ComboBox = QComboBox()
        self.InversorConfig_GroupBox_WattPriority_ComboBox.addItems(["Pot. Ativa", "Pot. Reativa"])
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_WattPriority_Label, 5, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_WattPriority_ComboBox, 5, 3, 1, 1)

        self.InversorConfig_GroupBox.setLayout(
            self.InversorConfig_GroupBox_Layout)  # define o Layout do GroupBox InversorConfig

        self.Tab_layout = QGridLayout()
        self.Tab_layout.addWidget(self.InversorConfig_GroupBox, 1, 1, 1, 1)  # adiciona o GroupBox InversorConfig ao Tab

        self.setLayout(self.Tab_layout)

    def EffCurveConfig(self):
        self.EffCurve.show()

    def verificaLineEdits(self):
        for i in [
            self.InversorConfig_GroupBox_kVA_LineEdit,
            self.InversorConfig_GroupBox_kWrated_LineEdit,
            self.InversorConfig_GroupBox_CutIn_LineEdit,
            self.InversorConfig_GroupBox_CutOut_LineEdit,
            self.InversorConfig_GroupBox_kvarMax_LineEdit,
            self.InversorConfig_GroupBox_kvarMaxAbs_LineEdit,
            self.InversorConfig_GroupBox_PminNoVars_LineEdit,
            self.InversorConfig_GroupBox_PminkvarMax_LineEdit
        ]:
            if not i.hasAcceptableInput():
                QMessageBox(QMessageBox.Warning, "Insert Storage","Algum valor inserido nas Configurações do Inversor não é válido!\n Verifique os valores inseridos!",
                        QMessageBox.Ok).exec()
                return False
            else:
                return True

class Storage_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, bus, dispatchmode):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Storage_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)
        ## Column 1 - Bus:
        self.setText(1, bus)
        ## Column 2 - Modo Despacho:
        self.setText(2, dispatchmode)
