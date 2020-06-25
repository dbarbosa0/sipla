import csv

import pyqtgraph
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QComboBox, QLineEdit, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import unidecode

import opendss.class_conn
import opendss.class_opendss
import config as cfg


class Relay(QWidget):

    def __init__(self):
        super().__init__()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Relay = EditRelay(self)
        self.RelaySettings_GroupBox = QGroupBox('Selecionar Relé')
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
        self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_Relay.removeRelay)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        # self.Edit_Btn.setFixedWidth(80)
        self.Edit_Btn.clicked.connect(self.Edit_Relay.editRelay(self.RelaySelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.Add_Btn.setFixedWidth(80)
        self.Add_Btn.clicked.connect(self.Edit_Relay.addRelay())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.RelaySettings_GroupBox.setLayout(self.RelaySettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.RelaySettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_RelayInfo(self):
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
                self.Edit_Relay.UnderVoltCurve_ComboBox.setCurrentText(item["Undervoltcurve"])
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
        except IndexError:
            pass

        # Caso algum Relay tenha sido adicionado
        if self.AddRelayDataInfo:
            self.flag = True

        # Caso não haja Relayes adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.RelayDataInfo.clear()
            self.AddRelayDataInfo.clear()

        # Caso a lista de Relays esteja vazia:
        if not self.RelayDataInfo:
            for item in databaseRelay:
                databaseRelaydict["Device"] = 'Relay'
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
                databaseRelaydict["Undervoltcurve"] = ''

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
        self.TesteDialog_Layout = QHBoxLayout()
        self.RelayInfo()
        self.Btns()
        self.setLayout(self.TesteDialog_Layout)
        self.PlotState = True

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

        self.GroundCurveList = ['', 'a', 'b', 'c', 'd']
        self.GroundCurve_ComboBox = QComboBox()
        self.GroundCurve_ComboBox.setMaximumWidth(150)
        self.GroundCurve_ComboBox_Label = QLabel("Ground Curve")
        for index, item in enumerate(self.GroundCurveList):
            self.GroundCurve_ComboBox.addItem(item, item)

        self.GroundTrip_LineEdit = QLineEdit()
        self.GroundTrip_LineEdit.setMaximumWidth(50)
        self.GroundTrip_LineEdit.setPlaceholderText("1.0")
        self.GroundTrip_LineEdit_Label = QLabel("Multiplier")
        self.GroundTrip_LineEdit_Label.setAlignment(Qt.AlignRight)

        self.GroundTimeDial_LineEdit = QLineEdit()
        self.GroundTimeDial_LineEdit.setMaximumWidth(50)
        self.GroundTimeDial_LineEdit.setPlaceholderText("1.0")
        self.GroundTimeDial_LineEdit_Label = QLabel("Time dial")
        self.GroundTimeDial_LineEdit_Label.setAlignment(Qt.AlignRight)

        self.PhaseCurveList = ['', 'a', 'b', 'c', 'd']
        self.PhaseCurve_ComboBox = QComboBox()
        self.PhaseCurve_ComboBox.setMaximumWidth(150)
        self.PhaseCurve_ComboBox_Label = QLabel("Phase Curve")
        for index, item in enumerate(self.PhaseCurveList):
            self.PhaseCurve_ComboBox.addItem(item, item)

        self.PhaseTrip_LineEdit = QLineEdit()
        self.PhaseTrip_LineEdit.setMaximumWidth(50)
        self.PhaseTrip_LineEdit.setPlaceholderText("1.0")
        self.PhaseTrip_LineEdit_Label = QLabel("Multiplier")
        self.PhaseTrip_LineEdit_Label.setAlignment(Qt.AlignRight)

        self.PhaseTimeDial_LineEdit = QLineEdit()
        self.PhaseTimeDial_LineEdit.setMaximumWidth(50)
        self.PhaseTimeDial_LineEdit.setPlaceholderText("1.0")
        self.PhaseTimeDial_LineEdit_Label = QLabel("Time dial")
        self.PhaseTimeDial_LineEdit_Label.setAlignment(Qt.AlignRight)

        self.OverVoltCurveList = ['', 'a', 'b', 'c', 'd']
        self.OverVoltCurve_ComboBox = QComboBox()
        self.OverVoltCurve_ComboBox.setMaximumWidth(150)
        self.OverVoltCurve_ComboBox_Label = QLabel("OverVolt Curve")
        for index, item in enumerate(self.OverVoltCurveList):
            self.OverVoltCurve_ComboBox.addItem(item, item)

        self.OverVoltTrip_LineEdit = QLineEdit()
        self.OverVoltTrip_LineEdit.setMaximumWidth(50)
        self.OverVoltTrip_LineEdit.setPlaceholderText("1.0")
        self.OverVoltTrip_LineEdit_Label = QLabel("Multiplier")
        self.OverVoltTrip_LineEdit_Label.setAlignment(Qt.AlignRight)

        self.UnderVoltCurveList = ['', 'a', 'b', 'c', 'd']
        self.UnderVoltCurve_ComboBox = QComboBox()
        self.UnderVoltCurve_ComboBox.setMaximumWidth(150)
        self.UnderVoltCurve_ComboBox_Label = QLabel("UnderVolt Curve")
        for index, item in enumerate(self.UnderVoltCurveList):
            self.UnderVoltCurve_ComboBox.addItem(item, item)

        self.UnderVoltTrip_LineEdit = QLineEdit()
        self.UnderVoltTrip_LineEdit.setMaximumWidth(50)
        self.UnderVoltTrip_LineEdit.setPlaceholderText("1.0")
        self.UnderVoltTrip_LineEdit_Label = QLabel("Multiplier")
        self.UnderVoltTrip_LineEdit_Label.setAlignment(Qt.AlignRight)

        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundCurve_ComboBox_Label, 0, 0, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundCurve_ComboBox, 0, 1, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit_Label, 0, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit, 0, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTimeDial_LineEdit_Label, 0, 4, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.GroundTimeDial_LineEdit, 0, 5, 1, 1)

        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseCurve_ComboBox_Label, 4, 0, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseCurve_ComboBox, 4, 1, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit_Label, 4, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit, 4, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTimeDial_LineEdit_Label, 4, 4, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.PhaseTimeDial_LineEdit, 4, 5, 1, 1)

        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltCurve_ComboBox_Label, 6, 0, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltCurve_ComboBox, 6, 1, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltTrip_LineEdit_Label, 6, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.OverVoltTrip_LineEdit, 6, 3, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltCurve_ComboBox_Label, 8, 0, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltCurve_ComboBox, 8, 1, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltTrip_LineEdit_Label, 8, 2, 1, 1)
        self.TCCCurves_Relay_GroupBox_Layout.addWidget(self.UnderVoltTrip_LineEdit, 8, 3, 1, 1)

        self.TCCCurves_Relay_GroupBox.setLayout(self.TCCCurves_Relay_GroupBox_Layout)

        self.graphWidget = pyqtgraph.PlotWidget()
        self.graphWidget.setHidden(True)


        self.Dialog_Layout.addWidget(self.Edit_Relay_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Relay_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Relay_GroupBox)

        self.TesteDialog_Layout.addLayout(self.Dialog_Layout)
        self.TesteDialog_Layout.addWidget(self.graphWidget)


    def viewCurve(self):
        dataCSV = {}
        pointsXList = []
        pointsYList = []
        groundmult = self.GroundTrip_LineEdit.text()
        tdground = self.GroundTimeDial_LineEdit.text()
        phasemult = self.PhaseTrip_LineEdit.text()
        tdphase = self.PhaseTimeDial_LineEdit.text()
        overvoltmult = self.OverVoltTrip_LineEdit.text()
        undervoltmult = self.UnderVoltTrip_LineEdit.text()

        # Limpando
        self.graphWidget.clear()
        self.graphWidget.setBackground('w')
        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Tempo (s)', color='blue', size=20)
        self.graphWidget.setLabel('bottom', 'Corrente (A)', color='blue', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLogMode(x=True, y=True)
        pen = pyqtgraph.mkPen(color = 'b')
        self.PlotState = not self.PlotState

        if not self.PlotState:
            fname = "./prodist/tcapelofu.csv".replace("/","\\")

            with open(fname, 'r', newline='') as file:
                csv_reader_object = csv.reader(file)
                # if csv.Sniffer().has_header:
                name_col = next(csv_reader_object)

                for row in name_col:
                    dataCSV[row] = []

                for row in csv_reader_object:  ##Varendo todas as linhas
                    for ndata in range(0, len(name_col)):  ## Varendo todas as colunas
                        dataCSV[name_col[ndata]].append(row[ndata])

                # Phase Delayed
                if get_combobox(self.GroundCurve_ComboBox):
                    try:
                        for key, values in dataCSV.items():
                            if key == get_combobox(self.GroundCurve_ComboBox):
                                for value in values:
                                    if value:
                                        if groundmult == '':
                                            m = float(value.split(';')[0])
                                        else:
                                            m = float(value.split(';')[0])*float(groundmult)

                                        if tdground == '':
                                            t = float(value.split(';')[1])
                                        else:
                                            t = float(value.split(';')[1])*float(tdground)
                                        pointsXList.append(m)
                                        pointsYList.append(t)

                                name = 'Curva ' + key

                        print(pointsXList,pointsYList)
                        bluergb = (0, 0, 255, 255)
                        self.graphWidget.plot(pointsXList, pointsYList, name=name, pen=pen, symbol='o', symbolSize=10, symbolBrush=bluergb)
                    except ValueError:
                        QMessageBox(QMessageBox.Warning, "Curva TCC - Fusível", "Erro ao carregar curva" , QMessageBox.Ok).exec()
                        self.PlotState = not self.PlotState
                # Phase Fast
                if get_combobox(self.PhaseCurve_ComboBox):
                    try:
                        for key, values in dataCSV.items():
                            if key == get_combobox(self.PhaseCurve_ComboBox):
                                for value in values:
                                    if value:
                                        if phasemult == '':
                                            m = float(value.split(';')[0])
                                        else:
                                            m = float(value.split(';')[0])*float(phasemult)

                                        if tdphase == '':
                                            t = float(value.split(';')[1])
                                        else:
                                            t = float(value.split(';')[1])*float(tdphase)
                                        pointsXList.append(m)
                                        pointsYList.append(t)

                                name = 'Curva ' + key

                        print(pointsXList,pointsYList)
                        redrgb = (255, 0, 0, 255)
                        self.graphWidget.plot(pointsXList, pointsYList, name=name, pen=pen, symbol='o', symbolSize=10, symbolBrush=redrgb)
                    except ValueError:
                        QMessageBox(QMessageBox.Warning, "Curva TCC - Fusível", "Erro ao carregar curva" , QMessageBox.Ok).exec()
                        self.PlotState = not self.PlotState

                # Ground Delay
                if get_combobox(self.OverVoltCurve_ComboBox):
                    try:
                        for key, values in dataCSV.items():
                            if key == get_combobox(self.OverVoltCurve_ComboBox):
                                for value in values:
                                    if value:
                                        if overvoltmult == '':
                                            m = float(value.split(';')[0])
                                        else:
                                            m = float(value.split(';')[0])*float(overvoltmult)

                                        t = float(value.split(';')[1])
                                        pointsXList.append(m)
                                        pointsYList.append(t)

                                name = 'Curva ' + key

                        print(pointsXList,pointsYList)
                        greenrgb = (0, 255, 0, 255)
                        self.graphWidget.plot(pointsXList, pointsYList, name=name, pen=pen, symbol='o', symbolSize=10, symbolBrush=greenrgb)
                    except ValueError:
                        QMessageBox(QMessageBox.Warning, "Curva TCC - Fusível", "Erro ao carregar curva" , QMessageBox.Ok).exec()
                        self.PlotState = not self.PlotState

                # Ground Fast
                if get_combobox(self.UnderVoltCurve_ComboBox):
                    try:
                        for key, values in dataCSV.items():
                            if key == get_combobox(self.UnderVoltCurve_ComboBox):
                                for value in values:
                                    if value:
                                        if undervoltmult == '':
                                            m = float(value.split(';')[0])
                                        else:
                                            m = float(value.split(';')[0])*float(undervoltmult)

                                        t = float(value.split(';')[1])

                                        pointsXList.append(m)
                                        pointsYList.append(t)

                                name = 'Curva ' + key

                        print(pointsXList,pointsYList)
                        yellowrgb = (0, 255, 255, 255)
                        self.graphWidget.plot(pointsXList, pointsYList, name=name, pen=pen, symbol='o', symbolSize=10, symbolBrush=yellowrgb)
                    except ValueError:
                        QMessageBox(QMessageBox.Warning, "Curva TCC - Fusível", "Erro ao carregar curva" , QMessageBox.Ok).exec()
                        self.PlotState = not self.PlotState

        if not self.PlotState:
             self.setFixedWidth(900)
             self.move(325,0)
        else:
            self.setFixedWidth(440)
            self.move(860, 0)
        self.graphWidget.setHidden(self.PlotState)


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

        self.AddTCC_Btn = QPushButton("Visualizar TCC")
        self.AddTCC_Btn.setMaximumWidth(150)
        self.AddTCC_Btn.clicked.connect(self.viewCurve)

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
            self.Relay_parent.load_RelayInfo()
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

        self.datainfo["Device"] = 'Relay'
        self.datainfo["Name"] = get_lineedit(self.RelayName_LineEdit)
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
        self.datainfo["Undervoltcurve"] = get_combobox(self.UnderVoltCurve_ComboBox)
        self.datainfo["UnderTrip"] = get_lineedit(self.UnderVoltTrip_LineEdit)

    def AcceptAddEditRelay(self):  # Dá para otimizar e muito // Somente um teste

        datainfo = {"Device": 'Relay',
                    "Name": unidecode.unidecode(get_lineedit(self.RelayName_LineEdit).replace(" ", "_")),
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
                    "Undervoltcurve": get_combobox(self.UnderVoltCurve_ComboBox),
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
                    ctd["Undervoltcurve"] = datainfo["Undervoltcurve"]
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


def get_lineedit(lineedit):
    return lineedit.text()


def get_combobox(combobox):
    return str(combobox.itemData(combobox.currentIndex()))