from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

import class_exception
import opendss.class_opendss
import config as cfg
import unidecode


class C_Insert_InvControl_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Inserir Controle do Inversor"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)       # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        ##Layout principal
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        ####################### GroupBox InvControl ############################################################
        self.InvControl_GroupBox = QGroupBox("InvControl")  # Criando a GroupBox InvControl
        self.InvControl_GroupBox.setMinimumWidth(400)
        self.InvControl_GroupBox_Layout = QGridLayout()  # Layout da GroupBox é em Grid

        # Tree Widget
        self.InvControl_GroupBox_TreeWidget = QTreeWidget()
        self.InvControl_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Elementos PC', 'Modo'])
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_TreeWidget, 0, 1, 1, 3)
        # Botao Adicionar
        self.InvControl_GroupBox_Add_Btn = QPushButton("Adicionar")  # Botão de Adicionar dentro do GroupBox
        self.InvControl_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.InvControl_GroupBox_Add_Btn.clicked.connect(self.addInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Add_Btn, 1, 1, 1, 1)
        # Botao Excluir
        self.InvControl_GroupBox_Delete_Btn = QPushButton("Excluir")  # Botão de Excluir dentro do GroupBox
        self.InvControl_GroupBox_Delete_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.InvControl_GroupBox_Delete_Btn.clicked.connect(self.deleteInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Delete_Btn, 1, 2, 1, 1)
        # Botão Editar
        self.InvControl_GroupBox_Edit_Btn = QPushButton("Editar")  # Botão de editar dentro do GroupBox
        self.InvControl_GroupBox_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.InvControl_GroupBox_Edit_Btn.clicked.connect(self.editInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Edit_Btn, 1, 3, 1, 1)
        # Botao OK
        self.InvControl_GroupBox_OK_Btn = QPushButton("OK")  # Botão OK dentro do GroupBox
        self.InvControl_GroupBox_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.InvControl_GroupBox_OK_Btn.clicked.connect(self.acceptInsertInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_OK_Btn, 2, 1, 1, 2)
        # Botao Cancelar
        self.InvControl_GroupBox_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.InvControl_GroupBox_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.InvControl_GroupBox_Cancel_Btn.clicked.connect(self.cancelInsertInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Cancel_Btn, 2, 3, 1, 1)

        self.InvControl_GroupBox.setLayout(self.InvControl_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.InvControl_GroupBox)  # adiciona a GroupBox ao Dialog
        self.setLayout(self.Dialog_Layout)

        ##################################### Tabs #####################################################################
        self.TabWidget = QTabWidget()
        self.TabConfig = InvConfig()  # Tab das configurações gerais
        self.TabWidget.addTab(self.TabConfig, "Configurações")

        ################################### GroupBox das Configurações #################################################
        self.InvEConfig_GroupBox = QGroupBox()  # GroupBox que engloba as Tabs
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
        self.InvEConfig_GroupBox_Layout.addItem(self.Config_Btns_Layout)

        self.InvEConfig_GroupBox.setLayout(self.InvEConfig_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.InvEConfig_GroupBox)  # adiciona a GroupBox das Configurações ao Dialog

        self.setLayout(self.Dialog_Layout)

    def get_InvControlName(self):
        return unidecode.unidecode(self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.text().replace(" ", "_"))

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
        InvControl_TreeWidget_Item(self.InvControl_GroupBox_TreeWidget,
                                self.get_InvControlName(),
                                "Algum",
                                self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText())
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

        #FALTAM DEFAULT BOTOES DO VOLTVAR
        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("rated")
        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText("Yes")
        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText("INACTIVE")
        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_LineEdit.setText("0.0")
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_LineEdit.setText("0s")
        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_LineEdit.setText("0.025")
        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit.setText("0.0001")
        self.TabConfig.VoltVar_GroupBox_LPFtau_LineEdit.setText("0.001")
        self.TabConfig.VoltVar_GroupBox_RiseFallLimit_LineEdit.setText("0.001")
        self.TabConfig.VoltVar_GroupBox_DeltaQFactor_LineEdit.setText("-1.0")
        self.TabConfig.VoltVar_GroupBox_RefReactivePower_ComboBox.setCurrentText("VARAVAL")

        # FALTAM DEFAULT BOTOES DO VOLTWATT
        self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("rated")
        self.TabConfig.VoltWatt_GroupBox_EventLog_ComboBox.setCurrentText("Yes")
        self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.setCurrentText("INACTIVE")
        self.TabConfig.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.setCurrentText("PMPPPU")
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setText("0s")
        self.TabConfig.VoltWatt_GroupBox_LPFtau_LineEdit.setText("0.001")
        self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setText("0.001")
        self.TabConfig.VoltWatt_GroupBox_DeltaPFactor_LineEdit.setText("-1.0")
        self.TabConfig.VoltWatt_GroupBox_ActivePChangeTolerance_LineEdit.setText("0.01")

        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setEnabled(False)
        self.TabConfig.VoltWatt_GroupBox_LPFtau_LineEdit.setEnabled(False)
        self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)

    def clearInvControlParameters(self):
        self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setCurrentText("")

        # FALTAM DEFAULT BOTOES DO VOLTVAR
        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_LPFtau_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_RiseFallLimit_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_DeltaQFactor_LineEdit.setText("0")
        self.TabConfig.VoltVar_GroupBox_RefReactivePower_ComboBox.setCurrentText("")

        # FALTAM DEFAULT BOTOES DO VOLTWATT
        self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_EventLog_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setText("0")
        self.TabConfig.VoltWatt_GroupBox_LPFtau_LineEdit.setText("0")
        self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setText("0")
        self.TabConfig.VoltWatt_GroupBox_DeltaPFactor_LineEdit.setText("0")
        self.TabConfig.VoltWatt_GroupBox_ActivePChangeTolerance_LineEdit.setText("0")

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
        self.VoltVar_GroupBox_DERList_Btn.clicked.connect(self.SelectElement)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DERList_Label, 0, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DERList_Btn, 0, 1, 1, 1)
        # Configurar vvc_curve1
        self.VoltVar_GroupBox_VVCCurvex1_Label = QLabel("vvc_curve1")
        self.VoltVar_GroupBox_VVCCurvex1_Btn = QPushButton("Adicionar Curva XY")
        self.VoltVar_GroupBox_VVCCurvex1_Btn.clicked.connect(self.AddCurve)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VVCCurvex1_Label, 1, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VVCCurvex1_Btn, 1, 1, 1, 1)
        # Configurar EventLog
        self.VoltVar_GroupBox_EventLog_Label = QLabel("EventLog")
        self.VoltVar_GroupBox_EventLog_ComboBox = QComboBox()
        self.VoltVar_GroupBox_EventLog_ComboBox.addItems(["Yes", "No"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_EventLog_Label, 2, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_EventLog_ComboBox, 2, 1, 1, 1)
        # Configurar deltaQ_Factor
        self.VoltVar_GroupBox_DeltaQFactor_Label = QLabel("deltaQ_Factor")
        self.VoltVar_GroupBox_DeltaQFactor_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_DeltaQFactor_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DeltaQFactor_Label, 3, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DeltaQFactor_LineEdit, 3, 1, 1, 1)
        # Configurar VarChangeTolerance (p.u.)
        self.VoltVar_GroupBox_VarChangeTolerance_Label = QLabel("VarChangeTolerance (p.u.)")
        self.VoltVar_GroupBox_VarChangeTolerance_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_VarChangeTolerance_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VarChangeTolerance_Label, 4, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VarChangeTolerance_LineEdit, 4, 1, 1, 1)
        # Configurar VoltageChangeTolerance (p.u.)
        self.VoltVar_GroupBox_VoltageChangeTolerance_Label = QLabel("VoltageChangeTolerance (p.u.)")
        self.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageChangeTolerance_Label, 5, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageChangeTolerance_LineEdit, 5, 1, 1, 1)
        # Configurar hysteresis_offset
        self.VoltVar_GroupBox_HysteresisOffSet_Label = QLabel("hysteresis_offset")
        self.VoltVar_GroupBox_HysteresisOffSet_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_HysteresisOffSet_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_HysteresisOffSet_Label, 6, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_HysteresisOffSet_LineEdit, 6, 1, 1, 1)
        # Configurar voltage_curvex_ref
        self.VoltVar_GroupBox_VoltageCurvexRef_Label = QLabel("voltage_curvex_ref")
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.addItems(["rated", "avg"])
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentIndexChanged.connect(
                                                        self.Enable_VoltageCurvexRef_LineEdit)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageCurvexRef_Label, 7, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox, 7, 1, 1, 1)
        # Configurar avgwindowlen
        self.VoltVar_GroupBox_AvgWindowLen_Label = QLabel("avgwindowlen")
        self.VoltVar_GroupBox_AvgWindowLen_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_AvgWindowLen_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_AvgWindowLen_LineEdit.setEnabled(False)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_Label, 8, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_LineEdit, 8, 1, 1, 1)
        # Configurar RateofChangeMode
        self.VoltVar_GroupBox_RateofChangeMode_Label = QLabel("RateofChangeMode")
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox = QComboBox()
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox.addItems(["INACTIVE", "LPF", "RISEFALL"])
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentIndexChanged.connect(
                                                        self.Enable_RateofChageMode_LineEdit)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RateofChangeMode_Label, 9, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RateofChangeMode_ComboBox, 9, 1, 1, 1)
        # Configurar LPFtau
        self.VoltVar_GroupBox_LPFtau_Label = QLabel("LPFtau")
        self.VoltVar_GroupBox_LPFtau_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_LPFtau_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_LPFtau_LineEdit.setEnabled(False)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_LPFtau_Label, 10, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_LPFtau_LineEdit, 10, 1, 1, 1)
        # Configurar RiseFallLimit
        self.VoltVar_GroupBox_RiseFallLimit_Label = QLabel("RiseFallLimit")
        self.VoltVar_GroupBox_RiseFallLimit_LineEdit = QLineEdit()
        self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RiseFallLimit_Label, 11, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RiseFallLimit_LineEdit, 11, 1, 1, 1)
        # Configurar RefReactivePower
        self.VoltVar_GroupBox_RefReactivePower_Label = QLabel("RefReactivePower")
        self.VoltVar_GroupBox_RefReactivePower_ComboBox = QComboBox()
        self.VoltVar_GroupBox_RefReactivePower_ComboBox.addItems(["VARAVAL", "VARMAX"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RefReactivePower_Label, 12, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RefReactivePower_ComboBox, 12, 1, 1, 1)

        ###################### GroupBox VOLTWATT #######################################################
        self.VoltWatt_GroupBox = QGroupBox("VOLTWATT")  # Criando a GroupBox InvConfig
        self.VoltWatt_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        self.VoltWatt_GroupBox.setVisible(False)
        # Configurar DERList
        self.VoltWatt_GroupBox_DERList_Label = QLabel("DERList")
        self.VoltWatt_GroupBox_DERList_Btn = QPushButton("Selecionar Elementos")
        self.VoltWatt_GroupBox_DERList_Btn.clicked.connect(self.SelectElement)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DERList_Label, 0, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DERList_Btn, 0, 1, 1, 1)
        # Configurar voltwatt_curve
        self.VoltWatt_GroupBox_VoltWattCurve_Label = QLabel("voltwatt_curve")
        self.VoltWatt_GroupBox_VoltWattCurve_Btn = QPushButton("Adicionar Curva XY")
        self.VoltWatt_GroupBox_VoltWattCurve_Btn.clicked.connect(self.AddCurve)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattCurve_Label, 1, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattCurve_Btn, 1, 1, 1, 1)
        # Configurar EventLog
        self.VoltWatt_GroupBox_EventLog_Label = QLabel("EventLog")
        self.VoltWatt_GroupBox_EventLog_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_EventLog_ComboBox.addItems(["Yes", "No"])
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_EventLog_Label, 2, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_EventLog_ComboBox, 2, 1, 1, 1)
        # Configurar deltaP_Factor
        self.VoltWatt_GroupBox_DeltaPFactor_Label = QLabel("deltaP_Factor")
        self.VoltWatt_GroupBox_DeltaPFactor_LineEdit = QLineEdit()
        self.VoltWatt_GroupBox_DeltaPFactor_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DeltaPFactor_Label, 3, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DeltaPFactor_LineEdit, 3, 1, 1, 1)
        # Configurar ActivePChangeTolerance
        self.VoltWatt_GroupBox_ActivePChangeTolerance_Label = QLabel("ActivePChangeTolerance")
        self.VoltWatt_GroupBox_ActivePChangeTolerance_LineEdit = QLineEdit()
        self.VoltWatt_GroupBox_ActivePChangeTolerance_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_ActivePChangeTolerance_Label, 4, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_ActivePChangeTolerance_LineEdit, 4, 1, 1, 1)
        # Configurar voltage_curvex_ref
        self.VoltWatt_GroupBox_VoltageCurvexRef_Label = QLabel("voltage_curvex_ref")
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.addItems(["rated", "avg"])
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentIndexChanged.connect(
                                                                 self.Enable_VoltageCurvexRef_LineEdit)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltageCurvexRef_Label, 5, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox, 5, 1, 1, 1)
        # Configurar avgwindowlen
        self.VoltWatt_GroupBox_AvgWindowLen_Label = QLabel("avgwindowlen")
        self.VoltWatt_GroupBox_AvgWindowLen_LineEdit = QLineEdit()
        self.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setEnabled(False)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_AvgWindowLen_Label, 6, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_AvgWindowLen_LineEdit, 6, 1, 1, 1)
        # Configurar RateofChangeMode
        self.VoltWatt_GroupBox_RateofChangeMode_Label = QLabel("RateofChangeMode")
        self.VoltWatt_GroupBox_RateofChangeMode_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.addItems(["INACTIVE", "LPF", "RISEFALL"])
        self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentIndexChanged.connect(
                                                            self.Enable_RateofChageMode_LineEdit)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RateofChangeMode_Label, 7, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RateofChangeMode_ComboBox, 7, 1, 1, 1)
        # Configurar LPFtau
        self.VoltWatt_GroupBox_LPFtau_Label = QLabel("LPFtau")
        self.VoltWatt_GroupBox_LPFtau_LineEdit = QLineEdit()
        self.VoltWatt_GroupBox_LPFtau_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltWatt_GroupBox_LPFtau_LineEdit.setEnabled(False)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_LPFtau_Label,8, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_LPFtau_LineEdit, 8, 1, 1, 1)
        # Configurar RiseFallLimit
        self.VoltWatt_GroupBox_RiseFallLimit_Label = QLabel("RiseFallLimit")
        self.VoltWatt_GroupBox_RiseFallLimit_LineEdit = QLineEdit()
        self.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setValidator(self.LineEditsValidos)
        self.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RiseFallLimit_Label, 9, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RiseFallLimit_LineEdit, 9, 1, 1, 1)
        # Configurar VoltwattYAxis
        self.VoltWatt_GroupBox_VoltWattYAxis_Label = QLabel("VoltwattYAxis")
        self.VoltWatt_GroupBox_VoltWattYAxis_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.addItems(["PMPPPU", "PAVAILABLEPU", "PCTPMPPPU", "KVARATINGPU"])
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattYAxis_Label, 10, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattYAxis_ComboBox, 10, 1, 1, 1)

        ##################################################################################################

        self.Tab_layout = QGridLayout()

        self.NameEMode_GroupBox.setLayout(self.NameEMode_GroupBox_Layout)
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

    def Enable_VoltageCurvexRef_LineEdit(self):
        if self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            if self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                self.VoltVar_GroupBox_AvgWindowLen_LineEdit.setEnabled(True)
            else:
                self.VoltVar_GroupBox_AvgWindowLen_LineEdit.setEnabled(False)
        else:
            if self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                self.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setEnabled(True)
            else:
                self.VoltWatt_GroupBox_AvgWindowLen_LineEdit.setEnabled(False)

    def Enable_RateofChageMode_LineEdit(self):
        if self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            if self.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                self.VoltVar_GroupBox_LPFtau_LineEdit.setEnabled(True)
                self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
            elif self.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setEnabled(True)
                self.VoltVar_GroupBox_LPFtau_LineEdit.setEnabled(False)
            else:
                self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
                self.VoltVar_GroupBox_LPFtau_LineEdit.setEnabled(False)
                self.VoltVar_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
        else:
            if self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                self.VoltWatt_GroupBox_LPFtau_LineEdit.setEnabled(True)
                self.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
            elif self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                self.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setEnabled(True)
                self.VoltWatt_GroupBox_LPFtau_LineEdit.setEnabled(False)
            else:
                self.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)
                self.VoltWatt_GroupBox_LPFtau_LineEdit.setEnabled(False)
                self.VoltWatt_GroupBox_RiseFallLimit_LineEdit.setEnabled(False)

    def SelectElement(self):
        pass

    def AddCurve(self):
        pass

    def verificaLineEdits(self):
        pass

class InvControl_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, elementos, mode):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(InvControl_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)
        ## Column 1 - PVSystem:
        self.setText(1, elementos)
        ## Column 2 - Modo Despacho:
        self.setText(2, mode)
