from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLineEdit, QLabel, \
    QWidget
from PyQt5.QtCore import Qt
from opendss.PVSystem.class_pvsystem_tempcurve_import import C_Temp_Curve_Import

import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception


class C_Config_TempCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva de Temperatura"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.tempcurve_import = C_Temp_Curve_Import()
        self.tempcurve_name = ''
        self.temp_xpoints = ''
        self.temp_ypoints = ''
        self.temp_import_ok = self.tempcurve_import.Temp_Curve_Btns_Dialog_Ok_Btn
        self.datatempCurve = {}

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(850, 475)

        # self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ### Curvas de Eficiências - TreeWidget
        self.TempCurve_GroupBox = QGroupBox("Curvas de Temperatura")
        self.TempCurve_GroupBox.setFixedWidth(450)

        self.TempCurve_GroupBox_Layout = QGridLayout()
        self.TempCurve_GroupBox_TreeWidget = QTreeWidget()
        self.TempCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos X', 'Pontos Y'])
        self.TempCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.TempCurve_GroupBox_Layout.addWidget(self.TempCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        ### Label
        self.TempCurve_GroupBox_Label = QLabel(
            "Pontos X: número de amostras\n\
Pontos Y: Temperatura °C")
        self.TempCurve_GroupBox_Layout.addWidget(self.TempCurve_GroupBox_Label, 2, 1, 1, 2)

        ### Botões adicionar/remover/visualizar curvas

        self.TempCurve_GroupBox_Add_Btn = QPushButton("Adicionar")
        self.TempCurve_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.EffCurve_GroupBox_Add_Btn.setFixedWidth(80)
        self.TempCurve_GroupBox_Add_Btn.clicked.connect(self.open_Irrad_import)
        self.TempCurve_GroupBox_Layout.addWidget(self.TempCurve_GroupBox_Add_Btn, 3, 2, 1, 1)

        self.TempCurve_GroupBox_Remove_Btn = QPushButton("Remover")
        self.TempCurve_GroupBox_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        # self.Shapes_GroupBox_Remove_Btn.setFixedWidth(80)
        self.TempCurve_GroupBox_Remove_Btn.clicked.connect(self.removeEffCurve)
        self.TempCurve_GroupBox_Layout.addWidget(self.TempCurve_GroupBox_Remove_Btn, 3, 1, 1, 1)

        self.TempCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.TempCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        # self.Shapes_GroupBox_Show_Btn.setFixedWidth(100)
        self.TempCurve_GroupBox_Show_Btn.clicked.connect(self.viewEffCurve)
        self.TempCurve_GroupBox_Layout.addWidget(self.TempCurve_GroupBox_Show_Btn, 4, 1, 1, 2)

        self.TempCurve_GroupBox.setLayout(self.TempCurve_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.TempCurve_GroupBox, 1, 1, 1, 1)

        #########################################################

        # Curvas de Eficiência - Groupbox Plot
        self.TempCurve_View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) de Temperatura")
        self.TempCurve_View_GroupBox_Layout = QHBoxLayout()

        self.graphWidget = pyqtgraph.PlotWidget()
        self.TempCurve_View_GroupBox_Layout.addWidget(self.graphWidget)

        self.TempCurve_View_GroupBox.setLayout(self.TempCurve_View_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.TempCurve_View_GroupBox, 1, 2, 1, 2)

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

    def open_Irrad_import(self):
        self.tempcurve_import.show()
        self.temp_import_ok.clicked.connect(self.teste)

    def teste(self):
        self.tempcurve_name = self.tempcurve_import.curve_name
        self.temp_xpoints = self.tempcurve_import.x_axys
        self.temp_ypoints = self.tempcurve_import.y_axys

        countName = 0
        for ctd in range(0, self.TempCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.TempCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.name == str(self.tempcurve_name):
                countName += 1

        if countName == 0:
            ptsX = self.temp_xpoints
            ptsY = self.temp_ypoints

            Config_TempCurve_GroupBox_TreeWidget_Item(self.TempCurve_GroupBox_TreeWidget,
                                                      self.tempcurve_name,
                                                      ptsX,
                                                      ptsY,
                                                      cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
        else:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Temperatura',
                            "Não foi possível adicionar a curva de Temperatura!\nCurva já existente!")

    def removeEffCurve(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Carga')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:

            for ctd in range(self.TempCurve_GroupBox_TreeWidget.topLevelItemCount(), 0, -1):
                Item = self.TempCurve_GroupBox_TreeWidget.topLevelItem(ctd - 1)

                if Item.checkState(0) == Qt.Checked:
                    self.TempCurve_GroupBox_TreeWidget.takeTopLevelItem(ctd - 1)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curvas de Temperatura', str(contChecked) + " curva(s) de temperatura removida(s)!")
            else:
                msg.information(self, 'Curvas de Temperatura', "Nenhuma curva de carga selecionada!")

        else:
            msg.information(self, 'Curvas de Temperatura', "Nenhuma curva de Temperatura foi removida!")

    def viewEffCurve(self):

        # Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Irradiação (p.u.)', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Amostras', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        countSelected = 0
        for ctd in range(0, self.TempCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.TempCurve_GroupBox_TreeWidget.topLevelItem(ctd)

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
            msg.information(self, 'Curvas de Temperatura', "Nenhuma curva selecionada para visualização!")

    def Cancel(self):
        self.TempCurve_GroupBox_TreeWidget.clear()
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
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de Irradiação!"
            for ctd in pointsYEffCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de Irradiação!"

        if msgText != "":
            msg = QMessageBox()
            msg.information(self, 'Curvas de Irradiação',
                            "Não foi possível adicionar a curva de Irradiação:\n" + msgText)
            return False
        else:
            return True

    def setDataEffCurve(self):
        self.IrradCurveXarray = []
        self.IrradCurveYarray = []
        self.datatempCurve = {}
        checkCont = 0
        try:
            for ctd in range(0, self.TempCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.TempCurve_GroupBox_TreeWidget.topLevelItem(ctd)
                if Item.checkState(0) == Qt.Checked:
                    checkCont += 1
                if checkCont > 1:
                    raise class_exception.ExecConfigOpenDSS("Erro na seleção da Curva de Irradiação ",
                                                            "Selecione somente uma curva!")
                elif checkCont == 0:
                    raise class_exception.ExecConfigOpenDSS("Erro na seleção da Curva de Irradiação ",
                                                            "Selecione ao menos uma curva!")
                else:
                    if self.checkEffCurve(Item.name, Item.getPointsX(), Item.getPointsY()):
                        self.IrradCurveXarray = Item.getPointsXList()
                        self.IrradCurveYarray = Item.getPointsYList()
                        self.datatempCurve["EffCurveName"] = Item.name
                        self.datatempCurve["npts"] = str(len(self.IrradCurveXarray))
                        self.datatempCurve["Xarray"] = self.IrradCurveXarray
                        self.datatempCurve["Yarray"] = self.IrradCurveYarray
                    else:
                        raise class_exception.ExecConfigOpenDSS("Erro na verificação da Curva de Irradiação " \
                                                                + Item.name + " !",
                                                                "Verifique se todos os pontos estão presentes!")

        except:
            pass


class Config_TempCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, pointsX, pointsY, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_TempCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_EffCurve = C_Config_TempCurve_Dialog()
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
