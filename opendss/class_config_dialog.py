from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QCheckBox, \
    QPushButton, QVBoxLayout, QTabWidget, QLabel, QComboBox, QLineEdit, QRadioButton, QSpinBox, QWidget, QMessageBox
from PyQt5.QtCore import Qt

import configparser
import class_exception
import platform
import config as cfg

import opendss.class_config_loadshape_dialog



class C_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Settings"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.dataInfo = {}

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()


        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ##### Option OpenDSS
        self.Conn_GroupBox = QGroupBox("Método de Conexão com o OpenDSS")
        self.Conn_GroupBox_Layout = QHBoxLayout()

        self.Conn_GroupBox_OpenDSSDirect = QRadioButton("OpenDSSDirect.py")
        self.Conn_GroupBox_OpenDSSDirect.setChecked(True)
        #self.Conn_GroupBox_OpenDSSDirect.toggled.connect(lambda: self.onConnRadioBtn(self.Conn_GroupBox_OpenDSSDirect))
        self.Conn_GroupBox_Layout.addWidget(self.Conn_GroupBox_OpenDSSDirect)

        self.Conn_GroupBox_COMInterface = QRadioButton("COM Interface")
        self.Conn_GroupBox_COMInterface.setChecked(False)
        #self.Conn_GroupBox_COMInterface.toggled.connect(lambda: self.onConnRadioBtn(self.Conn_GroupBox_COMInterface))
        if platform.system() == "Windows":
            self.Conn_GroupBox_COMInterface.setDisabled(False)
        else:
            self.Conn_GroupBox_COMInterface.setDisabled(True)

        self.Conn_GroupBox_Layout.addWidget(self.Conn_GroupBox_COMInterface)

        self.Conn_GroupBox.setLayout(self.Conn_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Conn_GroupBox)

        ###### Tabs
        self.TabWidget = QTabWidget()
        self.TabLoadFlow = LoadFlow()  # QWidget
        self.TabWidget.addTab(self.TabLoadFlow, "Simulação")

        self.Dialog_Layout.addWidget(self.TabWidget)

        ###### Botões
        self.Dilalog_Btns_Layout = QHBoxLayout()
        self.Dilalog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dilalog_Btns_Save_Btn = QPushButton("Salvar Parâmetros")
        self.Dilalog_Btns_Save_Btn.setIcon(QIcon('img/icon_save.png'))
        self.Dilalog_Btns_Save_Btn.setFixedWidth(170)
        self.Dilalog_Btns_Save_Btn.clicked.connect(self.saveDefaultParameters)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Save_Btn)


        self.Dilalog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dilalog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dilalog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Cancel_Btn)

        self.Dilalog_Btns_Ok_Btn = QPushButton("OK")
        self.Dilalog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dilalog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Ok_Btn)


        self.Dialog_Layout.addLayout(self.Dilalog_Btns_Layout,0)

        self.setLayout(self.Dialog_Layout)

        ###
        self.loadDefaultParameters()

    def getConn_GroupBox_Radio_Btn(self):
        if self.Conn_GroupBox_OpenDSSDirect.isChecked():
            return "OpenDSSDirect"
        else:
            return "COM"

    def loadParameters(self):

        ## Geral
        self.dataInfo["openDSSConn"] = self.getConn_GroupBox_Radio_Btn()
        ### LoadFlow
        self.dataInfo["VoltageBase"] = self.TabLoadFlow.get_VoltageBases() #voltagebase
        self.dataInfo["UNCMT"] = self.TabLoadFlow.get_UNC(self.TabLoadFlow.LoadFlow_GroupBox_UNCMT_CheckBox)
        self.dataInfo["UNCBTTD"] = self.TabLoadFlow.get_UNC(self.TabLoadFlow.LoadFlow_GroupBox_UNCBT_TD_CheckBox)
        self.dataInfo["Mode"] = self.TabLoadFlow.get_Mode()

        #if self.dataInfo["Mode"] == "Daily":
        self.dataInfo["StepSize"] = self.TabLoadFlow.get_Stepsize()
        self.dataInfo["StepSizeTime"] = self.TabLoadFlow.get_Stepsize_Time()
        self.dataInfo["Number"] = self.TabLoadFlow.get_Number()
        self.dataInfo["Maxiterations"] = self.TabLoadFlow.get_Maxiterations()
        self.dataInfo["Maxcontroliter"] = self.TabLoadFlow.get_Maxcontroliter()
        self.dataInfo["LoadShapes"] = self.TabLoadFlow.get_LoadShapes()

        if self.dataInfo["Mode"] == "Daily":
            if not self.dataInfo["LoadShapes"]:
                QMessageBox(QMessageBox.Information, "OpenDSS Configuration", "Curvas de cargas não estão carregadas!",
                            QMessageBox.Ok).exec()

            if (self.dataInfo["UNCMT"] == "0") or (self.dataInfo["UNCBTTD"] == "0"):
                QMessageBox(QMessageBox.Information, "OpenDSS Configuration", "Algumas cargas não serão consideradas!",
                            QMessageBox.Ok).exec()

    def Accept(self):
        self.loadParameters()
        self.close()

    def saveDefaultParameters(self):
        try:
            config = configparser.ConfigParser()

            ## Default
            config['Default']= {  }
            config['Default']['OpenDSSConn'] = self.getConn_GroupBox_Radio_Btn()

            ## Load Flow
            config['LoadFlow']= {  }
            config['LoadFlow']['VoltageBase'] = self.TabLoadFlow.get_VoltageBases()
            config['LoadFlow']["UNCMT"] = self.TabLoadFlow.get_UNC(self.TabLoadFlow.LoadFlow_GroupBox_UNCMT_CheckBox)
            config['LoadFlow']["UNCBTTD"] = self.TabLoadFlow.get_UNC(self.TabLoadFlow.LoadFlow_GroupBox_UNCBT_TD_CheckBox)
            config['LoadFlow']['Mode'] = self.TabLoadFlow.get_Mode()
            config['LoadFlow']['StepSize'] = str(self.TabLoadFlow.get_Stepsize())
            config['LoadFlow']['StepSizeTime'] = self.TabLoadFlow.get_Stepsize_Time()
            config['LoadFlow']['Number'] = str(self.TabLoadFlow.get_Number())
            config['LoadFlow']['Maxiterations'] = str(self.TabLoadFlow.get_Maxiterations())
            config['LoadFlow']['Maxcontroliter']  = str(self.TabLoadFlow.get_Maxcontroliter())

            with open('siplaconfig.ini', 'w') as configfile:
                config.write(configfile)

            QMessageBox(QMessageBox.Information, "OpenDSS Configuration", "Configurações Salvas com Sucesso!", QMessageBox.Ok).exec()

        except:
            raise class_exception.ExecConfigOpenDSS("Configuração da Simulação", "Erro ao salvar os parâmetros do Fluxo de Carga!")


    def loadDefaultParameters(self): # Só carrega quando abre a janela pela primeira vez
        try:
            config = configparser.ConfigParser()
            config.read('siplaconfig.ini')

            ## Default
            if config['Default']['OpenDSSConn'] == "OpenDSSDirect":
                self.Conn_GroupBox_OpenDSSDirect.setChecked(True)
                self.Conn_GroupBox_COMInterface.setChecked(False)
            else:
                self.Conn_GroupBox_OpenDSSDirect.setChecked(False)
                self.Conn_GroupBox_COMInterface.setChecked(True)

            if config['LoadFlow']["UNCMT"] == "1":
                self.TabLoadFlow.LoadFlow_GroupBox_UNCMT_CheckBox.setChecked(True)
            else:
                self.TabLoadFlow.LoadFlow_GroupBox_UNCMT_CheckBox.setChecked(False)

            if config['LoadFlow']["UNCBTTD"] == "1":
                self.TabLoadFlow.LoadFlow_GroupBox_UNCBT_TD_CheckBox.setChecked(True)
            else:
                self.TabLoadFlow.LoadFlow_GroupBox_UNCBT_TD_CheckBox.setChecked(False)


            ### Tab Load Flow
            self.TabLoadFlow.LoadFlow_GroupBox_VoltageBase_LineEdit.setText(config['LoadFlow']['VoltageBase'])
            self.TabLoadFlow.Mode_GroupBox_ComboBox.setCurrentText(config['LoadFlow']['Mode'] )
            self.TabLoadFlow.Complements_Daily_GroupBox_Stepsize_SpinBox.setValue( int( config['LoadFlow']['StepSize']))
            self.TabLoadFlow.Complements_Daily_GroupBox_Stepsize_ComboBox.setCurrentText(config['LoadFlow']['StepSizeTime'])
            self.TabLoadFlow.Complements_Daily_GroupBox_Number_SpinBox.setValue( int(config['LoadFlow']['Number'] ))
            self.TabLoadFlow.Complements_Daily_GroupBox_Maxiterations_SpinBox.setValue( int(config['LoadFlow']['Maxiterations']))
            self.TabLoadFlow.Complements_Daily_GroupBox_Maxcontroliter_SpinBox.setValue(int(config['LoadFlow']['Maxcontroliter']))

            ##### Carregando parâmetros
            self.loadParameters()

        except:
            raise class_exception.ExecConfigOpenDSS("Configuração da Simulação", "Erro ao carregar os parâmetros do Fluxo de Carga!")


class LoadFlow(QWidget):
    def __init__(self):
        super().__init__()

        self.listmode = ["Direct", "Snapshot", "Daily"]  # lista de modos disponíveis

        self.InitUILoadFlow()

    def InitUILoadFlow(self):
        #Curvas de Carga
        self.LoadShapesDialog = opendss.class_config_loadshape_dialog.C_Config_LoadShape_Dialog()

        ## GroupBox Fluxo de Carga
        self.LoadFlow_GroupBox = QGroupBox("Fluxo de Carga")
        self.LoadFlow_GroupBox_VoltageBase_Label = QLabel("Set VoltageBases")
        self.LoadFlow_GroupBox_VoltageBase_LineEdit = QLineEdit()
        # Layout do GroupoBox Fluxo de Carga
        self.LoadFlow_GroupBox_Layout = QGridLayout()
        self.LoadFlow_GroupBox_Layout.addWidget(self.LoadFlow_GroupBox_VoltageBase_Label, 0, 0, 1, 1)
        self.LoadFlow_GroupBox_Layout.addWidget(self.LoadFlow_GroupBox_VoltageBase_LineEdit, 0, 1, 1, 1)

        ##
        self.LoadFlow_GroupBox_UNCMT_CheckBox = QCheckBox("Considerar Cargas de Média Tensão")
        self.LoadFlow_GroupBox_UNCBT_TD_CheckBox = QCheckBox("Considerar Cargas de Baixa Tensão no Transformador de Distribuição")

        self.LoadFlow_GroupBox_Layout.addWidget(self.LoadFlow_GroupBox_UNCMT_CheckBox, 1, 0, 1, 2)
        self.LoadFlow_GroupBox_Layout.addWidget(self.LoadFlow_GroupBox_UNCBT_TD_CheckBox, 2, 0, 1, 2)

        ## GroupBox Modo
        self.Mode_GroupBox = QGroupBox("Modo")

        self.Mode_GroupBox_Label = QLabel("Set Mode")
        self.Mode_GroupBox_ComboBox = QComboBox()
        self.Mode_GroupBox_ComboBox.addItems(self.listmode)
        self.Mode_GroupBox_ComboBox.currentIndexChanged.connect(self.setDisabled_Complements_Snapshot_GroupBox)
        self.Mode_GroupBox_QPushButton = QPushButton("Ok")
        self.Mode_GroupBox_QPushButton.setFixedWidth(30)
        self.Mode_GroupBox_QPushButton.clicked.connect(self.setDisabled_Complements_Snapshot_GroupBox)

        # Layout do GroupoBox modo
        self.Mode_GroupBox_Layout = QGridLayout()
        self.Mode_GroupBox_Layout.addWidget(self.Mode_GroupBox_Label, 1, 1, 1, 1)
        self.Mode_GroupBox_Layout.addWidget(self.Mode_GroupBox_ComboBox, 1, 2, 1, 1)
        self.Mode_GroupBox_Layout.addWidget(self.Mode_GroupBox_QPushButton, 1, 3, 1, 1)

        ## GroupBox complementos do Daily
        self.Complements_Daily_GroupBox = QGroupBox("Complementos do Daily")

        self.Complements_Daily_GroupBox_Stepsize_Label = QLabel("Set Stepsize:")
        self.Complements_Daily_GroupBox_Stepsize_ComboBox = QComboBox()
        self.Complements_Daily_GroupBox_Stepsize_ComboBox.addItems(["sec", "min", "hr"])
        self.Complements_Daily_GroupBox_Number_Label = QLabel("Set Number:")
        self.Complements_Daily_GroupBox_Maxiterations_Label = QLabel("Set Maxiterations:")
        self.Complements_Daily_GroupBox_Maxcontroliter_Label = QLabel("Set Maxcontroliter:")

        ## LineEdit complementos

        self.Complements_Daily_GroupBox_Stepsize_SpinBox = QSpinBox()
        self.Complements_Daily_GroupBox_Number_SpinBox = QSpinBox()
        self.Complements_Daily_GroupBox_Maxiterations_SpinBox = QSpinBox()
        self.Complements_Daily_GroupBox_Maxcontroliter_SpinBox = QSpinBox()

        self.Complements_Daily_LoadShape_Btn = QPushButton("Load Shapes")
        self.Complements_Daily_LoadShape_Btn.setIcon(QIcon('img/icon_ok.png'))
        #self.Complements_Daily_LoadShape_Btn.setFixedWidth(300)
        self.Complements_Daily_LoadShape_Btn.clicked.connect(self.dialogLoadShape)


        # Layout do GroupoBox complementos
        self.Complements_Daily_GroupBox_Layout = QGridLayout()
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Stepsize_Label, 0, 0, 1, 1)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Number_Label, 1, 0, 1, 1)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Stepsize_SpinBox, 0, 1, 1, 1)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Stepsize_ComboBox, 0, 2, 1, 1)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Number_SpinBox, 1, 1, 1, 2)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Maxiterations_Label, 2, 0, 1, 1)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Maxcontroliter_Label, 3, 0, 1, 1)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Maxiterations_SpinBox, 2, 1, 1, 2)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_GroupBox_Maxcontroliter_SpinBox, 3, 1, 1, 2)
        self.Complements_Daily_GroupBox_Layout.addWidget(self.Complements_Daily_LoadShape_Btn, 4, 1, 1, 2)

        # Seta layouts

        self.LoadFlow_GroupBox.setLayout(self.LoadFlow_GroupBox_Layout)
        self.Mode_GroupBox.setLayout(self.Mode_GroupBox_Layout)
        self.Complements_Daily_GroupBox.setLayout(self.Complements_Daily_GroupBox_Layout)

        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.LoadFlow_GroupBox)
        self.Tab_layout.addWidget(self.Mode_GroupBox)
        self.Tab_layout.addWidget(self.Complements_Daily_GroupBox)

        self.setLayout(self.Tab_layout)

        self.setDisabled_Complements_Snapshot_GroupBox()

    def setDisabled_Complements_Snapshot_GroupBox(self):

        if self.Mode_GroupBox_ComboBox.currentText() == "Daily":
            self.Complements_Daily_GroupBox.setHidden(False)
            self.Complements_Daily_GroupBox_Stepsize_SpinBox.setEnabled(True)
            self.Complements_Daily_GroupBox_Stepsize_ComboBox.setEnabled(True)
            self.Complements_Daily_GroupBox_Number_SpinBox.setEnabled(True)
            self.Complements_Daily_GroupBox_Maxiterations_SpinBox.setEnabled(True)
            self.Complements_Daily_GroupBox_Maxcontroliter_SpinBox.setEnabled(True)
            self.Complements_Daily_LoadShape_Btn.setEnabled(True)
        else:
            self.Complements_Daily_GroupBox.setHidden(True)
            self.Complements_Daily_GroupBox_Stepsize_SpinBox.setEnabled(False)
            self.Complements_Daily_GroupBox_Stepsize_ComboBox.setEnabled(False)
            self.Complements_Daily_GroupBox_Number_SpinBox.setEnabled(False)
            self.Complements_Daily_GroupBox_Maxiterations_SpinBox.setEnabled(False)
            self.Complements_Daily_GroupBox_Maxcontroliter_SpinBox.setEnabled(False)
            self.Complements_Daily_LoadShape_Btn.setEnabled(False)


    # Métodos Set Variáveis

    def dialogLoadShape(self):
        self.LoadShapesDialog.nPointsLoadDef = self.get_Number()
        self.LoadShapesDialog.nStepSizeDef = self.get_Stepsize()
        self.LoadShapesDialog.nStepSizeTimeDef = self.get_Stepsize_Time()
        self.LoadShapesDialog.show()


    def get_VoltageBases(self):
        return self.LoadFlow_GroupBox_VoltageBase_LineEdit.text()

    def get_UNC(self, obj):
        if obj.checkState() == Qt.Checked:
            return "1"
        else:
            return "0"

    def get_Mode(self):
        return self.Mode_GroupBox_ComboBox.currentText()

    def get_Stepsize(self):
        return self.Complements_Daily_GroupBox_Stepsize_SpinBox.value()

    def get_Stepsize_Time(self):
        return self.Complements_Daily_GroupBox_Stepsize_ComboBox.currentText()

    def get_Number(self):
        return self.Complements_Daily_GroupBox_Number_SpinBox.value()

    def get_Maxiterations(self):
        return self.Complements_Daily_GroupBox_Maxiterations_SpinBox.value()

    def get_Maxcontroliter(self):
        return self.Complements_Daily_GroupBox_Maxcontroliter_SpinBox.value()

    def get_LoadShapes(self):
        return self.LoadShapesDialog.dataLoadShapes


