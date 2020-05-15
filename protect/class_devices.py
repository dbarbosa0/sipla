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

        self.TabWidget.addTab(self.TabRecloser, "Recloser")
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


# Método "estático", não precisa estar dentro de alguma classe
def get_lineedit(lineedit):
    return lineedit.text()


def get_combobox(combobox):
    return str(combobox.itemData(combobox.currentIndex()))


class Recloser(QWidget):

    def __init__(self):
        super().__init__()
        self.TCClist = ['A', 'B', 'C', 'D', 'E']
        self.TCClist_data = ['1', '2', '3', '4', '5']

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
                #print(item)

    def load_ReclosersDatabase(self):
        databaseRecloserdict = {}
        databaseRecloser = self.OpenDSS.getRecloserList()
        # Se trocar de subestação
        try:
            for item in databaseRecloser:
                for item2 in self.RecloserDataInfo:
                    if item.split(" MonitoredObj=")[0].split("New Recloser.")[1] == item2["Name"]:
                        self.flag = True
                        print(f' Flag 1 : {self.flag}')
                        return
                    else:
                        self.flag = False
                        print(f' Flag 2 : {self.flag}')
        except:
            pass

        if self.AddRecloserDataInfo:
            self.flag = True
            print(f' Flag 3 : {self.flag}')

        if not self.flag:
            self.loadDatabaseFlag = False
            self.RecloserDataInfo.clear()
            self.AddRecloserDataInfo.clear()
            print(f' Flag 4 : {self.flag}')


        # Se estiver vazio.
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
                    print(f' Flag 5 : {self.flag}')

            print(f' Flag 6 : {self.flag}')
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
