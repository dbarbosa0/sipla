from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg

class C_Insert_Monitor_Dialog(QDialog): ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Monitor Insert"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.Monitors = []

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ###
        ## GroupBox Medidores
        self.Monitor_GroupBox_MEnergy = QGroupBox("Monitores de Energia")
        self.Monitor_GroupBox_MEnergy_Label = QLabel("Monitores Existentes")
        self.Monitor_GroupBox_MEnergy_ComboBox = QComboBox()

        # Layout do GroupBox Medidores
        self.Monitor_GroupBox_MEnergy_Layout = QGridLayout()
        self.Monitor_GroupBox_MEnergy_Layout.addWidget(self.Monitor_GroupBox_MEnergy_Label, 0, 0, 1, 1)
        self.Monitor_GroupBox_MEnergy_Layout.addWidget(self.Monitor_GroupBox_MEnergy_ComboBox, 0, 1, 1, 3)
        self.Monitor_GroupBox_MEnergy.setLayout(self.Monitor_GroupBox_MEnergy_Layout)

        self.Dialog_Layout.addWidget(self.Monitor_GroupBox_MEnergy)

        ##### Btns
        self.Monitor_GroupBox_MEnergy_Remover_Btn = QPushButton("Remover")
        self.Monitor_GroupBox_MEnergy_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Shapes_GroupBox_Remover_Btn.setFixedWidth(80)
        self.Monitor_GroupBox_MEnergy_Remover_Btn.clicked.connect(self.removeMonitor)
        self.Monitor_GroupBox_MEnergy_Layout.addWidget(self.Monitor_GroupBox_MEnergy_Remover_Btn,1,1,1,1)

        self.Monitor_GroupBox_MEnergy_Edit_Btn = QPushButton("Editar")
        self.Monitor_GroupBox_MEnergy_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        #self.Shapes_GroupBox_Edit_Btn.setFixedWidth(80)
        self.Monitor_GroupBox_MEnergy_Edit_Btn.clicked.connect(self.editMonitor)
        self.Monitor_GroupBox_MEnergy_Layout.addWidget(self.Monitor_GroupBox_MEnergy_Edit_Btn,1,2,1,1)

        self.Monitor_GroupBox_MEnergy_Adicionar_Btn = QPushButton("Adicionar")
        self.Monitor_GroupBox_MEnergy_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Shapes_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.Monitor_GroupBox_MEnergy_Adicionar_Btn.clicked.connect(self.addMonitor)
        self.Monitor_GroupBox_MEnergy_Layout.addWidget(self.Monitor_GroupBox_MEnergy_Adicionar_Btn,1,3,1,1)

        #### Energy Meter

        self.Monitor_GroupBox = QGroupBox("Configuração do Monitor de Energia")
        self.Monitor_GroupBox.setVisible(False)
        ## GroupBox opções
        ### Labels New Monitor.Sourcebus
        self.Monitor_Name_Label = QLabel("Nome:")
        self.Monitor_Element_Label = QLabel("Elemento:")
        self.Monitor_Terminal_Label = QLabel("Terminal:")
        self.Monitor_Mode_Label = QLabel("Mode:")
        self.Monitor_Action_Label = QLabel("Action:")
        self.Monitor_Enable_Label = QLabel("Enable:")
        self.Monitor_Ppolar_Label = QLabel("PPolar:")
        self.Monitor_VIPolar_Label = QLabel("VIPolar:")

        ### LineEdits
        self.Monitor_Name = QLineEdit()

        # Comboboxs
        self.modelist_data = ["Voltages and currents", "Powers", "Tap Position", "State Variables",
                              "Flicker level and severity index for voltages", "Solutions Variables",
                              "Capacitor Switching", "Storage state vars", "Wall windings currents",
                              "Losses, watts and var", "All Winding voltage"]
        self.modelist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.Monitor_Element_ComboBox = QComboBox()
        self.Monitor_Element_ComboBox.clear()
        self.Monitor_Terminal_ComboBox = QComboBox()
        self.Monitor_Terminal_ComboBox.addItems(["1", "2"])
        self.Monitor_Mode_ComboBox = QComboBox()
        #self.Monitor_Mode_ComboBox.addItems(modelist_data)
        for index, item in enumerate(self.modelist_data):
            self.Monitor_Mode_ComboBox.addItem(item, self.modelist[index])
        self.Monitor_Action_ComboBox = QComboBox()
        self.Monitor_Action_ComboBox.addItems(["Clear", "Save", "Take", "Process"])
        self.Monitor_Enable_ComboBox = QComboBox()
        self.Monitor_Enable_ComboBox.addItems(["Yes", "No"])
        self.Monitor_Ppolar_ComboBox = QComboBox()
        self.Monitor_Ppolar_ComboBox.addItems(["Yes", "No"])
        self.Monitor_VIPolar_ComboBox = QComboBox()
        self.Monitor_VIPolar_ComboBox.addItems(["Yes", "No"])

        self.Monitor_Element_PushButton = QPushButton(QIcon('img/icon_opendss_pesquisar.png'), str())

        ### Layout
        self.Monitor_Layout = QGridLayout()
        self.Monitor_Layout.addWidget(self.Monitor_Name_Label, 0, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Element_Label, 1, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Terminal_Label, 2, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Mode_Label, 3, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Action_Label, 4, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Enable_Label, 5, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Ppolar_Label, 6, 0, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_VIPolar_Label, 7, 0, 1, 1)

        self.Monitor_Layout.addWidget(self.Monitor_Name, 0, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Element_ComboBox, 1, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Terminal_ComboBox, 2, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Mode_ComboBox, 3, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Action_ComboBox, 4, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Enable_ComboBox, 5, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_Ppolar_ComboBox, 6, 1, 1, 1)
        self.Monitor_Layout.addWidget(self.Monitor_VIPolar_ComboBox, 7, 1, 1, 1)

        
        ###### Botões dos Parâmetros
        self.Monitor_Btns_Layout = QHBoxLayout()
        self.Monitor_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Monitor_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Monitor_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        #self.Monitor_Btns_Cancel_Btn.setFixedWidth(100)
        self.Monitor_Btns_Cancel_Btn.clicked.connect(self.CancelAddEdit)
        self.Monitor_Btns_Layout.addWidget(self.Monitor_Btns_Cancel_Btn)

        self.Monitor_Btns_Ok_Btn = QPushButton("OK")
        self.Monitor_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        #self.Monitor_Btns_Ok_Btn.setFixedWidth(100)
        self.Monitor_Btns_Ok_Btn.clicked.connect(self.AcceptAddEditMonitor)
        self.Monitor_Btns_Layout.addWidget(self.Monitor_Btns_Ok_Btn)
        self.Monitor_Layout.addItem(self.Monitor_Btns_Layout,13, 0, 1, 2)
        ####

        self.Monitor_GroupBox.setLayout(self.Monitor_Layout)

        self.Dialog_Layout.addWidget(self.Monitor_GroupBox)

        ##############################################################################################

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout)

        self.setLayout(self.Dialog_Layout)

        ####
        self.setLayout(self.Dialog_Layout)
        
    def get_Monitor_Name(self):
        return self.Monitor_Name.text()

    def get_ElementMonitor(self):
        return self.Monitor_Element_ComboBox.currentText()

    def get_TerminalMonitor(self):
        return self.Monitor_Terminal_ComboBox.currentText()

    def get_ModeMonitor(self):
        return self.Monitor_Mode_ComboBox.itemData(self.Monitor_Mode_ComboBox.currentIndex())
        #return self.Monitor_Mode_ComboBox.currentText()

    def get_ActionMonitor(self):
        return self.Monitor_Action_ComboBox.currentText()

    def get_EnableMonitor(self):
        return self.Monitor_Enable_ComboBox.currentText()

    def get_PpolarMonitor(self):
        return self.Monitor_Ppolar_ComboBox.currentText()

    def get_VIPolarMonitor(self):
        return self.Monitor_VIPolar_ComboBox.currentText()

    
    def clearMonitorParameters(self):
        self.Monitor_Name.setText("")
        self.Monitor_Element_ComboBox.setCurrentIndex(0)
        self.Monitor_Terminal_ComboBox.setCurrentIndex(0)
        self.Monitor_Mode_ComboBox.setCurrentIndex(0)
        self.Monitor_Action_ComboBox.setCurrentIndex(0)
        self.Monitor_Enable_ComboBox.setCurrentIndex(0)
        self.Monitor_Ppolar_ComboBox.setCurrentIndex(0)
        self.Monitor_VIPolar_ComboBox.setCurrentIndex(0)
        
    def addMonitor(self):
        self.clearMonitorParameters()
        self.Monitor_Name.setEnabled(True)
        self.EnableDisableParameters(True)

    def editMonitor(self):

        if self.Monitor_GroupBox_MEnergy_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Energy Monitor", "Pelo menos um Energy Monitor deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            self.clearMonitorParameters()

            for ctd in self.Monitors:
                if ctd["Name"] == self.Monitor_GroupBox_MEnergy_ComboBox.currentText():
                    self.Monitor_Name.setText(ctd["Name"])
                    self.Monitor_Element_ComboBox.setCurrentText(ctd["Element"])
                    self.Monitor_Terminal_ComboBox.setCurrentText(ctd["Terminal"])
                    self.Monitor_Mode_ComboBox.setCurrentIndex(int(ctd["Mode"]))
                    self.Monitor_Action_ComboBox.setCurrentText(ctd["Action"])
                    self.Monitor_Enable_ComboBox.setCurrentText(ctd["Enable"])
                    self.Monitor_Ppolar_ComboBox.setCurrentText(ctd["Ppolar"])
                    self.Monitor_VIPolar_ComboBox.setCurrentText(ctd["VIpolar"])

            self.Monitor_Name.setEnabled(False)
            self.EnableDisableParameters(True)
        
    def removeMonitor(self):
        
        for ctd in self.Monitors:
            if ctd["Name"] == self.Monitor_GroupBox_MEnergy_ComboBox.currentText():
                self.Monitors.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Energy Monitor", "Energy Monitor " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()

        self.updateDialog()
                
    def AcceptAddEditMonitor(self): ## Dá para otimizar e muito // Somente um teste
        
        Monitor = {}
        Monitor["Name"] = self.get_Monitor_Name()
        Monitor["Element"] = self.get_ElementMonitor()
        Monitor["Terminal"] = self.get_TerminalMonitor()
        Monitor["Mode"] = self.get_ModeMonitor()
        Monitor["Action"] = self.get_ActionMonitor()
        Monitor["Enable"] = self.get_EnableMonitor()
        Monitor["Ppolar"] = self.get_PpolarMonitor()
        Monitor["VIpolar"] = self.get_VIPolarMonitor()

        if self.Monitor_Name.isEnabled():
            ctdExist = False
            for ctd in self.Monitors:
                if ctd["Name"] == Monitor["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.Monitors.append(Monitor)
                QMessageBox(QMessageBox.Information, "Energy Monitor", "Energy Monitor " + Monitor["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Energy Monitor",
                            "Energy Monitor" + Monitor["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.Monitors:
                if ctd["Name"] == Monitor["Name"]:
                    ctd["Element"] = Monitor["Element"]
                    ctd["Terminal"] = Monitor["Terminal"]
                    ctd["Mode"] = Monitor["Mode"]
                    ctd["Action"] = Monitor["Action"]
                    ctd["Enable"] = Monitor["Enable"]
                    ctd["Ppolar"] = Monitor["Ppolar"]
                    ctd["VIpolar"] = Monitor["VIpolar"]

                    QMessageBox(QMessageBox.Information, "Energy Monitor",
                                "Energy Monitor" + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()
        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def CancelAddEdit(self):
        self.clearMonitorParameters()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):

        if bool:
            self.Monitor_GroupBox.setVisible(True)
            self.Monitor_GroupBox_MEnergy.setEnabled(False)
            self.Dialog_Btns_Ok_Btn.setEnabled(False)
            self.Dialog_Btns_Cancel_Btn.setEnabled(False)
        else:
            self.Monitor_GroupBox.setVisible(False)
            self.Monitor_GroupBox_MEnergy.setEnabled(True)
            self.Dialog_Btns_Ok_Btn.setEnabled(True)
            self.Dialog_Btns_Cancel_Btn.setEnabled(True)


    def Accept(self):
        self.OpenDSS.Monitors = self.Monitors
        self.close()
            
    def updateDialog(self):
        self.Monitor_GroupBox_MEnergy_ComboBox.clear()

        for ctd in self.Monitors:
            self.Monitor_GroupBox_MEnergy_ComboBox.addItem(ctd["Name"])

        self.Monitor_Element_ComboBox.clear()
        #self.Monitor_Element_ComboBox.addItems(self.OpenDSS.getAllNamesElements())
        self.Monitor_Element_ComboBox.addItems(self.OpenDSS.getBusList())


