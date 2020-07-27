from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QColorDialog, QMessageBox, QInputDialog, QLabel
from PyQt5.QtCore import Qt

import random
import pyqtgraph
import config as cfg


class C_Config_VoltVar_XYCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva XY"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.dataVV_XYCurve = {}

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
        self.XYCurve_GroupBox = QGroupBox("vcc_curve1")
        self.XYCurve_GroupBox.setFixedWidth(450)

        self.XYCurve_GroupBox_Layout = QGridLayout()
        self.XYCurve_GroupBox_TreeWidget = QTreeWidget()
        self.XYCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos X', 'Pontos Y'])
        self.XYCurve_GroupBox_TreeWidget.setColumnWidth(0, 120)
        self.XYCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.XYCurve_GroupBox_Layout.addWidget(self.XYCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        ### Label
        self.XYCurve_GroupBox_Label = QLabel(
            "Pontos X: Tensão (p.u.)\nPontos Y: Potência reativa disponível (p.u.)")
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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curva XY')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:

            for ctd in range(self.XYCurve_GroupBox_TreeWidget.topLevelItemCount(), 0, -1):
                Item = self.XYCurve_GroupBox_TreeWidget.topLevelItem(ctd - 1)

                if Item.checkState(0) == Qt.Checked:
                    self.XYCurve_GroupBox_TreeWidget.takeTopLevelItem(ctd - 1)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curva XY', str(contChecked) + " curva(s) XY removida(s)!")
                self.graphWidget.clear()
            else:
                msg.information(self, 'Curva XY', "Nenhuma curva selecionada!")

        else:
            msg.information(self, 'Curva XY', "Nenhuma Curva XY foi removida!")

    def addXYCurve(self):

        inputLoadName, inputOk = QInputDialog.getText(self, 'Curva XY','Entre com o nome da nova Curva XY:')
        inputLoadName = str(inputLoadName).strip().replace(" ", "_")

        if inputOk:
            countName = 0
            for ctd in range(0, self.XYCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.XYCurve_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.name == str(inputLoadName):
                    countName += 1

            if countName == 0:
                ptsX = [0.5, 0.95, 1.05, 1.5]
                ptsX = str(ptsX).strip('[]').replace("'", "")

                ptsY = [1.0, 1.0, -1.0, -1.0]
                ptsY = str(ptsY).strip('[]').replace("'", "")

                Config_XYCurve_GroupBox_TreeWidget_Item(self.XYCurve_GroupBox_TreeWidget,
                                                         inputLoadName,
                                                         ptsX,
                                                         ptsY,
                                                         cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
            else:
                msg = QMessageBox()
                msg.information(self, 'Curva XY',
                                "Não foi possível adicionar a Curva XY\nCurva já existente!")

    def viewXYCurve(self):

        #Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add Axis Labels
        self.graphWidget.setLabel('left', 'Potência reativa disponível (p.u.)', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Tensão (p.u.)', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        countSelected = 0
        for ctd in range(0, self.XYCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.XYCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                if self.checkXYCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                    pen = pyqtgraph.mkPen(color = Item.getColorRGB())

                    pointsXList = Item.getPointsXList()
                    pointsYList = Item.getPointsYList()
                    self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())

                    countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curva XY', "Nenhuma curva selecionada para visualização!")

    def Accept(self):
        self.XYCurveXarray = []
        self.XYCurveYarray = []
        checkCont = 0

        for ctd in range(0, self.XYCurve_GroupBox_TreeWidget.topLevelItemCount()):
            if self.XYCurve_GroupBox_TreeWidget.topLevelItem(ctd).checkState(0) == Qt.Checked:
                checkCont += 1
                Item = self.XYCurve_GroupBox_TreeWidget.topLevelItem(ctd)

        if checkCont > 1:
            QMessageBox(QMessageBox.Warning, "Curva XY",
                        "Erro na seleção da Curva XY\nSelecione somente uma curva!",
                        QMessageBox.Ok).exec()
        elif checkCont == 0:
            QMessageBox(QMessageBox.Warning, "Curva XY",
                        "Erro na seleção da Curva XY\nSelecione ao menos uma curva!",
                        QMessageBox.Ok).exec()
        else:
            if self.checkXYCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                self.XYCurveXarray = Item.getPointsXList()
                self.XYCurveYarray = Item.getPointsYList()
                self.dataVV_XYCurve["XYCurveName"] = Item.name
                self.dataVV_XYCurve["npts"] = str(len(self.XYCurveXarray))
                self.dataVV_XYCurve["Xarray"] = self.XYCurveXarray
                self.dataVV_XYCurve["Yarray"] = self.XYCurveYarray
                self.close()

    def Cancel(self):
        self.XYCurve_GroupBox_TreeWidget.clear()
        self.graphWidget.clear()
        self.close()

    def checkXYCurve(self, nameXYCurve, XpointsXYCurve, YpointsXYCurve):

        msgText = ''
        XpointsXYCurve = XpointsXYCurve.split(',')
        YpointsXYCurve = YpointsXYCurve.split(',')

        if len(XpointsXYCurve) != len(YpointsXYCurve):
            msgText += "Erro na curva " + nameXYCurve + ". O número de pontos do eixo das coordenadas está diferente do eixo das abcissas! \n"
        else:
            for ctd in XpointsXYCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva XY!"
            for ctd in YpointsXYCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva XY!"

        if msgText != "":
            msg = QMessageBox()
            msg.information(self, 'Curva XY',
                            "Não foi possível adicionar a curva XY:\n" + msgText)
            return False
        else:
            return True

class Config_XYCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent,  name, pointsX, pointsY, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_XYCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_XYCurve = C_Config_VoltVar_XYCurve_Dialog()
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