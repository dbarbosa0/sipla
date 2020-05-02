from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg

class C_Insert_EnergyMeter_Dialog(QDialog): ## Classe Dialog principal
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Energy Meter Insert"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.InitUI()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.EnergyMeters = []

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ###
        ## GroupBox Medidores
        self.EnergyMeter_GroupBox_MEnergy = QGroupBox("Medidores de Energia")
        self.EnergyMeter_GroupBox_MEnergy_Label = QLabel("Medidores Existentes")
        self.EnergyMeter_GroupBox_MEnergy_ComboBox = QComboBox()

        # Layout do GroupBox Medidores
        self.EnergyMeter_GroupBox_MEnergy_Layout = QGridLayout()
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_Label, 0, 0, 1, 1)
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_ComboBox, 0, 1, 1, 3)
        self.EnergyMeter_GroupBox_MEnergy.setLayout(self.EnergyMeter_GroupBox_MEnergy_Layout)

        self.Dialog_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy)

        ##### Btns
        self.EnergyMeter_GroupBox_MEnergy_Remover_Btn = QPushButton("Remover")
        self.EnergyMeter_GroupBox_MEnergy_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Shapes_GroupBox_Remover_Btn.setFixedWidth(80)
        self.EnergyMeter_GroupBox_MEnergy_Remover_Btn.clicked.connect(self.removeEnergyMeter)
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_Remover_Btn,1,1,1,1)

        self.EnergyMeter_GroupBox_MEnergy_Edit_Btn = QPushButton("Editar")
        self.EnergyMeter_GroupBox_MEnergy_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        #self.Shapes_GroupBox_Edit_Btn.setFixedWidth(80)
        self.EnergyMeter_GroupBox_MEnergy_Edit_Btn.clicked.connect(self.editEnergyMeter)
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_Edit_Btn,1,2,1,1)

        self.EnergyMeter_GroupBox_MEnergy_Adicionar_Btn = QPushButton("Adicionar")
        self.EnergyMeter_GroupBox_MEnergy_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Shapes_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.EnergyMeter_GroupBox_MEnergy_Adicionar_Btn.clicked.connect(self.addEnergyMeter)
        self.EnergyMeter_GroupBox_MEnergy_Layout.addWidget(self.EnergyMeter_GroupBox_MEnergy_Adicionar_Btn,1,3,1,1)



        #### Energy Meter

        self.EnergyMeter_GroupBox = QGroupBox("Configuração do Medidor de Energia")
        self.EnergyMeter_GroupBox.setVisible(False)
        ## GroupBox opções
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

        ### LineEdits
        self.EnergyMeter_Name = QLineEdit()

        # Comboboxs
        self.EnergyMeter_Element_ComboBox = QComboBox()
        self.EnergyMeter_Element_ComboBox.clear()
        self.EnergyMeter_Terminal_ComboBox = QComboBox()
        self.EnergyMeter_Terminal_ComboBox.addItems(["1", "2"])
        self.EnergyMeter_3phaseLosses_ComboBox = QComboBox()
        self.EnergyMeter_3phaseLosses_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_LineLosses_ComboBox = QComboBox()
        self.EnergyMeter_LineLosses_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_Losses_ComboBox = QComboBox()
        self.EnergyMeter_Losses_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_SeqLosses_ComboBox = QComboBox()
        self.EnergyMeter_SeqLosses_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_VbaseLosses_ComboBox = QComboBox()
        self.EnergyMeter_VbaseLosses_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_XfmrLosses_ComboBox = QComboBox()
        self.EnergyMeter_XfmrLosses_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_LocalOnly_ComboBox = QComboBox()
        self.EnergyMeter_LocalOnly_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_PhaseVoltageReport_ComboBox = QComboBox()
        self.EnergyMeter_PhaseVoltageReport_ComboBox.addItems(["Yes", "No"])
        self.EnergyMeter_Action_ComboBox = QComboBox()
        self.EnergyMeter_Action_ComboBox.addItems(["Clear", "Save", "Take", "Zonedump", "Allocate", "Reduce"])
        self.EnergyMeter_Enabled_ComboBox = QComboBox()
        self.EnergyMeter_Enabled_ComboBox.addItems(["Yes", "No"])

        self.EnergyMeter_Element_PushButton = QPushButton(QIcon('img/icon_opendss_pesquisar.png'), str())

        ### Layout
        self.EnergyMeter_Layout = QGridLayout()
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Name_Label, 0, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Name, 0, 1, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Element_Label, 1, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Terminal_Label, 2, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_3phaseLosses_Label, 3, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_LineLosses_Label, 4, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Losses_Label, 5, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_SeqLosses_Label, 6, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_VbaseLosses_Label, 7, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_XfmrLosses_Label, 8, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_LocalOnly_Label, 9, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_PhaseVoltageReport_Label, 10, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Enabled_Label, 11, 0, 1, 1)
        self.EnergyMeter_Layout.addWidget(self.EnergyMeter_Action_Label, 12, 0, 1, 1)

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
        
        ###### Botões dos Parâmetros
        self.EnergyMeter_Btns_Layout = QHBoxLayout()
        self.EnergyMeter_Btns_Layout.setAlignment(Qt.AlignRight)

        self.EnergyMeter_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.EnergyMeter_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        #self.EnergyMeter_Btns_Cancel_Btn.setFixedWidth(100)
        self.EnergyMeter_Btns_Cancel_Btn.clicked.connect(self.CancelAddEdit)
        self.EnergyMeter_Btns_Layout.addWidget(self.EnergyMeter_Btns_Cancel_Btn)

        self.EnergyMeter_Btns_Ok_Btn = QPushButton("OK")
        self.EnergyMeter_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        #self.EnergyMeter_Btns_Ok_Btn.setFixedWidth(100)
        self.EnergyMeter_Btns_Ok_Btn.clicked.connect(self.AcceptAddEditEnergyMeter)
        self.EnergyMeter_Btns_Layout.addWidget(self.EnergyMeter_Btns_Ok_Btn)
        self.EnergyMeter_Layout.addItem(self.EnergyMeter_Btns_Layout,13, 0, 1, 2)
        ####

        self.EnergyMeter_GroupBox.setLayout(self.EnergyMeter_Layout)

        self.Dialog_Layout.addWidget(self.EnergyMeter_GroupBox)

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
        
    def get_EnergyMeter_Name(self):
        return self.EnergyMeter_Name.text()

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
    
    def clearEnergyMeterParameters(self):
        self.EnergyMeter_Name.setText("")
        self.EnergyMeter_Element_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_Terminal_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_3phaseLosses_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_LineLosses_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_Losses_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_SeqLosses_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_VbaseLosses_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_XfmrLosses_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_LocalOnly_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_PhaseVoltageReport_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_Action_ComboBox.setCurrentIndex(0)
        self.EnergyMeter_Enabled_ComboBox.setCurrentIndex(0)
        
    def addEnergyMeter(self):
        self.clearEnergyMeterParameters()
        self.EnergyMeter_Name.setEnabled(True)
        self.EnableDisableParameters(True)

    def editEnergyMeter(self):

        if self.EnergyMeter_GroupBox_MEnergy_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Energy Meter", "Pelo menos um Energy Meter deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            self.clearEnergyMeterParameters()

            for ctd in self.EnergyMeters:
                if ctd["Name"] == self.EnergyMeter_GroupBox_MEnergy_ComboBox.currentText():
                    self.EnergyMeter_Name.setText(ctd["Name"])
                    self.EnergyMeter_Element_ComboBox.setCurrentText(ctd["Element"])
                    self.EnergyMeter_Terminal_ComboBox.setCurrentText(ctd["Terminal"])
                    self.EnergyMeter_3phaseLosses_ComboBox.setCurrentText(ctd["3phaseLosses"])
                    self.EnergyMeter_LineLosses_ComboBox.setCurrentText(ctd["LineLosses"])
                    self.EnergyMeter_Losses_ComboBox.setCurrentText(ctd["Losses"])
                    self.EnergyMeter_SeqLosses_ComboBox.setCurrentText(ctd["SeqLosses"])
                    self.EnergyMeter_VbaseLosses_ComboBox.setCurrentText(ctd["VbaseLosses"])
                    self.EnergyMeter_XfmrLosses_ComboBox.setCurrentText(ctd["XfmrLosses"])
                    self.EnergyMeter_LocalOnly_ComboBox.setCurrentText(ctd["LocalOnly"])
                    self.EnergyMeter_PhaseVoltageReport_ComboBox.setCurrentText(ctd["PhaseVoltageReport"])
                    self.EnergyMeter_Action_ComboBox.setCurrentText(ctd["Action"])
                    self.EnergyMeter_Enabled_ComboBox.setCurrentText(ctd["Enabled"])

            self.EnergyMeter_Name.setEnabled(False)
            self.EnableDisableParameters(True)
        
    def removeEnergyMeter(self):
        
        for ctd in self.EnergyMeters:
            if ctd["Name"] == self.EnergyMeter_GroupBox_MEnergy_ComboBox.currentText():
                self.EnergyMeters.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Energy Monitor", "Energy Monitor " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()

        self.updateDialog()
                
    def AcceptAddEditEnergyMeter(self): ## Dá para otimizar e muito // Somente um teste
        
        energyMeter = {}
        energyMeter["Name"] = self.get_EnergyMeter_Name()
        energyMeter["Element"] = self.get_ElementEnergyMeter()
        energyMeter["Terminal"] = self.get_TerminalEnergyMeter()
        energyMeter["3phaseLosses"] = self.get_3phaseLossesEnergyMeter()
        energyMeter["LineLosses"] = self.get_LineLossesEnergyMeter()
        energyMeter["Losses"] = self.get_LossesEnergyMeter()
        energyMeter["SeqLosses"] = self.get_SeqLossesEnergyMeter()
        energyMeter["VbaseLosses"] = self.get_VbaseLossesEnergyMeter()
        energyMeter["XfmrLosses"] = self.get_XfmrLossesEnergyMeter()
        energyMeter["LocalOnly"] = self.get_LocalOnlyEnergyMeter()
        energyMeter["PhaseVoltageReport"] = self.get_PhaseVoltageReportEnergyMeter()
        energyMeter["Action"] = self.get_ActionEnergyMeter()
        energyMeter["Enabled"] = self.get_EnabledEnergyMeter()

        if self.EnergyMeter_Name.isEnabled():
            ctdExist = False
            for ctd in self.EnergyMeters:
                if ctd["Name"] == energyMeter["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.EnergyMeters.append(energyMeter)
                QMessageBox(QMessageBox.Information, "Energy Meter", "Energy Meter " + energyMeter["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Energy Meter",
                            "Energy Meter " + energyMeter["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.EnergyMeters:
                if ctd["Name"] == energyMeter["Name"]:
                    ctd["Element"] = energyMeter["Element"]
                    ctd["Terminal"] = energyMeter["Terminal"]
                    ctd["3phaseLosses"] = energyMeter["3phaseLosses"]
                    ctd["LineLosses"] = energyMeter["LineLosses"]
                    ctd["Losses"] = energyMeter["Losses"]
                    ctd["SeqLosses"] = energyMeter["SeqLosses"]
                    ctd["VbaseLosses"] = energyMeter["VbaseLosses"]
                    ctd["XfmrLosses"] = energyMeter["XfmrLosses"]
                    ctd["LocalOnly"] = energyMeter["LocalOnly"]
                    ctd["PhaseVoltageReport"] = energyMeter["PhaseVoltageReport"]
                    ctd["Action"] = energyMeter["Action"]
                    ctd["Enabled"] = energyMeter["Enabled"]

                    QMessageBox(QMessageBox.Information, "Energy Meter",
                                "Energy Meter " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def CancelAddEdit(self):
        self.clearEnergyMeterParameters()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):

        if bool:
            self.EnergyMeter_GroupBox.setVisible(True)
            self.EnergyMeter_GroupBox_MEnergy.setEnabled(False)
            self.Dialog_Btns_Ok_Btn.setEnabled(False)
            self.Dialog_Btns_Cancel_Btn.setEnabled(False)
        else:
            self.EnergyMeter_GroupBox.setVisible(False)
            self.EnergyMeter_GroupBox_MEnergy.setEnabled(True)
            self.Dialog_Btns_Ok_Btn.setEnabled(True)
            self.Dialog_Btns_Cancel_Btn.setEnabled(True)


    def Accept(self):
        self.OpenDSS.EnergyMeters = self.EnergyMeters
        self.close()
            
    def updateDialog(self):
        self.EnergyMeter_GroupBox_MEnergy_ComboBox.clear()
        for ctd in self.EnergyMeters:
            self.EnergyMeter_GroupBox_MEnergy_ComboBox.addItem(ctd["Name"])

        self.EnergyMeter_Element_ComboBox.clear()
        #self.EnergyMeter_Element_ComboBox.addItems(self.OpenDSS.getAllNamesElements())
        self.EnergyMeter_Element_ComboBox.addItems(self.OpenDSS.getBusList())


