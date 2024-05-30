from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QDesktopWidget, QDoubleSpinBox
from PyQt5.QtCore import Qt

import random
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

        self._OpenDSSConfig = {}

        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.DispModeActPowDialog = opendss.storage.class_active_pow_dispmode_dialog.C_Active_Pow_DispMode_Dialog()
        self.DispModeReactPowDialog = opendss.storage.class_reactive_pow_dispmode_dialog.C_Reactive_Pow_DispMode_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QHBoxLayout()  # Layout da Dialog

        ####################### GroupBox Storages ############################################################
        self.Storages_GroupBox = QGroupBox("Storages")  # Criando a GroupBox Storages
        self.Storages_GroupBox.setMinimumWidth(400)
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

        ################################################################################################################
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
        self.Config_Btns_Layout.setAlignment(Qt.AlignmentFlag.AlignRight)
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
        self.setMaximumWidth(330)

    def get_StorageName(self):
        return unidecode.unidecode(self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.text().replace(" ", "_"))

    def removeStorages(self):
        for ctd in range(self.Storages_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
            Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.CheckState.Checked:
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
        self.updateDialog()

        self.TabInversorConfig.EffCurve.Storages = self.Storages  # Getter/Setter para o class_config_eff_curve.py

    def editStorages(self):
        checkCont = 0
        try:
            for ctd in range(self.Storages_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
                if self.Storages_GroupBox_TreeWidget.topLevelItem(ctd).checkState(0) == Qt.CheckState.Checked:
                    checkCont += 1
                    Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)

            if checkCont == 1:
                self.clearStorageParameters()
                for i in self.Storages:
                        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setText(i["StorageName"])
                        self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.setCurrentText(i["Conn"])
                        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.setCurrentText(i["Bus"])
                        self.TabConfig.StorageConfig_GroupBox_kW_DoubleSpinBox.setValue(float(i["kW"]))
                        self.TabConfig.StorageConfig_GroupBox_kv_DoubleSpinBox.setValue(float(i["kV"]))
                        self.TabConfig.StorageConfig_GroupBox_kWhrated_DoubleSpinBox.setValue(float(i["kWhrated"]))
                        self.TabConfig.StorageConfig_GroupBox_kWhstored_DoubleSpinBox.setValue(float(i["%stored"]))
                        self.TabConfig.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox.setValue(float(i["%reserve"]))
                        self.TabConfig.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox.setValue(float(i["%IdlingkW"]))
                        self.TabConfig.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox.setValue(float(i["%Charge"]))
                        self.TabConfig.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox.setValue(float(i["%Discharge"]))
                        self.TabConfig.StorageConfig_GroupBox_EffCharge_DoubleSpinBox.setValue(float(i["%EffCharge"]))
                        self.TabConfig.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox.setValue(float(i["%EffDischarge"]))
                        if i["state"] == "Idling":
                            self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Ocioso")
                        elif i["state"] == "Charging":
                            self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Carregando")
                        else:
                            self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Descarregando")
                        self.TabConfig.StorageConfig_GroupBox_vMinPu_DoubleSpinBox.setValue(float(i["vMinpu"]))
                        self.TabConfig.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox.setValue(float(i["vMaxpu"]))
                        self.TabConfig.StorageConfig_GroupBox_R_DoubleSpinBox.setValue(float(i["%R"]))
                        self.TabConfig.StorageConfig_GroupBox_X_DoubleSpinBox.setValue(float(i["%X"]))
                        self.TabConfig.StorageConfig_GroupBox_model_ComboBox.setCurrentText(i["model"])
                        self.TabConfig.StorageConfig_GroupBox_phases_ComboBox.setCurrentText(i["phases"])

                        self.TabInversorConfig.InversorConfig_GroupBox_kVA_DoubleSpinBox.setValue(float(i["kVA"]))
                        self.TabInversorConfig.InversorConfig_GroupBox_kWrated_DoubleSpinBox.setValue(float(i["kWrated"]))
                        if i["varFollowInverter"] == "Yes":
                            self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText(
                                "Ativa CutIn/CutOut")
                        else:
                            self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText(
                                "Desativa CutIn/CutOut")
                        self.TabInversorConfig.InversorConfig_GroupBox_CutIn_DoubleSpinBox.setValue(float(i["%CutIn"]))
                        self.TabInversorConfig.InversorConfig_GroupBox_CutOut_DoubleSpinBox.setValue(float(i["%CutOut"]))
                        self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_DoubleSpinBox.setValue(float(i["kvarMax"]))
                        self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox.setValue(float(i["kvarMaxAbs"]))
                        self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox.setValue(float(i["%PminNoVars"]))
                        self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox.setValue(float(i["%PminkvarMax"]))
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
                            self.DispModeReactPowDialog.FPConst_DoubleSpinBox.setEnabled(True)
                            self.DispModeReactPowDialog.FPConst_DoubleSpinBox.setText(i['ReactPow']['FP'])
                        elif 'kvar' in i['ReactPow']:
                            self.DispModeReactPowDialog.kvarConst_RadioBtn.setChecked(True)
                            self.DispModeReactPowDialog.kvarConst_DoubleSpinBox.setEnabled(True)
                            self.DispModeReactPowDialog.kvarConst_DoubleSpinBox.setText(i['ReactPow']['kvar'])

                        self.TabInversorConfig.EffCurveFile.Config_EffCurve_GroupBox_TreeWidget_Item(
                            self.TabInversorConfig.EffCurve.EffCurve_GroupBox_TreeWidget,
                            i["EffCurve"]["EffCurveName"],
                            str(i["EffCurve"]["Xarray"]).strip('[]').replace("'", ""),
                            str(i["EffCurve"]["Yarray"]).strip('[]').replace("'", ""),
                            cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])

                        if i["Carga/Descarga"] == "Sincronizados":
                            self.DispModeActPowDialog.DispSinc_Radio_Btn.setChecked(True)
                            self.DispModeActPowDialog.DispSinc_GroupBox.setEnabled(True)

                            if i['ModoCarga/Descarga'] == 'Default':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn.setChecked(
                                    True)
                                self.DispModeActPowDialog.DialogActPowDefault.ChargeTrigger_DoubleSpinBox.setText(
                                    i["ActPow"]["ChargeTrigger"])
                                self.DispModeActPowDialog.DialogActPowDefault.DischargeTrigger_DoubleSpinBox.setText(
                                    i["ActPow"]["DischargeTrigger"])
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.TimeTrigger_DoubleSpinBox.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowDefault.TimeTrigger_DoubleSpinBox.setText(
                                        i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowDefault.TimeTrigger_CheckBox.setChecked(True)
                                pts = str(i["ActPow"]["mult"]).strip('[]').replace("'", "")
                                self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurveFile.Config_DispCurve_GroupBox_TreeWidget_Item(
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.DispCurve_GroupBox_TreeWidget,
                                    i["ActPow"]["DispCurveName"],
                                    pts,
                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                                if "sinterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        0)
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["sinterval"])
                                elif "minterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        1)
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["minterval"])
                                elif "interval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        2)
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["interval"])
                                self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Number_SpinBox.setValue(
                                    i["ActPow"]["npts"])

                            elif i['ModoCarga/Descarga'] == 'Follow':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn.setChecked(
                                    True)
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowFollow.TimeTrigger_DoubleSpinBox.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowFollow.TimeTrigger_DoubleSpinBox.setText(
                                        i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowFollow.TimeTrigger_CheckBox.setChecked(True)
                                pts = str(i["ActPow"]["mult"]).strip('[]').replace("'", "")
                                self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurveFile.Config_DispCurve_GroupBox_TreeWidget_Item(
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.DispCurve_GroupBox_TreeWidget,
                                    i["ActPow"]["DispCurveName"],
                                    pts,
                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                                if "sinterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        0)
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["sinterval"])
                                elif "minterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        1)
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["minterval"])
                                elif "interval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        2)
                                    self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["interval"])
                                self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Number_SpinBox.setValue(
                                    i["ActPow"]["npts"])

                            elif i['ModoCarga/Descarga'] == 'LoadLevel':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn.setChecked(
                                    True)
                                self.DispModeActPowDialog.DialogActPowLoadLevel.ChargeTrigger_DoubleSpinBox.setText(
                                    i["ActPow"]["ChargeTrigger"])
                                self.DispModeActPowDialog.DialogActPowLoadLevel.DischargeTrigger_DoubleSpinBox.setText(
                                    i["ActPow"]["DischargeTrigger"])
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowLoadLevel.TimeTrigger_DoubleSpinBox.setEnabled(
                                        True)
                                    self.DispModeActPowDialog.DialogActPowLoadLevel.TimeTrigger_DoubleSpinBox.setText(
                                        i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowLoadLevel.TimeTrigger_CheckBox.setChecked(
                                        True)
                                pts = str(i["ActPow"]["price"]).strip('[]').replace("'", "")
                                self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurveFile.Config_PriceCurve_GroupBox_TreeWidget_Item(
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.PriceCurve_GroupBox_TreeWidget,
                                    i["ActPow"]["PriceCurveName"],
                                    pts,
                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                                if "sinterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        0)
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["sinterval"])
                                elif "minterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        1)
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["minterval"])
                                elif "interval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        2)
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["interval"])
                                self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Number_SpinBox.setValue(
                                    i["ActPow"]["npts"])

                            elif i['ModoCarga/Descarga'] == 'Price':
                                self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn.setChecked(
                                    True)
                                self.DispModeActPowDialog.DialogActPowPrice.ChargeTrigger_DoubleSpinBox.setText(
                                    i["ActPow"]["ChargeTrigger"])
                                self.DispModeActPowDialog.DialogActPowPrice.DischargeTrigger_DoubleSpinBox.setText(
                                    i["ActPow"]["DischargeTrigger"])
                                if 'TimeChargeTrigger' in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.TimeTrigger_DoubleSpinBox.setEnabled(True)
                                    self.DispModeActPowDialog.DialogActPowPrice.TimeTrigger_DoubleSpinBox.setText(
                                        i["ActPow"]['TimeChargeTrigger'])
                                    self.DispModeActPowDialog.DialogActPowPrice.TimeTrigger_CheckBox.setChecked(True)
                                pts = str(i["ActPow"]["price"]).strip('[]').replace("'", "")
                                self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurveFile.Config_PriceCurve_GroupBox_TreeWidget_Item(
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.PriceCurve_GroupBox_TreeWidget,
                                    i["ActPow"]["PriceCurveName"],
                                    pts,
                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                                if "sinterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        0)
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["sinterval"])
                                elif "minterval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        1)
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["minterval"])
                                elif "interval" in i["ActPow"]:
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                        2)
                                    self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                        i["ActPow"]["interval"])
                                self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.Daily_GroupBox_Number_SpinBox.setValue(
                                    i["ActPow"]["npts"])

                            elif i['ModoCarga/Descarga'] == 'LoadShape':
                                self.DispModeActPowDialog.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn.setChecked(
                                    True)
                                for ctd in self.StorageControllers:
                                    if i["StorageName"] in ctd["ElementList"]:
                                        pts = str(ctd["mult"]).strip('[]').replace("'", "")
                                        self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurveFile.Config_DispCurve_GroupBox_TreeWidget_Item(
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.DispCurve_GroupBox_TreeWidget,
                                            ctd["DispCurveName"],
                                            pts,
                                            cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                                        if "sinterval" in ctd:
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                                0)
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                                ctd["sinterval"])
                                        elif "minterval" in ctd:
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                                1)
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                                ctd["minterval"])
                                        elif "interval" in ctd:
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_ComboBox.setCurrentIndex(
                                                2)
                                            self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Stepsize_SpinBox.setValue(
                                                ctd["interval"])
                                        self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.Daily_GroupBox_Number_SpinBox.setValue(
                                            ctd["npts"])



                        elif i["Carga/Descarga"] == "Independentes":
                            self.DispModeActPowDialog.DispIndep_Radio_Btn.setChecked(True)
                            self.DispModeActPowDialog.DispIndep_GroupBox.setEnabled(True)

                            if i['ModoCarga'] == 'PeakShaveLow':
                                self.DispModeActPowDialog.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_PeakShaveLow_RadioBtn.setChecked(
                                    True)
                            elif i['ModoCarga'] == 'I-PeakShaveLow':
                                self.DispModeActPowDialog.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShaveLow_RadioBtn.setChecked(
                                    True)
                            elif i['ModoCarga'] == 'Time':
                                self.DispModeActPowDialog.ModoCarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(
                                    True)

                            if i['ModoDescarga'] == 'PeakShave':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_PeakShave_RadioBtn.setChecked(
                                    True)
                            elif i['ModoDescarga'] == 'I-PeakShave':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_IPeakShave_RadioBtn.setChecked(
                                    True)
                            elif i['ModoDescarga'] == 'Follow':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Follow_RadioBtn.setChecked(
                                    True)
                            elif i['ModoDescarga'] == 'Support':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Support_RadioBtn.setChecked(
                                    True)
                            elif i['ModoDescarga'] == 'Schedule':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Schedule_RadioBtn.setChecked(
                                    True)
                            elif i['ModoDescarga'] == 'Time':
                                self.DispModeActPowDialog.ModoDescarga_GroupBox_StorageCont_GroupBox_Layout_Time_RadioBtn.setChecked(
                                    True)

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
            msg = QMessageBox()
            msg.information(self, 'Storage',
                            "Antes de configurar o Despacho da Potência Ativa, escolha\num nome para o Storage!")
        else:
            self.DispModeActPowDialog.ConfigStorageController.StorageConfig_GroupBox_Nome_LineEdit = self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit
            self.DispModeActPowDialog.DialogActPowLoadShape.StorageConfig_GroupBox_Nome_LineEdit = self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit
            self.DispModeActPowDialog.ConfigStorageController.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox  = self.TabConfig.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox
            self.DispModeActPowDialog.DialogActPowLoadShape.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox = self.TabConfig.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox

            self.DispModeActPowDialog.exec()
            self.DispModeActPowDialog.centralize()

            self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setReadOnly(True)

    def DispModeReactPow(self):
        if self.get_StorageName() == "":
            msg = QMessageBox()
            msg.information(self, 'Storage',
                            "Antes de configurar o Despacho da Potência Reativa, escolha\num nome para o Storage!")
        else:
            self.DispModeReactPowDialog.exec()
            self.DispModeReactPowDialog.centralize()

    def AcceptAddEditStorage(self):
        if self.verificaBusCombobox():

            if self.TabInversorConfig.EffCurve.dataEffCurve == {}:
                msg = QMessageBox()
                msg.information(self, "Insert Storage", "Selecione uma curva de eficiência do Inversor!")

            elif self.DispModeActPowDialog.None_Radio_Btn.isChecked():
                QMessageBox(QMessageBox.Icon.Information, "Insert Storage",
                            "Configure algum Modo de Despacho!",
                            QMessageBox.StandardButton.Ok).exec()

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
                Storage["kW"] = self.TabConfig.StorageConfig_GroupBox_kW_DoubleSpinBox.text().replace(",", ".")
                Storage["kV"] = self.TabConfig.StorageConfig_GroupBox_kv_DoubleSpinBox.text().replace(",", ".")
                Storage["kWhrated"] = self.TabConfig.StorageConfig_GroupBox_kWhrated_DoubleSpinBox.text().replace(",", ".")
                Storage["%stored"] = self.TabConfig.StorageConfig_GroupBox_kWhstored_DoubleSpinBox.text().replace(",", ".")
                Storage["%reserve"] = self.TabConfig.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox.text().replace(",", ".")
                Storage["%IdlingkW"] = self.TabConfig.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox.text().replace(",", ".")
                Storage["%Charge"] = self.TabConfig.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox.text().replace(",", ".")
                Storage["%Discharge"] = self.TabConfig.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox.text().replace(",", ".")
                Storage["%EffCharge"] = self.TabConfig.StorageConfig_GroupBox_EffCharge_DoubleSpinBox.text().replace(",", ".")
                Storage["%EffDischarge"] = self.TabConfig.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox.text().replace(",", ".")
                if self.TabConfig.StorageConfig_GroupBox_state_ComboBox.currentText() == "Ocioso":
                    Storage["state"] = "Idling"
                if self.TabConfig.StorageConfig_GroupBox_state_ComboBox.currentText() == "Carregando":
                    Storage["state"] = "Charging"
                if self.TabConfig.StorageConfig_GroupBox_state_ComboBox.currentText() == "Descarregando":
                    Storage["state"] = "Discharging"
                Storage["vMinpu"] = self.TabConfig.StorageConfig_GroupBox_vMinPu_DoubleSpinBox.text().replace(",", ".")
                Storage["vMaxpu"] = self.TabConfig.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox.text().replace(",", ".")
                Storage["%R"] = self.TabConfig.StorageConfig_GroupBox_R_DoubleSpinBox.text().replace(",", ".")
                Storage["%X"] = self.TabConfig.StorageConfig_GroupBox_X_DoubleSpinBox.text().replace(",", ".")
                Storage["model"] = self.TabConfig.StorageConfig_GroupBox_model_ComboBox.currentText()
                Storage["phases"] = self.TabConfig.StorageConfig_GroupBox_phases_ComboBox.currentText()
                ############# seta data das configurações do inversor
                Storage["kVA"] = self.TabInversorConfig.InversorConfig_GroupBox_kVA_DoubleSpinBox.text().replace(",", ".")
                Storage["kWrated"] = self.TabInversorConfig.InversorConfig_GroupBox_kWrated_DoubleSpinBox.text().replace(",", ".")
                if self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.currentText() == "Ativa CutIn/CutOut":
                    Storage["varFollowInverter"] = "Yes"
                else:
                    Storage["varFollowInverter"] = "No"
                Storage["%CutIn"] = self.TabInversorConfig.InversorConfig_GroupBox_CutIn_DoubleSpinBox.text().replace(",", ".")
                Storage["%CutOut"] = self.TabInversorConfig.InversorConfig_GroupBox_CutOut_DoubleSpinBox.text().replace(",", ".")
                Storage["kvarMax"] = self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_DoubleSpinBox.text().replace(",", ".")
                Storage["kvarMaxAbs"] = self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox.text().replace(",", ".")
                Storage["%PminNoVars"] = self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox.text().replace(",", ".")
                Storage["%PminkvarMax"] = self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox.text().replace(",", ".")
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
                    for i in [
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Default_RadioBtn,
                         "Default"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Follow_RadioBtn,
                         "Follow"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_LoadLevel_RadioBtn,
                         "LoadLevel"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_AutoDespacho_GroupBox_Layout_Price_RadioBtn,
                         "Price"],
                        [self.DispModeActPowDialog.DispSinc_GroupBox_StorageCont_GroupBox_Layout_LoadShape_RadioBtn,
                         "LoadShape"]]:
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
                                Storage.update(
                                    {"ActPow": self.DispModeActPowDialog.DialogActPowDefault.DefaultParameters})
                            elif Storage["ModoCarga/Descarga"] == "Follow":
                                Storage.update(
                                    {"ActPow": self.DispModeActPowDialog.DialogActPowFollow.FollowParameters})
                            elif Storage["ModoCarga/Descarga"] == "LoadLevel":
                                Storage.update(
                                    {"ActPow": self.DispModeActPowDialog.DialogActPowLoadLevel.LoadLevelParameters})
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

                        ElementList = [] # Garante que dois controladores nao controlem um Storage
                        for i in self.StorageControllers:
                            if self.get_StorageName() in i["ElementList"]:
                                ElementList = i["ElementList"]

                        for i in ElementList:
                            listRemove = []
                            for e in self.StorageControllers:
                                if (not self.get_StorageName() in e["ElementList"]) and (i in e["ElementList"]):
                                    listRemove.append(e)
                            for e in listRemove:
                                self.StorageControllers.remove(e)

                    else:
                        msg = QMessageBox()
                        msg.information(self, 'Insert Storage',
                                        "Não foi possível adicionar, pois já existe um Storage com esse nome.")

                else:  # Se estiver editando um Storage
                    for ctd in self.Storages:
                        if ctd["StorageName"] == Storage["StorageName"]:

                            ctd["Conn"] = Storage["Conn"]
                            ctd["Bus"] = Storage["Bus"]
                            ctd["kW"] = Storage["kW"]
                            ctd["kV"] = Storage["kV"]
                            ctd["kWhrated"] = Storage["kWhrated"]
                            ctd["%stored"] = Storage["%stored"]
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
                                          ["LoadLevel",
                                           self.DispModeActPowDialog.DialogActPowLoadLevel.LoadLevelParameters],
                                          ["Price", self.DispModeActPowDialog.DialogActPowPrice.PriceParameters]]:
                                    if Storage["ModoCarga/Descarga"] == i[0]:
                                        ctd["ModoCarga/Descarga"] = Storage["ModoCarga/Descarga"]
                                        ctd.update({"ActPow": i[1]})

                                if Storage["ModoCarga/Descarga"] == "LoadShape":
                                    ctd["ModoCarga/Descarga"] = Storage["ModoCarga/Descarga"]
                                    ctd.update({"ActPow": None})

                                    if not self.DispModeActPowDialog.DialogActPowLoadShape.StorageControllersTemporario == []:
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

                            ElementList = []  # Garante que dois controladores nao controlem um Storage
                            for i in self.StorageControllers:
                                if self.get_StorageName() in i["ElementList"]:
                                    ElementList = i["ElementList"]

                            for i in ElementList:
                                listRemove = []
                                for e in self.StorageControllers:
                                    if (not self.get_StorageName() in e["ElementList"]) and (i in e["ElementList"]):
                                        listRemove.append(e)
                                for e in listRemove:
                                    self.StorageControllers.remove(e)

                if not self.StorageControllers == []:
                    listRemove = []
                    for ctd in self.StorageControllers:
                        ctd["ElementList"] = list(set(ctd["ElementList"]))
                        if not ctd["ElementList"]:  # Garante que nao haja StorageController que não controle nenhum Storage
                            listRemove.append(ctd)
                    for ctd in listRemove:
                        self.StorageControllers.remove(ctd)

                self.adjustSize()
                self.updateDialog()
                self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setEnabled(True)
                self.clearStorageParameters()
                self.DefaultConfigParameters()
                self.EnableDisableParameters(False)

    def CancelAddEditStorage(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setEnabled(True)
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setReadOnly(False)
        self.EnableDisableParameters(False)
        self.adjustSize()
        self.centralize()

    def acceptInsertStorage(self):
        self.OpenDSS.Storages = self.Storages
        self.OpenDSS.StorageControllers = self.StorageControllers
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
        self.centralize()

    def DefaultConfigParameters(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.setCurrentText("Wye")
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_kW_DoubleSpinBox.setValue(0.1)
        self.TabConfig.StorageConfig_GroupBox_kv_DoubleSpinBox.setValue(0.1)
        self.TabConfig.StorageConfig_GroupBox_kWhrated_DoubleSpinBox.setValue(50.0)
        self.TabConfig.StorageConfig_GroupBox_kWhstored_DoubleSpinBox.setValue(100.0)
        self.TabConfig.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox.setValue(20.0)
        self.TabConfig.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox.setValue(1.0)
        self.TabConfig.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox.setValue(100.0)
        self.TabConfig.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox.setValue(100.0)
        self.TabConfig.StorageConfig_GroupBox_EffCharge_DoubleSpinBox.setValue(90.0)
        self.TabConfig.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox.setValue(90.0)
        self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Ocioso")
        self.TabConfig.StorageConfig_GroupBox_vMinPu_DoubleSpinBox.setValue(0.9)
        self.TabConfig.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox.setValue(1.1)
        self.TabConfig.StorageConfig_GroupBox_R_DoubleSpinBox.setValue(0)
        self.TabConfig.StorageConfig_GroupBox_X_DoubleSpinBox.setValue(50)
        self.TabConfig.StorageConfig_GroupBox_model_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_phases_ComboBox.setCurrentIndex(0)

        self.TabInversorConfig.InversorConfig_GroupBox_kVA_DoubleSpinBox.setValue(0.1)
        self.TabInversorConfig.InversorConfig_GroupBox_kWrated_DoubleSpinBox.setValue(25.0)
        self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText("Desativa CutIn/CutOut")
        self.TabInversorConfig.InversorConfig_GroupBox_CutIn_DoubleSpinBox.setValue(0)
        self.TabInversorConfig.InversorConfig_GroupBox_CutOut_DoubleSpinBox.setValue(0)
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_DoubleSpinBox.setValue(999999.0)
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox.setValue(999999.0)
        self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox.setValue(0)
        self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox.setValue(0)
        self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.setCurrentText("Não")
        self.TabInversorConfig.InversorConfig_GroupBox_WattPriority_ComboBox.setCurrentText("Pot. Reativa")

    def clearStorageParameters(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setReadOnly(False)
        self.DefaultConfigParameters()

        self.TabInversorConfig.EffCurve.EffCurve_GroupBox_TreeWidget.clear()  # Limpa o TreeWidget e o plot da Curva de Eficiencia
        self.TabInversorConfig.EffCurve.graphWidget.clear()
        self.TabInversorConfig.EffCurve.dataEffCurve = {}

        self.DispModeActPowDialog.DialogActPowPrice.Select_PriceCurve.restoreParameters()
        self.DispModeActPowDialog.DialogActPowDefault.Select_DispCurve.restoreParameters()

        self.DispModeActPowDialog.DialogActPowDefault.clearParameters()
        self.DispModeActPowDialog.DialogActPowFollow.clearParameters()
        self.DispModeActPowDialog.DialogActPowLoadLevel.clearParameters()
        self.DispModeActPowDialog.DialogActPowPrice.clearParameters()

    def centralize(self):
        qr = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerpoint)
        self.move(qr.topLeft())

    def verificaBusCombobox(self):
        ctd = 0
        for i in self.OpenDSS.getBusList():
            if self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText() == i:
                ctd += 1

        if ctd == 0:
            msg = QMessageBox()
            msg.information(self, "Configuração do Storage", "Barra selecionada inexistente!")
            return False
        else:
            return True

class StorageConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUIStorageConfig()

    def InitUIStorageConfig(self):

        self.ConfigStorageController = opendss.storage.class_config_storagecontroller.C_ActPow_Config_StorageController_Dialog()

        ###################### GroupBox StorageConfig #######################################################
        self.StorageConfig_GroupBox = QGroupBox()  # Criando a GroupBox StorageConfig
        self.StorageConfig_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do StorageConfig é em Grid
        # Configurar nome do elemento Storage
        self.StorageConfig_GroupBox_Nome_Label = QLabel("Nome")
        self.StorageConfig_GroupBox_Nome_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Nome_LineEdit.setFixedWidth(120)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Nome_Label, 0, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Nome_LineEdit, 0, 1, 1, 1)
        # Configurar propriedade "conn"
        self.StorageConfig_GroupBox_conn_Label = QLabel("Tipo de conexão")
        self.StorageConfig_GroupBox_conn_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_conn_ComboBox.setFixedWidth(120)
        self.StorageConfig_GroupBox_conn_ComboBox.addItems(["Wye", "LN", "Delta", "LN"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_conn_Label, 0, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_conn_ComboBox, 0, 3, 1, 1)
        # Configurar propriedade "Bus"
        self.StorageConfig_GroupBox_Bus_Label = QLabel("Barra de conexão")
        self.StorageConfig_GroupBox_Bus_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_Bus_ComboBox.setEditable(True)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Bus_Label, 1, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Bus_ComboBox, 1, 1, 1, 1)
        # Configurar propriedade "kW" (potência de saída)
        self.StorageConfig_GroupBox_kW_Label = QLabel("Potência nominal de saída (kW)")
        self.StorageConfig_GroupBox_kW_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_kW_DoubleSpinBox.setRange(0.1, 999999999)
        self.StorageConfig_GroupBox_kW_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_kW_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kW_Label, 2, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kW_DoubleSpinBox, 2, 1, 1, 1)
        # Configurar propriedade "kv" (tensão de saída)
        self.StorageConfig_GroupBox_kv_Label = QLabel("Tensão de saída (kV)")
        self.StorageConfig_GroupBox_kv_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_kv_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_kv_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_kv_DoubleSpinBox.setRange(0.1, 999999999)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kv_Label, 1, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kv_DoubleSpinBox, 1, 3, 1, 1)
        # Configurar propriedade "kWhrated" (capacidade nominal do Storage em kWh)
        self.StorageConfig_GroupBox_kWhrated_Label = QLabel("Capacidade Nominal (kWh)")
        self.StorageConfig_GroupBox_kWhrated_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_kWhrated_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_kWhrated_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_kWhrated_DoubleSpinBox.setRange(0.1, 999999999)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhrated_Label, 2, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhrated_DoubleSpinBox, 2, 3, 1, 1)
        # Configurar propriedade "%stored" (porcentagem atual de energia armazenada)
        self.StorageConfig_GroupBox_kWhstored_Label = QLabel("Energia armazenada atual (%)")
        self.StorageConfig_GroupBox_kWhstored_Label.setToolTip("Energia Armazenada atual em % da capacidade nominal.")
        self.StorageConfig_GroupBox_kWhstored_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_kWhstored_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_kWhstored_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_kWhstored_DoubleSpinBox.setRange(0.0, 100.0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhstored_Label, 3, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhstored_DoubleSpinBox, 3, 3, 1, 1)
        # Configurar propriedade "%reserve" (quantidade de energia para ser deixada como reserva em %)
        self.StorageConfig_GroupBox_PercentageReserve_Label = QLabel("Energia reserva (%)")
        self.StorageConfig_GroupBox_PercentageReserve_Label.setToolTip(
            "Percentual da capacidade de armazenamento nominal (kWh)\npara ser mantida em reserva. É tratado como nível mínimo de\ndescarregamento, em situações normais")
        self.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox.setRange(0.0, 100.0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_PercentageReserve_Label, 3, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_PercentageReserve_DoubleSpinBox , 3, 1, 1, 1)
        # Configurar propriedade "%IdlingkW" (kW consumida por perdas por inatividade)
        self.StorageConfig_GroupBox_IdlingkW_Label = QLabel("Perdas por inatividade (%)")
        self.StorageConfig_GroupBox_IdlingkW_Label.setToolTip(
            "Percentual de potência ativa nominal (kW)\nconsumida por perdas por inatividade.")
        self.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox.setRange(0.0, 99.999)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_IdlingkW_Label, 4, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_IdlingkW_DoubleSpinBox, 4, 3, 1, 1)
        # Configurar propriedade "%Charge" (Taxa de carregamento em % da potencia nominal)
        self.StorageConfig_GroupBox_Per100Charge_Label = QLabel("Taxa de carregamento (%)")
        self.StorageConfig_GroupBox_Per100Charge_Label.setToolTip(
            "Taxa de carregamento em percentual da\npotência ativa nominal (kW).")
        self.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox.setRange(0.1, 100.0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Charge_Label, 4, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Charge_DoubleSpinBox, 4, 1, 1, 1)
        # Configurar propriedade "%Discharge" (Taxa de descarregamento em % da potencia nominal)
        self.StorageConfig_GroupBox_Per100Discharge_Label = QLabel("Taxa de descarregamento (%)")
        self.StorageConfig_GroupBox_Per100Discharge_Label.setToolTip(
            "Taxa de descarregamento em percentual da\npotência ativa nominal (kW).")
        self.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox.setRange(0.1, 100.0)
        self.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Discharge_Label, 5, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Discharge_DoubleSpinBox, 5, 3, 1, 1)
        # Configurar propriedade "%EffCharge" (% de eficiencia ao carregar o Storage)
        self.StorageConfig_GroupBox_EffCharge_Label = QLabel("Eficiência do carregamento (%) ")
        self.StorageConfig_GroupBox_EffCharge_Label.setToolTip("Percentual de eficiência para o carregamento")
        self.StorageConfig_GroupBox_EffCharge_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_EffCharge_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_EffCharge_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_EffCharge_DoubleSpinBox.setRange(0.1, 100.0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffCharge_Label, 5, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffCharge_DoubleSpinBox, 5, 1, 1, 1)
        # Configurar propriedade "%EffDischarge" (% de eficiencia ao descarregar o Storage)
        self.StorageConfig_GroupBox_EffDischarge_Label = QLabel("Eficiência do descarregamento (%)")
        self.StorageConfig_GroupBox_EffDischarge_Label.setToolTip("Percentual de eficiência para o carregamento")
        self.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox.setRange(0.1, 100.0)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffDischarge_Label, 6, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffDischarge_DoubleSpinBox, 6, 3, 1, 1)
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
        self.StorageConfig_GroupBox_vMinPu_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_vMinPu_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_vMinPu_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_vMinPu_DoubleSpinBox.setRange(0.001, 100)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMinPu_Label, 7, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMinPu_DoubleSpinBox, 7, 1, 1, 1)
        # Configurar propriedade "vmaxpu" (tensão maxima, em pu, para a qual o modelo se aplica)
        self.StorageConfig_GroupBox_vMaxPu_Label = QLabel("Tensão máxima (p.u.)")
        self.StorageConfig_GroupBox_vMaxPu_Label.setToolTip(
            "Tensão máxima em p.u. para a qual o modelo se aplica. Abaixo\ndesse valor,o modelo da carga se torna um modelo de impedância constante.")
        self.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox.setRange(0.001, 100)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMaxPu_Label, 7, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMaxPu_DoubleSpinBox, 7, 3, 1, 1)
        # Configurar propriedade "%R" (resistência interna equivalente percentual)
        self.StorageConfig_GroupBox_R_Label = QLabel("Resistência interna (%)")
        self.StorageConfig_GroupBox_R_Label.setToolTip("Percentual da resistência interna equivalente")
        self.StorageConfig_GroupBox_R_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_R_DoubleSpinBox.setRange(0.0, 999999999)
        self.StorageConfig_GroupBox_R_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_R_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_R_Label, 8, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_R_DoubleSpinBox, 8, 1, 1, 1)
        # Configurar propriedade "%X" (reatância interna equivalente percentual)
        self.StorageConfig_GroupBox_X_Label = QLabel("Reatância interna (%)")
        self.StorageConfig_GroupBox_X_Label.setToolTip("Percentual da reatância interna equivalente")
        self.StorageConfig_GroupBox_X_DoubleSpinBox = QDoubleSpinBox()
        self.StorageConfig_GroupBox_X_DoubleSpinBox.setDecimals(3)
        self.StorageConfig_GroupBox_X_DoubleSpinBox.setButtonSymbols(2)
        self.StorageConfig_GroupBox_X_DoubleSpinBox.setRange(0.0, 999999999)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_X_Label, 8, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_X_DoubleSpinBox, 8, 3, 1, 1)
        # Configurar propriedade "model" (modelo de saída da potência)
        self.StorageConfig_GroupBox_model_Label = QLabel("Modelo do Storage")
        self.StorageConfig_GroupBox_model_Label.setToolTip("1: Storage injeta/absorve potência constante.\n2: Storage é modelado como uma impedância constante.")
        self.StorageConfig_GroupBox_model_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_model_ComboBox.addItems(["1", "2"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_model_Label, 9, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_model_ComboBox, 9, 1, 1, 1)
        # Configurar propriedade "phases" (fases)
        self.StorageConfig_GroupBox_phases_Label = QLabel("Número de fases")
        self.StorageConfig_GroupBox_phases_Label.setToolTip("A potência é dividida igualmente para o número de fases.")
        self.StorageConfig_GroupBox_phases_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_phases_ComboBox.addItems(["3", "2", "1"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_phases_Label, 9, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_phases_ComboBox, 9, 3, 1, 1)

        self.StorageConfig_GroupBox.setLayout(
            self.StorageConfig_GroupBox_Layout)  # define o Layout do GroupBox StoragesConfig

        self.Tab_layout = QGridLayout()
        self.Tab_layout.addWidget(self.StorageConfig_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Tab_layout)

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
        self.InversorConfig_GroupBox_kVA_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_kVA_DoubleSpinBox.setRange(0.1, 999999999)
        self.InversorConfig_GroupBox_kVA_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_kVA_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kVA_Label, 0, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kVA_DoubleSpinBox, 0, 1, 1, 1)
        # Configurar propriedade "kWrated" (Pot. ativa máxima de saída do inversor)
        self.InversorConfig_GroupBox_kWrated_Label = QLabel("kWrated")
        self.InversorConfig_GroupBox_kWrated_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_kWrated_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_kWrated_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_kWrated_DoubleSpinBox.setRange(0.1, 999999999)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kWrated_Label, 0, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kWrated_DoubleSpinBox, 0, 3, 1, 1)
        # Configurar propriedade "%varFollowInverter" (True ativa %CutIn %CutOut False desativa %CutIn %CutOut)
        self.InversorConfig_GroupBox_varFollowInverter_Label = QLabel("Seta status do CutIn/CutOut")
        self.InversorConfig_GroupBox_varFollowInverter_Label.setToolTip("Quando desativado, o inversor gera/absorve \
potência reativa independentemente\ndo status do inversor. Quando ativado, a geração/absorção de potência reativa\nirá \
cessar quando o inversor estiver desligado devido a queda da potência DC\nabaixo do CutOut. A geração/absorção vai \
começar novamente quando a potência\nDC estiver acima de CutIn")
        self.InversorConfig_GroupBox_varFollowInverter_ComboBox = QComboBox()
        self.InversorConfig_GroupBox_varFollowInverter_ComboBox.addItems(
            ["Ativa CutIn/CutOut", "Desativa CutIn/CutOut"])
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_varFollowInverter_Label, 1, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_varFollowInverter_ComboBox, 1, 1, 1,
1)
        # Configurar propriedade "EffCurve" (True ativa %CutIn %CutOut False desativa %CutIn %CutOut)
        self.InversorConfig_GroupBox_EffCurve_Btn = QPushButton("Selecionar curva de Eficiência")
        self.InversorConfig_GroupBox_EffCurve_Btn.clicked.connect(self.EffCurveConfig)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_EffCurve_Btn, 1, 2, 1, 2)
        # Configurar propriedade "%CutIn"
        self.InversorConfig_GroupBox_CutIn_Label = QLabel("CutIn (%)")
        self.InversorConfig_GroupBox_CutIn_Label.setToolTip("Potência CutIn em percentual da potência aparente (kVA) do\
 inversor.\nÉ a potência DC mínima para ligar o inversor quando ele está desligado.\nPrecisa ser igual ou maior que CutOut")
        self.InversorConfig_GroupBox_CutIn_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_CutIn_DoubleSpinBox.setRange(0.0, 100.0)
        self.InversorConfig_GroupBox_CutIn_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_CutIn_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutIn_Label, 2, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutIn_DoubleSpinBox, 2, 1, 1, 1)
        # Configurar propriedade "CutOut" (Pot. ativa máxima de saída do inversor)
        self.InversorConfig_GroupBox_CutOut_Label = QLabel("CutOut (%)")
        self.InversorConfig_GroupBox_CutOut_Label.setToolTip("Potência CutOut em percentual da potência aparente (kVA) do\
inversor.\nÉ a potência DC mínima para manter o inversor ligado. Precisa ser\nigual ou menor que CutIn")
        self.InversorConfig_GroupBox_CutOut_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_CutOut_DoubleSpinBox.setRange(0.0, 100.0)
        self.InversorConfig_GroupBox_CutOut_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_CutOut_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutOut_Label, 2, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutOut_DoubleSpinBox, 2, 3, 1, 1)
        # Configurar propriedade "kvarMax" (máximo geração de kvar aceita pelo inversor)
        self.InversorConfig_GroupBox_kvarMax_Label = QLabel("kvarMax")
        self.InversorConfig_GroupBox_kvarMax_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_kvarMax_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_kvarMax_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_kvarMax_DoubleSpinBox.setRange(0.0, 999999999)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMax_Label, 3, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMax_DoubleSpinBox, 3, 1, 1, 1)
        # Configurar propriedade "kvarMaxAbs" (máximo absorção de kvar aceita pelo inversor)
        self.InversorConfig_GroupBox_kvarMaxAbs_Label = QLabel("kvarMaxAbs")
        self.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox.setRange(0.0, 999999999)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMaxAbs_Label, 3, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMaxAbs_DoubleSpinBox, 3, 3, 1, 1)
        # Configurar propriedade "%PminNoVars" (pot. ativa mínima na qual o inversor nao produz/absorve pot. reativa)
        self.InversorConfig_GroupBox_PminNoVars_Label = QLabel("%PminNoVars")
        self.InversorConfig_GroupBox_PminNoVars_Label.setToolTip("Potência ativa mínima, em percentual da potência ativa \
máxima (kW),\nna qual não há produção/absorção de reativo")
        self.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox.setRange(0.0, 100.0)
        self.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminNoVars_Label, 4, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminNoVars_DoubleSpinBox, 4, 1, 1, 1)
        # Configurar propriedade "%PminkvarMax" (pot. ativa mínima que permite o inversor produzir/absorver pot. reativa)
        self.InversorConfig_GroupBox_PminkvarMax_Label = QLabel("%PminkvarMax")
        self.InversorConfig_GroupBox_PminkvarMax_Label.setToolTip("Potência ativa mínima, em percentual da potência ativa \
máxima (kW), que permite\no inversor produzir/absorver potencia reativa até um valor máximo")
        self.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox = QDoubleSpinBox()
        self.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox.setRange(0.0, 100.0)
        self.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox.setDecimals(3)
        self.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox.setButtonSymbols(2)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminkvarMax_Label, 4, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminkvarMax_DoubleSpinBox, 4, 3, 1, 1)
        # Configurar propriedade "PFPriority" (True: seta PF para seu valor quando kVA excedido)
        self.InversorConfig_GroupBox_PFPriority_Label = QLabel("PFPriority")
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
        self.EffCurve.exec()
        self.EffCurve.centralize()


class Storage_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, bus, dispatchmode):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Storage_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)
        self.setCheckState(0, Qt.CheckState.Unchecked)
        ## Column 1 - Bus:
        self.setText(1, bus)
        ## Column 2 - Modo Despacho:
        self.setText(2, dispatchmode)
