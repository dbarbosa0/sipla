from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt

import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception



class C_Config_Curves_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Curvas de Característica Tempo Corrente"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._nPointsDef = 0
        self._nStepSizeDef = 0
        self._nStepSizeTimeDef = ""

        self._dataCurves = {}

        self.InitUI()


    @property
    def dataCurves(self):
        return self._dataCurves

    @dataCurves.setter
    def dataCurves(self, value):
        self._dataCurves = value

    @property
    def nPointsDef(self):
        return self._nPointsDef

    @nPointsDef.setter
    def nPointsDef(self, value):
        self._nPointsDef = int(value)

    @property
    def nStepSizeDef(self):
        return self._nStepSizeDef

    @nStepSizeDef.setter
    def nStepSizeDef(self, value):
        self._nStepSizeDef = value

    @property
    def nStepSizeTimeDef(self):
        return self._nStepSizeTimeDef

    @nStepSizeTimeDef.setter
    def nStepSizeTimeDef(self, value):
        self._nStepSizeTimeDef = value

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(800, 500)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog


        #####  Curves
        self.Curves_GroupBox = QGroupBox("Curvas TCC")
        self.Curves_GroupBox.setFixedWidth(400)

        self.Curves_GroupBox_Layout = QGridLayout()
        self.Curves_GroupBox_TreeWidget = QTreeWidget()
        self.Curves_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Corrente', 'Tempo'])
        self.Curves_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_TreeWidget, 1, 1, 1, 2)

        self.Curves_GroupBox_Checkbox_GroupBox = QGroupBox()
        self.Curves_GroupBox_Checkbox_Layout = QHBoxLayout()
        self.Curves_GroupBox_Checkbox_SelectAll = QCheckBox("Selecionar todas as curvas")
        self.Curves_GroupBox_Checkbox_SelectAll.clicked.connect(self.onAllCurves)
        self.Curves_GroupBox_Checkbox_Layout.addWidget(self.Curves_GroupBox_Checkbox_SelectAll)
        self.Curves_GroupBox_Checkbox_Current = QCheckBox("Plotar Corrente de Curto")
        #self.Curves_GroupBox_Checkbox_SelectAll.clicked.connect(self.onAllCurves)
        self.Curves_GroupBox_Checkbox_Layout.addWidget(self.Curves_GroupBox_Checkbox_Current)
        self.Curves_GroupBox_LineEdit_Current = QLineEdit()
        self.Curves_GroupBox_LineEdit_Current.setPlaceholderText("A")
        self.Curves_GroupBox_Checkbox_Layout.addWidget(self.Curves_GroupBox_LineEdit_Current)

        self.Curves_GroupBox_Checkbox_GroupBox.setLayout(self.Curves_GroupBox_Checkbox_Layout)

        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Checkbox_GroupBox, 2, 1, 1, 2)



        self.Curves_GroupBox_Remover_Btn = QPushButton("Remover")
        self.Curves_GroupBox_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Curves_GroupBox_Remover_Btn.setFixedWidth(80)
        self.Curves_GroupBox_Remover_Btn.clicked.connect(self.removeTCCCurves)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Remover_Btn,3,1,1,1)

        self.Curves_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.Curves_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Curves_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.Curves_GroupBox_Adicionar_Btn.clicked.connect(self.addTCCCurves)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Adicionar_Btn,3,2,1,1)


        #########################################################

        self.Curves_GroupBox_Import_Btn = QPushButton("Importar")
        self.Curves_GroupBox_Import_Btn.setIcon(QIcon('img/icon_import_csv.png'))
        #self.Curves_GroupBox_Import_Btn.setFixedWidth(80)
        self.Curves_GroupBox_Import_Btn.clicked.connect(self.csvImport)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Import_Btn,4,1,1,1)

        self.Curves_GroupBox_Export_Btn = QPushButton("Exportar")
        self.Curves_GroupBox_Export_Btn.setIcon(QIcon('img/icon_export_csv.png'))
        #self.Curves_GroupBox_Export_Btn.setFixedWidth(80)
        self.Curves_GroupBox_Export_Btn.clicked.connect(self.csvExport)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Export_Btn,4,2,1,1)

        self.Curves_GroupBox.setLayout(self.Curves_GroupBox_Layout)
        #########################################################

        self.Curves_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.Curves_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        #self.Curves_GroupBox_Show_Btn.setFixedWidth(100)
        self.Curves_GroupBox_Show_Btn.clicked.connect(self.viewCurves)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Show_Btn,5,1,1,2)


        self.Dialog_Layout.addWidget(self.Curves_GroupBox, 1, 1, 1, 1)

        ##############################################################################################

        #####  Curves
        self.View_GroupBox = QGroupBox("Visualizar as Curvas TCC")
        self.View_GroupBox_Layout = QHBoxLayout()

        self.graphWidget = pyqtgraph.PlotWidget()

        self.View_GroupBox_Layout.addWidget(self.graphWidget)
        self.View_GroupBox.setLayout(self.View_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.View_GroupBox, 1, 2, 1, 2)


        ##############################################################################################

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

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout,2,3,1,1)

        self.setLayout(self.Dialog_Layout)

    def Cancel(self):

        self.Curves_GroupBox_TreeWidget.clear()
        self.graphWidget.clear()
        self.close()

    def Accept(self):

        self.setDataCurves()
        self.close()


    def onAllCurves(self):

        for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)
            Item.setCheckState(0, self.Curves_GroupBox_Checkbox_SelectAll.checkState())


    def setDataCurves(self):

        self.dataCurves = {}
        self.dataPointsX = {}
        self.dataPointsY = {}
        self.nPoints = 0

        try:
            for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)

                self.dataCurves[Item.name] = Item.getPointsList(2)
                self.dataPointsX[Item.name] = Item.getPointsList(2)
                self.dataPointsY[Item.name] = Item.getPointsList(3)
                print(f'dataPointsX{self.dataPointsX}')

            for key,value in self.dataPointsX.items():
                if len(value)> self.nPoints:
                    self.nPoints = len(value)

        except:
            pass


    def csvImport(self):
        try:
            dataCSV = {} #Dicionário para as variáveis
            pointsXList = []
            pointsYList = []
            fname = QFileDialog.getOpenFileName(self, 'Open CSV file',
                                                "", "CSV files (*.csv)")
                                                #str(pathlib.Path.home()), "CSV files (*.csv)")

            if platform.system() == "Windows":
                fname = fname[0].replace('/', '\\')
            else:
                fname = fname[0]

            with open(fname, 'r', newline='') as file:
                csv_reader_object = csv.reader(file)
                # if csv.Sniffer().has_header:
                name_col = next(csv_reader_object)

                for row in name_col:
                    dataCSV[row] = []

                for row in csv_reader_object:  ##Varendo todas as linhas
                    for ndata in range(0, len(name_col)):  ## Varendo todas as colunas
                        dataCSV[name_col[ndata]].append(row[ndata])

                for key, values in dataCSV.items():
                    for value in values:
                        if value:
                            pointsXList.append(float(value.split(';')[0]))
                            pointsYList.append(float(value.split(';')[1]))

                    if pointsXList:
                        flag = True
                    else:
                        flag = False

                    if flag:
                        Config_TCCCurves_GroupBox_TreeWidget_Item(self.Curves_GroupBox_TreeWidget,
                                                                  self.Curves_GroupBox_Checkbox_SelectAll.checkState(),
                                                                  key, str(pointsXList).strip('[]').replace("'",""),
                                                                  str(pointsYList).strip('[]').replace("'", ""),
                                                                  cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    pointsXList = []
                    pointsYList = []

        except:
            class_exception.ExecConfigOpenDSS("Erro ao importar a(s) Curva(s) TCC!","Verifique o arquivo CSV!")

    def viewCurves(self):

        # Limpando
        self.graphWidget.clear()
        self.graphWidget.setBackground('w')
        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Tempo (s)', color='blue', size=20)
        self.graphWidget.setLabel('bottom', 'Corrente (A)', color='blue', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLogMode(x=True, y=True)


        countSelected = 0
        for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:

                pen = pyqtgraph.mkPen(color = Item.getColorRGB(), width=2)
                pointsXList = Item.getPointsList(2)
                pointsYList = Item.getPointsList(3)

                self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())
                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas TCC', "Nenhuma curva selecionada para visualização!")

        if self.Curves_GroupBox_Checkbox_Current.isChecked() and self.Curves_GroupBox_LineEdit_Current.text():
            current = float(self.Curves_GroupBox_LineEdit_Current.text())
            tempo = [0.01,100]
            corrente = [current,current]
            pen = pyqtgraph.mkPen(color='r', width=1, style=pyqtgraph.QtCore.Qt.DashLine)
            redrgb = (255, 0, 0, 255)
            self.graphWidget.plot(corrente, tempo, name="Icc", pen=pen, symbol='x', symbolSize=10,
                                  symbolBrush=redrgb)


    def csvExport(self):

        fname = QFileDialog.getSaveFileName(self, 'Open CSV file',
                                            str(pathlib.Path.home()), "CSV files (*.csv)")

        if platform.system() == "Windows":
            fname = fname[0].replace('/', '\\')
        else:
            fname = fname[0]

        self.setDataCurves()


        with open(str(fname), 'w' , newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            rowText = []
            for nameShape in self.dataCurves:
                rowText.append(nameShape)

            writer.writerow(rowText)

            for ctdPoints in range(0, self.nPoints):
                # region Description
                rowText.clear()
                # endregion
                for dataShape in self.dataPointsX:
                    try:
                        m = str(self.dataPointsX[dataShape][ctdPoints]) + ";" + str(self.dataPointsY[dataShape][ctdPoints])
                        rowText.append(m)
                    except:
                        rowText.append('')
                writer.writerow(rowText)

    def removeTCCCurves(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas TCC')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:
            for ctd in range(self.Curves_GroupBox_TreeWidget.topLevelItemCount() - 1, -1 , -1):
                Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.checkState(0) == Qt.Checked:
                    self.Curves_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curvas TCC', str(contChecked) + " curva(s) TCC removida(s)!")
            else:
                msg.information(self, 'Curvas TCC', "Nenhuma curva TCC selecionada!")

        else:
            msg.information(self, 'Curvas TCC', "Nenhuma curva TCC foi removida!")

    def addTCCCurves(self):

        inputName, inputOk = QInputDialog.getText(self, 'Curvas TCC', 'Entre com o nome da nova Curva TCC:')

        if inputOk:
            countName = 0
            for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.name == str(inputName):
                    countName += 1

            if countName == 0:
                pts = [0 for ctd in range(0,self.nPointsDef)]
                pts = str(pts).strip('[]').replace("'","")
                Config_TCCCurves_GroupBox_TreeWidget_Item(self.Curves_GroupBox_TreeWidget,
                                                          self.Curves_GroupBox_Checkbox_SelectAll.checkState(),
                                                          inputName, pts, pts,
                                                          cfg.colorsList[
                                                                     random.randint(0, len(cfg.colorsList) - 1)])
            else:
                msg = QMessageBox()
                msg.information(self, 'Curvas TCC', "Não foi possível adicionar a curva TCC!\nCurva TCC já existente!")


class Config_TCCCurves_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, check, name, pointsX,pointsY,color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_TCCCurves_GroupBox_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:


        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, check)

        self.color = color

        ## Column 1 - Button:
        self.TreeWidget_Item_Btn = QPushButton()
        self.TreeWidget_Item_Btn.setFixedSize(20, 20)
        self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
        self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
        self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)

        ## Column 2 - Pontos:
        self.setText(2, pointsX)
        self.setText(3, pointsY)

    @property
    def name(self):
        return self.text(0)

    def getPoints(self,column):
        return self.text(column)

    def getPointsList(self,column):
        points = [float(x) for x in self.text(column).split(',')]
        return points

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


