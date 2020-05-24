# Carvalho Tag
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QTabWidget, QComboBox, QLineEdit, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import unidecode

import opendss.class_conn
import opendss.class_opendss
import config as cfg


class C_Devices_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Dispositivos de proteção"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        # self.OpenDSS = opendss.class_opendss.C_OpenDSS()

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
        self.TabFuse = Fuse()
        self.TabRelay = Relay()
        self.TabSwtControl = SwtControl()

        self.TabWidget.addTab(self.TabRecloser, "Religador")
        self.TabWidget.addTab(self.TabFuse, "Fusível")
        self.TabWidget.addTab(self.TabRelay, "Relé")
        self.TabWidget.addTab(self.TabSwtControl, "Switch Control")
        self.Dialog_Layout.addWidget(self.TabWidget)

        #  Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 0)

        self.setLayout(self.Dialog_Layout)

    def Accept(self):
        self.close()

    def updateMainProtectDialog(self):
        self.TabRecloser.updateProtectDialog()
        self.TabFuse.updateProtectDialog()
        self.TabRelay.updateProtectDialog()
        self.TabSwtControl.updateProtectDialog()


class Recloser(QWidget):

    def __init__(self):
        super().__init__()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Recloser = EditRecloser(self)
        self.RecloserSettings_GroupBox = QGroupBox('Selecionar Religador')
        self.RecloserSettings_GroupBox_Layout = QVBoxLayout()
        self.RecloserSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RecloserSelect_Combobox = QComboBox()
        self.RecloserSelect_Combobox.setMaximumWidth(150)
        self.RecloserSettings_GroupBox_Layout.addWidget(self.RecloserSelect_Combobox)

        self.ElementList = []
        self.AddRecloserDataInfo = []
        self.RecloserDataInfo = []
        self.loadDatabaseFlag = False
        self.flag = False

        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        # self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_Recloser.removeRecloser)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        # self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        # self.Edit_Btn.setFixedWidth(80)
        self.Edit_Btn.clicked.connect(self.Edit_Recloser.editRecloser(self.RecloserSelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        # self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.Add_Btn.setFixedWidth(80)
        self.Add_Btn.clicked.connect(self.Edit_Recloser.addRecloser())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.RecloserSettings_GroupBox.setLayout(self.RecloserSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.RecloserSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_RecloserInfoBOM(self):
        recloserSelected = self.RecloserSelect_Combobox.currentText()
        for item in self.RecloserDataInfo:
            if item["Name"] == recloserSelected:

                self.Edit_Recloser.RecloserName_LineEdit.setText(item["Name"])

                if item["Action"] == 'close':
                    self.Edit_Recloser.Action_ComboBox.setCurrentIndex(1)
                else:
                    self.Edit_Recloser.Action_ComboBox.setCurrentIndex(0)

                self.Edit_Recloser.Delay_LineEdit.setText(item["Delay"])

                if item["Enabled"] == 'yes' or item["Enabled"] == '':
                    self.Edit_Recloser.Enable_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_Recloser.Enable_ComboBox.setCurrentIndex(1)

                self.Edit_Recloser.Shots_LineEdit.setText(item["Shots"])
                self.Edit_Recloser.NumFast_LineEdit.setText(item["NumFast"])
                self.Edit_Recloser.RecloserIntervals_LineEdit.setText(item["RecloseIntervals"])
                self.Edit_Recloser.ResetTime_LineEdit.setText(item["Reset"])

                self.Edit_Recloser.MonitObj_ComboBox.setCurrentText(item["MonitoredObj"])
                self.Edit_Recloser.SwitchedObj_ComboBox.setCurrentText(item["SwitchedObj"])
                self.Edit_Recloser.MonitTerm_ComboBox.setCurrentText(item["MonitoredTerm"])
                self.Edit_Recloser.SwitchedTerm_ComboBox.setCurrentText(item["SwitchedTerm"])

                self.Edit_Recloser.PhaseDelay_ComboBox.setCurrentText(item["PhaseDelayed"])
                self.Edit_Recloser.PhaseFast_ComboBox.setCurrentText(item["PhaseFast"])
                self.Edit_Recloser.PhaseTrip_LineEdit.setText(item["PhaseTrip"])
                self.Edit_Recloser.PhaseDelayTimeDial_LineEdit.setText(item["TDPhDelayed"])
                self.Edit_Recloser.PhaseFastTimeDial_LineEdit.setText(item["TDPhFast"])

                self.Edit_Recloser.GroundDelay_ComboBox.setCurrentText(item["GroundDelayed"])
                self.Edit_Recloser.GroundFast_ComboBox.setCurrentText(item["GroundFast"])
                self.Edit_Recloser.GroundTrip_LineEdit.setText(item["GroundTrip"])
                self.Edit_Recloser.GroundDelayTimeDial_LineEdit.setText(item["TDGrDelayed"])
                self.Edit_Recloser.GroundFastTimeDial_LineEdit.setText(item["TDGrFast"])
                # print(item)

    def load_ReclosersDatabase(self):
        databaseRecloserdict = {}
        databaseRecloser = self.OpenDSS.getRecloserList()
        # Se trocar de subestação

        # Caso seja encontrado algum religador que ainda pertence ao database, ou seja, se não foi trocado de subestação
        try:
            for item in databaseRecloser:
                for item2 in self.RecloserDataInfo:
                    if item.split(" MonitoredObj=")[0].split("New Recloser.")[1] == item2["Name"]:
                        self.flag = True
                        return
                    else:
                        self.flag = False
        except:
            pass

        # Caso algum religador tenha sido adicionado
        if self.AddRecloserDataInfo:
            self.flag = True

        # Caso não haja religadores adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.RecloserDataInfo.clear()
            self.AddRecloserDataInfo.clear()

        # Caso a lista de religadores esteja vazia:
        if not self.RecloserDataInfo:
            for item in databaseRecloser:
                databaseRecloserdict["Name"] = item.split(" MonitoredObj=")[0].split("New Recloser.")[1]
                # Basic
                if item.split(" action=")[1] == 'c':
                    databaseRecloserdict["Action"] = 'close'
                else:
                    databaseRecloserdict["Action"] = 'open'

                databaseRecloserdict["Delay"] = ''
                databaseRecloserdict["Enabled"] = ''
                databaseRecloserdict["Shots"] = ''
                databaseRecloserdict["NumFast"] = ''
                databaseRecloserdict["RecloseIntervals"] = ''
                databaseRecloserdict["Reset"] = ''
                # Connections
                databaseRecloserdict["MonitoredObj"] = item.split(" SwitchedObj=")[0].split("MonitoredObj=")[1]
                databaseRecloserdict["MonitoredTerm"] = ''
                databaseRecloserdict["SwitchedObj"] = item.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
                databaseRecloserdict["SwitchedTerm"] = item.split(" action=")[0].split("SwitchedTerm=")[1]
                # TCC Curves
                databaseRecloserdict["PhaseDelayed"] = ''
                databaseRecloserdict["PhaseFast"] = ''
                databaseRecloserdict["PhaseTrip"] = ''
                databaseRecloserdict["TDPhDelayed"] = ''
                databaseRecloserdict["TDPhFast"] = ''
                databaseRecloserdict["GroundDelayed"] = ''
                databaseRecloserdict["GroundFast"] = ''
                databaseRecloserdict["GroundTrip"] = ''
                databaseRecloserdict["TDGrDelayed"] = ''
                databaseRecloserdict["TDGrFast"] = ''

                if not self.loadDatabaseFlag:
                    self.RecloserDataInfo.append(databaseRecloserdict.copy())

            self.loadDatabaseFlag = True

    def updateProtectDialog(self):
        self.load_ReclosersDatabase()
        # Carregando a ElementList para ser usada na Edit Dialog
        self.ElementList = self.OpenDSS.getElementList()
        self.RecloserSelect_Combobox.clear()
        for dicio in self.RecloserDataInfo:
            self.RecloserSelect_Combobox.addItem(dicio["Name"], dicio["Name"])


class EditRecloser(QDialog):
    def __init__(self, recloser_parent):
        super().__init__()
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.recloser_parent = recloser_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825, 0)  ##Resolução 1366x768
        self.Dialog_Layout = QVBoxLayout()
        self.RecInfo()
        self.Btns()
        self.setLayout(self.Dialog_Layout)

    def RecInfo(self):
        # Parâmetros Intrínsecos do religador
        self.Edit_Recloser_GroupBox = QGroupBox('Geral')
        self.Edit_Recloser_GroupBox_Layout = QGridLayout()
        self.Edit_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RecloserName_LineEdit = QLineEdit()
        self.RecloserName_LineEdit_Label = QLabel("Dispositivo")
        self.RecloserName_LineEdit.setMaximumWidth(150)

        self.actionlist = ['Aberto', 'Fechado']
        self.actionlist_data = ['Open', 'Closed']
        self.Action_ComboBox = QComboBox()
        self.Action_ComboBox.setMaximumWidth(150)
        self.Action_ComboBox_Label = QLabel("Action")
        for index, item in enumerate(self.actionlist):
            self.Action_ComboBox.addItem(item, self.actionlist_data[index])

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.enablelist = ['Sim', 'Não']
        self.enablelist_data = ['yes', 'no']
        self.Enable_ComboBox = QComboBox()
        self.Enable_ComboBox.setMaximumWidth(150)
        self.Enable_ComboBox_Label = QLabel("Habilitado")
        for index, item in enumerate(self.enablelist):
            self.Enable_ComboBox.addItem(item, self.enablelist_data[index])

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

        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserName_LineEdit_Label, 0, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserName_LineEdit, 0, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 1, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_ComboBox, 1, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 2, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit, 2, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 3, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Enable_ComboBox, 3, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Shots_LineEdit_Label, 4, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Shots_LineEdit, 4, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.NumFast_LineEdit_Label, 5, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.NumFast_LineEdit, 5, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserIntervals_LineEdit_Label, 6, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserIntervals_LineEdit, 6, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.ResetTime_LineEdit_Label, 7, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.ResetTime_LineEdit, 7, 1)
        self.Edit_Recloser_GroupBox.setLayout(self.Edit_Recloser_GroupBox_Layout)

        # Parâmetros de conexões do religador
        self.Conn_Recloser_GroupBox = QGroupBox('Conexões ')
        self.Conn_Recloser_GroupBox_Layout = QGridLayout()
        self.Conn_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.MonitObj_ComboBox = QComboBox()
        self.MonitObj_ComboBox.setMinimumWidth(150)
        self.MonitObj_ComboBox_Label = QLabel("Elemento Monitorado")

        self.MonitTermList = ['1', '2']
        self.MonitTerm_ComboBox = QComboBox()
        # self.MonitTerm_ComboBox.setMaximumWidth(150)
        self.MonitTerm_ComboBox_Label = QLabel("Terminal Monitorado")
        for index, item in enumerate(self.MonitTermList):
            self.MonitTerm_ComboBox.addItem(item, item)

        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMinimumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitObj_ComboBox_Label, 0, 0, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitObj_ComboBox, 0, 1, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox_Label, 0, 2, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox, 0, 3, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
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
            self.GroundDelay_ComboBox.addItem(item, item)

        self.GroundFastList = ['A', 'B', 'C', 'D']
        self.GroundFast_ComboBox = QComboBox()
        self.GroundFast_ComboBox.setMaximumWidth(150)
        self.GroundFast_ComboBox_Label = QLabel("Ground Fast")
        for index, item in enumerate(self.GroundFastList):
            self.GroundFast_ComboBox.addItem(item, item)

        self.GroundTrip_LineEdit = QLineEdit()
        self.GroundTrip_LineEdit.setMaximumWidth(50)
        self.GroundTrip_LineEdit.setPlaceholderText("1.0")
        self.GroundTrip_LineEdit_Label = QLabel("Ground Multiplier Amps")

        self.GroundDelayTimeDial_LineEdit = QLineEdit()
        self.GroundDelayTimeDial_LineEdit.setMaximumWidth(50)
        self.GroundDelayTimeDial_LineEdit.setPlaceholderText("1.0")
        self.GroundDelayTimeDial_LineEdit_Label = QLabel("Time dial - Ground Delayed")

        self.GroundFastTimeDial_LineEdit = QLineEdit()
        self.GroundFastTimeDial_LineEdit.setMaximumWidth(50)
        self.GroundFastTimeDial_LineEdit.setPlaceholderText("1.0")
        self.GroundFastTimeDial_LineEdit_Label = QLabel("Time dial - Ground Fast")

        self.PhaseDelayList = ['aaa', 'bbb', 'ccc', 'ddd']
        self.PhaseDelay_ComboBox = QComboBox()
        self.PhaseDelay_ComboBox.setMaximumWidth(150)
        self.PhaseDelay_ComboBox_Label = QLabel("Phase Delayed")
        for index, item in enumerate(self.PhaseDelayList):
            self.PhaseDelay_ComboBox.addItem(item, item)

        self.PhaseFastList = ['AAA', 'BBB', 'CCC', 'DDD']
        self.PhaseFast_ComboBox = QComboBox()
        self.PhaseFast_ComboBox.setMaximumWidth(150)
        self.PhaseFast_ComboBox_Label = QLabel("Phase Fast")
        for index, item in enumerate(self.PhaseFastList):
            self.PhaseFast_ComboBox.addItem(item, item)

        self.PhaseTrip_LineEdit = QLineEdit()
        self.PhaseTrip_LineEdit.setMaximumWidth(50)
        self.PhaseTrip_LineEdit.setPlaceholderText("1.0")
        self.PhaseTrip_LineEdit_Label = QLabel("Phase Multiplier Amps")

        self.PhaseDelayTimeDial_LineEdit = QLineEdit()
        self.PhaseDelayTimeDial_LineEdit.setMaximumWidth(50)
        self.PhaseDelayTimeDial_LineEdit.setPlaceholderText("1.0")
        self.PhaseDelayTimeDial_LineEdit_Label = QLabel("Time dial - Phase Delayed")

        self.PhaseFastTimeDial_LineEdit = QLineEdit()
        self.PhaseFastTimeDial_LineEdit.setMaximumWidth(50)
        self.PhaseFastTimeDial_LineEdit.setPlaceholderText("1.0")
        self.PhaseFastTimeDial_LineEdit_Label = QLabel("Time dial - Phase Fast")

        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit_Label, 0, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit, 0, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelayTimeDial_LineEdit_Label, 1, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelayTimeDial_LineEdit, 1, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelay_ComboBox_Label, 1, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelay_ComboBox, 1, 1, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFastTimeDial_LineEdit_Label, 2, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFastTimeDial_LineEdit, 2, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFast_ComboBox_Label, 2, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFast_ComboBox, 2, 1, 1, 1)

        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit_Label, 4, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit, 4, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelayTimeDial_LineEdit_Label, 5, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelayTimeDial_LineEdit, 5, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelay_ComboBox_Label, 5, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelay_ComboBox, 5, 1, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFastTimeDial_LineEdit_Label, 6, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFastTimeDial_LineEdit, 6, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFast_ComboBox_Label, 6, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFast_ComboBox, 6, 1, 1, 1)

        self.TCCCurves_Recloser_GroupBox.setLayout(self.TCCCurves_Recloser_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_Recloser_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Recloser_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Recloser_GroupBox)

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.AcceptAddEditRecloser)

        self.AddTCC_Btn = QPushButton("Add TCC Curve")
        self.AddTCC_Btn.setMaximumWidth(150)
        # self.AddTCC_Btn.clicked.connect(self.recloser_parent.RecloserList)

        self.btngroupbox_layout.addWidget(self.AddTCC_Btn)
        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def editRecloser(self, get_name):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar religador {get_name()}'
            self.setWindowTitle(self.titleWindow)

            self.RecloserName_LineEdit.setEnabled(False)
            self.show()
            self.updateEditDialog()
            self.recloser_parent.load_RecloserInfoBOM()
            self.recloser_parent.load_ReclosersDatabase()

        return process

    def addRecloser(self):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar religador'
            self.setWindowTitle(self.titleWindow)

            self.RecloserName_LineEdit.setEnabled(True)
            self.show()
            self.clearRecloserParameters()
            self.updateEditDialog()

        return process

    def removeRecloser(self):
        for ctd in self.recloser_parent.RecloserDataInfo:
            if ctd["Name"] == self.recloser_parent.RecloserSelect_Combobox.currentText():
                self.recloser_parent.RecloserDataInfo.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Religador",
                            "Religador " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()

        self.recloser_parent.RecloserSelect_Combobox.clear()
        for dicio in self.recloser_parent.RecloserDataInfo:
            self.recloser_parent.RecloserSelect_Combobox.addItem(dicio["Name"], dicio["Name"])
        self.clearRecloserParameters()

    def loadParameters(self):
        self.datainfo["Name"] = get_lineedit(self.RecloserName_LineEdit)
        ## Basic
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        self.datainfo["Shots"] = get_lineedit(self.Shots_LineEdit)
        self.datainfo["NumFast"] = get_lineedit(self.NumFast_LineEdit)
        self.datainfo["RecloseIntervals"] = get_lineedit(self.RecloserIntervals_LineEdit)
        self.datainfo["Reset"] = get_lineedit(self.ResetTime_LineEdit)

        #  Connections
        self.datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        self.datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        #  TCC Curves
        #  Phase
        self.datainfo["PhaseDelayed"] = get_combobox(self.PhaseDelay_ComboBox)
        self.datainfo["PhaseFast"] = get_combobox(self.PhaseFast_ComboBox)
        self.datainfo["PhaseTrip"] = get_lineedit(self.PhaseTrip_LineEdit)
        self.datainfo["TDPhDelayed"] = get_lineedit(self.PhaseDelayTimeDial_LineEdit)
        self.datainfo["TDPhFast"] = get_lineedit(self.PhaseFastTimeDial_LineEdit)
        #  Ground
        self.datainfo["GroundDelayed"] = get_combobox(self.GroundDelay_ComboBox)
        self.datainfo["GroundFast"] = get_combobox(self.GroundFast_ComboBox)
        self.datainfo["GroundTrip"] = get_lineedit(self.GroundTrip_LineEdit)
        self.datainfo["TDGrDelayed"] = get_lineedit(self.GroundDelayTimeDial_LineEdit)
        self.datainfo["TDGrFast"] = get_lineedit(self.GroundFastTimeDial_LineEdit)

    def AcceptAddEditRecloser(self):  ## Dá para otimizar e muito // Somente um teste

        datainfo = {}
        datainfo["Name"] = unidecode.unidecode(get_lineedit(self.RecloserName_LineEdit).replace(" ", "_"))
        ## Basic
        datainfo["Action"] = get_combobox(self.Action_ComboBox)
        datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        datainfo["Shots"] = get_lineedit(self.Shots_LineEdit)
        datainfo["NumFast"] = get_lineedit(self.NumFast_LineEdit)
        datainfo["RecloseIntervals"] = get_lineedit(self.RecloserIntervals_LineEdit)
        datainfo["Reset"] = get_lineedit(self.ResetTime_LineEdit)

        #  Connections
        datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        #  TCC Curves
        #  Phase
        datainfo["PhaseDelayed"] = get_combobox(self.PhaseDelay_ComboBox)
        datainfo["PhaseFast"] = get_combobox(self.PhaseFast_ComboBox)
        datainfo["PhaseTrip"] = get_lineedit(self.PhaseTrip_LineEdit)
        datainfo["TDPhDelayed"] = get_lineedit(self.PhaseDelayTimeDial_LineEdit)
        datainfo["TDPhFast"] = get_lineedit(self.PhaseFastTimeDial_LineEdit)
        #  Ground
        datainfo["GroundDelayed"] = get_combobox(self.GroundDelay_ComboBox)
        datainfo["GroundFast"] = get_combobox(self.GroundFast_ComboBox)
        datainfo["GroundTrip"] = get_lineedit(self.GroundTrip_LineEdit)
        datainfo["TDGrDelayed"] = get_lineedit(self.GroundDelayTimeDial_LineEdit)
        datainfo["TDGrFast"] = get_lineedit(self.GroundFastTimeDial_LineEdit)

        if self.RecloserName_LineEdit.isEnabled():
            ctdExist = False
            for ctd in self.recloser_parent.RecloserDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.recloser_parent.RecloserDataInfo.append(datainfo)
                self.recloser_parent.AddRecloserDataInfo.append(datainfo)
                QMessageBox(QMessageBox.Information, "Religador",
                            "Religador " + datainfo["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Religador",
                            "Religador " + datainfo["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.recloser_parent.RecloserDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ## Basic
                    ctd["Action"] = datainfo["Action"]
                    ctd["Delay"] = datainfo["Delay"]
                    ctd["Enabled"] = datainfo["Enabled"]
                    ctd["Shots"] = datainfo["Shots"]
                    ctd["NumFast"] = datainfo["NumFast"]
                    ctd["RecloseIntervals"] = datainfo["RecloseIntervals"]
                    ctd["Reset"] = datainfo["Reset"]
                    #  Connections
                    ctd["MonitoredObj"] = datainfo["MonitoredObj"]
                    ctd["MonitoredTerm"] = datainfo["MonitoredTerm"]
                    ctd["SwitchedObj"] = datainfo["SwitchedObj"]
                    ctd["SwitchedTerm"] = datainfo["SwitchedTerm"]
                    #  TCC Curves
                    #  Phase
                    ctd["PhaseDelayed"] = datainfo["PhaseDelayed"]
                    ctd["PhaseFast"] = datainfo["PhaseFast"]
                    ctd["PhaseTrip"] = datainfo["PhaseTrip"]
                    ctd["TDPhDelayed"] = datainfo["TDPhDelayed"]
                    ctd["TDPhFast"] = datainfo["TDPhFast"]
                    #  Ground
                    ctd["GroundDelayed"] = datainfo["GroundDelayed"]
                    ctd["GroundFast"] = datainfo["GroundFast"]
                    ctd["GroundTrip"] = datainfo["GroundTrip"]
                    ctd["TDGrDelayed"] = datainfo["TDGrDelayed"]
                    ctd["TDGrFast"] = datainfo["TDGrFast"]

                    QMessageBox(QMessageBox.Information, "Religador",
                                "Religador " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.recloser_parent.updateProtectDialog()
        self.adjustSize()
        self.close()

    def clearRecloserParameters(self):
        self.RecloserName_LineEdit.setText("")
        ## Basic
        self.Action_ComboBox.setCurrentIndex(0)
        self.Delay_LineEdit.setText("")
        self.Enable_ComboBox.setCurrentIndex(0)
        self.Shots_LineEdit.setText("")
        self.NumFast_LineEdit.setText("")
        self.RecloserIntervals_LineEdit.setText("")
        self.ResetTime_LineEdit.setText("")

        self.MonitObj_ComboBox.setCurrentIndex(0)
        self.MonitTerm_ComboBox.setCurrentIndex(0)
        self.SwitchedObj_ComboBox.setCurrentIndex(0)
        self.SwitchedTerm_ComboBox.setCurrentIndex(0)

        self.PhaseDelay_ComboBox.setCurrentIndex(0)
        self.PhaseFast_ComboBox.setCurrentIndex(0)
        self.PhaseTrip_LineEdit.setText("")
        self.PhaseDelayTimeDial_LineEdit.setText("")
        self.PhaseFastTimeDial_LineEdit.setText("")

        self.GroundDelay_ComboBox.setCurrentIndex(0)
        self.GroundFast_ComboBox.setCurrentIndex(0)
        self.GroundTrip_LineEdit.setText("")
        self.GroundDelayTimeDial_LineEdit.setText("")
        self.GroundFastTimeDial_LineEdit.setText("")

    def updateEditDialog(self):
        self.MonitObj_ComboBox.clear()
        self.SwitchedObj_ComboBox.clear()

        for index, item in enumerate(self.recloser_parent.ElementList):
            self.MonitObj_ComboBox.addItem(item, item)
            self.SwitchedObj_ComboBox.addItem(item, item)


class Fuse(QWidget):

    def __init__(self):
        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Fuse = EditFuse(self)
        self.FuseSettings_GroupBox = QGroupBox('Selecionar Fusível')
        self.FuseSettings_GroupBox_Layout = QVBoxLayout()
        self.FuseSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.FuseSelect_Combobox = QComboBox()
        self.FuseSelect_Combobox.setMaximumWidth(150)
        self.FuseSettings_GroupBox_Layout.addWidget(self.FuseSelect_Combobox)

        self.ElementList = []
        self.AddFuseDataInfo = []
        self.FuseDataInfo = []
        self.loadDatabaseFlag = False
        self.flag = False

        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_Fuse.removeFuse)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.Edit_Btn.clicked.connect(self.Edit_Fuse.editFuse(self.FuseSelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.Add_Btn.clicked.connect(self.Edit_Fuse.addFuse())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.FuseSettings_GroupBox.setLayout(self.FuseSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.FuseSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_FuseInfoBOM(self):
        FuseSelected = self.FuseSelect_Combobox.currentText()
        for item in self.FuseDataInfo:
            if item["Name"] == FuseSelected:

                self.Edit_Fuse.FuseName_LineEdit.setText(item["Name"])
                self.Edit_Fuse.Action_ComboBox.setCurrentText(item["Action"])
                self.Edit_Fuse.Delay_LineEdit.setText(item["Delay"])

                if item["Enabled"] == 'yes' or item["Enabled"] == '':
                    self.Edit_Fuse.Enable_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_Fuse.Enable_ComboBox.setCurrentIndex(1)

                self.Edit_Fuse.MonitObj_ComboBox.setCurrentText(item["MonitoredObj"])
                self.Edit_Fuse.SwitchedObj_ComboBox.setCurrentText(item["SwitchedObj"])
                self.Edit_Fuse.MonitTerm_ComboBox.setCurrentText(item["MonitoredTerm"])
                self.Edit_Fuse.SwitchedTerm_ComboBox.setCurrentText(item["SwitchedTerm"])

                self.Edit_Fuse.FuseCurve_ComboBox.setCurrentText(item["FuseCurve"])
                self.Edit_Fuse.RatedCurrent_LineEdit.setText(item["RatedCurrent"])

    def load_FusesDatabase(self):
        databaseFusedict = {}
        databaseFuse = self.OpenDSS.getFuseList()
        # print(databaseFuse)
        # Se trocar de subestação

        # Caso seja encontrado algum Fusível que ainda pertence ao database, ou seja, se não foi trocado de subestação
        try:
            for item in databaseFuse:
                for item2 in self.FuseDataInfo:
                    if item.split(" MonitoredObj=")[0].split("New Fuse.")[1] == item2["Name"]:
                        self.flag = True
                        return
                    else:
                        self.flag = False
        except:
            pass

        # Caso algum Fusível tenha sido adicionado
        if self.AddFuseDataInfo:
            self.flag = True

        # Caso não haja Fusíveles adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.FuseDataInfo.clear()
            self.AddFuseDataInfo.clear()

        # Caso a lista de Fusíveles esteja vazia:
        if not self.FuseDataInfo and not self.loadDatabaseFlag:
            for item in databaseFuse:
                databaseFusedict["Name"] = item.split(" MonitoredObj=")[0].split("New Fuse.")[1]
                # Basic
                databaseFusedict["Action"] = ''
                databaseFusedict["Delay"] = ''
                databaseFusedict["Enabled"] = ''
                # Connections
                databaseFusedict["MonitoredObj"] = item.split(" SwitchedObj=")[0].split("MonitoredObj=")[1]
                databaseFusedict["MonitoredTerm"] = ''
                databaseFusedict["SwitchedObj"] = item.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
                databaseFusedict["SwitchedTerm"] = item.split(" FuseCurve=")[0].split("SwitchedTerm=")[1]
                # TCC Curves
                databaseFusedict["FuseCurve"] = item.split(" RatedCurrent=")[0].split("FuseCurve=")[1]
                databaseFusedict["RatedCurrent"] = item.split(" RatedCurrent=")[1]

                self.FuseDataInfo.append(databaseFusedict.copy())

            self.loadDatabaseFlag = True

    def updateProtectDialog(self):
        self.load_FusesDatabase()
        # Carregando a ElementList para ser usada na Edit Dialog
        self.ElementList = self.OpenDSS.getElementList()
        self.FuseSelect_Combobox.clear()
        for dicio in self.FuseDataInfo:
            self.FuseSelect_Combobox.addItem(dicio["Name"], dicio["Name"])


class EditFuse(QDialog):
    def __init__(self, Fuse_parent):
        super().__init__()
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.Fuse_parent = Fuse_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825, 170)
        self.Dialog_Layout = QVBoxLayout()
        self.FuseInfo()
        self.Btns()
        self.setLayout(self.Dialog_Layout)

    def FuseInfo(self):
        # Parâmetros Intrínsecos do Fusível
        self.Edit_Fuse_GroupBox = QGroupBox('Geral')
        self.Edit_Fuse_GroupBox_Layout = QGridLayout()
        self.Edit_Fuse_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.FuseName_LineEdit = QLineEdit()
        self.FuseName_LineEdit_Label = QLabel("Dispositivo")
        self.FuseName_LineEdit.setMaximumWidth(150)

        self.actionlist = ['Aberto', 'Fechado']
        self.actionlist_data = ['Open', 'Closed']
        self.Action_ComboBox = QComboBox()
        self.Action_ComboBox.setMaximumWidth(150)
        self.Action_ComboBox_Label = QLabel("Action")
        for index, item in enumerate(self.actionlist):
            self.Action_ComboBox.addItem(item, self.actionlist_data[index])

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.enablelist = ['Sim', 'Não']
        self.enablelist_data = ['yes', 'no']
        self.Enable_ComboBox = QComboBox()
        self.Enable_ComboBox.setMaximumWidth(150)
        self.Enable_ComboBox_Label = QLabel("Habilitado")
        for index, item in enumerate(self.enablelist):
            self.Enable_ComboBox.addItem(item, self.enablelist_data[index])

        self.Edit_Fuse_GroupBox_Layout.addWidget(self.FuseName_LineEdit_Label, 0, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.FuseName_LineEdit, 0, 1)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 1, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Action_ComboBox, 1, 1)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 2, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Delay_LineEdit, 2, 1)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 3, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Enable_ComboBox, 3, 1)

        self.Edit_Fuse_GroupBox.setLayout(self.Edit_Fuse_GroupBox_Layout)

        # Parâmetros de conexões do Fusível
        self.Conn_Fuse_GroupBox = QGroupBox('Conexões ')
        self.Conn_Fuse_GroupBox_Layout = QGridLayout()
        self.Conn_Fuse_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.MonitObj_ComboBox = QComboBox()
        self.MonitObj_ComboBox.setMinimumWidth(150)
        self.MonitObj_ComboBox_Label = QLabel("Elemento Monitorado")

        self.MonitTermList = ['1', '2']
        self.MonitTerm_ComboBox = QComboBox()
        # self.MonitTerm_ComboBox.setMaximumWidth(150)
        self.MonitTerm_ComboBox_Label = QLabel("Terminal Monitorado")
        for index, item in enumerate(self.MonitTermList):
            self.MonitTerm_ComboBox.addItem(item, item)

        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMinimumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitObj_ComboBox_Label, 0, 0, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitObj_ComboBox, 0, 1, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox_Label, 0, 2, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox, 0, 3, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
        self.Conn_Fuse_GroupBox.setLayout(self.Conn_Fuse_GroupBox_Layout)

        # Curvas TCC
        self.TCCCurves_Fuse_GroupBox = QGroupBox('Curvas TCC')
        self.TCCCurves_Fuse_GroupBox_Layout = QGridLayout()
        self.TCCCurves_Fuse_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        # Tipo de Capacidade de Elo Fusível (TCAPELFU)
        self.TCAPELFU = {"0": "Não", "1H": "1H", "2H": "2H", "3H": "3H", "5H": "5H", "6K": "6K", "8K": "8K",
                         "10K": "10K",
                         "12K": "12K", "15K": "15K", "20K": "20K", "25K": "25K", "30K": "30K", "40K": "40K",
                         "50K": "50K",
                         "60K": "60K", "65K": "65K", "75K": "75K", "80K": "80K", "100K": "100K", "140K": "140K",
                         "200K": "200K", "LAM": "LAMINA", "DIR": "ELO", "SC": "S/C", "08H": "0,8H", "04H": "0,4H",
                         "05H": "0,5H", "100EF": "100EF", "10F": "10F", "1EF": "1EF", "30T": "30T", "3K": "3K",
                         "40EF": "40EF", "5K": "5K", "65EF": "65EF", "65T": "65T", "6T": "6T", "80EF": "80EF",
                         "80T": "80T",
                         "8T": "8T", "10T": "10T", "12T": "12T", "15T": "15T", "20T": "20T", "25T": "25T", "40T": "40T",
                         "50T": "50T", "100T": "100T"}

        self.FuseCurveList = self.TCAPELFU.values()
        self.FuseCurve_ComboBox = QComboBox()
        self.FuseCurve_ComboBox.setMaximumWidth(150)
        self.FuseCurve_ComboBox_Label = QLabel("Fuse Curve")
        for index, item in enumerate(self.FuseCurveList):
            self.FuseCurve_ComboBox.addItem(item, item)

        self.RatedCurrent_LineEdit = QLineEdit()
        self.RatedCurrent_LineEdit.setMaximumWidth(50)
        self.RatedCurrent_LineEdit.setPlaceholderText("1.0")
        self.RatedCurrent_LineEdit_Label = QLabel("Rated Current")

        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.FuseCurve_ComboBox_Label, 0, 0, 1, 1)
        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.FuseCurve_ComboBox, 0, 1, 1, 1)
        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.RatedCurrent_LineEdit_Label, 0, 2, 1, 1)
        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.RatedCurrent_LineEdit, 0, 3, 1, 1)

        self.TCCCurves_Fuse_GroupBox.setLayout(self.TCCCurves_Fuse_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_Fuse_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Fuse_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Fuse_GroupBox)

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.AcceptAddEditFuse)

        self.AddTCC_Btn = QPushButton("Add TCC Curve")
        self.AddTCC_Btn.setMaximumWidth(150)
        # self.AddTCC_Btn.clicked.connect(self.Fuse_parent.FuseList)

        self.btngroupbox_layout.addWidget(self.AddTCC_Btn)
        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def editFuse(self, get_name):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar Fusível {get_name()}'
            self.setWindowTitle(self.titleWindow)

            self.FuseName_LineEdit.setEnabled(False)
            self.show()
            self.updateEditDialog()
            self.Fuse_parent.load_FuseInfoBOM()
            self.Fuse_parent.load_FusesDatabase()

        return process

    def addFuse(self):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar Fusível'
            self.setWindowTitle(self.titleWindow)

            self.FuseName_LineEdit.setEnabled(True)
            self.show()
            self.clearFuseParameters()
            self.updateEditDialog()

        return process

    def removeFuse(self):
        for ctd in self.Fuse_parent.FuseDataInfo:
            if ctd["Name"] == self.Fuse_parent.FuseSelect_Combobox.currentText():
                self.Fuse_parent.FuseDataInfo.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Fusível",
                            "Fusível " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
        self.clearFuseParameters()

        self.Fuse_parent.FuseSelect_Combobox.clear()
        for dicio in self.Fuse_parent.FuseDataInfo:
            self.Fuse_parent.FuseSelect_Combobox.addItem(dicio["Name"], dicio["Name"])

    def loadParameters(self):
        self.datainfo["Name"] = get_lineedit(self.FuseName_LineEdit)
        ## Basic
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)

        #  Connections
        self.datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        self.datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        #  TCC Curves
        self.datainfo["FuseCurve"] = get_combobox(self.FuseCurve_ComboBox)
        self.datainfo["RatedCurrent"] = get_lineedit(self.RatedCurrent_LineEdit)

    def AcceptAddEditFuse(self):  # Dá para otimizar e muito // Somente um teste

        datainfo = {}
        datainfo["Name"] = unidecode.unidecode(get_lineedit(self.FuseName_LineEdit).replace(" ", "_"))
        ## Basic
        datainfo["Action"] = get_combobox(self.Action_ComboBox)
        datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        #  Connections
        datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        #  TCC Curves
        datainfo["FuseCurve"] = get_combobox(self.FuseCurve_ComboBox)
        datainfo["RatedCurrent"] = get_lineedit(self.RatedCurrent_LineEdit)

        if self.FuseName_LineEdit.isEnabled():
            ctdExist = False
            for ctd in self.Fuse_parent.FuseDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.Fuse_parent.FuseDataInfo.append(datainfo)
                self.Fuse_parent.AddFuseDataInfo.append(datainfo)
                QMessageBox(QMessageBox.Information, "Fusível",
                            "Fusível " + datainfo["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Fusível",
                            "Fusível " + datainfo["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.Fuse_parent.FuseDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ## Basic
                    ctd["Action"] = datainfo["Action"]
                    ctd["Delay"] = datainfo["Delay"]
                    ctd["Enabled"] = datainfo["Enabled"]

                    #  Connections
                    ctd["MonitoredObj"] = datainfo["MonitoredObj"]
                    ctd["MonitoredTerm"] = datainfo["MonitoredTerm"]
                    ctd["SwitchedObj"] = datainfo["SwitchedObj"]
                    ctd["SwitchedTerm"] = datainfo["SwitchedTerm"]
                    #  TCC Curves
                    #  Phase
                    ctd["FuseCurve"] = datainfo["FuseCurve"]
                    ctd["RatedCurrent"] = datainfo["RatedCurrent"]

                    QMessageBox(QMessageBox.Information, "Fusível",
                                "Fusível " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.Fuse_parent.updateProtectDialog()
        self.adjustSize()
        self.close()

    def clearFuseParameters(self):
        self.FuseName_LineEdit.setText("")
        ## Basic
        self.Action_ComboBox.setCurrentIndex(0)
        self.Delay_LineEdit.setText("")
        self.Enable_ComboBox.setCurrentIndex(0)

        self.MonitObj_ComboBox.setCurrentIndex(0)
        self.MonitTerm_ComboBox.setCurrentIndex(0)
        self.SwitchedObj_ComboBox.setCurrentIndex(0)
        self.SwitchedTerm_ComboBox.setCurrentIndex(0)

        self.FuseCurve_ComboBox.setCurrentIndex(0)
        self.RatedCurrent_LineEdit.setText("")

    def updateEditDialog(self):
        self.MonitObj_ComboBox.clear()
        self.SwitchedObj_ComboBox.clear()

        for index, item in enumerate(self.Fuse_parent.ElementList):
            self.MonitObj_ComboBox.addItem(item, item)
            self.SwitchedObj_ComboBox.addItem(item, item)


class Relay(QWidget):

    def __init__(self):
        super().__init__()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Relay = EditRelay(self)
        self.RelaySettings_GroupBox = QGroupBox('Selecionar Relay')
        self.RelaySettings_GroupBox_Layout = QVBoxLayout()
        self.RelaySettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RelaySelect_Combobox = QComboBox()
        self.RelaySelect_Combobox.setMaximumWidth(150)
        self.RelaySettings_GroupBox_Layout.addWidget(self.RelaySelect_Combobox)

        self.ElementList = []
        self.AddRelayDataInfo = []
        self.RelayDataInfo = []
        self.loadDatabaseFlag = False
        self.flag = False

        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        # self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_Relay.removeRelay)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        # self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        # self.Edit_Btn.setFixedWidth(80)
        self.Edit_Btn.clicked.connect(self.Edit_Relay.editRelay(self.RelaySelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        # self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.Add_Btn.setFixedWidth(80)
        self.Add_Btn.clicked.connect(self.Edit_Relay.addRelay())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.RelaySettings_GroupBox.setLayout(self.RelaySettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.RelaySettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_RelayInfoBOM(self):
        RelaySelected = self.RelaySelect_Combobox.currentText()
        for item in self.RelayDataInfo:
            if item["Name"] == RelaySelected:

                self.Edit_Relay.RelayName_LineEdit.setText(item["Name"])

                if item["Enabled"] == 'yes' or item["Enabled"] == '':
                    self.Edit_Relay.Enable_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_Relay.Enable_ComboBox.setCurrentIndex(1)

                self.Edit_Relay.type_ComboBox.setCurrentText(item["Type"])
                self.Edit_Relay.Action_ComboBox.setCurrentText(item["Action"])
                self.Edit_Relay.Delay_LineEdit.setText(item["Delay"])
                self.Edit_Relay.Shots_LineEdit.setText(item["Shots"])
                self.Edit_Relay.RecloseIntervals_LineEdit.setText(item["RecloseIntervals"])
                self.Edit_Relay.Kvbase_LineEdit.setText(item["Kvbase"])
                self.Edit_Relay.Breakertime_LineEdit.setText(item["Breakertime"])
                self.Edit_Relay.ResetTime_LineEdit.setText(item["Reset"])
                self.Edit_Relay.Pickup46_LineEdit.setText(item["46%Pickup"])
                self.Edit_Relay.BaseAmps46_LineEdit.setText(item["46BaseAmps"])
                self.Edit_Relay.isqt46_LineEdit.setText(item["46isqt"])
                self.Edit_Relay.Pickup47_LineEdit.setText(item["47%Pickup"])

                self.Edit_Relay.MonitObj_ComboBox.setCurrentText(item["MonitoredObj"])
                self.Edit_Relay.MonitTerm_ComboBox.setCurrentText(item["MonitoredTerm"])
                self.Edit_Relay.SwitchedObj_ComboBox.setCurrentText(item["SwitchedObj"])
                self.Edit_Relay.SwitchedTerm_ComboBox.setCurrentText(item["SwitchedTerm"])

                self.Edit_Relay.GroundCurve_ComboBox.setCurrentText(item["Groundcurve"])
                self.Edit_Relay.GroundTrip_LineEdit.setText(item["GroundTrip"])
                self.Edit_Relay.GroundTimeDial_LineEdit.setText(item["TdGround"])

                self.Edit_Relay.PhaseCurve_ComboBox.setCurrentText(item["Phasecurve"])
                self.Edit_Relay.PhaseTrip_LineEdit.setText(item["PhaseTrip"])
                self.Edit_Relay.PhaseTimeDial_LineEdit.setText(item["TdPhase"])

                self.Edit_Relay.OverVoltCurve_ComboBox.setCurrentText(item["Overvoltcurve"])
                self.Edit_Relay.OverVoltTrip_LineEdit.setText(item["Overtrip"])
                self.Edit_Relay.UnderVoltCurve_ComboBox.setCurrentText(item["Undervolcurve"])
                self.Edit_Relay.UnderVoltTrip_LineEdit.setText(item["UnderTrip"])

    def load_RelaysDatabase(self):
        databaseRelaydict = {}
        databaseRelay = self.OpenDSS.getRelayList()
        # Se trocar de subestação

        # Caso seja encontrado algum Relay que ainda pertence ao database, ou seja, se não foi trocado de subestação
        try:
            for item in databaseRelay:
                for item2 in self.RelayDataInfo:
                    if item.split(" MonitoredObj=")[0].split("New Relay.")[1] == item2["Name"]:
                        self.flag = True
                        return
                    else:
                        self.flag = False
        except:
            pass

        # Caso algum Relay tenha sido adicionado
        if self.AddRelayDataInfo:
            self.flag = True

        # Caso não haja Relayes adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.RelayDataInfo.clear()
            self.AddRelayDataInfo.clear()

        # Caso a lista de Relayes esteja vazia:
        if not self.RelayDataInfo:
            for item in databaseRelay:
                databaseRelaydict["Name"] = item.split(" MonitoredObj=")[0].split("New Relay.")[1]
                # Basic

                databaseRelaydict["Action"] = ''
                databaseRelaydict["Enabled"] = ''
                databaseRelaydict["Type"] = item.split("type=")[1].capitalize()

                databaseRelaydict["46%Pickup"] = ''
                databaseRelaydict["46BaseAmps"] = ''
                databaseRelaydict["46isqt"] = ''
                databaseRelaydict["47%Pickup"] = ''
                databaseRelaydict["Breakertime"] = ''
                databaseRelaydict["Delay"] = ''
                databaseRelaydict["Kvbase"] = ''
                databaseRelaydict["RecloseIntervals"] = ''
                databaseRelaydict["Reset"] = ''
                databaseRelaydict["Shots"] = ''
                # Connections
                databaseRelaydict["MonitoredObj"] = item.split(" SwitchedObj=")[0].split("MonitoredObj=")[1]
                databaseRelaydict["MonitoredTerm"] = ''
                databaseRelaydict["SwitchedObj"] = item.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
                databaseRelaydict["SwitchedTerm"] = item.split(" type=")[0].split("SwitchedTerm=")[1]
                # TCC Curves
                # Ground
                databaseRelaydict["Groundcurve"] = ''
                #databaseRelaydict["GroundInst"] = ''
                databaseRelaydict["GroundTrip"] = ''
                databaseRelaydict["TdGround"] = ''
                # Phase
                databaseRelaydict["Phasecurve"] = ''
                #databaseRelaydict["PhaseInst"] = ''
                databaseRelaydict["PhaseTrip"] = ''
                databaseRelaydict["TdPhase"] = ''
                # Under n' Over trp
                databaseRelaydict["Overtrip"] = ''
                databaseRelaydict["Overvoltcurve"] = ''
                databaseRelaydict["UnderTrip"] = ''
                databaseRelaydict["Undervolcurve"] = ''

                #databaseRelaydict["Variable"] = ''
                # print(databaseRelaydict)
                if not self.loadDatabaseFlag:
                    self.RelayDataInfo.append(databaseRelaydict.copy())

            self.loadDatabaseFlag = True

    def updateProtectDialog(self):
        self.load_RelaysDatabase()
        # Carregando a ElementList para ser usada na Edit Dialog
        self.ElementList = self.OpenDSS.getElementList()
        self.RelaySelect_Combobox.clear()
        for dicio in self.RelayDataInfo:
            self.RelaySelect_Combobox.addItem(dicio["Name"], dicio["Name"])


class EditRelay(QDialog):
    def __init__(self, Relay_parent):
        super().__init__()
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.Relay_parent = Relay_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825, 0)  ##Resolução 1366x768
        self.Dialog_Layout = QVBoxLayout()
        self.RelayInfo()
        self.Btns()
        self.setLayout(self.Dialog_Layout)

    def RelayInfo(self):
        # Parâmetros Intrínsecos do Relay
        self.Edit_Relay_GroupBox = QGroupBox('Geral')
        self.Edit_Relay_GroupBox_Layout = QGridLayout()
        self.Edit_Relay_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RelayName_LineEdit = QLineEdit()
        self.RelayName_LineEdit_Label = QLabel("Dispositivo")
        self.RelayName_LineEdit.setMaximumWidth(150)

        self.actionlist = ['Aberto', 'Fechado']
        self.actionlist_data = ['Open', 'Closed']
        self.Action_ComboBox = QComboBox()
        self.Action_ComboBox.setMaximumWidth(150)
        self.Action_ComboBox_Label = QLabel("Action")
        for index, item in enumerate(self.actionlist):
            self.Action_ComboBox.addItem(item, self.actionlist_data[index])

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.enablelist = ['Sim', 'Não']
        self.enablelist_data = ['yes', 'no']
        self.Enable_ComboBox = QComboBox()
        self.Enable_ComboBox.setMaximumWidth(150)
        self.Enable_ComboBox_Label = QLabel("Habilitado")
        for index, item in enumerate(self.enablelist):
            self.Enable_ComboBox.addItem(item, self.enablelist_data[index])

        self.typelist = [ 'Voltage','Current', 'Reversepower', '46 (neg seq current)', '47 (neg seq voltage)',
                         'Generic']
        self.typelist_data = ['Voltage', 'Current', 'Reversepower', '46', '47', 'Generic']
        self.type_ComboBox = QComboBox()
        self.type_ComboBox.currentIndexChanged.connect(self.HideNegSeqPar)
        self.type_ComboBox.setMaximumWidth(150)
        self.type_ComboBox_Label = QLabel("Tipo")
        for index, item in enumerate(self.typelist):
            self.type_ComboBox.addItem(item, self.typelist_data[index])

        self.Pickup46_LineEdit = QLineEdit()
        self.Pickup46_LineEdit.setMaximumWidth(150)
        self.Pickup46_LineEdit_Label = QLabel("46%Pickup")

        self.BaseAmps46_LineEdit = QLineEdit()
        self.BaseAmps46_LineEdit.setMaximumWidth(150)
        self.BaseAmps46_LineEdit_Label = QLabel("46BaseAmps")

        self.isqt46_LineEdit = QLineEdit()
        self.isqt46_LineEdit.setMaximumWidth(150)
        self.isqt46_LineEdit_Label = QLabel("46%isqt")

        self.Pickup47_LineEdit = QLineEdit()
        self.Pickup47_LineEdit.setMaximumWidth(150)
        self.Pickup47_LineEdit_Label = QLabel("47%Pickup")

        self.Breakertime_LineEdit = QLineEdit()
        self.Breakertime_LineEdit.setMaximumWidth(150)
        self.Breakertime_LineEdit_Label = QLabel("Breakertime")

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.Kvbase_LineEdit = QLineEdit()
        self.Kvbase_LineEdit.setMaximumWidth(150)
        self.Kvbase_LineEdit_Label = QLabel("Kvbase")

        self.RecloseIntervals_LineEdit = QLineEdit()
        self.RecloseIntervals_LineEdit.setPlaceholderText("Ex: 2,2,5,5")
        self.RecloseIntervals_LineEdit.setMaximumWidth(150)
        self.RecloseIntervals_LineEdit_Label = QLabel("RecloseIntervals")

        self.ResetTime_LineEdit = QLineEdit()
        self.ResetTime_LineEdit_Label = QLabel("ResetTime")
        self.ResetTime_LineEdit.setMaximumWidth(150)

        self.Shots_LineEdit = QLineEdit()
        self.Shots_LineEdit.setMaximumWidth(150)
        self.Shots_LineEdit_Label = QLabel("Shots")

        self.Edit_Relay_GroupBox_Layout.addWidget(self.RelayName_LineEdit_Label, 0, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.RelayName_LineEdit, 0, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 1, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Enable_ComboBox, 1, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.type_ComboBox_Label, 2, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.type_ComboBox, 2, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 3, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Action_ComboBox, 3, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 4, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Delay_LineEdit, 4, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Shots_LineEdit_Label, 5, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Shots_LineEdit, 5, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.RecloseIntervals_LineEdit_Label, 6, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.RecloseIntervals_LineEdit, 6, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Pickup46_LineEdit_Label, 7, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Pickup46_LineEdit, 7, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.BaseAmps46_LineEdit_Label, 8, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.BaseAmps46_LineEdit, 8, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.isqt46_LineEdit_Label, 9, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.isqt46_LineEdit, 9, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Pickup47_LineEdit_Label, 10, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Pickup47_LineEdit, 10, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Kvbase_LineEdit_Label, 11, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Kvbase_LineEdit, 11, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Breakertime_LineEdit_Label, 12, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.Breakertime_LineEdit, 12, 1)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.ResetTime_LineEdit_Label, 13, 0)
        self.Edit_Relay_GroupBox_Layout.addWidget(self.ResetTime_LineEdit, 13, 1)

        self.Edit_Relay_GroupBox.setLayout(self.Edit_Relay_GroupBox_Layout)

        # Parâmetros de conexões do Relay
        self.Conn_Relay_GroupBox = QGroupBox('Conexões ')
        self.Conn_Relay_GroupBox_Layout = QGridLayout()
        self.Conn_Relay_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.MonitObj_ComboBox = QComboBox()
        self.MonitObj_ComboBox.setMinimumWidth(150)
        self.MonitObj_ComboBox_Label = QLabel("Elemento Monitorado")

        self.MonitTermList = ['1', '2']
        self.MonitTerm_ComboBox = QComboBox()
        # self.MonitTerm_ComboBox.setMaximumWidth(150)
        self.MonitTerm_ComboBox_Label = QLabel("Terminal Monitorado")
        for index, item in enumerate(self.MonitTermList):
            self.MonitTerm_ComboBox.addItem(item, item)

        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMinimumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_Relay_GroupBox_Layout.addWidget(self.MonitObj_ComboBox_Label, 0, 0, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.MonitObj_ComboBox, 0, 1, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox_Label, 0, 2, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox, 0, 3, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_Relay_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
        self.Conn_Relay_GroupBox.setLayout(self.Conn_Relay_GroupBox_Layout)

        # Curvas TCC
        self.TCCCurves_Relay_GroupBox = QGroupBox('Curvas TCC')
        self.TCCCurves_Relay_GroupBox_Layout = QGridLayout()
        self.TCCCurves_Relay_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.GroundCurveList = ['a', 'b', 'c', 'd']
        self.GroundCurve_ComboBox = QComboBox()
        self.GroundCurve_ComboBox.setMaximumWidth(150)
        self.GroundCurve_ComboBox_Label = QLabel("Ground Curve")
        for index, item in enumerate(self.GroundCurveList):
            self.GroundCurve_ComboBox.addItem(item, item)

        self.GroundTrip_LineEdit = QLineEdit()
        self.GroundTrip_LineEdit.setMaximumWidth(50)
        self.GroundTrip_LineEdit.setPlaceholderText("1.0")
        self.GroundTrip_LineEdit_Label = QLabel("Ground Multiplier Amps")

        self.GroundTimeDial_LineEdit = QLineEdit()
        self.GroundTimeDial_LineEdit.setMaximumWidth(50)
        self.GroundTimeDial_LineEdit.setPlaceholderText("1.0")
        self.GroundTimeDial_LineEdit_Label = QLabel("Time dial - Ground")

        self.PhaseCurveList = ['a', 'b', 'c', 'd']
        self.PhaseCurve_ComboBox = QComboBox()
        self.PhaseCurve_ComboBox.setMaximumWidth(150)
        self.PhaseCurve_ComboBox_Label = QLabel("Phase Curve")
        for index, item in enumerate(self.PhaseCurveList):
            self.PhaseCurve_ComboBox.addItem(item, item)

        self.PhaseTrip_LineEdit = QLineEdit()
        self.PhaseTrip_LineEdit.setMaximumWidth(50)
        self.PhaseTrip_LineEdit.setPlaceholderText("1.0")
        self.PhaseTrip_LineEdit_Label = QLabel("Phase Multiplier Amps")

        self.PhaseTimeDial_LineEdit = QLineEdit()
        self.PhaseTimeDial_LineEdit.setMaximumWidth(50)
        self.PhaseTimeDial_LineEdit.setPlaceholderText("1.0")
        self.PhaseTimeDial_LineEdit_Label = QLabel("Time dial - Phase")

        self.OverVoltCurveList = ['a', 'b', 'c', 'd']
        self.OverVoltCurve_ComboBox = QComboBox()
        self.OverVoltCurve_ComboBox.setMaximumWidth(150)
        self.OverVoltCurve_ComboBox_Label = QLabel("OverVolt Curve")
        for index, item in enumerate(self.OverVoltCurveList):
            self.OverVoltCurve_ComboBox.addItem(item, item)

        self.OverVoltTrip_LineEdit = QLineEdit()
        self.OverVoltTrip_LineEdit.setMaximumWidth(50)
        self.OverVoltTrip_LineEdit.setPlaceholderText("1.0")
        self.OverVoltTrip_LineEdit_Label = QLabel("OverVolt Multiplier Amps")

        self.UnderVoltCurveList = ['a', 'b', 'c', 'd']
        self.UnderVoltCurve_ComboBox = QComboBox()
        self.UnderVoltCurve_ComboBox.setMaximumWidth(150)
        self.UnderVoltCurve_ComboBox_Label = QLabel("UnderVolt Curve")
        for index, item in enumerate(self.UnderVoltCurveList):
            self.UnderVoltCurve_ComboBox.addItem(item, item)

        self.UnderVoltTrip_LineEdit = QLineEdit()
        self.UnderVoltTrip_LineEdit.setMaximumWidth(50)
        self.UnderVoltTrip_LineEdit.setPlaceholderText("1.0")
        self.UnderVoltTrip_LineEdit_Label = QLabel("UnderVolt Multiplier Amps")

        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundCurve_ComboBox_Label, 0, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundCurve_ComboBox, 0, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit_Label, 1, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit, 1, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTimeDial_LineEdit_Label, 2, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTimeDial_LineEdit, 2, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseCurve_ComboBox_Label, 3, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseCurve_ComboBox, 3, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit_Label, 4, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit, 4, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTimeDial_LineEdit_Label, 5, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTimeDial_LineEdit, 5, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltCurve_ComboBox_Label, 6, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltCurve_ComboBox, 6, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltTrip_LineEdit_Label, 7, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltTrip_LineEdit, 7, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltCurve_ComboBox_Label, 8, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltCurve_ComboBox, 8, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltTrip_LineEdit_Label, 9, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltTrip_LineEdit, 9, 3, 1, 1)

        self.TCCCurves_Relay_GroupBox.setLayout(self.TCCCurves_Relay_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_Relay_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Relay_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Relay_GroupBox)

    def HideNegSeqPar(self):
        if self.type_ComboBox.currentText() == self.typelist[3]:
            self.Pickup46_LineEdit.setHidden(False)
            self.BaseAmps46_LineEdit.setHidden(False)
            self.isqt46_LineEdit.setHidden(False)
            self.Pickup47_LineEdit.setHidden(True)
            self.Pickup46_LineEdit_Label.setHidden(False)
            self.BaseAmps46_LineEdit_Label.setHidden(False)
            self.isqt46_LineEdit_Label.setHidden(False)
            self.Pickup47_LineEdit_Label.setHidden(True)

        elif self.type_ComboBox.currentText() == self.typelist[4]:
            self.Pickup46_LineEdit.setHidden(True)
            self.BaseAmps46_LineEdit.setHidden(True)
            self.isqt46_LineEdit.setHidden(True)
            self.Pickup47_LineEdit.setHidden(False)
            self.Pickup46_LineEdit_Label.setHidden(True)
            self.BaseAmps46_LineEdit_Label.setHidden(True)
            self.isqt46_LineEdit_Label.setHidden(True)
            self.Pickup47_LineEdit_Label.setHidden(False)
        else:
            try:
                self.Pickup46_LineEdit.setHidden(True)
                self.BaseAmps46_LineEdit.setHidden(True)
                self.isqt46_LineEdit.setHidden(True)
                self.Pickup47_LineEdit.setHidden(True)
                self.Pickup46_LineEdit_Label.setHidden(True)
                self.BaseAmps46_LineEdit_Label.setHidden(True)
                self.isqt46_LineEdit_Label.setHidden(True)
                self.Pickup47_LineEdit_Label.setHidden(True)
            except AttributeError:
                pass

        self.adjustSize()

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.AcceptAddEditRelay)

        self.AddTCC_Btn = QPushButton("Add TCC Curve")
        self.AddTCC_Btn.setMaximumWidth(150)
        # self.AddTCC_Btn.clicked.connect(self.Relay_parent.RelayList)

        self.btngroupbox_layout.addWidget(self.AddTCC_Btn)
        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def editRelay(self, get_name):
        # Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar Relay {get_name()}'
            self.setWindowTitle(self.titleWindow)

            self.RelayName_LineEdit.setEnabled(False)
            self.show()
            self.updateEditDialog()
            self.adjustSize()
            self.Relay_parent.load_RelayInfoBOM()
            self.Relay_parent.load_RelaysDatabase()
            self.HideNegSeqPar()

        return process

    def addRelay(self):
        # Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar Relay'
            self.setWindowTitle(self.titleWindow)

            self.RelayName_LineEdit.setEnabled(True)
            self.show()
            self.clearRelayParameters()
            self.updateEditDialog()
            self.HideNegSeqPar()
            self.adjustSize()


        return process

    def removeRelay(self):
        for ctd in self.Relay_parent.RelayDataInfo:
            if ctd["Name"] == self.Relay_parent.RelaySelect_Combobox.currentText():
                self.Relay_parent.RelayDataInfo.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Relay",
                            "Relay " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()

        self.Relay_parent.RelaySelect_Combobox.clear()
        for dicio in self.Relay_parent.RelayDataInfo:
            self.Relay_parent.RelaySelect_Combobox.addItem(dicio["Name"], dicio["Name"])
        self.clearRelayParameters()

    def loadParameters(self):

        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        self.datainfo["Type"] = get_combobox(self.type_ComboBox)
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Shots"] = get_lineedit(self.Shots_LineEdit)
        self.datainfo["RecloseIntervals"] = get_lineedit(self.RecloseIntervals_LineEdit)
        self.datainfo["Kvbase"] = get_lineedit(self.Kvbase_LineEdit)
        self.datainfo["Breakertime"] = get_lineedit(self.Breakertime_LineEdit)
        self.datainfo["Reset"] = get_lineedit(self.ResetTime_LineEdit)
        self.datainfo["46%Pickup"] = get_lineedit(self.Pickup46_LineEdit)
        self.datainfo["46BaseAmps"] = get_lineedit(self.BaseAmps46_LineEdit)
        self.datainfo["46isqt"] = get_lineedit(self.isqt46_LineEdit)
        self.datainfo["47%Pickup"] = get_lineedit(self.Pickup47_LineEdit)
        # Connections
        self.datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        self.datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)
        # TCC Curves
        # Ground
        self.datainfo["Groundcurve"] = get_combobox(self.GroundCurve_ComboBox)
        self.datainfo["GroundTrip"] = get_lineedit(self.GroundTrip_LineEdit)
        self.datainfo["TdGround"] = get_lineedit(self.GroundTimeDial_LineEdit)
        # Ph
        self.datainfo["Phasecurve"] = get_combobox(self.PhaseCurve_ComboBox)
        self.datainfo["PhaseTrip"] = get_lineedit(self.PhaseTrip_LineEdit)
        self.datainfo["TdPhase"] = get_lineedit(self.PhaseTimeDial_LineEdit)
        # Under n' Over
        self.datainfo["Overvoltcurve"] = get_combobox(self.OverVoltCurve_ComboBox)
        self.datainfo["Overtrip"] = get_lineedit(self.OverVoltTrip_LineEdit)
        self.datainfo["Undervolcurve"] = get_combobox(self.UnderVoltCurve_ComboBox)
        self.datainfo["UnderTrip"] = get_lineedit(self.UnderVoltTrip_LineEdit)

    def AcceptAddEditRelay(self):  # Dá para otimizar e muito // Somente um teste

        datainfo = {"Name": unidecode.unidecode(get_lineedit(self.RelayName_LineEdit).replace(" ", "_")),
                    "Enabled": get_combobox(self.Enable_ComboBox), "Type": get_combobox(self.type_ComboBox),
                    "Action": get_combobox(self.Action_ComboBox), "Delay": get_lineedit(self.Delay_LineEdit),
                    "Shots": get_lineedit(self.Shots_LineEdit),
                    "RecloseIntervals": get_lineedit(self.RecloseIntervals_LineEdit),
                    "Kvbase": get_lineedit(self.Kvbase_LineEdit),
                    "Breakertime": get_lineedit(self.Breakertime_LineEdit),
                    "Reset": get_lineedit(self.ResetTime_LineEdit), "46%Pickup": get_lineedit(self.Pickup46_LineEdit),
                    "46BaseAmps": get_lineedit(self.BaseAmps46_LineEdit), "46isqt": get_lineedit(self.isqt46_LineEdit),
                    "47%Pickup": get_lineedit(self.Pickup47_LineEdit),
                    "MonitoredObj": get_combobox(self.MonitObj_ComboBox),
                    "MonitoredTerm": get_combobox(self.MonitTerm_ComboBox),
                    "SwitchedObj": get_combobox(self.SwitchedObj_ComboBox),
                    "SwitchedTerm": get_combobox(self.SwitchedTerm_ComboBox),
                    "Groundcurve": get_combobox(self.GroundCurve_ComboBox),
                    "GroundTrip": get_lineedit(self.GroundTrip_LineEdit),
                    "TdGround": get_lineedit(self.GroundTimeDial_LineEdit),
                    "Phasecurve": get_combobox(self.PhaseCurve_ComboBox),
                    "PhaseTrip": get_lineedit(self.PhaseTrip_LineEdit),
                    "TdPhase": get_lineedit(self.PhaseTimeDial_LineEdit),
                    "Overvoltcurve": get_combobox(self.OverVoltCurve_ComboBox),
                    "Overtrip": get_lineedit(self.OverVoltTrip_LineEdit),
                    "Undervolcurve": get_combobox(self.UnderVoltCurve_ComboBox),
                    "UnderTrip": get_lineedit(self.UnderVoltTrip_LineEdit)}

        if self.RelayName_LineEdit.isEnabled():
            ctdExist = False
            for ctd in self.Relay_parent.RelayDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.Relay_parent.RelayDataInfo.append(datainfo)
                self.Relay_parent.AddRelayDataInfo.append(datainfo)
                QMessageBox(QMessageBox.Information, "Relay",
                            "Relay " + datainfo["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Relay",
                            "Relay " + datainfo["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.Relay_parent.RelayDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    #  Geral
                    ctd["Enabled"] = datainfo["Enabled"]
                    ctd["Type"] = datainfo["Type"]
                    ctd["Delay"] = datainfo["Delay"]
                    ctd["Shots"] = datainfo["Shots"]
                    ctd["RecloseIntervals"] = datainfo["RecloseIntervals"]
                    ctd["Kvbase"] = datainfo["Kvbase"]
                    ctd["Breakertime"] = datainfo["Breakertime"]
                    ctd["Reset"] = datainfo["Reset"]
                    ctd["46%Pickup"] = datainfo["46%Pickup"]
                    ctd["46BaseAmps"] = datainfo["46BaseAmps"]
                    ctd["46isqt"] = datainfo["46isqt"]
                    ctd["47%Pickup"] = datainfo["47%Pickup"]
                    # Connections
                    ctd["MonitoredObj"] = datainfo["MonitoredObj"]
                    ctd["MonitoredTerm"] = datainfo["MonitoredTerm"]
                    ctd["SwitchedObj"] = datainfo["SwitchedObj"]
                    ctd["SwitchedTerm"] = datainfo["SwitchedTerm"]
                    # TCC Curves
                    # Ground
                    ctd["Groundcurve"] = datainfo["Groundcurve"]
                    ctd["GroundTrip"] = datainfo["GroundTrip"]
                    ctd["TdGround"] = datainfo["TdGround"]
                    # Ph
                    ctd["Phasecurve"] = datainfo["Phasecurve"]
                    ctd["PhaseTrip"] = datainfo["PhaseTrip"]
                    ctd["TdPhase"] = datainfo["TdPhase"]
                    # Under n' Over
                    ctd["Overvoltcurve"] = datainfo["Overvoltcurve"]
                    ctd["Overtrip"] = datainfo["Overtrip"]
                    ctd["Undervolcurve"] = datainfo["Undervolcurve"]
                    ctd["UnderTrip"] = datainfo["UnderTrip"]

                    QMessageBox(QMessageBox.Information, "Relay",
                                "Relay " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.Relay_parent.updateProtectDialog()
        self.adjustSize()
        self.close()

    def clearRelayParameters(self):
        self.RelayName_LineEdit.setText("")
        self.Enable_ComboBox.setCurrentIndex(0)
        self.type_ComboBox.setCurrentIndex(0)
        self.Action_ComboBox.setCurrentIndex(0)
        self.Delay_LineEdit.setText("")
        self.Shots_LineEdit.setText("")
        self.RecloseIntervals_LineEdit.setText("")
        self.Kvbase_LineEdit.setText("")
        self.Breakertime_LineEdit.setText("")
        self.ResetTime_LineEdit.setText("")
        self.Pickup46_LineEdit.setText("")
        self.BaseAmps46_LineEdit.setText("")
        self.isqt46_LineEdit.setText("")
        self.Pickup47_LineEdit.setText("")

        self.MonitObj_ComboBox.setCurrentIndex(0)
        self.MonitTerm_ComboBox.setCurrentIndex(0)
        self.SwitchedObj_ComboBox.setCurrentIndex(0)
        self.SwitchedTerm_ComboBox.setCurrentIndex(0)

        self.GroundCurve_ComboBox.setCurrentIndex(0)
        self.GroundTrip_LineEdit.setText("")
        self.GroundTimeDial_LineEdit.setText("")

        self.PhaseCurve_ComboBox.setCurrentIndex(0)
        self.PhaseTrip_LineEdit.setText("")
        self.PhaseTimeDial_LineEdit.setText("")

        self.OverVoltCurve_ComboBox.setCurrentIndex(0)
        self.OverVoltTrip_LineEdit.setText("")
        self.UnderVoltCurve_ComboBox.setCurrentIndex(0)
        self.UnderVoltTrip_LineEdit.setText("")

    def updateEditDialog(self):
        self.MonitObj_ComboBox.clear()
        self.SwitchedObj_ComboBox.clear()
        self.HideNegSeqPar()
        for index, item in enumerate(self.Relay_parent.ElementList):
            self.MonitObj_ComboBox.addItem(item, item)
            self.SwitchedObj_ComboBox.addItem(item, item)


class SwtControl(QWidget):

    def __init__(self):
        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_SwtControl = EditSwtControl(self)
        self.SwtControlSettings_GroupBox = QGroupBox('Selecionar Switch')
        self.SwtControlSettings_GroupBox_Layout = QVBoxLayout()
        self.SwtControlSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.SwtControlSelect_Combobox = QComboBox()
        self.SwtControlSelect_Combobox.setMaximumWidth(150)
        self.SwtControlSettings_GroupBox_Layout.addWidget(self.SwtControlSelect_Combobox)

        self.ElementList = []
        self.AddSwtControlDataInfo = []
        self.SwtControlDataInfo = []
        self.loadDatabaseFlag = False
        self.flag = False

        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_SwtControl.removeSwtControl)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.Edit_Btn.clicked.connect(self.Edit_SwtControl.editSwtControl(self.SwtControlSelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.Add_Btn.clicked.connect(self.Edit_SwtControl.addSwtControl())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.SwtControlSettings_GroupBox.setLayout(self.SwtControlSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.SwtControlSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_SwtControlInfoBOM(self):
        SwtControlSelected = self.SwtControlSelect_Combobox.currentText()
        for item in self.SwtControlDataInfo:
            if item["Name"] == SwtControlSelected:

                self.Edit_SwtControl.SwtControlName_LineEdit.setText(item["Name"])

                if item["Action"] == 'close':
                    self.Edit_SwtControl.Action_ComboBox.setCurrentIndex(1)
                else:
                    self.Edit_SwtControl.Action_ComboBox.setCurrentIndex(0)

                self.Edit_SwtControl.Delay_LineEdit.setText(item["Delay"])

                if item["Enabled"] == 'yes' or item["Enabled"] == '':
                    self.Edit_SwtControl.Enable_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_SwtControl.Enable_ComboBox.setCurrentIndex(1)

                if item["Lock"] == 'yes':
                    self.Edit_SwtControl.Lock_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_SwtControl.Lock_ComboBox.setCurrentIndex(1)

                self.Edit_SwtControl.Normal_ComboBox.setCurrentText(item["Normal"])
                self.Edit_SwtControl.Reset_ComboBox.setCurrentText(item["Reset"])
                self.Edit_SwtControl.State_ComboBox.setCurrentText(item["State"])

                self.Edit_SwtControl.SwitchedObj_ComboBox.setCurrentText(item["SwitchedObj"])
                self.Edit_SwtControl.SwitchedTerm_ComboBox.setCurrentText(item["SwitchedTerm"])

    def load_SwtControlsDatabase(self):
        databaseSwtControldict = {}
        databaseSwtControl = self.OpenDSS.getSwtControlList()
        # print(databaseSwtControl)
        # Se trocar de subestação

        # Caso seja encontrado algum Switch que ainda pertence ao database, ou seja, se não foi trocado de subestação
        try:
            for item in databaseSwtControl:
                for item2 in self.SwtControlDataInfo:
                    if item.split(" SwitchedObj=")[0].split("New SwtControl.")[1] == item2["Name"]:
                        self.flag = True
                        return
                    else:
                        self.flag = False
        except:
            pass

        # Caso algum Switch tenha sido adicionado
        if self.AddSwtControlDataInfo:
            self.flag = True

        # Caso não haja Switches adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.SwtControlDataInfo.clear()
            self.AddSwtControlDataInfo.clear()

        # Caso a lista de Switches esteja vazia:
        if not self.SwtControlDataInfo and not self.loadDatabaseFlag:
            for item in databaseSwtControl:
                databaseSwtControldict["Name"] = item.split(" SwitchedObj=")[0].split("New Swtcontrol.")[1]
                # Basic
                if item.split(" lock=")[0].split("Action=")[1] == 'c':
                    databaseSwtControldict["Action"] = 'close'
                else:
                    databaseSwtControldict["Action"] = 'open'

                databaseSwtControldict["Delay"] = ''
                databaseSwtControldict["Enabled"] = ''
                databaseSwtControldict["Lock"] = item.split(" lock=")[1]
                databaseSwtControldict["Normal"] = ''
                databaseSwtControldict["Reset"] = ''
                databaseSwtControldict["State"] = ''
                # Connections
                databaseSwtControldict["SwitchedObj"] = item.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
                databaseSwtControldict["SwitchedTerm"] = item.split(" Action=")[0].split("SwitchedTerm=")[1]
                self.SwtControlDataInfo.append(databaseSwtControldict.copy())

            self.loadDatabaseFlag = True

    def updateProtectDialog(self):
        self.load_SwtControlsDatabase()
        # Carregando a ElementList para ser usada na Edit Dialog
        self.ElementList = self.OpenDSS.getElementList()
        self.SwtControlSelect_Combobox.clear()
        for dicio in self.SwtControlDataInfo:
            self.SwtControlSelect_Combobox.addItem(dicio["Name"], dicio["Name"])


class EditSwtControl(QDialog):
    def __init__(self, SwtControl_parent):
        super().__init__()
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.SwtControl_parent = SwtControl_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825, 170)
        self.Dialog_Layout = QVBoxLayout()
        self.SwtControlInfo()
        self.Btns()
        self.setLayout(self.Dialog_Layout)

    def SwtControlInfo(self):
        # Parâmetros Intrínsecos do Switch
        self.Edit_SwtControl_GroupBox = QGroupBox('Geral')
        self.Edit_SwtControl_GroupBox_Layout = QGridLayout()
        self.Edit_SwtControl_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.SwtControlName_LineEdit = QLineEdit()
        self.SwtControlName_LineEdit_Label = QLabel("Dispositivo")
        self.SwtControlName_LineEdit.setMaximumWidth(150)

        self.actionlist = ['Aberto', 'Fechado']
        self.actionlist_data = ['Open', 'Closed']
        self.Action_ComboBox = QComboBox()
        self.Action_ComboBox.setMaximumWidth(150)
        self.Action_ComboBox_Label = QLabel("Action")
        for index, item in enumerate(self.actionlist):
            self.Action_ComboBox.addItem(item, self.actionlist_data[index])

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.enablelist = ['Sim', 'Não']
        self.enablelist_data = ['yes', 'no']
        self.Enable_ComboBox = QComboBox()
        self.Enable_ComboBox.setMaximumWidth(150)
        self.Enable_ComboBox_Label = QLabel("Habilitado")
        for index, item in enumerate(self.enablelist):
            self.Enable_ComboBox.addItem(item, self.enablelist_data[index])
            
        self.Locklist = ['Sim', 'Não']
        self.Locklist_data = ['yes', 'no']
        self.Lock_ComboBox = QComboBox()
        self.Lock_ComboBox.setMaximumWidth(150)
        self.Lock_ComboBox_Label = QLabel("Lock")
        for index, item in enumerate(self.Locklist):
            self.Lock_ComboBox.addItem(item, self.Locklist_data[index])


        self.Normallist = ['Aberto', 'Fechado']
        self.Normallist_data = ['Open', 'Closed']
        self.Normal_ComboBox = QComboBox()
        self.Normal_ComboBox.setMaximumWidth(150)
        self.Normal_ComboBox_Label = QLabel("Normal State")
        for index, item in enumerate(self.Normallist):
            self.Normal_ComboBox.addItem(item, self.Normallist_data[index])

        self.Resetlist = ['Sim', 'Não']
        self.Resetlist_data = ['yes', 'no']
        self.Reset_ComboBox = QComboBox()
        self.Reset_ComboBox.setMaximumWidth(150)
        self.Reset_ComboBox_Label = QLabel("Reset")
        for index, item in enumerate(self.Resetlist):
            self.Reset_ComboBox.addItem(item, self.Resetlist_data[index])
            

        self.Statelist = ['Aberto', 'Fechado']
        self.Statelist_data = ['Open', 'Closed']
        self.State_ComboBox = QComboBox()
        self.State_ComboBox.setMaximumWidth(150)
        self.State_ComboBox_Label = QLabel("State")
        for index, item in enumerate(self.Statelist):
            self.State_ComboBox.addItem(item, self.Statelist_data[index])
            

        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.SwtControlName_LineEdit_Label, 0, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.SwtControlName_LineEdit, 0, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 1, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Action_ComboBox, 1, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 2, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Delay_LineEdit, 2, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 3, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Enable_ComboBox, 3, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Lock_ComboBox_Label, 4, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Lock_ComboBox, 4, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Normal_ComboBox_Label, 5, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Normal_ComboBox, 5, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Reset_ComboBox_Label, 6, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Reset_ComboBox, 6, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.State_ComboBox_Label, 7, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.State_ComboBox, 7, 1)

        self.Edit_SwtControl_GroupBox.setLayout(self.Edit_SwtControl_GroupBox_Layout)

        # Parâmetros de conexões do Switch
        self.Conn_SwtControl_GroupBox = QGroupBox('Conexões ')
        self.Conn_SwtControl_GroupBox_Layout = QGridLayout()
        self.Conn_SwtControl_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMinimumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
        self.Conn_SwtControl_GroupBox.setLayout(self.Conn_SwtControl_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_SwtControl_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_SwtControl_GroupBox)

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.AcceptAddEditSwtControl)

        self.AddTCC_Btn = QPushButton("Add TCC Curve")
        self.AddTCC_Btn.setMaximumWidth(150)
        # self.AddTCC_Btn.clicked.connect(self.SwtControl_parent.SwtControlList)

        self.btngroupbox_layout.addWidget(self.AddTCC_Btn)
        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def editSwtControl(self, get_name):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar Switch {get_name()}'
            self.setWindowTitle(self.titleWindow)

            self.SwtControlName_LineEdit.setEnabled(False)
            self.show()
            self.updateEditDialog()
            self.SwtControl_parent.load_SwtControlInfoBOM()
            self.SwtControl_parent.load_SwtControlsDatabase()

        return process

    def addSwtControl(self):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar Switch'
            self.setWindowTitle(self.titleWindow)

            self.SwtControlName_LineEdit.setEnabled(True)
            self.show()
            self.clearSwtControlParameters()
            self.updateEditDialog()

        return process

    def removeSwtControl(self):
        for ctd in self.SwtControl_parent.SwtControlDataInfo:
            if ctd["Name"] == self.SwtControl_parent.SwtControlSelect_Combobox.currentText():
                self.SwtControl_parent.SwtControlDataInfo.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Switch",
                            "Switch " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
        self.clearSwtControlParameters()

        self.SwtControl_parent.SwtControlSelect_Combobox.clear()
        for dicio in self.SwtControl_parent.SwtControlDataInfo:
            self.SwtControl_parent.SwtControlSelect_Combobox.addItem(dicio["Name"], dicio["Name"])

    def loadParameters(self):
        self.datainfo["Name"] = get_lineedit(self.SwtControlName_LineEdit)
        ## Basic
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        self.datainfo["Lock"] = get_combobox(self.Lock_ComboBox)
        self.datainfo["Normal"] = get_combobox(self.Normal_ComboBox)
        self.datainfo["Reset"] = get_combobox(self.Reset_ComboBox)
        self.datainfo["State"] = get_combobox(self.State_ComboBox)

        #  Connections
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)


    def AcceptAddEditSwtControl(self):  # Dá para otimizar e muito // Somente um teste

        datainfo = {}
        datainfo["Name"] = unidecode.unidecode(get_lineedit(self.SwtControlName_LineEdit).replace(" ", "_"))
        ## Basic
        datainfo["Action"] = get_combobox(self.Action_ComboBox)
        datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        datainfo["Lock"] = get_combobox(self.Lock_ComboBox)
        datainfo["Normal"] = get_combobox(self.Normal_ComboBox)
        datainfo["Reset"] = get_combobox(self.Reset_ComboBox)
        datainfo["State"] = get_combobox(self.State_ComboBox)
        #  Connections

        datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        if self.SwtControlName_LineEdit.isEnabled():
            ctdExist = False
            for ctd in self.SwtControl_parent.SwtControlDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.SwtControl_parent.SwtControlDataInfo.append(datainfo)
                self.SwtControl_parent.AddSwtControlDataInfo.append(datainfo)
                QMessageBox(QMessageBox.Information, "Switch",
                            "Switch " + datainfo["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Switch",
                            "Switch " + datainfo["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.SwtControl_parent.SwtControlDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ## Basic
                    ctd["Action"] = datainfo["Action"]
                    ctd["Delay"] = datainfo["Delay"]
                    ctd["Enabled"] = datainfo["Enabled"]
                    ctd["Lock"] = datainfo["Lock"]
                    ctd["Normal"] = datainfo["Normal"]
                    ctd["Reset"]  = datainfo["Reset"]
                    ctd["State"]  = datainfo["State"]

                    #  Connections
                    ctd["SwitchedObj"] = datainfo["SwitchedObj"]
                    ctd["SwitchedTerm"] = datainfo["SwitchedTerm"]


                    QMessageBox(QMessageBox.Information, "Switch",
                                "Switch " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.SwtControl_parent.updateProtectDialog()
        self.adjustSize()
        self.close()

    def clearSwtControlParameters(self):
        self.SwtControlName_LineEdit.setText("")
        ## Basic
        self.Action_ComboBox.setCurrentIndex(0)
        self.Delay_LineEdit.setText("")
        self.Enable_ComboBox.setCurrentIndex(0)
        self.Lock_ComboBox.setCurrentIndex(0)
        self.Normal_ComboBox.setCurrentIndex(0)
        self.Reset_ComboBox.setCurrentIndex(0)
        self.State_ComboBox.setCurrentIndex(0)

        self.SwitchedObj_ComboBox.setCurrentIndex(0)
        self.SwitchedTerm_ComboBox.setCurrentIndex(0)


    def updateEditDialog(self):
        self.SwitchedObj_ComboBox.clear()

        for index, item in enumerate(self.SwtControl_parent.ElementList):
            self.SwitchedObj_ComboBox.addItem(item, item)

# Método "estático", não precisa estar dentro de alguma classe
def get_lineedit(lineedit):
    return lineedit.text()


def get_combobox(combobox):
    return str(combobox.itemData(combobox.currentIndex()))
