from PyQt6.QtGui import QColor, QIcon, QGuiApplication
from PyQt6.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QColorDialog, QMessageBox, QInputDialog, QLabel, QWidget
from PyQt6.QtCore import Qt


import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception
import unidecode
import opendss.storage.class_add_effcurve



class C_Config_EffCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva de Eficiência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.dataEffCurve = {}
        self.AddEffCurve = opendss.storage.class_add_effcurve.C_Add_EffCurve()
        self.AddEffCurve.Eff_Curve_Btns_Dialog_Ok_Btn.clicked.connect(self.AddEffCurveToTreeWidget)

        self._Storages = []

        self.InitUI()

    @property
    def Storages(self):
        return self._Storages

    @Storages.setter
    def Storages(self, value):
        self._Storages = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(850, 475)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMinMaxButtonsHint)

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
            "Pontos X: Potência aparente (kVA) em p.u.\n\
Pontos Y: Eficiência do inversor em p.u.")
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Label, 2, 1, 1, 2)

        ### Botões adicionar/remover curvas
        self.EffCurve_GroupBox_Remover_Btn = QPushButton("Remover")
        self.EffCurve_GroupBox_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        # self.Shapes_GroupBox_Remover_Btn.setFixedWidth(80)
        self.EffCurve_GroupBox_Remover_Btn.clicked.connect(self.removeEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Remover_Btn, 3, 1, 1, 1)

        self.EffCurve_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.EffCurve_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.EffCurve_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.EffCurve_GroupBox_Adicionar_Btn.clicked.connect(self.addEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Adicionar_Btn, 3, 2, 1, 1)

        self.EffCurve_GroupBox.setLayout(self.EffCurve_GroupBox_Layout)

        #########################################################

        self.EffCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.EffCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        # self.Shapes_GroupBox_Show_Btn.setFixedWidth(100)
        self.EffCurve_GroupBox_Show_Btn.clicked.connect(self.viewEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Show_Btn, 4, 1, 1, 2)

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

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def addEffCurve(self):
        self.AddEffCurve.exec()
        self.AddEffCurve.centralize()

    def AddEffCurveToTreeWidget(self):
        ItemCount = 0

        for ctd in range(self.EffCurve_GroupBox_TreeWidget.topLevelItemCount(), 0, -1):
            Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd - 1)
            if self.AddEffCurve.curve_name == Item.name or self.AddEffCurve.curve_name == '':
                ItemCount += 1

        if ItemCount == 0:
            self.effcurve_name = self.AddEffCurve.curve_name
            self.eff_xpoints = self.AddEffCurve.x_axys
            self.eff_ypoints = self.AddEffCurve.y_axys

            Config_EffCurve_GroupBox_TreeWidget_Item(self.EffCurve_GroupBox_TreeWidget,
                                                     self.effcurve_name,
                                                     self.eff_xpoints,
                                                     self.eff_ypoints,
                                                     cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
        else:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência',
                            "Não foi possível adicionar a curva de Eficiência!\nCurva já existente ou dados inválidos!")

    def removeEffCurve(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Carga')
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        retval = msg.exec()

        contChecked = 0
        if retval == QMessageBox.StandardButton.Yes:

            for ctd in range(self.EffCurve_GroupBox_TreeWidget.topLevelItemCount(), 0, -1):
                Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd-1)

                if Item.checkState(0) == Qt.CheckState.Checked:
                    self.EffCurve_GroupBox_TreeWidget.takeTopLevelItem(ctd-1)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curvas de Eficiência', str(contChecked) + " curva(s) de eficiência removida(s)!")
            else:
                msg.information(self, 'Curvas de Eficiência', "Nenhuma curva de carga selecionada!")

        else:
            msg.information(self, 'Curvas de Eficiência', "Nenhuma curva de eficiência foi removida!")

    def viewEffCurve(self):

        #Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add Axis Labels
        self.graphWidget.setLabel('left', 'Eficiência (p.u.)', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Pot. aparente (p.u.)', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        countSelected = 0
        for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.CheckState.Checked:
                if self.checkEffCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                    pen = pyqtgraph.mkPen(color = Item.getColorRGB())

                    pointsXList = Item.getPointsXList()
                    pointsYList = Item.getPointsYList()
                    self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())

                    countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência', "Nenhuma curva selecionada para visualização!")

    def Cancel(self):
        self.graphWidget.clear()
        self.close()

    def Accept(self):
        self.setDataEffCurve()

    def checkEffCurve(self, nameEffCurve, pointsXEffCurve, pointsYEffCurve):

        msgText = ''
        pointsXEffCurve = pointsXEffCurve.split(',')
        pointsYEffCurve = pointsYEffCurve.split(',')

        if len(pointsXEffCurve) != len(pointsYEffCurve):
            msgText += "Erro na curva " + nameEffCurve + ". O número de pontos do eixo das coordenadas está diferente do eixo das abcissas! \n"
        else:
            for ctd in pointsXEffCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de eficiência!"
            for ctd in pointsYEffCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de eficiência!"

        if msgText != "":
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência',
                            "Não foi possível adicionar a curva de Eficiência:\n" + msgText)
            return False
        else:
            return True

    def setDataEffCurve(self):
        self.EffCurveXarray = []
        self.EffCurveYarray = []
        self.dataEffCurve = {}
        checkCont = 0
        for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)
            if Item.checkState(0) == Qt.CheckState.Checked:
                checkCont += 1

        if checkCont > 1:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência', "Selecione somente uma curva!")
        elif checkCont == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência', "Selecione ao menos uma curva!")

        elif checkCont == 1:
            for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):
                Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)
                if Item.checkState(0) == Qt.CheckState.Checked:

                    if self.checkEffCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                        self.EffCurveXarray = Item.getPointsXList()
                        self.EffCurveYarray = Item.getPointsYList()
                        self.dataEffCurve["EffCurveName"] = Item.name
                        self.dataEffCurve["npts"] = str(len(self.EffCurveXarray))
                        self.dataEffCurve["Xarray"] = self.EffCurveXarray
                        self.dataEffCurve["Yarray"] = self.EffCurveYarray
                        self.close()

    def centralize(self):
        qr = self.frameGeometry()
        centerpoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(centerpoint)
        self.move(qr.topLeft())


class Config_EffCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent,  name, pointsX, pointsY, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_EffCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_EffCurve = C_Config_EffCurve_Dialog()
        ## Column 0 - Text:


        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)
        self.setCheckState(0, Qt.CheckState.Unchecked)

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