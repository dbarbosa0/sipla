from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton

from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg

class C_ResultsEnergyMeter_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS EnergyMeter Results"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        #self.resize(600, 600)

        ##Layout principal
        self.Dialog_Layout = QGridLayout()

        ##GroupBOX Monitor
        self.EnergyMeter_GroupBox = QGroupBox("Medidores")
        self.EnergyMeter_GroupBox.setMaximumWidth(650)
        self.EnergyMeter_GroupBox_Layout = QVBoxLayout()
        self.EnergyMeter_GroupBox.setLayout(self.EnergyMeter_GroupBox_Layout)

        ##GroupBOx Select
        self.EnergyMeter_Select_GroupBox = QGroupBox("&Configuração")
        self.EnergyMeter_Select_GroupBox.setMaximumWidth(650)
        self.EnergyMeter_Select_GroupBox.setMaximumHeight(80)
        self.EnergyMeter_Select_GroupBox_Label = QLabel("Selecione um medidor:")
        self.EnergyMeter_Select_GroupBox_ComboBox = QComboBox()
        self.EnergyMeter_Select_GroupBox_ComboBox.setMinimumWidth(200)
        self.EnergyMeter_Select_GroupBox_ComboBox.currentIndexChanged.connect(self.clearDialog)


        ##Button
        self.EnergyMeter_Select_Ok_Btn = QPushButton("Ok")
        self.EnergyMeter_Select_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.EnergyMeter_Select_Ok_Btn.setFixedWidth(50)
        self.EnergyMeter_Select_Ok_Btn.clicked.connect(self.Select_monitor_active)

        self.EnergyMeter_Select_GroupBox_Layout = QGridLayout()
        self.EnergyMeter_Select_GroupBox_Layout.addWidget(self.EnergyMeter_Select_GroupBox_Label,0,0,1,1)
        self.EnergyMeter_Select_GroupBox_Layout.addWidget(self.EnergyMeter_Select_GroupBox_ComboBox,0,1,1,1)
        self.EnergyMeter_Select_GroupBox_Layout.addWidget(self.EnergyMeter_Select_Ok_Btn,0,2,1,1)
        self.EnergyMeter_Select_GroupBox.setLayout(self.EnergyMeter_Select_GroupBox_Layout)

        self.TabWidget = QTabWidget()
        self.TabResultsEnergia = ResultsEnergia()
        self.TabResultsLosses = ResultsLosses()
        self.TabWidget.addTab(self.TabResultsEnergia, "Energia")
        self.TabWidget.addTab(self.TabResultsLosses, "Losses")

        ##Adciona os GroupBox ao GroupBox principal
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_Select_GroupBox)
        self.EnergyMeter_GroupBox_Layout.addWidget(self.TabWidget)
        self.Dialog_Layout.addWidget(self.EnergyMeter_GroupBox, 0, 0, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def Select_monitor_active(self):
        self.OpenDSS.setEnergyMeterActive(self.EnergyMeter_Select_GroupBox_ComboBox.currentText())
        #print(self.OpenDSS.getRegisterNames())
        listavalores = self.OpenDSS.getRegisterValues()
        self.TabResultsEnergia.set_info_ResultsEnergia(listavalores)
        self.TabResultsLosses.set_info_ResultsLosses(listavalores)


    def updateDialog(self):
        self.EnergyMeter_Select_GroupBox_ComboBox.clear()
        nEnergyMeter = self.OpenDSS.getAllNamesEnergyMeter()
        self.EnergyMeter_Select_GroupBox_ComboBox.addItems(nEnergyMeter)

    def clearDialog(self):
        ##Energia

        self.TabResultsEnergia.KWh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.Kvarh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.ZonekWh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.Zonekvarh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.MaxkW_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.MaxkVA_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.ZoneMaxkW_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.ZoneMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.OverloadkWhNormal_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.LoadEEN_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.LoadUE_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.GenkWh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.Genkvarh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.GenMaxkW_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsEnergia.GenMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.clear()
        
        ##Losses
        
        self.TabResultsLosses.ZoneLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.LoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.LoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.LineLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.TransformerLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.LineModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.tresphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        self.TabResultsLosses.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.clear()
        

class ResultsLosses(QWidget):
    def __init__(self):
        super().__init__()

        ##GroupBoxRegistros
        self.EnergyMeter_Results_GroupBox = QGroupBox("&Registros")
        self.EnergyMeter_Results_GroupBox.setMaximumWidth(1500)
        ##Labels
        self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_Label = QLabel("Zone Losses kWh:")
        self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_Label = QLabel("Zone Losses kvarh:")
        self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Zone Max kW Losses:")
        self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Zone Max kvar Losses:")
        self.LoadLosseskWh_EnergyMeter_Results_GroupBox_Label = QLabel("Load Losses kWh:")
        self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_Label = QLabel("Load Losses kvarh:")
        self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_Label = QLabel("No Load Losses kWh:")
        self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_Label = QLabel("No Load Losses kvarh:")
        self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Max kW Load Losses:")
        self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Max kW No Load Losses:")
        self.LineLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Line Losses:")
        self.TransformerLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Transformer Losses:")
        self.LineModeLineLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Line Mode Line Losses:")
        self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_Label = QLabel("Zero Mode Line Losses:")
        self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_Label = QLabel("3-phase Line Losses:")
        self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_Label = QLabel("1- and 2-phase Line Losses:")


        ##LineEdit
        self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.LoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.LoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.LoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.LineLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.LineLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.LineLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.TransformerLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.TransformerLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.TransformerLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.LineModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.LineModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.LineModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)

        ###Layout
        self.EnergyMeter_Results_GroupBox_Layout = QGridLayout()
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_Label,0,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_LineEdit,0,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_Label,1,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit,1,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_Label,2,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_LineEdit,2,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_Label,3,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_LineEdit,3,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadLosseskWh_EnergyMeter_Results_GroupBox_Label,4,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit,4,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_Label,5,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit,5,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_Label,6,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit,6,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_Label,7,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit,7,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_Label,8,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_LineEdit,8,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_Label,9,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_LineEdit,9,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LineLosses_EnergyMeter_Results_GroupBox_Label,10,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LineLosses_EnergyMeter_Results_GroupBox_LineEdit,10,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.TransformerLosses_EnergyMeter_Results_GroupBox_Label,11,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.TransformerLosses_EnergyMeter_Results_GroupBox_LineEdit,11,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LineModeLineLosses_EnergyMeter_Results_GroupBox_Label,12,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LineModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit,12,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_Label,13,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit,13,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_Label,14,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit,14,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_Label,15,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit,15,1,1,1)

        self.EnergyMeter_Results_GroupBox.setLayout(self.EnergyMeter_Results_GroupBox_Layout)
        ## Layout da TAB2
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.EnergyMeter_Results_GroupBox)
        self.setLayout(self.Tab_layout)

    def set_info_ResultsLosses(self, listavalores):
        self.ZoneLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[12],4)))
        self.ZoneLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[13],4)))
        self.ZoneMaxkWLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[14],4)))
        self.ZoneMaxkvarLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[15],4)))
        self.LoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[16],4)))
        self.LoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[17],4)))
        self.NoLoadLosseskWh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[18],4)))
        self.NoLoadLosseskvarh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[19], 4)))
        self.MaxkWLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[20],4)))
        self.MaxkWNoLoadLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[21],4)))
        self.LineLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[22],4)))
        self.TransformerLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[23],4)))
        self.LineModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[24],4)))
        self.ZeroModeLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[25],4)))
        self.tresphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[26],4)))
        self.umedoisphaseLineLosses_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[27],4)))


class ResultsEnergia(QWidget):
    def __init__(self):
        super().__init__()

        ##GroupBoxRegistros
        self.EnergyMeter_Results_GroupBox = QGroupBox("&Registros")
        self.EnergyMeter_Results_GroupBox.setMaximumWidth(1500)

        ##Labels
        self.KWh_EnergyMeter_Results_GroupBox_Label = QLabel("kWh:")
        self.Kvarh_EnergyMeter_Results_GroupBox_Label = QLabel("kvarh:")
        self.ZonekWh_EnergyMeter_Results_GroupBox_Label = QLabel("Zone kWh:")
        self.Zonekvarh_EnergyMeter_Results_GroupBox_Label = QLabel("Zone kvarh:")
        self.MaxkW_EnergyMeter_Results_GroupBox_Label = QLabel("Max kW:")
        self.MaxkVA_EnergyMeter_Results_GroupBox_Label = QLabel("Max kVA:")
        self.ZoneMaxkW_EnergyMeter_Results_GroupBox_Label = QLabel("Zone Max kW:")
        self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_Label = QLabel("Zone Max kVA:")
        self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_Label = QLabel("Overload kWh Normal:")
        self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_Label = QLabel("Overload kWh Emerg:")
        self.LoadEEN_EnergyMeter_Results_GroupBox_Label = QLabel("Load EEN:")
        self.LoadUE_EnergyMeter_Results_GroupBox_Label = QLabel("Load UE:")
        self.GenkWh_EnergyMeter_Results_GroupBox_Label = QLabel("Gen kWh:")
        self.Genkvarh_EnergyMeter_Results_GroupBox_Label = QLabel("Gen kvarh:")
        self.GenMaxkW_EnergyMeter_Results_GroupBox_Label = QLabel("Gen Max kW:")
        self.GenMaxkVA_EnergyMeter_Results_GroupBox_Label = QLabel("Gen Max kVA:")

        ##LineEdit
        self.KWh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.KWh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.KWh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.Kvarh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.Kvarh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.Kvarh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZonekWh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZonekWh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZonekWh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.Zonekvarh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.Zonekvarh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.Zonekvarh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.MaxkW_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.MaxkW_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.MaxkW_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.MaxkVA_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.MaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.MaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZoneMaxkW_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZoneMaxkW_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZoneMaxkW_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.LoadEEN_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.LoadEEN_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.LoadEEN_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.LoadUE_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.LoadUE_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.LoadUE_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.GenkWh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.GenkWh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.GenkWh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.Genkvarh_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.Genkvarh_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.Genkvarh_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.GenMaxkW_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.GenMaxkW_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.GenMaxkW_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)
        self.GenMaxkVA_EnergyMeter_Results_GroupBox_LineEdit = QLineEdit()
        self.GenMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setFixedWidth(120)
        self.GenMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setReadOnly(True)


        ###Layout
        self.EnergyMeter_Results_GroupBox_Layout = QGridLayout()
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.KWh_EnergyMeter_Results_GroupBox_Label,0,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.KWh_EnergyMeter_Results_GroupBox_LineEdit,0,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.Kvarh_EnergyMeter_Results_GroupBox_Label,1,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.Kvarh_EnergyMeter_Results_GroupBox_LineEdit,1,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkW_EnergyMeter_Results_GroupBox_Label,2,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkW_EnergyMeter_Results_GroupBox_LineEdit,2,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkVA_EnergyMeter_Results_GroupBox_Label,3,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.MaxkVA_EnergyMeter_Results_GroupBox_LineEdit,3,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZonekWh_EnergyMeter_Results_GroupBox_Label,4,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZonekWh_EnergyMeter_Results_GroupBox_LineEdit,4,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.Zonekvarh_EnergyMeter_Results_GroupBox_Label,5,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.Zonekvarh_EnergyMeter_Results_GroupBox_LineEdit,5,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkW_EnergyMeter_Results_GroupBox_Label,6,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkW_EnergyMeter_Results_GroupBox_LineEdit,6,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_Label,7,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_LineEdit,7,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_Label,8,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_LineEdit,8,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_Label,9,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_LineEdit,9,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadEEN_EnergyMeter_Results_GroupBox_Label,10,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadEEN_EnergyMeter_Results_GroupBox_LineEdit,10,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadUE_EnergyMeter_Results_GroupBox_Label,11,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.LoadUE_EnergyMeter_Results_GroupBox_LineEdit,11,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.GenkWh_EnergyMeter_Results_GroupBox_Label,12,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.GenkWh_EnergyMeter_Results_GroupBox_LineEdit,12,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.Genkvarh_EnergyMeter_Results_GroupBox_Label,13,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.Genkvarh_EnergyMeter_Results_GroupBox_LineEdit,13,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.GenMaxkW_EnergyMeter_Results_GroupBox_Label,14,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.GenMaxkW_EnergyMeter_Results_GroupBox_LineEdit,14,1,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.GenMaxkVA_EnergyMeter_Results_GroupBox_Label,15,0,1,1)
        self.EnergyMeter_Results_GroupBox_Layout.addWidget(self.GenMaxkVA_EnergyMeter_Results_GroupBox_LineEdit,15,1,1,1)

        self.EnergyMeter_Results_GroupBox.setLayout(self.EnergyMeter_Results_GroupBox_Layout)
        ## Layout da TAB1
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.EnergyMeter_Results_GroupBox)
        self.setLayout(self.Tab_layout)


    def set_info_ResultsEnergia(self, listavalores):
        self.KWh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[0],4)))
        self.Kvarh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[1],4)))
        self.MaxkW_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[2],4)))
        self.MaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[3],4)))
        self.ZonekWh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[4],4)))
        self.Zonekvarh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[5],4)))
        self.ZoneMaxkW_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[6],4)))
        self.ZoneMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[7],4)))
        self.OverloadkWhNormal_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[8],4)))
        self.OverloadkWhEmerg_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[9],4)))
        self.LoadEEN_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[10],4)))
        self.LoadUE_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[11],4)))
        self.GenkWh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[28],4)))
        self.Genkvarh_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[29],4)))
        self.GenMaxkW_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[30],4)))
        self.GenMaxkVA_EnergyMeter_Results_GroupBox_LineEdit.setText(str(round(listavalores[31],4)))
