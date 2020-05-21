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

        self.addDialog = C_Add_EffCurve_Dialog()
    def InitUI(self):


        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(800, 500)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog


        ### Curvas de Eficiências - TreeWidget
        self.EffCurve_GroupBox = QGroupBox("Curvas de Eficiência")
        self.EffCurve_GroupBox.setFixedWidth(400)

        self.EffCurve_GroupBox_Layout = QGridLayout()
        self.EffCurve_GroupBox_TreeWidget = QTreeWidget()
        self.EffCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos Y', 'Pontos X'])
        self.EffCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

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
        #self.EffCurve_GroupBox_Show_Btn.clicked.connect(self.viewEffCurve)
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
        self.addDialog.show()




class C_Add_EffCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Adicionar Curva de Eficiência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

        self.Config_EffCurve = C_Config_EffCurve_Dialog()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()

        self.Label = QLabel("Escreva os pontos separados por vírgula")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)
        self.Label_Nome = QLabel("Nome")
        self.Dialog_Layout.addWidget(self.Label_Nome, 2, 1, 1, 1)
        self.Label_PontosX = QLabel("Pontos do eixo X")
        self.Dialog_Layout.addWidget(self.Label_PontosX, 3, 1, 1, 1)
        self.Label_PontosY = QLabel("Pontos do eixo Y")
        self.Dialog_Layout.addWidget(self.Label_PontosY, 4, 1, 1, 1)

        self.LineEdit_Nome = QLineEdit()
        self.Dialog_Layout.addWidget(self.LineEdit_Nome, 2, 2, 1, 1)
        self.LineEdit_PontosX = QLineEdit()
        self.Dialog_Layout.addWidget(self.LineEdit_PontosX, 3, 2, 1, 1)
        self.LineEdit_PontosY = QLineEdit()
        self.Dialog_Layout.addWidget(self.LineEdit_PontosY, 4, 2, 1, 1)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        #self.OK_Btn.clicked.connect(self.ConfirmAddEffCurve)
        self.Dialog_Layout.addWidget(self.OK_Btn, 5, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        #self.Cancel_Btn.clicked.connect(self.CancelAddEffCurve)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 5, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def ConfirmAddEffCurve(self):
        ptsX = self.LineEdit_PontosX.text()
        ptsX = [float(ctd) for ctd in ptsX.split(',')]

        ptsY = self.LineEdit_PontosY.text()
        ptsY = [float(ctd) for ctd in ptsY.split(',')]
    #
    #     countName = 0
    #     for ctd in range(0, self.Config_EffCurve.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):
    #
    #         Item = self.Config_EffCurve.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)
    #
    #         if Item.name == str(self.LineEdit_Nome):
    #             countName += 1
    #
    #     if countName == 0:
    #         pts = [0 for ctd in range(0, self.nPointsLoadDef)]
    #         pts = str(pts).strip('[]').replace("'", "")
    #         Config_LoadShape_Shapes_GroupBox_TreeWidget_Item(self.Shapes_GroupBox_TreeWidget,
    #                                                          self.Shapes_GroupBox_Checkbox_SelectAll.checkState(),
    #                                                          inputLoadName, pts,
    #                                                          cfg.colorsList[
    #                                                              random.randint(0, len(cfg.colorsList) - 1)])
    #     else:
    #         msg = QMessageBox()
    #         msg.information(self, 'Curvas de Carga',
    #                         "Não foi possível adicionar a curva de carga!\nCurva de carga já existente!")
#
#     def CancelAddEffCurve(self):
#         pass
#
#
# class Config_EffCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
#     def __init__(self, parent,  name, pointsX, pointsY, color):
#         ## Init super class ( QtGui.QTreeWidgetItem )
#         super(Config_EffCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
#
#         ## Column 0 - Text:
#
#
#         self.setText(0, name)
#         self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
#         self.setCheckState(0, Qt.Unchecked)
#
#         self.color = color
#
#         ## Column 1 - Button:
#         self.TreeWidget_Item_Btn = QPushButton()
#         self.TreeWidget_Item_Btn.setFixedSize(20, 20)
#         self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
#         self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
#         self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)
#
#         ## Column 2 - PontosX:
#         self.setText(2, pointsX)
#
#         ## Column 3 - PontosX:
#         self.setText(2, pointsY)
#
#     @property
#     def name(self):
#         return self.text(0)
#
#     def getPoints(self):
#         return self.text(2)
#
#     def getPointsList(self):
#         points = [float(x) for x in self.text(2).split(',')]
#         return points
#
#     def getColor(self):
#         return self.color
#
#     def getColorRGB(self):
#         return QColor(self.getColor()).getRgb()
#
#     def setColor(self):
#         self.openColorDialog()
#
#     def openColorDialog(self):
#
#         colorSelectDialog = QColorDialog()
#
#         colorSelected = colorSelectDialog.getColor()
#
#         if colorSelected.isValid():
#             self.color = colorSelected.name()
#             self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + colorSelected.name() + '}')

