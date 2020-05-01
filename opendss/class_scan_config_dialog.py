# Carvalho Tag
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QHBoxLayout, \
    QPushButton, QVBoxLayout, QTabWidget, QComboBox, QLineEdit,  QWidget, QMessageBox
from PyQt5.QtCore import Qt

import configparser
import class_exception
import random
import opendss.class_conn
import opendss.class_opendss
import config as cfg

class C_SCAnalyze_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Short Circuit Settings"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.SCDataInfo = [] ## Vetor com todos os dicionários para faltas  - Com

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)

        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        self.TabWidget = QTabWidget()
        self.TabBasic = BasicTab()  # QWidget
        self.TabAdvanced = AdvancedTab()  # QWidget
        self.TabWidget.addTab(self.TabBasic, "Basic")
        self.TabWidget.addTab(self.TabAdvanced, "Advanced")
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
        try:
            config = configparser.ConfigParser()
            ## Basic
            config['FltConfigBasic'] = {}
            config['FltConfigBasic']['FltBus'] = self.get_combobox(self.TabBasic.FltBus_GroupBox_ComboBox)
            config['FltConfigBasic']['FltPhases'] = self.get_combobox(self.TabBasic.FltPhases_GroupBox_ComboBox)
            config['FltConfigBasic']['FltRst'] = self.get_lineedit(self.TabBasic.FltResistance_GroupBox_LineEdit)
            config['FltConfigBasic']['FltType'] = self.get_combobox(self.TabBasic.FltType_GroupBox_ComboBox)
            config['FltConfigBasic']['FltTime'] = self.get_lineedit(self.TabBasic.FltTime_GroupBox_LineEdit)
            config['FltConfigBasic']['FltBus2'] = self.get_combobox(self.TabBasic.FltBus2_GroupBox_ComboBox)

            config['FltConfigAdvanced'] = {}
            config['FltConfigAdvanced']['FltBaseFreq'] = self.get_combobox(self.TabAdvanced.FltBaseFreq_GroupBox_ComboBox)
            config['FltConfigAdvanced']['FltRstDev'] = self.get_lineedit(self.TabAdvanced.FltRstDev_GroupBox_LineEdit)
            config['FltConfigAdvanced']['FltRepair'] = self.get_lineedit(self.TabAdvanced.FltRepair_GroupBox_LineEdit)

            with open('scanconfig.ini', 'w') as configfile:
                config.write(configfile)

            QMessageBox(QMessageBox.Information, "SC Analyze Configuration", "Configurações Salvas com Sucesso!",
                        QMessageBox.Ok).exec()

        except:
            raise class_exception.ExecConfigOpenDSS("Configuração da Análise de Curto Circuito", "Erro ao salvar parâmetros!")

    def get_lineedit(self, lineedit):
        self.lineedit = lineedit.text()
        return self.lineedit

    def get_combobox(self, combobox):
        ## itemData corresponde à tag do item selecionado no combobox. "None" aparece quando não há nada no combobox
        ## currentIndex indica o índice do item selecionado
        self.combobox = str(combobox.itemData(combobox.currentIndex()))
        return self.combobox

    def loadParameters(self):
        dataInfo = {}
        ## Basic
        dataInfo["FltBus"] = self.get_combobox(self.TabBasic.FltBus_GroupBox_ComboBox)
        dataInfo["FltPhases"] = self.get_combobox(self.TabBasic.FltPhases_GroupBox_ComboBox)
        dataInfo["FltRst"] = self.get_lineedit(self.TabBasic.FltResistance_GroupBox_LineEdit)
        dataInfo["FltTime"] = self.get_lineedit(self.TabBasic.FltTime_GroupBox_LineEdit)
        dataInfo["FltType"] = self.get_combobox(self.TabBasic.FltType_GroupBox_ComboBox)
        dataInfo["FltBus2"] = self.get_combobox(self.TabBasic.FltBus2_GroupBox_ComboBox)
        ## Advanced
        dataInfo["FltBaseFreq"] = self.get_combobox(self.TabAdvanced.FltBaseFreq_GroupBox_ComboBox)
        dataInfo["FltRstDev"] = self.get_lineedit(self.TabAdvanced.FltRstDev_GroupBox_LineEdit)
        dataInfo["FltRepair"] = self.get_lineedit(self.TabAdvanced.FltRepair_GroupBox_LineEdit)
        ####

        ## Multiplas faltas será aqui! Mesma lógica dos medidores
        self.SCDataInfo.clear() ## Apenas para deixar uma falta disponível
        self.SCDataInfo.append(dataInfo)

    def loadDefaultParameters(self):  # Só carrega quando abre a janela pela primeira vez
        try:
            config = configparser.ConfigParser()
            config.read('scanconfig.ini')

            ### Basic
            self.TabBasic.FltBus_GroupBox_ComboBox.setCurrentText(config['FltConfigBasic']['fltbus'])
            self.TabBasic.FltPhases_GroupBox_ComboBox.setCurrentText(config['FltConfigBasic']['fltphases'])
            self.TabBasic.FltResistance_GroupBox_LineEdit.setText(config['FltConfigBasic']['fltrst'])
            self.TabBasic.FltTime_GroupBox_LineEdit.setText(config['FltConfigBasic']['flttime'])
            self.TabBasic.FltType_GroupBox_ComboBox.setCurrentText(config['FltConfigBasic']['flttype'])
            self.TabBasic.FltBus2_GroupBox_ComboBox.setCurrentText(config['FltConfigBasic']['fltbus2'])
            ### Advanced
            self.TabAdvanced.FltBaseFreq_GroupBox_ComboBox.setCurrentText(config['FltConfigAdvanced']['fltbasefreq'])
            self.TabAdvanced.FltRstDev_GroupBox_LineEdit.setText(config['FltConfigAdvanced']['fltrstdev'])
            self.TabAdvanced.FltRepair_GroupBox_LineEdit.setText(config['FltConfigAdvanced']['fltrepair'])
            ##### Carregando parâmetros

            self.loadParameters()
        except:
            raise class_exception.ExecConfigOpenDSS("Configuração da Simulação",
                                                    "Erro ao carregar os parâmetros do Fluxo de Carga!")

    def Accept(self):
        self.loadParameters()
        self.OpenDSS.SCDataInfo = self.SCDataInfo
        self.close()

    def updateDialog(self):
        self.TabBasic.FltBus_GroupBox_ComboBox.clear()
        buslist = self.OpenDSS.getBusList()
        for index, item in enumerate(buslist):
            self.TabBasic.FltBus_GroupBox_ComboBox.addItem(item, item)
        print(f'Tamanho da buslist pelo AllBusNames : {len(buslist)}')

        print(f'Tamanho da buslist pelo AllBusNames : {len(buslist)}')



class BasicTab(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIBasicTab()

    def InitUIBasicTab(self):
        self.typelist = ['Temporary', 'Permanent']
        self.typelist_data = ['yes', 'no']

        self.FltType_GroupBox = QGroupBox("Fault Type")
        self.FltType_GroupBox_Layout = QHBoxLayout()
        self.FltType_GroupBox_ComboBox = QComboBox()
        self.FltType_GroupBox_ComboBox.setMaximumWidth(150)
        self.FltType_GroupBox_Layout.addWidget(self.FltType_GroupBox_ComboBox)
        self.FltType_GroupBox.setLayout(self.FltType_GroupBox_Layout)
        #Adicionando itens ao combobox com suas respectivas tags(data)
        for index,item in enumerate(self.typelist):
            self.FltType_GroupBox_ComboBox.addItem(item,self.typelist_data[index])

        ##### Fault Phases
        self.phaseslist = ['1 phase', '3 phases']
        self.phaseslist_data = ['1', '3']
        self.FltPhases_GroupBox = QGroupBox("Fault Phases")
        self.FltPhases_GroupBox_Layout = QHBoxLayout()
        self.FltPhases_GroupBox_ComboBox = QComboBox()
        self.FltPhases_GroupBox_ComboBox.setMaximumWidth(150)
        self.FltPhases_GroupBox_Layout.addWidget(self.FltPhases_GroupBox_ComboBox)
        self.FltPhases_GroupBox.setLayout(self.FltPhases_GroupBox_Layout)
        #Adicionando itens ao combobox com suas respectivas tags(data)
        for index,item in enumerate(self.phaseslist):
            self.FltPhases_GroupBox_ComboBox.addItem(item,self.phaseslist_data[index])

        ##### Fault Resistance
        self.FltResistance_GroupBox = QGroupBox("Fault Resistance (Ω)")
        self.FltResistance_GroupBox_Layout = QHBoxLayout()
        self.FltResistance_GroupBox_LineEdit = QLineEdit()
        self.FltResistance_GroupBox_LineEdit.setPlaceholderText('Ex: 0.0001')
        self.FltResistance_GroupBox_LineEdit.setMaximumWidth(150)
        self.FltResistance_GroupBox_Layout.addWidget(self.FltResistance_GroupBox_LineEdit)
        self.FltResistance_GroupBox.setLayout(self.FltResistance_GroupBox_Layout)

        ##### Fault Insert Time
        self.FltTime_GroupBox = QGroupBox("Fault On - time (s)")
        self.FltTime_GroupBox_Layout = QHBoxLayout()
        self.FltTime_GroupBox_LineEdit = QLineEdit()
        self.FltTime_GroupBox_LineEdit.setPlaceholderText('Ex: 1')
        self.FltTime_GroupBox_LineEdit.setMaximumWidth(150)
        self.FltTime_GroupBox_Layout.addWidget(self.FltTime_GroupBox_LineEdit)
        self.FltTime_GroupBox.setLayout(self.FltTime_GroupBox_Layout)

        ##### Fault Bus 1
        self.FltBus_GroupBox = QGroupBox("Fault Bus")
        self.FltBus_GroupBox_Layout = QHBoxLayout()
        self.FltBus_GroupBox_ComboBox = QComboBox()
        self.FltBus_GroupBox_ComboBox.currentIndexChanged.connect(self.addBusesFltBus2)
        self.FltBus_GroupBox_ComboBox.setMaximumWidth(150)
        self.FltBus_GroupBox_Layout.addWidget(self.FltBus_GroupBox_ComboBox)
        self.FltBus_GroupBox.setLayout(self.FltBus_GroupBox_Layout)

        ##### Fault Bus 2 (Optional)
        self.FltBus2_GroupBox = QGroupBox("Fault Bus 2 (Optional)")
        self.FltBus2_GroupBox_Layout = QHBoxLayout()
        self.FltBus2_GroupBox_ComboBox = QComboBox()
        self.FltBus2_GroupBox_ComboBox.setMaximumWidth(150)
        self.FltBus2_GroupBox_Layout.addWidget(self.FltBus2_GroupBox_ComboBox)
        self.FltBus2_GroupBox.setLayout(self.FltBus2_GroupBox_Layout)

        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.FltType_GroupBox)
        self.Tab_layout.addWidget(self.FltPhases_GroupBox)
        self.Tab_layout.addWidget(self.FltResistance_GroupBox)
        self.Tab_layout.addWidget(self.FltTime_GroupBox)
        self.Tab_layout.addWidget(self.FltBus_GroupBox)
        self.Tab_layout.addWidget(self.FltBus2_GroupBox)
        self.setLayout(self.Tab_layout)

    def addBusesFltBus2(self):

        tmpFltBus2 = self.FltBus2_GroupBox_ComboBox.currentText()

        self.FltBus2_GroupBox_ComboBox.clear()
        self.FltBus2_GroupBox_ComboBox.addItem("")
        listBus = [self.FltBus_GroupBox_ComboBox.itemText(i) for i in range(0, self.FltBus_GroupBox_ComboBox.count())]
        listBus.remove(self.FltBus_GroupBox_ComboBox.currentText())
        for index, item in enumerate(listBus):
            self.FltBus2_GroupBox_ComboBox.addItem(item, item)

        if self.FltBus_GroupBox_ComboBox.currentText() != tmpFltBus2:
            self.FltBus2_GroupBox_ComboBox.setCurrentText(tmpFltBus2)

class AdvancedTab(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUIAdvancedTab()

    def InitUIAdvancedTab(self):
        ##### Base frequency
        self.freqlist = ['60 Hz', '50 Hz']
        self.frelist_data = ['60', '50']
        self.FltBaseFreq_GroupBox = QGroupBox("Base Frequency ")
        self.FltBaseFreq_GroupBox_Layout = QHBoxLayout()
        self.FltBaseFreq_GroupBox_ComboBox = QComboBox()
        self.FltBaseFreq_GroupBox_ComboBox.setMaximumWidth(150)
        for index, item in enumerate(self.freqlist):
            self.FltBaseFreq_GroupBox_ComboBox.addItem(item, self.frelist_data[index])

        self.FltBaseFreq_GroupBox_Layout.addWidget(self.FltBaseFreq_GroupBox_ComboBox)
        self.FltBaseFreq_GroupBox.setLayout(self.FltBaseFreq_GroupBox_Layout)

        ##### Resistance Deviation for Monte Carlo Fault
        self.FltRstDev_GroupBox = QGroupBox("Resistance Deviation (%)")
        self.FltRstDev_GroupBox_Layout = QHBoxLayout()
        self.FltRstDev_GroupBox_LineEdit = QLineEdit()
        self.FltRstDev_GroupBox_LineEdit.setPlaceholderText('Default: 0')
        self.FltRstDev_GroupBox_LineEdit.setMaximumWidth(150)
        self.FltRstDev_GroupBox_Layout.addWidget(self.FltRstDev_GroupBox_LineEdit)
        self.FltRstDev_GroupBox.setLayout(self.FltRstDev_GroupBox_Layout)

        ##### Fault Repair
        self.FltRepair_GroupBox = QGroupBox("Hours to Repair")
        self.FltRepair_GroupBox_Layout = QHBoxLayout()
        self.FltRepair_GroupBox_LineEdit = QLineEdit()
        self.FltRepair_GroupBox_LineEdit.setPlaceholderText('Ex: 1')
        self.FltRepair_GroupBox_LineEdit.setMaximumWidth(150)
        self.FltRepair_GroupBox_Layout.addWidget(self.FltRepair_GroupBox_LineEdit)
        self.FltRepair_GroupBox.setLayout(self.FltRepair_GroupBox_Layout)

        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.FltBaseFreq_GroupBox)
        self.Tab_layout.addWidget(self.FltRstDev_GroupBox)
        self.Tab_layout.addWidget(self.FltRepair_GroupBox)

        self.setLayout(self.Tab_layout)