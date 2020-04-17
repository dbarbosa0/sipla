from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout,\
    QPushButton, QVBoxLayout, QTabWidget, QLabel, QComboBox, QLineEdit, QRadioButton, QSpinBox, QWidget, QMessageBox
from PyQt5.QtCore import Qt


import typing
import configparser
import class_exception
import platform


class simulationOpenDSS(typing.NamedTuple):
    ### Default
    openDSSConn: str
    ### LoadFlow
    VoltageBase: str
    Mode: str
    StepSize: str
    Number: str
    Maxiterations: int
    Maxcontroliter: int


class C_OpenDSS_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Settings"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(500, 500)

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
        self.Dilalog_Btns_Ok_Btn.clicked.connect(self.accept)
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
        self.dataInfo = simulationOpenDSS(
            ## Geral
            self.getConn_GroupBox_Radio_Btn(),
            ## Laod Flow
            self.TabLoadFlow.get_VoltageBases(), #voltagebase
            self.TabLoadFlow.get_Mode(), #mode
            self.TabLoadFlow.get_Stepsize(), #stepsize
            self.TabLoadFlow.get_Number(), #number
            self.TabLoadFlow.get_Maxiterations(), #maxiterations
            self.TabLoadFlow.get_Maxcontroliter() #maxcontroliter
            )

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
            config['LoadFlow']['Mode'] = self.TabLoadFlow.get_Mode()
            config['LoadFlow']['StepSize'] = self.TabLoadFlow.get_Stepsize()
            config['LoadFlow']['Number'] = self.TabLoadFlow.get_Number()
            config['LoadFlow']['Maxiterations'] = str( self.TabLoadFlow.get_Maxiterations() )
            config['LoadFlow']['Maxcontroliter']  = str( self.TabLoadFlow.get_Maxcontroliter() )

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
            if config['Default']['OpenDSSConn']  == "OpenDSSDirect":
                self.Conn_GroupBox_OpenDSSDirect.setChecked(True)
                self.Conn_GroupBox_COMInterface.setChecked(False)
            else:
                self.Conn_GroupBox_OpenDSSDirect.setChecked(False)
                self.Conn_GroupBox_COMInterface.setChecked(True)


            ### Tab Load Flow
            self.TabLoadFlow.LoadFlow_GroupBox_VoltageBase_LineEdit.setText(config['LoadFlow']['VoltageBase'])
            self.TabLoadFlow.Mode_GroupBox_ComboBox.setCurrentText(config['LoadFlow']['Mode'] )
            self.TabLoadFlow.Complements_GroupBox_Stepsize_LineEdit.setText( config['LoadFlow']['StepSize'])
            self.TabLoadFlow.Complements_GroupBox_Number_LineEdit.setText( config['LoadFlow']['Number'] )
            self.TabLoadFlow.Complements_GroupBox_Maxiterations_SpinBox.setValue( int(config['LoadFlow']['Maxiterations']))
            self.TabLoadFlow.Complements_GroupBox_Maxcontroliter_SpinBox.setValue(int(config['LoadFlow']['Maxcontroliter']))

            ##### Carregando parâmetros


            self.loadParameters()

        except:
            raise class_exception.ExecConfigOpenDSS("Configuração da Simulação", "Erro ao carregar os parâmetros do Fluxo de Carga!")


class LoadFlow(QWidget):
    def __init__(self):
        super().__init__()

        self.listmode = ["Snapshot", "Daily"]  # lista de modos disponíveis

        self.InitUILoadFlow()

    def InitUILoadFlow(self):


        ## GroupBox Fluxo de Carga
        self.LoadFlow_GroupBox = QGroupBox("Fluxo de Carga")
        self.LoadFlow_GroupBox_VoltageBase_Label = QLabel("Set VoltageBases")
        self.LoadFlow_GroupBox_VoltageBase_LineEdit = QLineEdit()

        # Layout do GroupoBox Fluxo de Carga
        self.LoadFlow_GroupBox_Layout = QGridLayout()
        self.LoadFlow_GroupBox_Layout.addWidget(self.LoadFlow_GroupBox_VoltageBase_Label, 0, 0, 1, 1)
        self.LoadFlow_GroupBox_Layout.addWidget(self.LoadFlow_GroupBox_VoltageBase_LineEdit, 0, 1, 1, 1)
        
        

        ## GroupBox Modo
        self.Mode_GroupBox = QGroupBox("Modo")

        self.Mode_GroupBox_Label = QLabel("Set Mode")
        self.Mode_GroupBox_ComboBox = QComboBox()
        self.Mode_GroupBox_ComboBox.addItems(self.listmode)
        self.Mode_GroupBox_ComboBox.currentIndexChanged.connect( self.setDisabled_Complements_GroupBox)
        self.Mode_GroupBox_QPushButton = QPushButton("Ok")
        self.Mode_GroupBox_QPushButton.setFixedWidth(30)
        self.Mode_GroupBox_QPushButton.clicked.connect(self.setDisabled_Complements_GroupBox)

        # Layout do GroupoBox modo
        self.Mode_GroupBox_Layout = QGridLayout()
        self.Mode_GroupBox_Layout.addWidget(self.Mode_GroupBox_Label, 1, 1, 1, 1)
        self.Mode_GroupBox_Layout.addWidget(self.Mode_GroupBox_ComboBox, 1, 2, 1, 1)
        self.Mode_GroupBox_Layout.addWidget(self.Mode_GroupBox_QPushButton, 1, 3, 1, 1)

        ## GroupBox complementos
        self.Complements_GroupBox = QGroupBox("Complementos")
        self.Complements_GroupBox_Stepsize_Label = QLabel("Set Stepsize:")
        self.Complements_GroupBox_Number_Label = QLabel("Set Number:")
        self.Complements_GroupBox_Maxiterations_Label = QLabel("Set Maxiterations:")
        self.Complements_GroupBox_Maxcontroliter_Label = QLabel("Set Maxcontroliter:")

        ## LineEdit complementos

        self.Complements_GroupBox_Stepsize_LineEdit = QLineEdit()
        self.Complements_GroupBox_Number_LineEdit = QLineEdit()
        self.Complements_GroupBox_Maxiterations_SpinBox = QSpinBox()
        self.Complements_GroupBox_Maxcontroliter_SpinBox = QSpinBox()

        # Layout do GroupoBox complementos
        self.Complements_GroupBox_Layout = QGridLayout()
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Stepsize_Label, 0, 0, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Number_Label, 1, 0, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Stepsize_LineEdit, 0, 1, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Number_LineEdit, 1, 1, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Maxiterations_Label, 2, 0, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Maxcontroliter_Label, 3, 0, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Maxiterations_SpinBox, 2, 1, 1, 1)
        self.Complements_GroupBox_Layout.addWidget(self.Complements_GroupBox_Maxcontroliter_SpinBox, 3, 1, 1, 1)

        # Seta layouts

        self.LoadFlow_GroupBox.setLayout(self.LoadFlow_GroupBox_Layout)
        self.Mode_GroupBox.setLayout(self.Mode_GroupBox_Layout)
        self.Complements_GroupBox.setLayout(self.Complements_GroupBox_Layout)

        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.LoadFlow_GroupBox)
        self.Tab_layout.addWidget(self.Mode_GroupBox)
        self.Tab_layout.addWidget(self.Complements_GroupBox)

        self.setLayout(self.Tab_layout)

        self.setDisabled_Complements_GroupBox()

    def setDisabled_Complements_GroupBox(self):

        if self.Mode_GroupBox_ComboBox.currentText() == "Daily":
            self.Complements_GroupBox_Stepsize_LineEdit.setEnabled(True)
            self.Complements_GroupBox_Number_LineEdit.setEnabled(True)
            self.Complements_GroupBox_Maxiterations_SpinBox.setEnabled(True)
            self.Complements_GroupBox_Maxcontroliter_SpinBox.setEnabled(True)
        else:
            self.Complements_GroupBox_Stepsize_LineEdit.setEnabled(False)
            self.Complements_GroupBox_Number_LineEdit.setEnabled(False)
            self.Complements_GroupBox_Maxiterations_SpinBox.setEnabled(False)
            self.Complements_GroupBox_Maxcontroliter_SpinBox.setEnabled(False)

    # Métodos Set Variáveis


    def get_VoltageBases(self):
        self.VoltageBases = self.LoadFlow_GroupBox_VoltageBase_LineEdit.text()
        return self.VoltageBases

    def get_Mode(self):
        self.mode = self.Mode_GroupBox_ComboBox.currentText()
        return self.mode

    def get_Stepsize(self):
        self.stepsize = self.Complements_GroupBox_Stepsize_LineEdit.text()
        return self.stepsize

    def get_Number(self):
        self.Number = self.Complements_GroupBox_Number_LineEdit.text()
        return self.Number

    def get_Maxiterations(self):
        self.Maxiterations = self.Complements_GroupBox_Maxiterations_SpinBox.value()
        return self.Maxiterations

    def get_Maxcontroliter(self):
        self.Maxcontroliter = self.Complements_GroupBox_Maxcontroliter_SpinBox.value()
        return self.Maxcontroliter




