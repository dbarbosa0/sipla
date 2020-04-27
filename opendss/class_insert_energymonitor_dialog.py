from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg

class C_Insert_EnergyMonitor_Dialog(QDialog): ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Insert"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.EnergyMonitors = []

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ###
        ## GroupBox Medidores
        self.EnergyMonitor_GroupBox_MEnergy = QGroupBox("Monitores de Energia")
        self.EnergyMonitor_GroupBox_MEnergy_Label = QLabel("Monitores Existentes")
        self.EnergyMonitor_GroupBox_MEnergy_ComboBox = QComboBox()

        # Layout do GroupBox Medidores
        self.EnergyMonitor_GroupBox_MEnergy_Layout = QGridLayout()
        self.EnergyMonitor_GroupBox_MEnergy_Layout.addWidget(self.EnergyMonitor_GroupBox_MEnergy_Label, 0, 0, 1, 1)
        self.EnergyMonitor_GroupBox_MEnergy_Layout.addWidget(self.EnergyMonitor_GroupBox_MEnergy_ComboBox, 0, 1, 1, 3)
        self.EnergyMonitor_GroupBox_MEnergy.setLayout(self.EnergyMonitor_GroupBox_MEnergy_Layout)

        self.Dialog_Layout.addWidget(self.EnergyMonitor_GroupBox_MEnergy)

        ##### Btns
        self.EnergyMonitor_GroupBox_MEnergy_Remover_Btn = QPushButton("Remover")
        self.EnergyMonitor_GroupBox_MEnergy_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Shapes_GroupBox_Remover_Btn.setFixedWidth(80)
        self.EnergyMonitor_GroupBox_MEnergy_Remover_Btn.clicked.connect(self.removeEnergyMonitor)
        self.EnergyMonitor_GroupBox_MEnergy_Layout.addWidget(self.EnergyMonitor_GroupBox_MEnergy_Remover_Btn,1,1,1,1)

        self.EnergyMonitor_GroupBox_MEnergy_Edit_Btn = QPushButton("Editar")
        self.EnergyMonitor_GroupBox_MEnergy_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        #self.Shapes_GroupBox_Edit_Btn.setFixedWidth(80)
        self.EnergyMonitor_GroupBox_MEnergy_Edit_Btn.clicked.connect(self.editEnergyMonitor)
        self.EnergyMonitor_GroupBox_MEnergy_Layout.addWidget(self.EnergyMonitor_GroupBox_MEnergy_Edit_Btn,1,2,1,1)

        self.EnergyMonitor_GroupBox_MEnergy_Adicionar_Btn = QPushButton("Adicionar")
        self.EnergyMonitor_GroupBox_MEnergy_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Shapes_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.EnergyMonitor_GroupBox_MEnergy_Adicionar_Btn.clicked.connect(self.addEnergyMonitor)
        self.EnergyMonitor_GroupBox_MEnergy_Layout.addWidget(self.EnergyMonitor_GroupBox_MEnergy_Adicionar_Btn,1,3,1,1)



        #### Energy Meter

        self.EnergyMonitor_GroupBox = QGroupBox("Configuração do Monitor de Energia")
        self.EnergyMonitor_GroupBox.setVisible(False)
        ## GroupBox opções
        ### Labels New Monitor.Sourcebus
        self.EnergyMonitor_Name_Label = QLabel("Nome:")
        self.EnergyMonitor_Element_Label = QLabel("Elemento:")
        self.EnergyMonitor_Terminal_Label = QLabel("Terminal:")
        self.EnergyMonitor_Mode_Label = QLabel("Mode:")
        self.EnergyMonitor_Ppolar_Label = QLabel("Ppolar:")

        ### LineEdits
        self.EnergyMonitor_Name = QLineEdit()

        # Comboboxs
        self.EnergyMonitor_Element_ComboBox = QComboBox()
        self.EnergyMonitor_Element_ComboBox.clear()
        self.EnergyMonitor_Terminal_ComboBox = QComboBox()
        self.EnergyMonitor_Terminal_ComboBox.addItems(["1", "2"])
        self.EnergyMonitor_Mode_ComboBox = QComboBox()
        self.EnergyMonitor_Mode_ComboBox.addItems(["1", "2"])
        self.EnergyMonitor_Ppolar_ComboBox = QComboBox()
        self.EnergyMonitor_Ppolar_ComboBox.addItems(["Yes", "No"])

        self.EnergyMonitor_Element_PushButton = QPushButton(QIcon('img/icon_opendss_pesquisar.png'), str())

        ### Layout
        self.EnergyMonitor_Layout = QGridLayout()
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Name_Label, 0, 0, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Element_Label, 1, 0, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Terminal_Label, 2, 0, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Mode_Label, 3, 0, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Ppolar_Label, 4, 0, 1, 1)

        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Name, 0, 1, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Element_ComboBox, 1, 1, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Terminal_ComboBox, 2, 1, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Mode_ComboBox, 3, 1, 1, 1)
        self.EnergyMonitor_Layout.addWidget(self.EnergyMonitor_Ppolar_ComboBox, 4, 1, 1, 1)

        
        ###### Botões dos Parâmetros
        self.EnergyMonitor_Btns_Layout = QHBoxLayout()
        self.EnergyMonitor_Btns_Layout.setAlignment(Qt.AlignRight)

        self.EnergyMonitor_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.EnergyMonitor_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        #self.EnergyMonitor_Btns_Cancel_Btn.setFixedWidth(100)
        self.EnergyMonitor_Btns_Cancel_Btn.clicked.connect(self.CancelAddEdit)
        self.EnergyMonitor_Btns_Layout.addWidget(self.EnergyMonitor_Btns_Cancel_Btn)

        self.EnergyMonitor_Btns_Ok_Btn = QPushButton("OK")
        self.EnergyMonitor_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        #self.EnergyMonitor_Btns_Ok_Btn.setFixedWidth(100)
        self.EnergyMonitor_Btns_Ok_Btn.clicked.connect(self.AcceptAddEditEnergyMonitor)
        self.EnergyMonitor_Btns_Layout.addWidget(self.EnergyMonitor_Btns_Ok_Btn)
        self.EnergyMonitor_Layout.addItem(self.EnergyMonitor_Btns_Layout,13, 0, 1, 2)
        ####

        self.EnergyMonitor_GroupBox.setLayout(self.EnergyMonitor_Layout)

        self.Dialog_Layout.addWidget(self.EnergyMonitor_GroupBox)

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
        
    def get_EnergyMonitor_Name(self):
        return self.EnergyMonitor_Name.text()

    def get_ElementEnergyMonitor(self):
        return self.EnergyMonitor_Element_ComboBox.currentText()

    def get_TerminalEnergyMonitor(self):
        return self.EnergyMonitor_Terminal_ComboBox.currentText()

    def get_ModeEnergyMonitor(self):
        return self.EnergyMonitor_Mode_ComboBox.currentText()

    def get_PpolarEnergyMonitor(self):
        return self.EnergyMonitor_Ppolar_ComboBox.currentText()

    
    def clearEnergyMonitorParameters(self):
        self.EnergyMonitor_Name.setText("")
        self.EnergyMonitor_Element_ComboBox.setCurrentText("")
        self.EnergyMonitor_Terminal_ComboBox.setCurrentText("")
        self.EnergyMonitor_Mode_ComboBox.setCurrentText("")
        self.EnergyMonitor_Ppolar_ComboBox.setCurrentText("")
        
    def addEnergyMonitor(self):
        self.clearEnergyMonitorParameters()
        self.EnergyMonitor_Name.setEnabled(True)
        self.EnableDisableParameters(True)

    def editEnergyMonitor(self):

        if self.EnergyMonitor_GroupBox_MEnergy_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Energy Monitor", "Pelo menos um Energy Monitor deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            self.clearEnergyMonitorParameters()

            for ctd in self.EnergyMonitors:
                if ctd["Name"] == self.EnergyMonitor_GroupBox_MEnergy_ComboBox.currentText():
                    self.EnergyMonitor_Name.setText(ctd["Name"])
                    self.EnergyMonitor_Element_ComboBox.setCurrentText(ctd["Element"])
                    self.EnergyMonitor_Terminal_ComboBox.setCurrentText(ctd["Terminal"])
                    self.EnergyMonitor_Mode_ComboBox.setCurrentText(ctd["Mode"])
                    self.EnergyMonitor_Ppolar_ComboBox.setCurrentText(ctd["Ppolar"])


            self.EnergyMonitor_Name.setEnabled(False)
            self.EnableDisableParameters(True)
        
    def removeEnergyMonitor(self):
        
        for ctd in range(0, len(self.EnergyMonitors)):
            meter = self.EnergyMonitors[ctd]
            if meter["Name"] == self.EnergyMonitor_GroupBox_MEnergy_ComboBox.currentText():
                self.EnergyMonitors.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Energy Monitor", "Energy Monitor " + meter["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
                
    def AcceptAddEditEnergyMonitor(self): ## Dá para otimizar e muito // Somente um teste
        
        EnergyMonitor = {}
        EnergyMonitor["Name"] = self.get_EnergyMonitor_Name()
        EnergyMonitor["Element"] = self.get_ElementEnergyMonitor()
        EnergyMonitor["Terminal"] = self.get_TerminalEnergyMonitor()
        EnergyMonitor["Mode"] = self.get_ModeEnergyMonitor()
        EnergyMonitor["Ppolar"] = self.get_PpolarEnergyMonitor()

        if self.EnergyMonitor_Name.isEnabled():
            ctdExist = False
            for ctd in self.EnergyMonitors:
                if ctd["Name"] == EnergyMonitor["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.EnergyMonitors.append(EnergyMonitor)
                QMessageBox(QMessageBox.Information, "Energy Monitor", "Energy Monitor " + EnergyMonitor["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Energy Monitor",
                            "Energy Monitor" + EnergyMonitor["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.EnergyMonitors:
                if ctd["Name"] == EnergyMonitor["Name"]:
                    ctd["Element"] = EnergyMonitor["Element"]
                    ctd["Terminal"] = EnergyMonitor["Terminal"]
                    ctd["Mode"] = EnergyMonitor["Mode"]
                    ctd["Ppolar"] = EnergyMonitor["Ppolar"]

                    QMessageBox(QMessageBox.Information, "Energy Monitor",
                                "Energy Monitor" + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def CancelAddEdit(self):
        self.clearEnergyMonitorParameters()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):

        if bool:
            self.EnergyMonitor_GroupBox.setVisible(True)
            self.EnergyMonitor_GroupBox_MEnergy.setEnabled(False)
            self.Dialog_Btns_Ok_Btn.setEnabled(False)
            self.Dialog_Btns_Cancel_Btn.setEnabled(False)
        else:
            self.EnergyMonitor_GroupBox.setVisible(False)
            self.EnergyMonitor_GroupBox_MEnergy.setEnabled(True)
            self.Dialog_Btns_Ok_Btn.setEnabled(True)
            self.Dialog_Btns_Cancel_Btn.setEnabled(True)


    def Accept(self):
        self.OpenDSS.EnergyMonitors = self.EnergyMonitors
        self.close()
            
    def updateDialog(self):
        self.EnergyMonitor_GroupBox_MEnergy_ComboBox.clear()
        for ctd in self.EnergyMonitors:
            self.EnergyMonitor_GroupBox_MEnergy_ComboBox.addItem(ctd["Name"])

        self.EnergyMonitor_Element_ComboBox.clear()
        self.EnergyMonitor_Element_ComboBox.addItems(self.OpenDSS.getAllNamesElements())


