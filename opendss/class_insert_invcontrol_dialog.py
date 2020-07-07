from PyQt5.QtGui import  QIcon, QDoubleValidator
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

    # Botão de Adiconar
    def addInvControl(self):
        pass

    # Botão de Excluir
    def deleteInvControl(self):
        pass

    # Botão de Editar
    def editInvControl(self):
        pass

    # Botão de Ok
    def acceptInsertInvControl(self):
        pass

    # Botão de Cancelar
    def cancelInsertInvControl(self):
        self.clearStorageParameters()
        self.DefaultConfigParameters()
        self.close()

    def updateDialog(self):
        pass

    def DefaultConfigParameters(self):
        pass

    def clearStorageParameters(self):
        pass