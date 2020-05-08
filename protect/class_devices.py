# Carvalho Tag
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QTabWidget, QComboBox, QLineEdit,  QWidget, QMessageBox, QLabel
from PyQt5.QtCore import Qt

import configparser
import class_exception
import opendss.class_conn
import opendss.class_opendss
import config as cfg

class C_Devices_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Dispositivos de proteção"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        #self.OpenDSS = opendss.class_opendss.C_OpenDSS()

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
        self.TabRecloser = Recloser()

        self.TabWidget.addTab(self.TabRecloser, "Recloser")
        self.Dialog_Layout.addWidget(self.TabWidget)

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 0)

        self.setLayout(self.Dialog_Layout)
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

    def Accept(self):
        self.close()


class Recloser(QWidget):

    def __init__(self):
        super().__init__()

        self.TCClist = ['A', 'B', 'C', 'D', 'E']
        self.TCClist_data = ['1', '2', '3', '4', '5']

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Recloser = EditRecloser()
        self.RecloserSettings_GroupBox = QGroupBox('Selecionar Religador')
        self.RecloserSettings_GroupBox_Layout = QVBoxLayout()
        self.RecloserSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RecloserSelect_Combobox = QComboBox()
        self.RecloserSelect_Combobox.setMaximumWidth(150)
        self.RecloserSettings_GroupBox_Layout.addWidget(self.RecloserSelect_Combobox)


        ##### Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        #self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Remover_Btn.clicked.connect(self.dialog)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        #self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        #self.Edit_Btn.setFixedWidth(80)
        self.Edit_Btn.clicked.connect( self.Edit_Recloser.edit_exec(self.RecloserSelect_Combobox.currentText) )
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        #self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Add_Btn.setFixedWidth(80)
        #self.Add_Btn.clicked.connect(self.addMonitor)
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.RecloserSettings_GroupBox.setLayout(self.RecloserSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.RecloserSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def updateDialog(self):
        self.RecloserSelect_Combobox.clear()
        RecloserList = ['Religador A', 'Religador B', 'Religador C', 'Religador D', 'Religador E']
        recloserList = self.OpenDSS.getRecloserList()
        for index, item in enumerate(RecloserList):
            self.RecloserSelect_Combobox.addItem(item, item)
        print(recloserList)

    def enlarge_window(self):
        self.setGeometry(0, 0, 100,100)

class EditRecloser(QDialog):
    def __init__(self):
        super().__init__()
        self.titleWindow = "Editar Religador"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825,238) ##Resolução 1366x768
        self.Dialog_Layout = QVBoxLayout()


        # Parâmetros Intrínsecos do religador
        self.Edit_Recloser_GroupBox = QGroupBox('Religador Selecionado')
        self.Edit_Recloser_GroupBox_Layout = QGridLayout()
        self.Edit_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.actionlist = ['Aberto', 'Fechado']
        self.actionlist_data = ['Open', 'Closed']
        self.Action_ComboBox = QComboBox()
        self.Action_ComboBox.setMaximumWidth(150)
        self.Action_ComboBox_Label = QLabel("Action")
        for index, item in enumerate(self.actionlist):
            self.Action_ComboBox.addItem(item,self.actionlist_data[index])

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.enablelist = ['Sim', 'Não']
        self.enablelist_data = ['yes', 'no']
        self.Enable_ComboBox = QComboBox()
        self.Enable_ComboBox.setMaximumWidth(150)
        self.Enable_ComboBox_Label = QLabel("Habilitado")
        for index, item in enumerate(self.enablelist):
            self.Enable_ComboBox.addItem(item,self.enablelist_data[index])

        self.NumFast_LineEdit = QLineEdit()
        self.NumFast_LineEdit.setMaximumWidth(150)
        self.NumFast_LineEdit_Label = QLabel("Fast Shots")

        self.Shots_LineEdit = QLineEdit()
        self.Shots_LineEdit.setMaximumWidth(150)
        self.Shots_LineEdit_Label = QLabel("Total Shots")

        self.RecloserIntervals_LineEdit = QLineEdit()
        self.RecloserIntervals_LineEdit.setPlaceholderText("Ex: 2,2,5,5")
        self.RecloserIntervals_LineEdit.setMaximumWidth(150)
        self.RecloserIntervals_LineEdit_Label = QLabel("RecloserIntervals")

        self.ResetTime_LineEdit = QLineEdit()
        self.ResetTime_LineEdit_Label = QLabel("ResetTime")
        self.ResetTime_LineEdit.setMaximumWidth(150)

        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 0, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_ComboBox, 0, 2)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 1, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit, 1, 2)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 2, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Enable_ComboBox, 2, 2)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Shots_LineEdit_Label, 3, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Shots_LineEdit, 3, 2)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.NumFast_LineEdit_Label, 4, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.NumFast_LineEdit, 4, 2)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserIntervals_LineEdit_Label, 5, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserIntervals_LineEdit, 5, 2)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.ResetTime_LineEdit_Label, 6, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.ResetTime_LineEdit, 6, 2)
        self.Edit_Recloser_GroupBox.setLayout(self.Edit_Recloser_GroupBox_Layout)

        # Parâmetros de conexões do religador
        self.Conn_Recloser_GroupBox = QGroupBox('Conexões ')
        self.Conn_Recloser_GroupBox_Layout = QGridLayout()
        self.Conn_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.MonitObjList = ['Linha', 'Trafo', 'Carga', 'Gerador']
        self.MonitObj_ComboBox = QComboBox()
        self.MonitObj_ComboBox.setMaximumWidth(150)
        self.MonitObj_ComboBox_Label = QLabel("Elemento Monitorado")
        for index, item in enumerate(self.MonitObjList):
            self.MonitObj_ComboBox.addItem(item,item)

        self.MonitTermList = ['1', '2']
        self.MonitTerm_ComboBox = QComboBox()
        self.MonitTerm_ComboBox.setMaximumWidth(150)
        self.MonitTerm_ComboBox_Label = QLabel("Terminal Monitorado")
        for index, item in enumerate(self.MonitTermList):
            self.MonitTerm_ComboBox.addItem(item,item)

        self.SwitchedObjList = ['Linha', 'Trafo', 'Carga', 'Gerador']
        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMaximumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")
        for index, item in enumerate(self.SwitchedObjList):
            self.SwitchedObj_ComboBox.addItem(item,item)

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitObj_ComboBox_Label,0,0,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitObj_ComboBox,0,1,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox_Label,0,2,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox,0,3,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label,1,0,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox,1,1,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label,1,2,1,1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox,1,3,1,1)
        self.Conn_Recloser_GroupBox.setLayout(self.Conn_Recloser_GroupBox_Layout)

        # Curvas TCC
        self.TCCCurves_Recloser_GroupBox = QGroupBox('Curvas TCC')
        self.TCCCurves_Recloser_GroupBox_Layout = QGridLayout()
        self.TCCCurves_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.GroundDelayList = ['a', 'b', 'c', 'd']
        self.GroundDelay_ComboBox = QComboBox()
        self.GroundDelay_ComboBox.setMaximumWidth(150)
        self.GroundDelay_ComboBox_Label = QLabel("Ground Delayed")
        for index, item in enumerate(self.GroundDelayList):
            self.GroundDelay_ComboBox.addItem(item,item)

        self.GroundFastList = ['A', 'B', 'C', 'D']
        self.GroundFast_ComboBox = QComboBox()
        self.GroundFast_ComboBox.setMaximumWidth(150)
        self.GroundFast_ComboBox_Label = QLabel("Ground Fast")
        for index, item in enumerate(self.GroundFastList):
            self.GroundFast_ComboBox.addItem(item,item)

        self.GroundTrip_LineEdit = QLineEdit()
        self.GroundTrip_LineEdit.setMaximumWidth(150)
        self.GroundTrip_LineEdit.setPlaceholderText("Default = 1.0")
        self.GroundTrip_LineEdit_Label = QLabel("Ground Multiplier Amps")

        self.GroundDelayTimeDial_LineEdit = QLineEdit()
        self.GroundDelayTimeDial_LineEdit.setMaximumWidth(150)
        self.GroundDelayTimeDial_LineEdit.setPlaceholderText("Default = 1.0")
        self.GroundDelayTimeDial_LineEdit_Label = QLabel("Time dial - Ground Delayed")

        self.GroundFastTimeDial_LineEdit = QLineEdit()
        self.GroundFastTimeDial_LineEdit.setMaximumWidth(150)
        self.GroundFastTimeDial_LineEdit.setPlaceholderText("Default = 1.0")
        self.GroundFastTimeDial_LineEdit_Label = QLabel("Time dial - Ground Fast")

        self.PhaseDelayList = ['aaa', 'bbb', 'ccc', 'ddd']
        self.PhaseDelay_ComboBox = QComboBox()
        self.PhaseDelay_ComboBox.setMaximumWidth(150)
        self.PhaseDelay_ComboBox_Label = QLabel("Phase Delayed")
        for index, item in enumerate(self.PhaseDelayList):
            self.PhaseDelay_ComboBox.addItem(item,item)

        self.PhaseFastList = ['AAA', 'BBB', 'CCC', 'DDD']
        self.PhaseFast_ComboBox = QComboBox()
        self.PhaseFast_ComboBox.setMaximumWidth(150)
        self.PhaseFast_ComboBox_Label = QLabel("Phase Fast")
        for index, item in enumerate(self.PhaseFastList):
            self.PhaseFast_ComboBox.addItem(item,item)

        self.PhaseTrip_LineEdit = QLineEdit()
        self.PhaseTrip_LineEdit.setMaximumWidth(150)
        self.PhaseTrip_LineEdit.setPlaceholderText("Default = 1.0")
        self.PhaseTrip_LineEdit_Label = QLabel("Phase Multiplier Amps")

        self.PhaseDelayTimeDial_LineEdit = QLineEdit()
        self.PhaseDelayTimeDial_LineEdit.setMaximumWidth(150)
        self.PhaseDelayTimeDial_LineEdit.setPlaceholderText("Default = 1.0")
        self.PhaseDelayTimeDial_LineEdit_Label = QLabel("Time dial - Phase Delayed")


        self.PhaseFastTimeDial_LineEdit = QLineEdit()
        self.PhaseFastTimeDial_LineEdit.setMaximumWidth(150)
        self.PhaseFastTimeDial_LineEdit.setPlaceholderText("Default = 1.0")
        self.PhaseFastTimeDial_LineEdit_Label = QLabel("Time dial - Phase Fast")


        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit_Label,0,2,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit,0,3,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelayTimeDial_LineEdit_Label,1,2,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelayTimeDial_LineEdit,1,3,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelay_ComboBox_Label,1,0,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelay_ComboBox,1,1,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFastTimeDial_LineEdit_Label,2,2,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFastTimeDial_LineEdit,2,3,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFast_ComboBox_Label,2,0,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFast_ComboBox,2,1,1,1)
        
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit_Label,3,2,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit,3,3,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelayTimeDial_LineEdit_Label,4,2,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelayTimeDial_LineEdit,4,3,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelay_ComboBox_Label,4,0,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelay_ComboBox,4,1,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFastTimeDial_LineEdit_Label,5,2,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFastTimeDial_LineEdit,5,3,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFast_ComboBox_Label,5,0,1,1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFast_ComboBox,5,1,1,1)

        self.TCCCurves_Recloser_GroupBox.setLayout(self.TCCCurves_Recloser_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_Recloser_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Recloser_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Recloser_GroupBox)
        self.setLayout(self.Dialog_Layout)


## Pro gamer movement pra poder usar argumentos dentro do " .connect "
    def edit_exec(self, get_name):
        def process():
            self.titleWindow = f' Editar religador {get_name()}'
            self.setWindowTitle(self.titleWindow)
            self.show()
        return process