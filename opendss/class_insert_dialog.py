from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from PyQt5.QtCore import Qt

import opendss.class_opendss

class C_Insert_Dialog(QDialog): ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Insert"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()

        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ###### Tabs
        self.TabWidget = QTabWidget()
        ## Energy Meter
        self.TabEnergyMeter = EnergyMeter()  # QWidget
        ## Monitor
        self.TabMonitor = Monitor()  # QWidget
        self.TabWidget.addTab(self.TabEnergyMeter, QIcon('img/icon_opendss_energymeter.png'), "Medidor") # icone tab1
        self.TabWidget.addTab(self.TabMonitor, QIcon('img/icon_opendss_monitor.png'), "Monitor") # icone tab2
        self.Dialog_Layout.addWidget(self.TabWidget)

        self.setLayout(self.Dialog_Layout)


class EnergyMeter(QWidget): # Classe widget define a configuração visual da classe principal
    def __init__(self):

        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUIEnergyMeter()

    def InitUIEnergyMeter(self):

        ## GroupBox Medidores
        self.EnergyMeter_GroupBox_MEnergy = QGroupBox("Medidores de Energia")

        self.EnergyMeter_GroupBox_MEnergy_Label = QLabel("Medidores Existentes")
        self.EnergyMeter_GroupBox_MEnergy_ComboBox = QComboBox()

        # Layout do GroupBox Medidores
        self.EnergyMeter_GroupBox_MEnergy_Layout = QGridLayout()
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_Label, 0, 0, 1, 1)
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_ComboBox, 0, 1, 1, 1)

        self.EnergyMeter_GroupBox_MEnergy.setLayout(self.EnergyMeter_GroupBox_MEnergy_Layout)

        ## GroupBox opções
        self.EnergyMeter_Options_GroupBox = QGroupBox()

        #### Layout GroupBox opções
        self.EnergyMeter_Options_GroupBox_Layout = QVBoxLayout()

        ##### TabWidgets
        self.TabWidget = QTabWidget()
        self.TabNewEnergyMeter = EnergyMeter_NewMeters()
        self.TabWidget.addTab(self.TabNewEnergyMeter, "New")
        self.TabEditEnergyMeter = EnergyMeter_EditMeters()
        self.TabWidget.addTab(self.TabEditEnergyMeter, "Edit")
        self.EnergyMeter_Options_GroupBox_Layout.addWidget(self.TabWidget)
        #####
        self.EnergyMeter_Options_GroupBox.setLayout(self.EnergyMeter_Options_GroupBox_Layout)

        # Layout do GroupBox Principal
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.EnergyMeter_GroupBox_MEnergy)
        self.Tab_layout.addWidget(self.EnergyMeter_Options_GroupBox)

        ##### Botão
        ## Btn
        self.EnergyMeter_Ok_Btn = QPushButton("OK")
        self.EnergyMeter_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.EnergyMeter_Ok_Btn.clicked.connect(self.Accept)
        self.Tab_layout.addWidget(self.EnergyMeter_Ok_Btn)

        self.setLayout(self.Tab_layout)

    def Accept(self):

        tab = self.TabWidget.currentIndex()

        if tab == 0:
            self.InsertUpdateEnergyMeter(self.TabNewEnergyMeter,"New")
        elif tab == 1:
            self.InsertUpdateEnergyMeter(self.TabEditEnergyMeter,"Edit")
            
    def InsertUpdateEnergyMeter(self, obj, action):

        energyMeter = obj.get_ElementEnergyMeter()

        if energyMeter == "":
            QMessageBox(QMessageBox.Warning, "Warning Insert", "Selecione um elemento do circuito !",
                        QMessageBox.Ok).exec()
        else:
            msg =  action + " EnergyMeter." + str(obj.get_NameEnergyMeter()) + \
                  " Element=" + str(obj.get_ElementEnergyMeter()) + \
                  " Terminal=" + str(obj.get_TerminalEnergyMeter()) + \
                  " 3phaseLosses=" + str(obj.get_3phaseLossesEnergyMeter()) + \
                  " LineLosses=" + str(obj.get_LineLossesEnergyMeter()) + \
                  " Losses=" + str(obj.get_LossesEnergyMeter()) + \
                  " SeqLosses=" + str(obj.get_SeqLossesEnergyMeter()) + \
                  " VbaseLosse=" + str(obj.get_VbaseLossesEnergyMeter()) + \
                  " XfmrLosses=" + str(obj.get_XfmrLossesEnergyMeter()) + \
                  " LocalOnly=" + str(obj.get_LocalOnlyEnergyMeter()) + \
                  " PhaseVoltageReport=" + str(obj.get_PhaseVoltageReportEnergyMeter()) + \
                  " Action=" + str(obj.get_ActionEnergyMeter()) + \
                  " Enabled=" + str( obj.get_EnabledEnergyMeter())

        self.OpenDSS.exec_OpenDSSRun(msg)

        print(msg)

        self.updateDialog()
            
    def updateDialog(self):
        self.EnergyMeter_GroupBox_MEnergy_ComboBox.clear()
        self.EnergyMeter_GroupBox_MEnergy_ComboBox.addItems(self.OpenDSS.getAllNamesEnergyMeter())
        
        ## New
        self.TabNewEnergyMeter.EnergyMeter_Element_ComboBox.clear()
        self.TabNewEnergyMeter.EnergyMeter_Element_ComboBox.addItems(self.OpenDSS.getAllNamesElements())

        ## Edit
        self.TabEditEnergyMeter.EnergyMeter_Name.clear()
        self.TabEditEnergyMeter.EnergyMeter_Name.addItems(self.OpenDSS.getAllNamesEnergyMeter())
        self.TabEditEnergyMeter.EnergyMeter_Element_ComboBox.clear()
        self.TabEditEnergyMeter.EnergyMeter_Element_ComboBox.addItems(self.OpenDSS.getAllNamesElements())



class EnergyMeter_Meters(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUINewMeters()

    def InitUINewMeters(self):

        ### Labels
        self.EnergyMeter_Name_Label = QLabel("Nome:")
        self.EnergyMeter_Element_Label = QLabel("Elemento:")
        self.EnergyMeter_Terminal_Label = QLabel("Terminal:")
        self.EnergyMeter_3phaseLosses_Label = QLabel("3phaseLosses:")
        self.EnergyMeter_LineLosses_Label = QLabel("LineLosses:")
        self.EnergyMeter_Losses_Label = QLabel("Losses:")
        self.EnergyMeter_SeqLosses_Label = QLabel("SeqLosses:")
        self.EnergyMeter_VbaseLosses_Label = QLabel("VbaseLosses:")
        self.EnergyMeter_XfmrLosses_Label = QLabel("XfmrLosses:")
        self.EnergyMeter_LocalOnly_Label = QLabel("LocalOnly:")
        self.EnergyMeter_PhaseVoltageReport_Label = QLabel("PhaseVoltageReport:")
        self.EnergyMeter_Enabled_Label = QLabel("Enabled:")
        self.EnergyMeter_Action_Label = QLabel("Action:")

        #Comboboxs
        self.EnergyMeter_Element_ComboBox = QComboBox()
        self.EnergyMeter_Element_ComboBox.clear()
        self.EnergyMeter_Terminal_ComboBox = QComboBox()
        self.EnergyMeter_Terminal_ComboBox.addItems(["1","2"])
        self.EnergyMeter_3phaseLosses_ComboBox = QComboBox()
        self.EnergyMeter_3phaseLosses_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_LineLosses_ComboBox = QComboBox()
        self.EnergyMeter_LineLosses_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_Losses_ComboBox = QComboBox()
        self.EnergyMeter_Losses_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_SeqLosses_ComboBox = QComboBox()
        self.EnergyMeter_SeqLosses_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_VbaseLosses_ComboBox = QComboBox()
        self.EnergyMeter_VbaseLosses_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_XfmrLosses_ComboBox = QComboBox()
        self.EnergyMeter_XfmrLosses_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_LocalOnly_ComboBox = QComboBox()
        self.EnergyMeter_LocalOnly_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_PhaseVoltageReport_ComboBox = QComboBox()
        self.EnergyMeter_PhaseVoltageReport_ComboBox.addItems(["Yes","No"])
        self.EnergyMeter_Action_ComboBox = QComboBox()
        self.EnergyMeter_Action_ComboBox.addItems(["Clear","Save", "Take", "Zonedump", "Allocate", "Reduce"])
        self.EnergyMeter_Enabled_ComboBox = QComboBox()
        self.EnergyMeter_Enabled_ComboBox.addItems(["Yes","No"])

        self.EnergyMeter_Element_PushButton = QPushButton(QIcon('img/icon_opendss_pesquisar.png'), str())

        ### Layout
        self.EnergyMeter_Layout = QGridLayout()
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Name_Label, 0, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Element_Label, 1, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Terminal_Label, 2, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_3phaseLosses_Label,3,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_LineLosses_Label,4,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Losses_Label,5,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_SeqLosses_Label,6,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_VbaseLosses_Label,7,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_XfmrLosses_Label,8,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_LocalOnly_Label,9,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_PhaseVoltageReport_Label,10,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Enabled_Label,11,0,1,1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Action_Label,12,0,1,1)

        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Element_ComboBox, 1, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Terminal_ComboBox, 2, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_3phaseLosses_ComboBox, 3, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_LineLosses_ComboBox, 4, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Losses_ComboBox, 5, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_SeqLosses_ComboBox, 6, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_VbaseLosses_ComboBox, 7, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_XfmrLosses_ComboBox, 8, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_LocalOnly_ComboBox, 9, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_PhaseVoltageReport_ComboBox, 10, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Enabled_ComboBox, 11, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Action_ComboBox, 12, 1, 1, 1)

        #####

        self.setLayout(self.EnergyMeter_Layout)

    def get_ElementEnergyMeter(self):
        return self.EnergyMeter_Element_ComboBox.currentText()

    def get_TerminalEnergyMeter(self):
        return self.EnergyMeter_Terminal_ComboBox.currentText()

    def get_3phaseLossesEnergyMeter(self):
        return self.EnergyMeter_3phaseLosses_ComboBox.currentText()

    def get_LineLossesEnergyMeter(self):
        return self.EnergyMeter_LineLosses_ComboBox.currentText()

    def get_LossesEnergyMeter(self):
        return self.EnergyMeter_Losses_ComboBox.currentText()

    def get_SeqLossesEnergyMeter(self):
        return self.EnergyMeter_SeqLosses_ComboBox.currentText()

    def get_VbaseLossesEnergyMeter(self):
        return self.EnergyMeter_VbaseLosses_ComboBox.currentText()

    def get_XfmrLossesEnergyMeter(self):
        return self.EnergyMeter_XfmrLosses_ComboBox.currentText()

    def get_LocalOnlyEnergyMeter(self):
        return self.EnergyMeter_LocalOnly_ComboBox.currentText()

    def get_PhaseVoltageReportEnergyMeter(self):
        return self.EnergyMeter_PhaseVoltageReport_ComboBox.currentText()

    def get_ActionEnergyMeter(self):
        return self.EnergyMeter_Action_ComboBox.currentText()

    def get_EnabledEnergyMeter(self):
        return self.EnergyMeter_Enabled_ComboBox.currentText()



class EnergyMeter_NewMeters(EnergyMeter_Meters):
    def __init__(self):
        super().__init__()

        ### LineEdits
        self.EnergyMeter_Name = QLineEdit()
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Name, 0, 1, 1, 1)

    ## Métodos Set Variáveis
    def get_NameEnergyMeter(self):
        return self.EnergyMeter_Name.text()

class EnergyMeter_EditMeters(EnergyMeter_Meters):
    def __init__(self):
        super().__init__()

        self.EnergyMeter_Name = QComboBox()
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Name, 0, 1, 1, 1)
        
    ## Métodos Set Variáveis
    def get_NameEnergyMeter(self):
        return self.EnergyMeter_Name.currentText()

class Monitor(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIMonitor()

    def InitUIMonitor(self):

        ## GroupBox Inserir Monitores
        self.Monitor_GroupBox = QGroupBox("Monitores")