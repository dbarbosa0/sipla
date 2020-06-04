from PyQt5.QtGui import QColor, QIcon
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


class C_Insert_Storage_Dialog(QDialog):  ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Storage Insert"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.Storages = []

        self._StorageControllers = []

        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.EffCurve = opendss.storage.class_config_eff_curve.C_Config_EffCurve_Dialog()
        self.DispModeActPowDialog = opendss.storage.class_active_pow_dispmode_dialog.C_Active_Pow_DispMode_Dialog()
        self.DispModeReactPowDialog = opendss.storage.class_reactive_pow_dispmode_dialog.C_Reactive_Pow_DispMode_Dialog()

    @property
    def StorageControllers(self):
        return self._StorageControllers

    @StorageControllers.setter
    def StorageControllers(self, value):
        self._StorageControllers = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        # self.resize(900, 600)

        # self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

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
        self.Storages_GroupBox_Excluir_Btn.clicked.connect(self.excluirStorages)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_Excluir_Btn, 3, 2, 1, 1)
        # Botão Editar
        self.Storages_GroupBox_Edit_Btn = QPushButton("Editar")  # Botão de editar dentro do GroupBox
        self.Storages_GroupBox_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.Storages_GroupBox_Edit_Btn.clicked.connect(self.editStorages)
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_Edit_Btn, 3, 3, 1, 1)
        # Botao OK
        self.Storages_GroupBox_OK_Btn = QPushButton("OK")  # Botão OK dentro do GroupBox
        self.Storages_GroupBox_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        # self.Storages_GroupBox_OK_Btn.clicked.connect()
        self.Storages_GroupBox_Layout.addWidget(self.Storages_GroupBox_OK_Btn, 4, 1, 1, 2)
        # Botao Cancelar
        self.Storages_GroupBox_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Storages_GroupBox_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        # self.Storages_GroupBox_Cancel_Btn.clicked.connect()
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
        self.ModoDespacho_GroupBox.setLayout(
            self.ModoDespacho_GroupBox_Layout)  # define o Layout do GroupBox ModoDespacho

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
        self.StorageEInvConfig_GroupBox_Layout.addWidget(
            self.ModoDespacho_GroupBox)  # adiciona o GroupBox ModoDespacho ao GroupBox superior
        self.StorageEInvConfig_GroupBox_Layout.addItem(
            self.Config_Btns_Layout)  # adiciona o Layout dos Botões das Configurações ao GroupBox superior

        self.StorageEInvConfig_GroupBox.setLayout(self.StorageEInvConfig_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.StorageEInvConfig_GroupBox)  # adiciona a GroupBox das Configurações ao Dialog

        self.setLayout(self.Dialog_Layout)

    # tenho que escrever o codigo desses botoes ainda
    def excluirStorages(self):
        self.updateDialog()
        self.DispModeActPowDialog.ConfigStorageController.updateDialog()


    def addStorages(self):
        self.EnableConfig(True)
        self.DefaultConfigParameters()
        self.adjustSize()

    def editStorages(self):
        pass

    def DispModeActPow(self):
        self.DispModeActPowDialog.show()


    def DispModeReactPow(self):
        self.DispModeReactPowDialog.show()

    def AcceptAddEditStorage(self):
        countName = 0

        for ctd in range(0, self.Storages_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.Storages_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.text(0) == str(self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.text()):
                print(Item.text(0) == str(self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.text()))
                countName += 1
        if countName == 0:
            Storage_TreeWidget_Item(self.Storages_GroupBox_TreeWidget,
                                    self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.text(),
                                    self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.currentText())
        else:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Carga',
                            "Não foi possível adicionar o Storage!\nJá existe um Storage com esse nome!")

        self.updateDialog()
        self.EnableConfig(False)
        self.adjustSize()

    def CancelAddEditStorage(self):
        self.EnableConfig(False)
        self.adjustSize()

    def EnableConfig(self, bool):
        if bool:
            self.StorageEInvConfig_GroupBox.setVisible(True)
            self.Storages_GroupBox.setVisible(False)
        else:
            self.StorageEInvConfig_GroupBox.setVisible(False)
            self.Storages_GroupBox.setVisible(True)

    def updateDialog(self):
        # segundo o class_insert_monitor, ainda falta coisa aqui, mas preciso ver se vou precisar mesmo
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.clear()
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.addItems(self.OpenDSS.getBusList())

    def DefaultConfigParameters(self):
        self.TabConfig.StorageConfig_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_conn_ComboBox.setCurrentText("Y")
        self.TabConfig.StorageConfig_GroupBox_Bus_ComboBox.setCurrentIndex(0)
        self.TabConfig.StorageConfig_GroupBox_kW_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kv_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_pf_LineEdit.setText("")
        self.TabConfig.StorageConfig_GroupBox_kWhrated_LineEdit.setText("50")
        self.TabConfig.StorageConfig_GroupBox_kWhstored_LineEdit.setText("50")
        self.TabConfig.StorageConfig_GroupBox_PercentageReserve_LineEdit.setText("20")
        self.TabConfig.StorageConfig_GroupBox_IdlingkW_LineEdit.setText("1")
        self.TabConfig.StorageConfig_GroupBox_Per100Charge_LineEdit.setText("100")
        self.TabConfig.StorageConfig_GroupBox_Per100Discharge_LineEdit.setText("100")
        self.TabConfig.StorageConfig_GroupBox_EffCharge_LineEdit.setText("90")
        self.TabConfig.StorageConfig_GroupBox_EffDischarge_LineEdit.setText("90")
        self.TabConfig.StorageConfig_GroupBox_state_ComboBox.setCurrentText("Ocioso")
        self.TabConfig.StorageConfig_GroupBox_model_ComboBox.setCurrentText("Pot. constante")
        self.TabConfig.StorageConfig_GroupBox_vMinPu_LineEdit.setText("0.9")
        self.TabConfig.StorageConfig_GroupBox_vMaxPu_LineEdit.setText("1.1")
        self.TabConfig.StorageConfig_GroupBox_R_LineEdit.setText("0")
        self.TabConfig.StorageConfig_GroupBox_X_LineEdit.setText("50")

        self.TabInversorConfig.InversorConfig_GroupBox_kVA_LineEdit.setText("")
        self.TabInversorConfig.InversorConfig_GroupBox_kWrated_LineEdit.setText("25")
        self.TabInversorConfig.InversorConfig_GroupBox_varFollowInverter_ComboBox.setCurrentText(
            "Desativa CutIn/CutOut")
        self.TabInversorConfig.InversorConfig_GroupBox_CutIn_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_CutOut_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMax_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_kvarMaxAbs_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_PminNoVars_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_PminkvarMax_LineEdit.setText("0")
        self.TabInversorConfig.InversorConfig_GroupBox_PFPriority_ComboBox.setCurrentText("Não")
        self.TabInversorConfig.InversorConfig_GroupBox_WattPriority_ComboBox.setCurrentText("Pot. Reativa")


class StorageConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIStorageConfig()


    def InitUIStorageConfig(self):

        self.ConfigStorageController = opendss.storage.class_config_storagecontroller.C_ActPow_Config_StorageController_Dialog()

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
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kW_Label, 2, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kW_LineEdit, 2, 1, 1, 1)
        # Configurar propriedade "kv" (tensão de saída)
        self.StorageConfig_GroupBox_kv_Label = QLabel("Tensão de saída (kV)")
        self.StorageConfig_GroupBox_kv_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kv_Label, 1, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kv_LineEdit, 1, 3, 1, 1)
        # Configurar propriedade "pf"
        self.StorageConfig_GroupBox_pf_Label = QLabel("Fator de Potência")
        self.StorageConfig_GroupBox_pf_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_pf_Label, 2, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_pf_LineEdit, 2, 3, 1, 1)
        # Configurar propriedade "kWhrated" (capacidade nominal do Storage em kWh)
        self.StorageConfig_GroupBox_kWhrated_Label = QLabel("Capacidade Nominal (kWh)")
        self.StorageConfig_GroupBox_kWhrated_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhrated_Label, 3, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhrated_LineEdit, 3, 1, 1, 1)
        # Configurar propriedade "kWhstored" (quantidade atual de energia armazenada em kWh)
        self.StorageConfig_GroupBox_kWhstored_Label = QLabel("Energia armazenada atual (kWh)")
        self.StorageConfig_GroupBox_kWhstored_Label.setToolTip("Energia Armazenada atual em kWh")
        self.StorageConfig_GroupBox_kWhstored_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhstored_Label, 3, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_kWhstored_LineEdit, 3, 3, 1, 1)
        # Configurar propriedade "%reserve" (quantidade de energia para ser deixada como reserva em %)
        self.StorageConfig_GroupBox_PercentageReserve_Label = QLabel("Energia reserva (%)")
        self.StorageConfig_GroupBox_PercentageReserve_Label.setToolTip(
            "Percentual da capacidade de armazenamento nominal (kWh)\npara ser mantida em reserva. É tratado como nível mínimo de\ndescarregamento, em situações normais")
        self.StorageConfig_GroupBox_PercentageReserve_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_PercentageReserve_Label, 4, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_PercentageReserve_LineEdit, 4, 1, 1, 1)
        # Configurar propriedade "%IdlingkW" (kW consumida por perdas por inatividade)
        self.StorageConfig_GroupBox_IdlingkW_Label = QLabel("Perdas por inatividade (%)")
        self.StorageConfig_GroupBox_IdlingkW_Label.setToolTip(
            "Percentual de potência ativa nominal (kW)\nconsumida por perdas por inatividade.")
        self.StorageConfig_GroupBox_IdlingkW_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_IdlingkW_Label, 4, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_IdlingkW_LineEdit, 4, 3, 1, 1)
        # Configurar propriedade "%Charge" (Taxa de carregamento em % da potencia nominal)
        self.StorageConfig_GroupBox_Per100Charge_Label = QLabel("Taxa de carregamento (%)")
        self.StorageConfig_GroupBox_Per100Charge_Label.setToolTip(
            "Taxa de carregamento em percentual da\npotência ativa nominal (kW).")
        self.StorageConfig_GroupBox_Per100Charge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Charge_Label, 5, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Charge_LineEdit, 5, 1, 1, 1)
        # Configurar propriedade "%Discharge" (Taxa de descarregamento em % da potencia nominal)
        self.StorageConfig_GroupBox_Per100Discharge_Label = QLabel("Taxa de descarregamento (%)")
        self.StorageConfig_GroupBox_Per100Discharge_Label.setToolTip(
            "Taxa de descarregamento em percentual da\npotência ativa nominal (kW).")
        self.StorageConfig_GroupBox_Per100Discharge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Discharge_Label, 5, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_Per100Discharge_LineEdit, 5, 3, 1, 1)
        # Configurar propriedade "%EffCharge" (% de eficiencia ao carregar o Storage)
        self.StorageConfig_GroupBox_EffCharge_Label = QLabel("Eficiência do carregamento (%) ")
        self.StorageConfig_GroupBox_EffCharge_Label.setToolTip("Percentual de eficiência para o carregamento")
        self.StorageConfig_GroupBox_EffCharge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffCharge_Label, 6, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffCharge_LineEdit, 6, 1, 1, 1)
        # Configurar propriedade "%EffDischarge" (% de eficiencia ao descarregar o Storage)
        self.StorageConfig_GroupBox_EffDischarge_Label = QLabel("Eficiência do descarregamento (%)")
        self.StorageConfig_GroupBox_EffDischarge_Label.setToolTip("Percentual de eficiência para o carregamento")
        self.StorageConfig_GroupBox_EffDischarge_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffDischarge_Label, 6, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_EffDischarge_LineEdit, 6, 3, 1, 1)
        # Configurar propriedade "state" (seta o estado de operação)
        self.StorageConfig_GroupBox_state_Label = QLabel("Estado de operação")
        self.StorageConfig_GroupBox_state_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_state_ComboBox.addItems(["Ocioso", "Carregando", "Descarregando"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_state_Label, 7, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_state_ComboBox, 7, 1, 1, 1)
        # Configarar propriedade "model" (modelo para variação da saida de Pot. ativa pela tensão)
        self.StorageConfig_GroupBox_model_Label = QLabel("Modelo do Storage")
        self.StorageConfig_GroupBox_model_ComboBox = QComboBox()
        self.StorageConfig_GroupBox_model_ComboBox.addItems(["Pot. constante", "Z Constante"])
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_model_Label, 7, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_model_ComboBox, 7, 3, 1, 1)
        # Configurar propriedade "vminpu" (tensão minima, em pu, para a qual o modelo se aplica)
        self.StorageConfig_GroupBox_vMinPu_Label = QLabel("Tensão mínima (p.u.)")
        self.StorageConfig_GroupBox_vMinPu_Label.setToolTip(
            "Tensão mínima em p.u. para a qual o modelo se aplica. Abaixo\ndesse valor,o modelo da carga se torna um modelo de impedância constante.")
        self.StorageConfig_GroupBox_vMinPu_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMinPu_Label, 8, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMinPu_LineEdit, 8, 1, 1, 1)
        # Configurar propriedade "vmaxpu" (tensão maxima, em pu, para a qual o modelo se aplica)
        self.StorageConfig_GroupBox_vMaxPu_Label = QLabel("Tensão máxima (p.u.)")
        self.StorageConfig_GroupBox_vMaxPu_Label.setToolTip(
            "Tensão máxima em p.u. para a qual o modelo se aplica. Abaixo\ndesse valor,o modelo da carga se torna um modelo de impedância constante.")
        self.StorageConfig_GroupBox_vMaxPu_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMaxPu_Label, 8, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_vMaxPu_LineEdit, 8, 3, 1, 1)
        # Configurar propriedade "%R" (resistência interna equivalente percentual)
        self.StorageConfig_GroupBox_R_Label = QLabel("Resistência interna (%)")
        self.StorageConfig_GroupBox_R_Label.setToolTip("Percentual da resistência interna equivalente")
        self.StorageConfig_GroupBox_R_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_R_Label, 9, 0, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_R_LineEdit, 9, 1, 1, 1)
        # Configurar propriedade "%X" (reatância interna equivalente percentual)
        self.StorageConfig_GroupBox_X_Label = QLabel("Reatância interna (%)")
        self.StorageConfig_GroupBox_X_Label.setToolTip("Percentual da reatância interna equivalente")
        self.StorageConfig_GroupBox_X_LineEdit = QLineEdit()
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_X_Label, 9, 2, 1, 1)
        self.StorageConfig_GroupBox_Layout.addWidget(self.StorageConfig_GroupBox_X_LineEdit, 9, 3, 1, 1)

        self.StorageConfig_GroupBox.setLayout(
            self.StorageConfig_GroupBox_Layout)  # define o Layout do GroupBox StoragesConfig

        self.Tab_layout = QGridLayout()
        self.Tab_layout.addWidget(self.StorageConfig_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Tab_layout)
        self.Storage_Name = self.StorageConfig_GroupBox_Nome_LineEdit.text()
        self.Storage_PercentageReserve = self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()

        self.ConfigStorageController.Storage_Name = self.Storage_Name
        self.ConfigStorageController.Storage_PercentageReserve = self.Storage_PercentageReserve



class InversorConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIInversorConfig()

        self.EffCurve = opendss.storage.class_config_eff_curve.C_Config_EffCurve_Dialog()

    def InitUIInversorConfig(self):
        ############################ GroupBox Configuracoes do Inversor ################################################
        self.InversorConfig_GroupBox = QGroupBox(
            "Configurações do Inversor")  # Criando a GroupBox Configurações do Inversor
        self.InversorConfig_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InversorConfig é em Grid
        # Configurar propriedade "kVA"
        self.InversorConfig_GroupBox_kVA_Label = QLabel("Pot. aparente máxima (kVA)")
        self.InversorConfig_GroupBox_kVA_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kVA_Label, 0, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kVA_LineEdit, 0, 1, 1, 1)
        # Configurar propriedade "kWrated" (Pot. ativa máxima de saída do inversor)
        self.InversorConfig_GroupBox_kWrated_Label = QLabel("Pot. ativa máxima (kW)")
        self.InversorConfig_GroupBox_kWrated_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kWrated_Label, 0, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kWrated_LineEdit, 0, 3, 1, 1)
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
        self.InversorConfig_GroupBox_CutIn_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutIn_Label, 2, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutIn_LineEdit, 2, 1, 1, 1)
        # Configurar propriedade "CutOut" (Pot. ativa máxima de saída do inversor)
        self.InversorConfig_GroupBox_CutOut_Label = QLabel("CutOut (%)")
        self.InversorConfig_GroupBox_CutOut_Label.setToolTip("Potência CutOut em percentual da potência aparente (kVA) do\
inversor.\nÉ a potência DC mínima para manter o inversor ligado. Precisa ser\nigual ou menor que CutIn")
        self.InversorConfig_GroupBox_CutOut_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutOut_Label, 2, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_CutOut_LineEdit, 2, 3, 1, 1)
        # Configurar propriedade "kvarMax" (máximo geração de kvar aceita pelo inversor)
        self.InversorConfig_GroupBox_kvarMax_Label = QLabel("Máxima Geração de kvar")
        self.InversorConfig_GroupBox_kvarMax_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMax_Label, 3, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMax_LineEdit, 3, 1, 1, 1)
        # Configurar propriedade "kvarMaxAbs" (máximo absorção de kvar aceita pelo inversor)
        self.InversorConfig_GroupBox_kvarMaxAbs_Label = QLabel("Máxima Absorção de kvar")
        self.InversorConfig_GroupBox_kvarMaxAbs_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMaxAbs_Label, 3, 2, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_kvarMaxAbs_LineEdit, 3, 3, 1, 1)
        # Configurar propriedade "%PminNoVars" (pot. ativa mínima na qual o inversor nao produz/absorve pot. reativa)
        self.InversorConfig_GroupBox_PminNoVars_Label = QLabel("Pot. mín. s/ despacho de reativo (%)")
        self.InversorConfig_GroupBox_PminNoVars_Label.setToolTip("Potência ativa mínima, em percentual da potência ativa \
máxima (kW),\nna qual não há produção/absorção de reativo")
        self.InversorConfig_GroupBox_PminNoVars_LineEdit = QLineEdit()
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminNoVars_Label, 4, 0, 1, 1)
        self.InversorConfig_GroupBox_Layout.addWidget(self.InversorConfig_GroupBox_PminNoVars_LineEdit, 4, 1, 1, 1)
        # Configurar propriedade "%PminkvarMax" (pot. ativa mínima que permite o inversor produzir/absorver pot. reativa)
        self.InversorConfig_GroupBox_PminkvarMax_Label = QLabel("Pot. mín. c/ despacho de reativo (%)")
        self.InversorConfig_GroupBox_PminkvarMax_Label.setToolTip("Potência ativa mínima, em percentual da potência ativa \
máxima (kW), que permite\no inversor produzir/absorver potencia reativa até um valor máximo")
        self.InversorConfig_GroupBox_PminkvarMax_LineEdit = QLineEdit()
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


class Storage_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, bus):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Storage_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)
        ## Column 1 - Bus:
        self.setText(1, bus)
        ## Column 2 - Modo Despacho:
        # self.setText(2, points)
