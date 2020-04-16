from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QPlainTextEdit, QWidget, QLineEdit, QPushButton, QHBoxLayout

from PyQt5.QtCore import Qt

import class_opendss_conn


class C_Insert_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Insert"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"


        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(500, 200)

        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ###### Tabs
        self.TabWidget = QTabWidget()
        self.TabEnergyMeter = EnergyMeter()  # QWidget
        self.TabMonitor = Monitor()  # QWidget
        self.TabWidget.addTab(self.TabEnergyMeter, QIcon('img/icon_opendss_energymeter.png'), "Medidor")
        self.TabWidget.addTab(self.TabMonitor, QIcon('img/icon_opendss_monitor.png'), "Monitor")
        self.Dialog_Layout.addWidget(self.TabWidget)

        self.setLayout(self.Dialog_Layout)

class EnergyMeter(QWidget):
    def __init__(self):
        super().__init__()

        self.acces_energymeter = class_opendss_conn.C_OpenDSSDirect_Conn()

        self.InitUIEnergyMeter()

    def InitUIEnergyMeter(self):
        ## GroupBox Medidores
        self.EnergyMeter_GroupBox = QGroupBox("Medidores de Energia ")

        self.EnergyMeter_GroupBox_Ver_PushButton = QPushButton(QIcon('img/icon_opendss_atualizar.png'), str())
        self.EnergyMeter_GroupBox_Ver_PushButton.setFixedWidth(25)
        self.EnergyMeter_GroupBox_Ver_PushButton.clicked.connect(self.get_EnergyMeter_AllBusNames)

        self.EnergyMeter_GroupBox_ComboBox = QComboBox()

        self.EnergyMeter_GroupBox_Edit_Pushbutton = QPushButton("Editar")
        self.EnergyMeter_GroupBox_Edit_Pushbutton.setFixedWidth(50)

        self.EnergyMeter_GroupBox_New_Pushbutton = QPushButton("Novo")
        self.EnergyMeter_GroupBox_New_Pushbutton.setFixedWidth(50)
        self.EnergyMeter_GroupBox_New_Pushbutton.clicked.connect(self.exec_Meters_OpenDSS)

        # Layout do GroupoBox
        self.EnergyMeter_GroupBox_Layout = QGridLayout()
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_Ver_PushButton, 0, 1, 1, 1)
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_ComboBox, 0, 0, 1, 1)
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_Edit_Pushbutton, 0, 2, 1, 1)
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_New_Pushbutton, 0, 3, 1, 1)

        # Layout do GroupoBox
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.EnergyMeter_GroupBox)


        self.EnergyMeter_GroupBox.setLayout(self.EnergyMeter_GroupBox_Layout)


        self.setLayout(self.Tab_layout)


    def get_EnergyMeter_AllBusNames_(self):
        self.EnergyMeter_GroupBox_ComboBox.clear()
        self.EnergyMeter_GroupBox_ComboBox.addItems(self.acces_energymeter.EnergyMeter_AllNames())


    def get_EnergyMeter_AllBusNames(self):
        if len(self.acces_energymeter.EnergyMeter_AllNames()) == 0:
            self.EnergyMeter_GroupBox_ComboBox.clear()
            self.EnergyMeter_GroupBox_ComboBox.addItems(["Nenhum"])
        else:
            self.EnergyMeter_GroupBox_ComboBox.clear()
            self.EnergyMeter_GroupBox_ComboBox.addItems(self.acces_energymeter.EnergyMeter_AllNames())


    def exec_Meters_OpenDSS(self):
        self.NewEnergyMetr_Dialog = NewEnergyMeter_Dialog()
        self.NewEnergyMetr_Dialog.show()

class NewEnergyMeter_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.titleWindow = "New EnergyMeter"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(500, 500)

        self.NewEnergyMeter_Layout = QVBoxLayout() #Layout da Dialog

        ###### Tabs
        self.NewMeterTabWidget = QTabWidget()
        self.TabEnergyMeter = NewEnergyMeter()
        self.NewMeterTabWidget.addTab(self.TabEnergyMeter, QIcon('img/icon_opendss_energymeter.png'), "Novo Medidor")
        self.NewEnergyMeter_Layout.addWidget(self.NewMeterTabWidget)

        ##### Botões

        self.NewEnergyMeter_Dialog_Btns_Layout = QHBoxLayout()
        self.NewEnergyMeter_Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.NewEnergyMeter_Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.NewEnergyMeter_Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.NewEnergyMeter_Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.NewEnergyMeter_Dialog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.NewEnergyMeter_Dialog_Btns_Layout.addWidget(self.NewEnergyMeter_Dialog_Btns_Cancel_Btn)

        self.NewEnergyMeter_Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.NewEnergyMeter_Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.NewEnergyMeter_Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.NewEnergyMeter_Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.NewEnergyMeter_Dialog_Btns_Layout.addWidget(self.NewEnergyMeter_Dialog_Btns_Ok_Btn)


        self.NewEnergyMeter_Layout.addLayout(self.NewEnergyMeter_Dialog_Btns_Layout, 0)

        self.setLayout(self.NewEnergyMeter_Layout)

    def Accept(self):
        self.TabEnergyMeter.get_RunNewEnergyMeter()

        self.close()



class NewEnergyMeter(QWidget):
    def __init__(self):
        super().__init__()

        self.acces_energymeter = class_opendss_conn.C_OpenDSSDirect_Conn()
        self.InitUINewEnergyMeter()

    def InitUINewEnergyMeter(self):
        self.Insert_EnergyMeter_GroupBox = QGroupBox(" Novo Medidor")

        ### Labels
        self.Insert_EnergyMeter_GroupBox_Name_Label = QLabel("Nome:")
        self.Insert_EnergyMeter_GroupBox_Element_Label = QLabel("Elemento:")
        self.Insert_EnergyMeter_GroupBox_Terminal_Label = QLabel("Terminal:")
        self.Insert_EnergyMeter_GroupBox_3phaseLosses_Label = QLabel("3phaseLosses:")
        self.Insert_EnergyMeter_GroupBox_LineLosses_Label = QLabel("LineLosses:")
        self.Insert_EnergyMeter_GroupBox_Losses_Label = QLabel("Losses:")
        self.Insert_EnergyMeter_GroupBox_SeqLosses_Label = QLabel("SeqLosses:")
        self.Insert_EnergyMeter_GroupBox_VbaseLosses_Label = QLabel("VbaseLosses:")
        self.Insert_EnergyMeter_GroupBox_XfmrLosses_Label = QLabel("XfmrLosses:")
        self.Insert_EnergyMeter_GroupBox_LocalOnly_Label = QLabel("LocalOnly:")
        self.Insert_EnergyMeter_GroupBox_PhaseVoltageReport_Label = QLabel("PhaseVoltageReport:")
        self.Insert_EnergyMeter_GroupBox_Enabled_Label = QLabel("Enabled:")
        self.Insert_EnergyMeter_GroupBox_Action_Label = QLabel("Action:")

        ### LineEdits
        self.Insert_EnergyMeter_GroupBox_Name_LineEdit = QLineEdit()

        #Comboboxs
        self.Insert_EnergyMeter_GroupBox_Element_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Element_ComboBox.clear()
        self.Insert_EnergyMeter_GroupBox_Element_ComboBox.addItems(["Pesquisar"])
        self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox.addItems(["1","2"])
        self.Insert_EnergyMeter_GroupBox_3phaseLosses_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_3phaseLosses_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_LineLosses_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_LineLosses_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_Losses_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Losses_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_SeqLosses_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_SeqLosses_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_VbaseLosses_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_VbaseLosses_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_XfmrLosses_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_XfmrLosses_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_LocalOnly_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_LocalOnly_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_PhaseVoltageReport_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_PhaseVoltageReport_ComboBox.addItems(["Yes","No"])
        self.Insert_EnergyMeter_GroupBox_Action_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Action_ComboBox.addItems(["Clear","Save", "Take", "Zonedump", "Allocate", "Reduce"])
        self.Insert_EnergyMeter_GroupBox_Enabled_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Enabled_ComboBox.addItems(["Yes","No"])

        self.Insert_EnergyMeter_GroupBox_Element_PushButton = QPushButton(QIcon('img/icon_opendss_pesquisar.png'), str())
        #self.Insert_EnergyMeter_GroupBox_Element_PushButton.clicked.connect(self.get_EnergyMeter_AllElementNames)
        self.Insert_EnergyMeter_GroupBox_Element_PushButton.clicked.connect(self.get_RunNewEnergyMeter)

        ### Layout
        self.Insert_EnergyMeter_GroupBox_Layout = QGridLayout()
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Name_Label, 0, 0, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Element_Label, 1, 0, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Terminal_Label, 2, 0, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_3phaseLosses_Label,3,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_LineLosses_Label,4,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Losses_Label,5,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_SeqLosses_Label,6,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_VbaseLosses_Label,7,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_XfmrLosses_Label,8,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_LocalOnly_Label,9,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_PhaseVoltageReport_Label,10,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Enabled_Label,11,0,1,1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Action_Label,12,0,1,1)


        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Name_LineEdit, 0, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Element_ComboBox, 1, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox, 2, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_3phaseLosses_ComboBox, 3, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_LineLosses_ComboBox, 4, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Losses_ComboBox, 5, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_SeqLosses_ComboBox, 6, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_VbaseLosses_ComboBox, 7, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_XfmrLosses_ComboBox, 8, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_LocalOnly_ComboBox, 9, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_PhaseVoltageReport_ComboBox, 10, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Enabled_ComboBox, 11, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Action_ComboBox, 12, 1, 1, 1)

        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Element_PushButton, 1, 2, 1, 1)


#        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Inserir_PushButton, 3, 0, 1,1)

        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.Insert_EnergyMeter_GroupBox)
        self.Insert_EnergyMeter_GroupBox.setLayout(self.Insert_EnergyMeter_GroupBox_Layout)

        self.setLayout(self.Tab_layout)


    def get_EnergyMeter_AllElementNames(self):
        if len(self.acces_energymeter.EnergyMeter_AllElementNames()) == 0:
            self.Insert_EnergyMeter_GroupBox_Element_ComboBox.clear()
            self.Insert_EnergyMeter_GroupBox_Element_ComboBox.addItems(["Nenhum"])
        else:
            self.Insert_EnergyMeter_GroupBox_Element_ComboBox.clear()
            self.Insert_EnergyMeter_GroupBox_Element_ComboBox.addItems(self.acces_energymeter.EnergyMeter_AllElementNames())

    # Métodos Set Variáveis

    def get_NameEnergyMeter(self):
        self.NameEnergyMeter = self.Insert_EnergyMeter_GroupBox_Name_LineEdit.text()
        return self.NameEnergyMeter

    def get_ElementEnergyMeter(self):
        self.ElementEnergyMeter = self.Insert_EnergyMeter_GroupBox_Element_ComboBox.currentText()
        return self.ElementEnergyMeter

    def get_TerminalEnergyMeter(self):
        self.TerminalEnergyMeter = self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox.currentText()
        return self.TerminalEnergyMeter

    def get_3phaseLossesEnergyMeter(self):
        self.treephaseLossesEnergyMeter = self.Insert_EnergyMeter_GroupBox_3phaseLosses_ComboBox.currentText()
        return self.treephaseLossesEnergyMeter

    def get_LineLossesEnergyMeter(self):
        self.LineLossesEnergyMeter = self.Insert_EnergyMeter_GroupBox_LineLosses_ComboBox.currentText()
        return self.LineLossesEnergyMeter

    def get_LossesEnergyMeter(self):
        self.LossesEnergyMeter = self.Insert_EnergyMeter_GroupBox_Losses_ComboBox.currentText()
        return self.LossesEnergyMeter

    def get_SeqLossesEnergyMeter(self):
        self.SeqLossesEnergyMeter = self.Insert_EnergyMeter_GroupBox_SeqLosses_ComboBox.currentText()
        return self.SeqLossesEnergyMeter

    def get_VbaseLossesEnergyMeter(self):
        self.VbaseLossesEnergyMeter = self.Insert_EnergyMeter_GroupBox_VbaseLosses_ComboBox.currentText()
        return self.VbaseLossesEnergyMeter

    def get_XfmrLossesEnergyMeter(self):
        self.XfmrLossesEnergyMeter = self.Insert_EnergyMeter_GroupBox_XfmrLosses_ComboBox.currentText()
        return self.XfmrLossesEnergyMeter

    def get_LocalOnlyEnergyMeter(self):
        self.LocalOnlyEnergyMeter = self.Insert_EnergyMeter_GroupBox_LocalOnly_ComboBox.currentText()
        return self.LocalOnlyEnergyMeter

    def get_PhaseVoltageReportEnergyMeter(self):
        self.PhaseVoltageReportEnergyMeter = self.Insert_EnergyMeter_GroupBox_PhaseVoltageReport_ComboBox.currentText()
        return self.PhaseVoltageReportEnergyMeter

    def get_ActionEnergyMeter(self):
        self.ActionEnergyMeter = self.Insert_EnergyMeter_GroupBox_Action_ComboBox.currentText()
        return self.ActionEnergyMeter

    def get_EnabledEnergyMeter(self):
        self.EnabledEnergyMeter = self.Insert_EnergyMeter_GroupBox_Enabled_ComboBox.currentText()
        return self.EnabledEnergyMeter


    def get_RunNewEnergyMeter(self):
        self.msg = "New EnergyMeter." + str(self.get_NameEnergyMeter())+" Element="+ str(self.get_ElementEnergyMeter())+ " Terminal=" + str(self.get_TerminalEnergyMeter()) + " 3phaseLosses=" + str(self.get_3phaseLossesEnergyMeter()) + " LineLosses=" + str(self.get_LineLossesEnergyMeter()) + " Losses=" + str(self.get_LossesEnergyMeter()) + " SeqLosses=" + str(self.get_SeqLossesEnergyMeter()) + " VbaseLosse=" + str(self.get_VbaseLossesEnergyMeter()) + " XfmrLosses=" + str(self.get_XfmrLossesEnergyMeter()) + " LocalOnly=" + str(self.get_LocalOnlyEnergyMeter())+ " PhaseVoltageReport=" + str(self.get_PhaseVoltageReportEnergyMeter()) + " Action="+ str(self.get_ActionEnergyMeter())+ " Enabled=" + str( self.get_EnabledEnergyMeter())
        return self.msg




class Monitor(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIMonitor()

    def InitUIMonitor(self):

        ## GroupBox Inserir Monitores
        self.Monitor_GroupBox = QGroupBox("Monitores")