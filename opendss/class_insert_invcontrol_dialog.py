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
        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

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

        ################################### GroupBox das Configurações #################################################
        self.InvConfig_GroupBox = QGroupBox("Configurações")  # GroupBox que engloba as Tabs e Modo de Despacho
        self.InvConfig_GroupBox_Layout = QGridLayout()
        self.InvConfig_GroupBox.setVisible(False)

        ### Botões das Configurações
        self.Config_Btns_Layout = QHBoxLayout()
        #self.Config_Btns_Layout.setAlignment(Qt.AlignRight)
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

        ### Valida as entradas dos LineEdits
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.LineEditsValidos0 = QDoubleValidator()
        self.LineEditsValidos0.setBottom(0.0)

        ###################### GroupBox InvConfig #######################################################

        # Configurar nome do elemento
        self.InvConfig_GroupBox_Nome_Label = QLabel("Nome")
        self.InvConfig_GroupBox_Nome_LineEdit = QLineEdit()
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_Nome_Label, 0, 0, 1, 1)
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_Nome_LineEdit, 0, 1, 1, 1)
        # Configurar modo de controle
        self.InvConfig_GroupBox_Mode_Label = QLabel("Modo de Controle")
        self.InvConfig_GroupBox_Mode_ComboBox = QComboBox()
        self.InvConfig_GroupBox_Mode_ComboBox.addItems(["VOLT-VAR", "VOLT-WATT"])
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_Mode_Label, 1, 0, 1, 1)
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_Mode_ComboBox, 1, 1, 1, 1)
        # Configurar PVSystemList
        self.InvConfig_GroupBox_PVSystemList_Label = QLabel("PVSystemList")
        self.InvConfig_GroupBox_PVSystemList_ComboBox = QComboBox()
        self.InvConfig_GroupBox_PVSystemList_ComboBox.addItems([""])
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_PVSystemList_Label, 2, 0, 1, 1)
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_PVSystemList_ComboBox, 2, 1, 1, 1)
        # Configurar Voltage Curvex Ref
        self.InvConfig_GroupBox_VoltageCurvexRef_Label = QLabel("Voltage Curvex Ref")
        self.InvConfig_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.InvConfig_GroupBox_VoltageCurvexRef_ComboBox.addItems(["Rated", "Avg", "Ravg"])
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_VoltageCurvexRef_Label, 3, 0, 1, 1)
        self.InvConfig_GroupBox_Layout.addWidget(self.InvConfig_GroupBox_VoltageCurvexRef_ComboBox, 3, 1, 1, 1)

        self.InvConfig_GroupBox_Layout.addItem(
            self.Config_Btns_Layout, 7, 1, 1, 1)  # adiciona o Layout dos Botões das Configurações ao GroupBox

        self.InvConfig_GroupBox.setLayout(self.InvConfig_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.InvConfig_GroupBox, 1, 1, 1, 1)

        self.Dialog_Layout.addWidget(self.InvConfig_GroupBox)  # adiciona a GroupBox das Configurações ao Dialog

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
        pass

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
            self.InvConfig_GroupBox.setVisible(True)
            self.InvControl_GroupBox.setVisible(False)
        else:
            self.InvConfig_GroupBox.setVisible(False)
            self.InvControl_GroupBox.setVisible(True)

    def updateDialog(self):
        pass

    def DefaultConfigParameters(self):
        pass

    def clearInvControlParameters(self):
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
