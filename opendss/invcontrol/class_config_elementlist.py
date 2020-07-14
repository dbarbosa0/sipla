from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QColorDialog, QMessageBox, QInputDialog, QLabel
from PyQt5.QtCore import Qt

import random
import pyqtgraph
import config as cfg
import class_exception


class C_Config_ElementList_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Lista de Elementos"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ### ElementList - TreeWidget
        self.ElementList_GroupBox = QGroupBox("")
        self.ElementList_GroupBox.setFixedWidth(400)
        self.ElementList_GroupBox.setFixedHeight(400)

        self.ElementList_GroupBox_Layout = QGridLayout()
        self.ElementList_GroupBox_TreeWidget = QTreeWidget()
        self.ElementList_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Elemento'])
        self.ElementList_GroupBox_TreeWidget.setColumnWidth(1, 100)
        self.ElementList_GroupBox_Layout.addWidget(self.ElementList_GroupBox_TreeWidget, 1, 1, 1, 1)

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.Cancel)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 1, 1, 1)

        self.ElementList_GroupBox.setLayout(self.ElementList_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.ElementList_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def Accept(self):
        pass

    def Cancel(self):
        pass


class Config_ElementList_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent,  name, element):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_ElementList_GroupBox_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Name:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)

        ## Column 1 - Element:
        self.setText(1, element)