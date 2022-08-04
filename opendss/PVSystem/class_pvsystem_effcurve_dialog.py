from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLineEdit, QLabel, \
    QWidget
from PyQt5.QtCore import Qt
from opendss.PVSystem.class_pvsystem_effcurve_import import C_Eff_Curve_Import

import csv
import random
import pyqtgraph
import config as cfg



class C_Config_EffCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Curva de Eficiência"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.effcurve_import = C_Eff_Curve_Import()
        self.effcurve_name = ''
        self.eff_xpoints = ''
        self.eff_ypoints = ''
        self.eff_import_ok = self.effcurve_import.Eff_Curve_Btns_Dialog_Ok_Btn
        self.eff_import_ok.clicked.connect(self.teste)
        self.dataEffCurve = {}
        self.list_curve_names = []
        self.EffCurve_list = []

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(850, 475)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ### Curvas de Eficiência - TreeWidget
        self.EffCurve_GroupBox = QGroupBox("Curvas de Eficiência")
        self.EffCurve_GroupBox.setFixedWidth(450)

        self.EffCurve_GroupBox_Layout = QGridLayout()
        self.EffCurve_GroupBox_TreeWidget = QTreeWidget()
        self.EffCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos X', 'Pontos Y'])
        self.EffCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        ### Label
        self.EffCurve_GroupBox_Label = QLabel(
            "Pontos X: Potência aparente em p.u.\n\
Pontos Y: Eficiência do inversor em p.u.")
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Label, 2, 1, 1, 2)

        ### Botões adicionar/remover/visualizar curvas

        self.EffCurve_GroupBox_Add_Btn = QPushButton("Adicionar")
        self.EffCurve_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.EffCurve_GroupBox_Add_Btn.setFixedWidth(80)
        self.EffCurve_GroupBox_Add_Btn.clicked.connect(self.open_Eff_import)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Add_Btn, 3, 2, 1, 1)

        self.EffCurve_GroupBox_Remove_Btn = QPushButton("Remover")
        self.EffCurve_GroupBox_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        # self.Shapes_GroupBox_Remove_Btn.setFixedWidth(80)
        self.EffCurve_GroupBox_Remove_Btn.clicked.connect(self.removeEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Remove_Btn, 3, 1, 1, 1)

        self.EffCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.EffCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        # self.Shapes_GroupBox_Show_Btn.setFixedWidth(100)
        self.EffCurve_GroupBox_Show_Btn.clicked.connect(self.viewEffCurve)
        self.EffCurve_GroupBox_Layout.addWidget(self.EffCurve_GroupBox_Show_Btn, 4, 1, 1, 2)

        self.EffCurve_GroupBox.setLayout(self.EffCurve_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.EffCurve_GroupBox, 1, 1, 1, 1)

        #########################################################

        # Curvas de Eficiência - Groupbox Plot
        self.EffCurve_View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) de Eficiência")
        self.EffCurve_View_GroupBox_Layout = QHBoxLayout()

        self.graphWidget = pyqtgraph.PlotWidget()
        self.EffCurve_View_GroupBox_Layout.addWidget(self.graphWidget)

        self.EffCurve_View_GroupBox.setLayout(self.EffCurve_View_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.EffCurve_View_GroupBox, 1, 2, 1, 2)

        ###########################################################

        # Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.Cancel)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Ok)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def open_Eff_import(self):
        self.effcurve_import.show()

    def teste(self):
        if self.effcurve_import.curve_name not in self.list_curve_names and self.effcurve_import.curve_name != '':

            self.effcurve_name = self.effcurve_import.curve_name
            self.list_curve_names.append(self.effcurve_name)
            self.eff_xpoints = self.effcurve_import.x_axys
            self.eff_ypoints = self.effcurve_import.y_axys

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
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Carga')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:

            for ctd in range(self.EffCurve_GroupBox_TreeWidget.topLevelItemCount(), 0, -1):
                Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd - 1)

                if Item.checkState(0) == Qt.Checked:
                    self.EffCurve_GroupBox_TreeWidget.takeTopLevelItem(ctd - 1)
                    for index, item in enumerate(self.list_curve_names):
                        if item == Item.name:
                            self.list_curve_names.pop(index)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curvas de Eficiência', str(contChecked) + " curva(s) de Eficiência removida(s)!")
            else:
                msg.information(self, 'Curvas de Eficiência', "Nenhuma curva de carga selecionada!")

        else:
            msg.information(self, 'Curvas de Eficiência', "Nenhuma curva de Eficiência foi removida!")

    def viewEffCurve(self):

        # Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Eficiência (p.u.)', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Potência (p.u.)', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        countSelected = 0

        for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                pen = pyqtgraph.mkPen(color=Item.getColorRGB())
                pointsXList = Item.getPointsXList()
                pointsYList = Item.getPointsYList()
                self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10,
                                      symbolBrush=Item.getColorRGB())
                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Eficiência', "Nenhuma curva selecionada para visualização!")

    def Cancel(self):
        self.graphWidget.clear()
        self.close()

    def Ok(self):
        self.setDataEffCurve()
        self.close()

    def setDataEffCurve(self):
        try:
            for ctd in range(0, self.EffCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.EffCurve_GroupBox_TreeWidget.topLevelItem(ctd)

                self.dataEffCurve["EffCurveName"] = Item.name
                self.dataEffCurve["npts"] = str(len(Item.getPointsXList()))
                self.dataEffCurve["Xarray"] = Item.getPointsXList()
                self.dataEffCurve["Yarray"] = Item.getPointsYList()
        except:
            pass
        #print(self.EffCurve_list)

    def default_entries(self):
        self.dataEffCurve = {}
        self.effcurve_import.define_default_entries()
        self.dataEffCurve["EffCurveName"] = self.effcurve_import.curve_name
        self.dataEffCurve["npts"] = self.effcurve_import.npts
        self.dataEffCurve["Xarray"] = self.effcurve_import.x_axys
        self.dataEffCurve["Yarray"] = self.effcurve_import.y_axys

class Config_EffCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, pointsX, pointsY, color):
        super(Config_EffCurve_GroupBox_TreeWidget_Item, self).__init__(parent)
        self.Config_EffCurve = C_Config_EffCurve_Dialog()

        # Column 0 - Text:

        self.setText(0, name)
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
