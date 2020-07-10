from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg


class C_Insert_InvControl_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Inserir Controle do Inversor de Frequência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        ##Layout principal
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        ####################### GroupBox InvControl ############################################################
        self.InvControl_GroupBox = QGroupBox("InvControl")  # Criando a GroupBox
        self.InvControl_GroupBox.setMinimumWidth(400)
        self.InvControl_GroupBox_Layout = QGridLayout()  # Layout da GroupBox é em Grid

        # Tree Widget
        self.InvControl_GroupBox_TreeWidget = QTreeWidget()
        self.InvControl_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'PVSystem', 'Modo'])
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_TreeWidget, 1, 1, 1, 3)
        # Botao Adicionar
        self.InvControl_GroupBox_Add_Btn = QPushButton("Adicionar")  # Botão de Adicionar dentro do GroupBox
        self.InvControl_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.InvControl_GroupBox_Add_Btn.clicked.connect(self.addInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Add_Btn, 3, 1, 1, 1)
        # Botao Excluir
        self.InvControl_GroupBox_Delete_Btn = QPushButton("Excluir")  # Botão de Excluir dentro do GroupBox
        self.InvControl_GroupBox_Delete_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.InvControl_GroupBox_Delete_Btn.clicked.connect(self.deleteInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Delete_Btn, 3, 2, 1, 1)
        # Botão Editar
        self.InvControl_GroupBox_Edit_Btn = QPushButton("Editar")  # Botão de editar dentro do GroupBox
        self.InvControl_GroupBox_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.InvControl_GroupBox_Edit_Btn.clicked.connect(self.editInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Edit_Btn, 3, 3, 1, 1)
        # Botao OK
        self.InvControl_GroupBox_OK_Btn = QPushButton("OK")  # Botão OK dentro do GroupBox
        self.InvControl_GroupBox_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.InvControl_GroupBox_OK_Btn.clicked.connect(self.acceptInsertInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_OK_Btn, 4, 1, 1, 2)
        # Botao Cancelar
        self.InvControl_GroupBox_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.InvControl_GroupBox_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.InvControl_GroupBox_Cancel_Btn.clicked.connect(self.cancelInsertInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Cancel_Btn, 4, 3, 1, 1)

        self.InvControl_GroupBox.setLayout(self.InvControl_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.InvControl_GroupBox)  # adiciona a GroupBox ao Dialog
        self.setLayout(self.Dialog_Layout)

        ##################################### Tabs #####################################################################
        self.TabWidget = QTabWidget()
        self.TabConfig = InvConfig()  # Tab das configurações gerais
        self.TabWidget.addTab(self.TabConfig, "Configurações")

        ################################### GroupBox das Configurações #################################################
        self.InvEConfig_GroupBox = QGroupBox()  # GroupBox que engloba as Tabs e Modo de Despacho
        self.InvEConfig_GroupBox_Layout = QGridLayout()
        self.InvEConfig_GroupBox.setVisible(False)

        ### Botões das Configurações
        self.Config_Btns_Layout = QHBoxLayout()
        self.Config_Btns_Layout.setAlignment(Qt.AlignRight)
        # Botao Restaurar Default
        self.Config_Btns_Default_Btn = QPushButton("Restaurar Default")  # Botão Default dentro do GroupBox
        self.Config_Btns_Default_Btn.setFixedHeight(30)
        self.Config_Btns_Default_Btn.setFixedWidth(200)
        self.Config_Btns_Default_Btn.clicked.connect(self.DefaultConfigParameters)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Default_Btn)
        # Botão OK
        self.Config_Btns_OK_Btn = QPushButton("OK")
        self.Config_Btns_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Config_Btns_OK_Btn.setFixedHeight(30)
        self.Config_Btns_OK_Btn.clicked.connect(self.AcceptAddEditInvControl)
        self.Config_Btns_OK_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_OK_Btn)
        # Botao Cancelar
        self.Config_Btns_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Config_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Config_Btns_Cancel_Btn.setFixedHeight(30)
        self.Config_Btns_Cancel_Btn.clicked.connect(self.CancelAddEditInvControl)
        self.Config_Btns_Cancel_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Cancel_Btn)

        self.InvEConfig_GroupBox_Layout.addWidget(self.TabWidget)
        self.InvEConfig_GroupBox_Layout.addItem(
            self.Config_Btns_Layout)  # adiciona o Layout dos Botões das Configurações ao GroupBox superior

        self.InvEConfig_GroupBox.setLayout(self.InvEConfig_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.InvEConfig_GroupBox)  # adiciona a GroupBox das Configurações ao Dialog

        self.setLayout(self.Dialog_Layout)

    def addInvControl(self):
        self.EnableDisableParameters(True)
        self.DefaultConfigParameters()
        self.adjustSize()

    def deleteInvControl(self):
        pass

    def editInvControl(self):
        pass

    def acceptInsertInvControl(self):
        self.clearInvControlParameters()
        self.DefaultConfigParameters()
        self.close()

    def cancelInsertInvControl(self):
        self.clearInvControlParameters()
        self.DefaultConfigParameters()
        self.close()

    def AcceptAddEditInvControl(self):
        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def CancelAddEditInvControl(self):
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):
        if bool:
            self.InvEConfig_GroupBox.setVisible(True)
            self.InvControl_GroupBox.setVisible(False)
        else:
            self.InvEConfig_GroupBox.setVisible(False)
            self.InvControl_GroupBox.setVisible(True)

    def updateDialog(self):
        pass

    def DefaultConfigParameters(self):
        self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setCurrentText("VOLTVAR")
        #FALTAM DEFAULT BOTOES VOLTVAR
        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("rated")
        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText("Yes")
        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText("INACTIVE")
        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_LineEdit.setText("0.0")
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_LineEdit.setText("0s")
        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_LineEdit.setText("0.025")
        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit.setText("0.0001")
        self.TabConfig.VoltVar_GroupBox_LPFtau_LineEdit.setText("0.001")
        self.TabConfig.VoltVar_GroupBox_RiseFallLimit_LineEdit.setText("0.001")

    def clearInvControlParameters(self):
        self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setCurrentText("")
        # FALTAM DEFAULT BOTOES VOLTVAR
        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_LPFtau_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_RiseFallLimit_LineEdit.setText("0")

class InvConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIInversorConfig()

    def InitUIInversorConfig(self):

        ### Valida as entradas dos LineEdits
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.LineEditsValidos0 = QDoubleValidator()
        self.LineEditsValidos0.setBottom(0.0)

        self.listmode = ["VOLTVAR", "VOLTWATT"]  # lista de modos disponíveis

        ###################### GroupBox NameEMode #######################################################
        self.NameEMode_GroupBox = QGroupBox()  # Criando a GroupBox InvConfig
        self.NameEMode_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        # Configurar nome do elemento
        self.NameEMode_GroupBox_Nome_Label = QLabel("Nome")
        self.NameEMode_GroupBox_Nome_LineEdit = QLineEdit()
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Nome_Label, 0, 0, 1, 1)
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Nome_LineEdit, 0, 1, 1, 1)
        # Configurar modo de controle
        self.NameEMode_GroupBox_Mode_Label = QLabel("Modo de Controle")
        self.NameEMode_GroupBox_Mode_ComboBox = QComboBox()
        self.NameEMode_GroupBox_Mode_ComboBox.addItems(self.listmode)
        self.NameEMode_GroupBox_Mode_ComboBox.currentIndexChanged.connect(self.setDisabled_Mode_GroupBox)
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Mode_Label, 1, 0, 1, 1)
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Mode_ComboBox, 1, 1, 1, 1)

        ###################### GroupBox VOLTVAR #######################################################
        self.VoltVar_GroupBox = QGroupBox("VOLTVAR")  # Criando a GroupBox InvConfig
        self.VoltVar_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        # Configurar DERList
        self.VoltVar_GroupBox_DERList_Label = QLabel("DERList")
        self.VoltVar_GroupBox_DERList_Btn = QPushButton("Selecionar Elementos")
        #self.VoltVar_GroupBox_DERList_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.VoltVar_GroupBox_DERList_Btn.clicked.connect(self.SelectElement)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DERList_Label, 0, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DERList_Btn, 0, 1, 1, 1)
        # Configurar vvc_curve1
        self.VoltVar_GroupBox_VVCCurvex1_Label = QLabel("vvc_curve1")
        self.VoltVar_GroupBox_VVCCurvex1_Btn = QPushButton("Adicionar Curva XY")
        #self.VoltVar_GroupBox_VVCCurvex1_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.VoltVar_GroupBox_VVCCurvex1_Btn.clicked.connect(self.AddCurve)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VVCCurvex1_Label, 1, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VVCCurvex1_Btn, 1, 1, 1, 1)
        # Configurar voltage_curvex_ref
        self.VoltVar_GroupBox_VoltageCurvexRef_Label = QLabel("voltage_curvex_ref")
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.addItems(["rated", "avg"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageCurvexRef_Label, 2, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox, 2, 1, 1, 1)
        # Configurar EventLog
        self.VoltVar_GroupBox_EventLog_Label = QLabel("EventLog")
        self.VoltVar_GroupBox_EventLog_ComboBox = QComboBox()
        self.VoltVar_GroupBox_EventLog_ComboBox.addItems(["Yes", "No"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_EventLog_Label, 3, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_EventLog_ComboBox, 3, 1, 1, 1)
        # Configurar RateofChangeMode
        self.VoltVar_GroupBox_RateofChangeMode_Label = QLabel("RateofChangeMode")
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox = QComboBox()
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox.addItems(["INACTIVE", "LPF", "RISEFALL"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RateofChangeMode_Label, 4, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RateofChangeMode_ComboBox, 4, 1, 1, 1)
        # Configurar hysteresis_offset
        self.VoltVar_GroupBox_HysteresisOffSet_Label = QLabel("hysteresis_offset")
        self.VoltVar_GroupBox_HysteresisOffSet_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_HysteresisOffSet_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_HysteresisOffSet_Label, 5, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_HysteresisOffSet_LineEdit, 5, 1, 1, 1)
        # Configurar avgwindowlen
        self.VoltVar_GroupBox_AvgWindowLen_Label = QLabel("avgwindowlen")
        self.VoltVar_GroupBox_AvgWindowLen_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_AvgWindowLen_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_Label, 6, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_LineEdit, 6, 1, 1, 1)
        # Configurar VarChangeTolerance (p.u.)
        self.VoltVar_GroupBox_VarChangeTolerance_Label = QLabel("VarChangeTolerance (p.u.)")
        self.VoltVar_GroupBox_VarChangeTolerance_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_VarChangeTolerance_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VarChangeTolerance_Label, 7, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VarChangeTolerance_LineEdit, 7, 1, 1, 1)
        # Configurar VoltageChangeTolerance (p.u.)
        self.VoltVar_GroupBox_VoltageChangeTolerance_Label = QLabel("VoltageChangeTolerance (p.u.)")
        self.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageChangeTolerance_Label, 8, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit, 8, 1, 1, 1)
        # Configurar LPFtau
        self.VoltVar_GroupBox_LPFtau_Label = QLabel("LPFtau")
        self.VoltVar_GroupBox_LPFtau_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_LPFtau_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_LPFtau_Label, 9, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_LPFtau_LineEdit, 9, 1, 1, 1)
        # Configurar RiseFallLimit
        self.VoltVar_GroupBox_RiseFallLimit_Label = QLabel("RiseFallLimit")
        self.VoltVar_GroupBox_RiseFallLimit_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RiseFallLimit_Label, 10, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RiseFallLimit_LineEdit, 10, 1, 1, 1)


        ###################### GroupBox VOLTWATT #######################################################
        self.VoltWatt_GroupBox = QGroupBox("VOLTWATT")  # Criando a GroupBox InvConfig
        self.VoltWatt_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        self.VoltWatt_GroupBox.setVisible(False)
        # Configurar PVSystemList
        self.VoltWatt_GroupBox_PVSystemList_Label = QLabel("PVSystemList")
        self.VoltWatt_GroupBox_PVSystemList_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_PVSystemList_ComboBox.addItems([""])
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_PVSystemList_Label, 0, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_PVSystemList_ComboBox, 0, 1, 1, 1)
        # Configurar Voltage Curvex Ref
        self.VoltWatt_GroupBox_VoltageCurvexRef_Label = QLabel("Voltage Curvex Ref")
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.addItems(["Rated", "Avg", "Ravg"])
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltageCurvexRef_Label, 1, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox, 1, 1, 1, 1)

        ##################################################################################################

        self.NameEMode_GroupBox.setLayout(self.NameEMode_GroupBox_Layout)
        self.Tab_layout = QGridLayout()
        self.Tab_layout.addWidget(self.NameEMode_GroupBox, 0, 1, 1, 1)

        self.VoltVar_GroupBox.setLayout(self.VoltVar_GroupBox_Layout)
        self.Tab_layout.addWidget(self.VoltVar_GroupBox, 1, 1, 1, 1)

        self.VoltWatt_GroupBox.setLayout(self.VoltWatt_GroupBox_Layout)
        self.Tab_layout.addWidget(self.VoltWatt_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Tab_layout)

    def setDisabled_Mode_GroupBox(self):

        if self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            self.VoltVar_GroupBox.setVisible(True)
            self.VoltWatt_GroupBox.setVisible(False)
        elif self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTWATT":
            self.VoltVar_GroupBox.setVisible(False)
            self.VoltWatt_GroupBox.setVisible(True)

    def SelectElement(self):
        pass

    def AddCurve(self):
        pass

class InvControl_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, pvsystem, mode):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(InvControl_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)
        ## Column 1 - PVSystem:
        self.setText(1, pvsystem)
        ## Column 2 - Modo Despacho:
        self.setText(2, mode)
