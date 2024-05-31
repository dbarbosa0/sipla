from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox
from PyQt6.QtCore import Qt

import config as cfg
import opendss.class_opendss


class C_Config_ElementList_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Lista de Elementos"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.Derlist = []
        self.namelist = []

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ### ElementList - TreeWidget
        self.ElementList_GroupBox = QGroupBox("")
        self.ElementList_GroupBox.setFixedWidth(400)
        self.ElementList_GroupBox.setFixedHeight(400)

        self.ElementList_GroupBox_Layout = QGridLayout()
        self.ElementList_GroupBox_TreeWidget = QTreeWidget()
        self.ElementList_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Elemento'])
        self.ElementList_GroupBox_TreeWidget.setColumnWidth(0, 150)
        self.ElementList_GroupBox_Layout.addWidget(self.ElementList_GroupBox_TreeWidget, 1, 1, 1, 2)

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignmentFlag.AlignRight)

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

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 2, 1, 1)

        self.ElementList_GroupBox.setLayout(self.ElementList_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.ElementList_GroupBox, 1, 1, 1, 2)

        self.setLayout(self.Dialog_Layout)

    def Accept(self):
        self.Derlist.clear()
        self.namelist.clear()
        checkCont = 0
        for ctd in range(0, self.ElementList_GroupBox_TreeWidget.topLevelItemCount()):
            if self.ElementList_GroupBox_TreeWidget.topLevelItem(ctd).checkState(0) == Qt.CheckState.Checked:
                checkCont += 1

        if checkCont == 0:
            msg = QMessageBox()
            msg.information(self, "Lista de Elementos", "Nenhum elemento selecionado")

        else:
            for ctd in range(0, self.ElementList_GroupBox_TreeWidget.topLevelItemCount()):
                Item = self.ElementList_GroupBox_TreeWidget.topLevelItem(ctd)
                if Item.checkState(0) == Qt.CheckState.Checked:
                    self.Derlist.append(str(Item.text(1)) + "." + str(Item.text(0)))
                    self.namelist.append(Item.text(0))
            self.close()

    def Cancel(self):
        self.close()

    def Update(self):
        for pv in self.OpenDSS.getPVSystem():
            ElementList_TreeWidget_Item(self.ElementList_GroupBox_TreeWidget,
                                        pv,
                                        "PVSystem")
        for storage in self.OpenDSS.getStorage():
            ElementList_TreeWidget_Item(self.ElementList_GroupBox_TreeWidget,
                                        storage,
                                        "Storage")

    def clear(self):
        self.ElementList_GroupBox_TreeWidget.clear()

class ElementList_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent,  name, element):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(ElementList_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Name:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.setCheckState(0, Qt.CheckState.Unchecked)

        ## Column 1 - Element:
        self.setText(1, element)