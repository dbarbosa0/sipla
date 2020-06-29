from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox
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

        self._nPointsLoadDef = 0
        self._nStepSizeDef = 0
        self._nStepSizeTimeDef = ""

        self._dataLoadCurves = {}

        self.InitUI()


    @property
    def dataLoadCurves(self):
        return self._dataLoadCurves

    @dataLoadCurves.setter
    def dataLoadCurves(self, value):
        self._dataLoadCurves = value

    @property
    def nPointsLoadDef(self):
        return self._nPointsLoadDef

    @nPointsLoadDef.setter
    def nPointsLoadDef(self, value):
        self._nPointsLoadDef = int(value)

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


        ##### Load Curves
        self.Curves_GroupBox = QGroupBox("Curvas de Carga")
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

        self.Curves_GroupBox_Checkbox_GroupBox.setLayout(self.Curves_GroupBox_Checkbox_Layout)

        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Checkbox_GroupBox, 2, 1, 1, 2)



        self.Curves_GroupBox_Remover_Btn = QPushButton("Remover")
        self.Curves_GroupBox_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Curves_GroupBox_Remover_Btn.setFixedWidth(80)
        self.Curves_GroupBox_Remover_Btn.clicked.connect(self.removeLoadShape)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Remover_Btn,3,1,1,1)

        self.Curves_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.Curves_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Curves_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.Curves_GroupBox_Adicionar_Btn.clicked.connect(self.addLoadShape)
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
        self.Curves_GroupBox_Show_Btn.clicked.connect(self.viewLoadCurves)
        self.Curves_GroupBox_Layout.addWidget(self.Curves_GroupBox_Show_Btn,5,1,1,2)


        self.Dialog_Layout.addWidget(self.Curves_GroupBox, 1, 1, 1, 1)

        ##############################################################################################

        ##### Load Curves
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

        self.setDataLoadCurves()
        self.close()


    def onAllCurves(self):

        for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)
            Item.setCheckState(0, self.Curves_GroupBox_Checkbox_SelectAll.checkState())


    def setDataLoadCurves(self):

        self.dataLoadCurves = {}
        self.dataPointsX = {}
        self.dataPointsY = {}

        try:
            for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)

                self.dataLoadCurves[Item.name] = Item.getPointsList(2)
                self.dataPointsX[Item.name] = Item.getPointsList(2)
                self.dataPointsY[Item.name] = Item.getPointsList(3)

        except:
            pass

    def csvImport(self):
        try:
            dataCSV = {} #Dicionário para as variáveis
            pointsXList = []
            pointsYList = []
            fname = QFileDialog.getOpenFileName(self, 'Open CSV file',
                                                "Curvas TCC", "CSV files (*.csv)")
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
                        Config_LoadShape_Curves_GroupBox_TreeWidget_Item(self.Curves_GroupBox_TreeWidget,
                                                                 self.Curves_GroupBox_Checkbox_SelectAll.checkState(),
                                                                key, str(pointsXList).strip('[]').replace("'",""),
                                                                         str(pointsYList).strip('[]').replace("'", ""),
                                                                cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    pointsXList = []
                    pointsYList = []
                print(pointsXList,pointsYList)

        except:
            class_exception.ExecConfigOpenDSS("Erro ao importar a(s) Curva(s) de Carga!","Verifique o arquivo CSV!")

    def viewLoadCurves(self):

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

                pen = pyqtgraph.mkPen(color = Item.getColorRGB())

                pointsXList = Item.getPointsList(2)
                pointsYList = Item.getPointsList(3)

                self.graphWidget.plot(pointsXList, pointsYList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())
                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas TCC', "Nenhuma curva selecionada para visualização!")

    def csvExport(self):

        fname = QFileDialog.getSaveFileName(self, 'Open CSV file',
                                            str(pathlib.Path.home()), "CSV files (*.csv)")

        if platform.system() == "Windows":
            fname = fname[0].replace('/', '\\')
        else:
            fname = fname[0]

        self.setDataLoadCurves()


        with open(str(fname), 'w' , newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            rowText = []
            for nameShape in self.dataLoadCurves:
                rowText.append(nameShape)

            writer.writerow(rowText)

            for ctdPoints in range(0, 10):
                rowText.clear()
                for dataShape in self.dataPointsX:
                    try:
                        m = str(self.dataPointsX[dataShape][ctdPoints]) + ";" + str(self.dataPointsY[dataShape][ctdPoints])
                        rowText.append(m)
                    except:
                        rowText.append('')
                writer.writerow(rowText)

    def removeLoadShape(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Carga')
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
                msg.information(self, 'Curvas de Carga', str(contChecked) + " curva(s) de carga removida(s)!")
            else:
                msg.information(self, 'Curvas de Carga', "Nenhuma curva de carga selecionada!")

        else:
            msg.information(self, 'Curvas de Carga', "Nenhuma curva de carga foi removida!")

    def addLoadShape(self):

        inputLoadName, inputOk = QInputDialog.getText(self, 'Curvas de Carga', 'Entre com o nome da nova Curva de Carga:')

        if inputOk:
            countName = 0
            for ctd in range(0, self.Curves_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.Curves_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.name == str(inputLoadName):
                    countName += 1

            if countName == 0:
                pts = [0 for ctd in range(0,self.nPointsLoadDef)]
                pts = str(pts).strip('[]').replace("'","")
                Config_LoadShape_Curves_GroupBox_TreeWidget_Item(self.Curves_GroupBox_TreeWidget,
                                                                 self.Curves_GroupBox_Checkbox_SelectAll.checkState(),
                                                                 inputLoadName, pts,pts,
                                                                 cfg.colorsList[
                                                                     random.randint(0, len(cfg.colorsList) - 1)])
            else:
                msg = QMessageBox()
                msg.information(self, 'Curvas de Carga', "Não foi possível adicionar a curva de carga!\nCurva de carga já existente!")

    def checkLoadShape(self, nameLoadShape, pointsLoadShape):

        msgText = ''
        pointsLoadShape = pointsLoadShape.split(',')
        if len(pointsLoadShape) != self.nPointsLoadDef:
            msgText += "Número de pontos da curva " + nameLoadShape + " está diferente do definido na configuração! \n"
        else:
            for ctd in pointsLoadShape:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de carga!"

        if msgText != "":
            msg = QMessageBox()
            msg.information(self, 'Curvas de Carga',
                            "Não foi possível adicionar a curva de carga:\n" + msgText)
            return False
        else:
            return True


class Config_LoadShape_Curves_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, check, name, pointsX,pointsY,color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_LoadShape_Curves_GroupBox_TreeWidget_Item, self).__init__(parent)

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


