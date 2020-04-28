from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox,QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt

import pyqtgraph
import random
import config as cfg

import opendss.class_opendss


class C_Config_Plot_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Monitor Plot"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()


    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(800, 500)

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        ##Layout principal
        self.Dialog_Layout = QGridLayout()

        ##GroupBOX Monitor
        self.Monitor_GroupBox = QGroupBox("Monitores")
        self.Monitor_GroupBox.setMaximumWidth(500)
        self.Monitor_GroupBox_Layout = QVBoxLayout()
        self.Monitor_GroupBox.setLayout(self.Monitor_GroupBox_Layout)

        ##GroupBOx Select
        self.Monitor_Select_GroupBox = QGroupBox("Selecione o Monitor")
        self.Monitor_Select_GroupBox.setMaximumHeight(200)
        self.Monitor_Select_GroupBox_Layout = QHBoxLayout()
        self.Monitor_Select_GroupBox_ComboBox = QComboBox()
        self.Monitor_Select_GroupBox_ComboBox.setMinimumWidth(200)
        self.Monitor_Select_GroupBox_Layout.addWidget(self.Monitor_Select_GroupBox_ComboBox)
        self.Monitor_Select_GroupBox.setLayout(self.Monitor_Select_GroupBox_Layout)

        ##Button
        self.Monitor_Select_Ok_Btn = QPushButton("Ok")
        self.Monitor_Select_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Monitor_Select_Ok_Btn.setFixedWidth(50)
        self.Monitor_Select_Ok_Btn.clicked.connect(self.SelectCurve)
        self.Monitor_Select_GroupBox_Layout.addWidget(self.Monitor_Select_Ok_Btn)

        ##GroupBOx Select grandeza eletrica
        self.Monitor_Select_Variable_GroupBox = QGroupBox("Grandeza elétrica")
        self.Monitor_Select_Variable_GroupBox_Layout = QVBoxLayout()
        self.Monitor_Select_Variable_GroupBox_TreeWidget = QTreeWidget()
        self.Monitor_Select_Variable_GroupBox_TreeWidget.setHeaderLabels(['Variáveis', 'Cor', '',''])
        self.Monitor_Select_Variable_GroupBox_TreeWidget.setColumnWidth(1,20)
        self.Monitor_Select_Variable_GroupBox_Layout.addWidget(self.Monitor_Select_Variable_GroupBox_TreeWidget)

        self.Monitor_Select_Variable_SelectAll = QCheckBox("Selecionar todas as curvas")
        self.Monitor_Select_Variable_SelectAll.clicked.connect(self.onAllCurves)
        self.Monitor_Select_Variable_GroupBox_Layout.addWidget(self.Monitor_Select_Variable_SelectAll)


        #########################################################

        self.Monitor_Select_Variable_Show_Btn = QPushButton("Visualizar")
        self.Monitor_Select_Variable_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        #self.Monitor_Select_Variable_Show_Btn.setFixedWidth(100)
        self.Monitor_Select_Variable_Show_Btn.clicked.connect(self.viewVariable)
        self.Monitor_Select_Variable_GroupBox_Layout.addWidget(self.Monitor_Select_Variable_Show_Btn)

        self.Monitor_Select_Variable_GroupBox.setLayout(self.Monitor_Select_Variable_GroupBox_Layout)

        ##Adciona os GroupBox ao GroupBox principal
        self.Monitor_GroupBox_Layout.addWidget(self.Monitor_Select_GroupBox)
        self.Monitor_GroupBox_Layout.addWidget(self.Monitor_Select_Variable_GroupBox)

        ##### Load visualizador
        self.View_GroupBox = QGroupBox("Visualizar a(s) Curva(s)")
        self.View_GroupBox_Layout = QHBoxLayout()
        self.graphWidget = pyqtgraph.PlotWidget()
        self.View_GroupBox_Layout.addWidget(self.graphWidget)
        self.View_GroupBox.setLayout(self.View_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Monitor_GroupBox, 1, 1, 1, 1)
        self.Dialog_Layout.addWidget(self.View_GroupBox, 1, 2, 1, 2)

        ##############################################################################################

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)
        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def onAllCurves(self):

        for ctd in range(0, self.Monitor_Select_Variable_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.Monitor_Select_Variable_GroupBox_TreeWidget.topLevelItem(ctd)
            Item.setCheckState(0, self.Monitor_Select_Variable_SelectAll.checkState())

    def SelectCurve(self):
        ##Pegar os Dados do MOnitor selecionado
        self.OpenDSS.setMonitorActive(self.Monitor_Select_GroupBox_ComboBox.currentText())

        listChannels = self.OpenDSS.getMonitorActive_ChannelNames()

        for ctd in range(0, len(listChannels)):
            data = self.OpenDSS.get_MonitorActive_DataChannel(ctd)
            Monitor_Select_Variable_GroupBox_TreeWidget_Item(self.Monitor_Select_Variable_GroupBox_TreeWidget,
                                                             self.Monitor_Select_Variable_SelectAll.checkState(),
                                                             listChannels[ctd], data,
                                                             cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])

    def viewVariable(self):

        #Limpando
        self.graphWidget.clear()

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add Axis Labels
        self.graphWidget.setLabel('left', 'Demanda', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Tempo', color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        #self.graphWidget.setXRange(0, max(plot_x), padding=0)
        #self.graphWidget.setYRange(20, 55, padding=0)

        countSelected = 0
        for ctd in range(0, self.Monitor_Select_Variable_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.Monitor_Select_Variable_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:

                pen = pyqtgraph.mkPen(color = Item.getColorRGB(), style = Item.getStyle())

                pointsList = Item.getPoints()

                ##Definindo o X
                plot_x = [ctd for ctd in range(0, len(pointsList))]

                symbol = Item.getMarker()

                self.graphWidget.plot(plot_x, pointsList, name=Item.name, pen=pen, symbol=symbol, symbolSize=10, symbolBrush=Item.getColorRGB())

                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Carga', "Nenhuma curva selecionada para visualização!")


    def Accept(self):
        self.close()

    def updateDialog(self):
        self.Monitor_Select_Variable_GroupBox_TreeWidget.clear()

        nMonitors = self.OpenDSS.getAllNamesMonitor()

        self.Monitor_Select_GroupBox_ComboBox.addItems(nMonitors)


class Monitor_Select_Variable_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, check, name, points, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Monitor_Select_Variable_GroupBox_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:


        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, check)

        self.color = color
        self.Points = points

        ## Column 1 - Button:
        self.TreeWidget_Item_Btn = QPushButton()
        self.TreeWidget_Item_Btn.setFixedSize(20, 20)
        self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
        self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
        self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)

        ## Column 2 - Style:
        self.listStyle = ['Solid', 'Dashed', 'Dotted', "DashDot", 'Dash Dotted']
        self.TreeWidget_Line_Combox = QComboBox()
        #self.TreeWidget_Line_Combox.setFixedSize(100, 20)
        self.TreeWidget_Line_Combox.addItems(self.listStyle)
        self.treeWidget().setItemWidget(self, 2, self.TreeWidget_Line_Combox)

        ## Column 3 - Mark:
        self.listMarker = ["Circular", "Square",  "Triangular", "Diamond", "Cross"]
        self.listMarkerPlot = ["o","s","t","d","+"]

        self.TreeWidget_Marker_Combox = QComboBox()
        #self.TreeWidget_Marker_Combox.setFixedSize(70, 20)
        self.TreeWidget_Marker_Combox.addItems(self.listMarker)
        self.treeWidget().setItemWidget(self, 3, self.TreeWidget_Marker_Combox)

    @property
    def name(self):
        return self.text(0)

    def getPoints(self):
        return self.text(2)

    def getStyle(self):
        listQT = [Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine]

        return listQT[self.TreeWidget_Line_Combox.currentIndex()]

    def getMarker(self):
        return self.listMarkerPlot[self.TreeWidget_Marker_Combox.currentIndex()]

    def getPoints(self):
        return self.Points

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






