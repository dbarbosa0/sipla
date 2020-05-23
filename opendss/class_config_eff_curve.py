from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLineEdit, QLabel, QWidget
from PyQt5.QtCore import Qt


import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception



class C_Config_EffCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva de Eficiência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._nPointsLoadDef = 0
        self._nStepSizeDef = 0
        self._nStepSizeTimeDef = ""

        self._dataLoadShapes = {}

        self.InitUI()

    def InitUI(self):


        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(850, 475)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog


        ### Curvas de Eficiências - TreeWidget
        self.EffCurve_GroupBox = QGroupBox("Curvas de Eficiência")
        self.EffCurve_GroupBox.setFixedWidth(450)

        self.EffCurve_GroupBox_Layout = QGridLayout()
        self.EffCurve_GroupBox_TreeWidget = QTreeWidget()
        self.EffCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos X', 'Pontos Y'])
        self.EffCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        ### Label
        self.EffCurve_GroupBox_Label = QLabel(
            "Pontos X: Eficiência do inversor em p.u.\n\
Pontos Y: Potência aparente (kVA) em p.u.")
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Label, 2, 1, 1, 2)


        ### Botões adicionar/remover curvas
        self.EffCurve_GroupBox_Remover_Btn = QPushButton("Remover")
        self.EffCurve_GroupBox_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        # self.Shapes_GroupBox_Remover_Btn.setFixedWidth(80)
        #self.EffCurve_GroupBox_Remover_Btn.clicked.connect(self.removeEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Remover_Btn, 3, 1, 1, 1)

        self.EffCurve_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.EffCurve_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.EffCurve_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.EffCurve_GroupBox_Adicionar_Btn.clicked.connect(self.addEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Adicionar_Btn, 3, 2, 1, 1)

        self.EffCurve_GroupBox_Import_Btn = QPushButton("Importar")
        self.EffCurve_GroupBox_Import_Btn.setIcon(QIcon('img/icon_import_csv.png'))
        # self.EffCurve_GroupBox_Import_Btn.setFixedWidth(80)
        #self.EffCurve_GroupBox_Import_Btn.clicked.connect(self.csvImport)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Import_Btn, 4, 1, 1, 1)

        self.EffCurve_GroupBox_Export_Btn = QPushButton("Exportar")
        self.EffCurve_GroupBox_Export_Btn.setIcon(QIcon('img/icon_export_csv.png'))
        # self.EffCurve_GroupBox_Export_Btn.setFixedWidth(80)
        #self.EffCurve_GroupBox_Export_Btn.clicked.connect(self.csvExport)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Export_Btn, 4, 2, 1, 1)

        self.EffCurve_GroupBox.setLayout(self.EffCurve_GroupBox_Layout)

        #########################################################

        self.EffCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.EffCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        # self.Shapes_GroupBox_Show_Btn.setFixedWidth(100)
        self.EffCurve_GroupBox_Show_Btn.clicked.connect(self.viewEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Show_Btn, 5, 1, 1, 2)

        self.Dialog_Layout.addWidget(self.EffCurve_GroupBox, 1, 1, 1, 1)

        #########################################################

        ### Curvas de Eficiência - Plot
        self.View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) de Eficiência")
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
        #self.Dialog_Btns_Cancel_Btn.clicked.connect(self.Cancel)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        #self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def addEffCurve(self):

        inputLoadName, inputOk = QInputDialog.getText(self, 'Curvas de Eficiência','Entre com o nome da nova Curva de\nEficiência do Inversor:')

        if inputOk:
            countName = 0
            for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.name == str(inputLoadName):
                    countName += 1

            if countName == 0:
                ptsX = [0.1, 0.2, 0.4, 1.0]
                ptsX = str(ptsX).strip('[]').replace("'", "")

                ptsY = [0.86, 0.9, 0.93, 0.97]
                ptsY = str(ptsY).strip('[]').replace("'", "")

                Config_EffCurve_GroupBox_TreeWidget_Item(self.EffCurve_GroupBox_TreeWidget,
                                                         inputLoadName,
                                                         ptsX,
                                                         ptsY,
                                                         cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
            else:
                msg = QMessageBox()
                msg.information(self, 'Curvas de Eficiência',
                                "Não foi possível adicionar a curva de eficiência!\nCurva já existente!")

    def viewEffCurve(self):

        #Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add Axis Labels
        self.graphWidget.setLabel('left', 'Pot. aparente (p.u.)', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Eficiência (p.u.)', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        countSelected = 0
        for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:

                pen = pyqtgraph.mkPen(color = Item.getColorRGB())

                pointsXList = Item.getPointsXList()
                pointsYList = Item.getPointsYList()

                self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())

                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência', "Nenhuma curva selecionada para visualização!")


class Config_EffCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent,  name, pointsX, pointsY, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_EffCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_EffCurve = C_Config_EffCurve_Dialog()
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

    def getPoints(self):
        return self.text(2)

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