from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QColorDialog, QMessageBox, QInputDialog, QLabel
from PyQt5.QtCore import Qt

import random
import pyqtgraph
import config as cfg
import class_exception


class C_Config_CurveXY_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva XY"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(850, 475)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog


        ### Curvas XY - TreeWidget
        self.XYCurve_GroupBox = QGroupBox("")
        self.XYCurve_GroupBox.setFixedWidth(450)

        self.XYCurve_GroupBox_Layout = QGridLayout()
        self.XYCurve_GroupBox_TreeWidget = QTreeWidget()
        self.XYCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos X', 'Pontos Y'])
        self.XYCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.XYCurve_GroupBox_Layout.addWidget(self.XYCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        ### Label
        self.XYCurve_GroupBox_Label = QLabel(
            "vcc_curve1 [Pontos X: Tensão (p.u.) e Pontos Y: Potência reativa disponível (p.u.)]\n\
voltwatt_curve [Pontos X: Tensão (p.u.) e Pontos Y: Potência ativa disponível (p.u.)]")
        self.XYCurve_GroupBox_Layout.addWidget(self.XYCurve_GroupBox_Label, 2, 1, 1, 2)

        ### Botões adicionar/remover curvas
        self.XYCurve_GroupBox_Delete_Btn = QPushButton("Remover")
        self.XYCurve_GroupBox_Delete_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.XYCurve_GroupBox_Delete_Btn.clicked.connect(self.deleteXYCurve)
        self.XYCurve_GroupBox_Layout.addWidget(self.XYCurve_GroupBox_Delete_Btn, 3, 1, 1, 1)

        self.XYCurve_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.XYCurve_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        self.XYCurve_GroupBox_Adicionar_Btn.clicked.connect(self.addXYCurve)
        self.XYCurve_GroupBox_Layout.addWidget(self.XYCurve_GroupBox_Adicionar_Btn, 3, 2, 1, 1)

        self.XYCurve_GroupBox.setLayout(self.XYCurve_GroupBox_Layout)

        #########################################################

        self.XYCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.XYCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        self.XYCurve_GroupBox_Show_Btn.clicked.connect(self.viewXYCurve)
        self.XYCurve_GroupBox_Layout.addWidget(self.XYCurve_GroupBox_Show_Btn, 4, 1, 1, 2)

        self.Dialog_Layout.addWidget(self.XYCurve_GroupBox, 1, 1, 1, 1)

        #########################################################

        ### Curvas Plot
        self.View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) XY")
        self.View_GroupBox_Layout = QHBoxLayout()

        self.graphWidget = pyqtgraph.PlotWidget()

        self.View_GroupBox_Layout.addWidget(self.graphWidget)
        self.View_GroupBox.setLayout(self.View_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.View_GroupBox, 1, 2, 1, 2)

        ###########################################################

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

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def deleteXYCurve(self):
        pass

    def addXYCurve(self):
        pass

    def viewXYCurve(self):
        pass

    def Accept(self):
        pass

    def Cancel(self):
        pass


class Config_XYCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent,  name, pointsX, pointsY, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_XYCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_XYCurve = C_Config_XYCurve_Dialog()
        ## Column 0 - Text:


        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)

        self.color = color

        ## Column 1 - Button:
        self.TreeWidget_Item_Btn = QPushButton()
        self.TreeWidget_Item_Btn.setFixedSize(20, 20)
        self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
        self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
        self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)

        ## Column 2 - PontosX:
        self.setText(2, pointsX)

        ## Column 3 - PontosY:
        self.setText(3, pointsY)

    @property
    def name(self):
        return self.text(0)

    def getPointsX(self):
        return self.text(2)

    def getPointsY(self):
        return self.text(3)

    def getPointsXList(self):
        pointsX = [float(x) for x in self.text(2).split(',')]
        return pointsX

    def getPointsYList(self):
        pointsY = [float(y) for y in self.text(3).split(',')]
        return pointsY

    def getColor(self):
        return self.color

    def getColorRGB(self):
        return QColor(self.getColor()).getRgb()

    def setColor(self):
        self.openColorDialog()

    def openColorDialog(self):

        colorSelectDialog = QColorDialog()

        colorSelected = colorSelectDialog.getColor()

        if colorSelected.isValid():
            self.color = colorSelected.name()
            self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + colorSelected.name() + '}')