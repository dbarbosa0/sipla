from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLineEdit, QLabel, \
    QWidget
from PyQt5.QtCore import Qt
from opendss.PVSystem.class_pvsystem_ptcurve_import import C_PT_Curve_Import

import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception


class C_Config_PTCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva de Potencia x Temperatura"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.ptcurve_import = C_PT_Curve_Import()
        self.ptcurve_name = ''
        self.pt_xpoints = ''
        self.pt_ypoints = ''
        self.pt_import_ok = self.ptcurve_import.PT_Curve_Btns_Dialog_Ok_Btn
        self.dataPTCurve = {}

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(850, 475)

        # self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ### Curvas de Potência-Temperatura - TreeWidget
        self.PTCurve_GroupBox = QGroupBox("Curvas de Potência x Temperatura")
        self.PTCurve_GroupBox.setFixedWidth(450)

        self.PTCurve_GroupBox_Layout = QGridLayout()
        self.PTCurve_GroupBox_TreeWidget = QTreeWidget()
        self.PTCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos X', 'Pontos Y'])
        self.PTCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.PTCurve_GroupBox_Layout.addWidget(self.PTCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        ### Label
        self.PTCurve_GroupBox_Label = QLabel(
            "Pontos X: Temperatura de operação em °C\n\
Pontos Y: Potência aparente (kVA) em p.u.")
        self.PTCurve_GroupBox_Layout.addWidget(self.PTCurve_GroupBox_Label, 2, 1, 1, 2)

        ### Botões adicionar/remover/visualizar curvas

        self.PTCurve_GroupBox_Add_Btn = QPushButton("Adicionar")
        self.PTCurve_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.EffCurve_GroupBox_Add_Btn.setFixedWidth(80)
        self.PTCurve_GroupBox_Add_Btn.clicked.connect(self.open_eff_import)
        self.PTCurve_GroupBox_Layout.addWidget(self.PTCurve_GroupBox_Add_Btn, 3, 2, 1, 1)

        self.PTCurve_GroupBox_Remove_Btn = QPushButton("Remover")
        self.PTCurve_GroupBox_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        # self.Shapes_GroupBox_Remove_Btn.setFixedWidth(80)
        self.PTCurve_GroupBox_Remove_Btn.clicked.connect(self.removeEffCurve)
        self.PTCurve_GroupBox_Layout.addWidget(self.PTCurve_GroupBox_Remove_Btn, 3, 1, 1, 1)

        self.PTCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.PTCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        # self.Shapes_GroupBox_Show_Btn.setFixedWidth(100)
        self.PTCurve_GroupBox_Show_Btn.clicked.connect(self.viewEffCurve)
        self.PTCurve_GroupBox_Layout.addWidget(self.PTCurve_GroupBox_Show_Btn, 4, 1, 1, 2)

        self.PTCurve_GroupBox.setLayout(self.PTCurve_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.PTCurve_GroupBox, 1, 1, 1, 1)

        #########################################################

        # Curvas de Eficiência - Groupbox Plot
        self.PTCurve_View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) de Potencia x Temperatura")
        self.PTCurve_View_GroupBox_Layout = QHBoxLayout()

        self.graphWidget = pyqtgraph.PlotWidget()
        self.PTCurve_View_GroupBox_Layout.addWidget(self.graphWidget)

        self.PTCurve_View_GroupBox.setLayout(self.PTCurve_View_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.PTCurve_View_GroupBox, 1, 2, 1, 2)

        ###########################################################

        # Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.Cancel)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Next_Btn = QPushButton("Ok")
        self.Dialog_Btns_Next_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Next_Btn.setFixedWidth(100)
        self.Dialog_Btns_Next_Btn.clicked.connect(self.Next)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Next_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def open_eff_import(self):
        self.ptcurve_import.show()
        self.pt_import_ok.clicked.connect(self.teste)

    def teste(self):
        self.ptcurve_name = self.ptcurve_import.curve_name
        self.pt_xpoints = self.ptcurve_import.x_axys
        self.pt_ypoints = self.ptcurve_import.y_axys

        countName = 0
        for ctd in range(0, self.PTCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.PTCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.name == str(self.ptcurve_name):
                countName += 1

        if countName == 0:
            ptsX = self.pt_xpoints
            ptsY = self.pt_ypoints

            Config_PTCurve_GroupBox_TreeWidget_Item(self.PTCurve_GroupBox_TreeWidget,
                                                    self.ptcurve_name,
                                                    ptsX,
                                                    ptsY,
                                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
        else:
            msg = QMessageBox()
            msg.information(self, 'Potencia x Temperatura',
                            "Não foi possível adicionar a curva de Potencia x Temperatura!\nCurva já existente!")

    def removeEffCurve(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Carga')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:

            for ctd in range(self.PTCurve_GroupBox_TreeWidget.topLevelItemCount(), 0, -1):
                Item = self.PTCurve_GroupBox_TreeWidget.topLevelItem(ctd - 1)

                if Item.checkState(0) == Qt.Checked:
                    self.PTCurve_GroupBox_TreeWidget.takeTopLevelItem(ctd - 1)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curvas de Potencia x Temperatura', str(contChecked) + " curva(s) de Potencia x Temperatura removida(s)!")
            else:
                msg.information(self, 'Curvas de Potencia x Temperatura', "Nenhuma curva de carga selecionada!")

        else:
            msg.information(self, 'Curvas de Potencia x Temperatura', "Nenhuma curva de Potencia x Temperatura foi removida!")

    def viewEffCurve(self):

        # Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Pot. aparente (p.u.)', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Temperatura (°C)', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        countSelected = 0
        for ctd in range(0, self.PTCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.PTCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                if self.checkEffCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                    pen = pyqtgraph.mkPen(color=Item.getColorRGB())

                    pointsXList = Item.getPointsXList()
                    pointsYList = Item.getPointsYList()
                    self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10,
                                          symbolBrush=Item.getColorRGB())

                    countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Potencia x Temperatura', "Nenhuma curva selecionada para visualização!")

    def Cancel(self):
        self.PTCurve_GroupBox_TreeWidget.clear()
        self.graphWidget.clear()
        self.close()

    def Next(self):
        self.setDataEffCurve()
        self.close()

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
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de Potencia x Temperatura!"
            for ctd in pointsYEffCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de Potencia x Temperatura!"

        if msgText != "":
            msg = QMessageBox()
            msg.information(self, 'Curvas de Potencia x Temperatura',
                            "Não foi possível adicionar a curva de Potencia x Temperatura:\n" + msgText)
            return False
        else:
            return True

    def setDataEffCurve(self):
        self.PTCurveXarray = []
        self.PTCurveYarray = []
        self.dataPTCurve = {}
        checkCont = 0
        try:
            for ctd in range(0, self.PTCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.PTCurve_GroupBox_TreeWidget.topLevelItem(ctd)
                if Item.checkState(0) == Qt.Checked:
                    checkCont += 1
                if checkCont > 1:
                    raise class_exception.ExecConfigOpenDSS("Erro na seleção da Curva de Potencia x Temperatura ",
                                                            "Selecione somente uma curva!")
                elif checkCont == 0:
                    raise class_exception.ExecConfigOpenDSS("Erro na seleção da Curva de Potencia x Temperatura ",
                                                            "Selecione ao menos uma curva!")
                else:
                    if self.checkEffCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                        self.PTCurveXarray = Item.getPointsXList()
                        self.PTCurveYarray = Item.getPointsYList()
                        self.dataPTCurve["EffCurveName"] = Item.name
                        self.dataPTCurve["npts"] = str(len(self.PTCurveXarray))
                        self.dataPTCurve["Xarray"] = self.PTCurveXarray
                        self.dataPTCurve["Yarray"] = self.PTCurveYarray
                    else:
                        raise class_exception.ExecConfigOpenDSS("Erro na verificação da Curva de Potencia x Temperatura " \
                                                                + Item.name + " !",
                                                                "Verifique se todos os pontos estão presentes!")

        except:
            pass


class Config_PTCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, pointsX, pointsY, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_PTCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_PTCurve = C_Config_PTCurve_Dialog()
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
