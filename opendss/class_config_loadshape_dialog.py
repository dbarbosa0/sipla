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
import unidecode



class C_Config_LoadShape_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Load Shapes Settings"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._nPointsLoadDef = 0
        self._nStepSizeDef = 0
        self._nStepSizeTimeDef = ""

        self._dataLoadShapes = {}

        self.InitUI()


    @property
    def dataLoadShapes(self):
        return self._dataLoadShapes

    @dataLoadShapes.setter
    def dataLoadShapes(self, value):
        self._dataLoadShapes = value

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


        ##### Load Shapes
        self.Shapes_GroupBox = QGroupBox("Curvas de Carga")
        self.Shapes_GroupBox.setFixedWidth(400)

        self.Shapes_GroupBox_Layout = QGridLayout()
        self.Shapes_GroupBox_TreeWidget = QTreeWidget()
        self.Shapes_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos'])
        self.Shapes_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_TreeWidget, 1, 1, 1, 2)

        self.Shapes_GroupBox_Checkbox_GroupBox = QGroupBox()
        self.Shapes_GroupBox_Checkbox_Layout = QHBoxLayout()
        self.Shapes_GroupBox_Checkbox_SelectAll = QCheckBox("Selecionar todas as curvas")
        self.Shapes_GroupBox_Checkbox_SelectAll.clicked.connect(self.onAllCurves)
        self.Shapes_GroupBox_Checkbox_Layout.addWidget(self.Shapes_GroupBox_Checkbox_SelectAll)

        self.Shapes_GroupBox_Checkbox_Normalize = QCheckBox("Visualizar as curvas normalizadas")
        self.Shapes_GroupBox_Checkbox_Normalize.setChecked(True)
        self.Shapes_GroupBox_Checkbox_Layout.addWidget(self.Shapes_GroupBox_Checkbox_Normalize)
        self.Shapes_GroupBox_Checkbox_GroupBox.setLayout(self.Shapes_GroupBox_Checkbox_Layout)

        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_Checkbox_GroupBox, 2, 1, 1, 2)



        self.Shapes_GroupBox_Remover_Btn = QPushButton("Remover")
        self.Shapes_GroupBox_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Shapes_GroupBox_Remover_Btn.setFixedWidth(80)
        self.Shapes_GroupBox_Remover_Btn.clicked.connect(self.removeLoadShape)
        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_Remover_Btn,3,1,1,1)

        self.Shapes_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.Shapes_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Shapes_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.Shapes_GroupBox_Adicionar_Btn.clicked.connect(self.addLoadShape)
        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_Adicionar_Btn,3,2,1,1)


        #########################################################

        self.Shapes_GroupBox_Import_Btn = QPushButton("Importar")
        self.Shapes_GroupBox_Import_Btn.setIcon(QIcon('img/icon_import_csv.png'))
        #self.Shapes_GroupBox_Import_Btn.setFixedWidth(80)
        self.Shapes_GroupBox_Import_Btn.clicked.connect(self.csvImport)
        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_Import_Btn,4,1,1,1)

        self.Shapes_GroupBox_Export_Btn = QPushButton("Exportar")
        self.Shapes_GroupBox_Export_Btn.setIcon(QIcon('img/icon_export_csv.png'))
        #self.Shapes_GroupBox_Export_Btn.setFixedWidth(80)
        self.Shapes_GroupBox_Export_Btn.clicked.connect(self.csvExport)
        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_Export_Btn,4,2,1,1)

        self.Shapes_GroupBox.setLayout(self.Shapes_GroupBox_Layout)
        #########################################################

        self.Shapes_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.Shapes_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        #self.Shapes_GroupBox_Show_Btn.setFixedWidth(100)
        self.Shapes_GroupBox_Show_Btn.clicked.connect(self.viewLoadShapes)
        self.Shapes_GroupBox_Layout.addWidget(self.Shapes_GroupBox_Show_Btn,5,1,1,2)


        self.Dialog_Layout.addWidget(self.Shapes_GroupBox, 1, 1, 1, 1)

        ##############################################################################################

        ##### Load Shapes
        self.View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) de Carga")
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

        self.Shapes_GroupBox_TreeWidget.clear()
        self.graphWidget.clear()
        self.close()

    def Accept(self):

        self.setDataLoadShapes()
        self.close()


    def onAllCurves(self):

        for ctd in range(0, self.Shapes_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.Shapes_GroupBox_TreeWidget.topLevelItem(ctd)
            Item.setCheckState(0, self.Shapes_GroupBox_Checkbox_SelectAll.checkState())


    def setDataLoadShapes(self):

        self.dataLoadShapes = {}

        try:
            for ctd in range(0, self.Shapes_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.Shapes_GroupBox_TreeWidget.topLevelItem(ctd)

                if self.checkLoadShape(Item.name, Item.getPoints()):
                    self.dataLoadShapes[Item.name] = Item.getPointsList()
                else:
                    raise class_exception.ExecConfigOpenDSS("Erro na verificação da Curva de Carga " \
                                     + Item.name + " !","Verifique se todos os " + self.nPointsLoadDef + " pontos estão presentes!")
        except:
            pass

    def csvExport(self):

        fname = QFileDialog.getSaveFileName(self, 'Open CSV file',
                                            str(pathlib.Path.home()), "CSV files (*.csv)")

        if platform.system() == "Windows":
            fname = fname[0].replace('/', '\\')
        else:
            fname = fname[0]

        self.setDataLoadShapes()


        with open(str(fname), 'w' , newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            rowText = []
            for nameShape in self.dataLoadShapes:
                rowText.append(nameShape)

            writer.writerow(rowText)

            for ctdPoints in range(0, self.nPointsLoadDef):
                rowText.clear()
                for dataShape in self.dataLoadShapes:
                    rowText.append(self.dataLoadShapes[dataShape][ctdPoints])
                writer.writerow(rowText)



    def csvImport(self):
        try:
            dataCSV = {} #Dicionário para as variáveis

            fname = QFileDialog.getOpenFileName(self, 'Open CSV file',
                                                "LoadShapes", "CSV files (*.csv)")
                                                #str(pathlib.Path.home()), "CSV files (*.csv)")

            if platform.system() == "Windows":
                fname = fname[0].replace('/', '\\')
            else:
                fname = fname[0]

            with open(str(fname), 'r', newline='') as file:
                csv_reader_object = csv.reader(file)
                #if csv.Sniffer().has_header:
                name_col = next(csv_reader_object)

                for row in name_col:
                    dataCSV[row] = []

                for row in csv_reader_object: ##Varendo todas as linhas
                    for ndata in range(0, len(name_col)): ## Varendo todas as colunas
                        dataCSV[name_col[ndata]].append(row[ndata])

                for ctd in dataCSV:
                    if self.checkLoadShape(ctd, str(dataCSV[ctd]).strip('[]').replace("'","")):
                        Config_LoadShape_Shapes_GroupBox_TreeWidget_Item(self.Shapes_GroupBox_TreeWidget,
                                                                         self.Shapes_GroupBox_Checkbox_SelectAll.checkState(),
                                                                        ctd, str(dataCSV[ctd]).strip('[]').replace("'",""),
                                                                        cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])

        except:
            class_exception.ExecConfigOpenDSS("Erro ao importar a(s) Curva(s) de Carga!","Verifique o arquivo CSV!")

    def removeLoadShape(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Carga')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:
            for ctd in range(self.Shapes_GroupBox_TreeWidget.topLevelItemCount() -1 , -1, -1):

                Item = self.Shapes_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.checkState(0) == Qt.Checked:
                    self.Shapes_GroupBox_TreeWidget.takeTopLevelItem(ctd)
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
            for ctd in range(0, self.Shapes_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.Shapes_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.name == str(inputLoadName):
                    countName += 1

            if countName == 0:
                pts = [0 for ctd in range(0,self.nPointsLoadDef)]
                pts = str(pts).strip('[]').replace("'","")
                Config_LoadShape_Shapes_GroupBox_TreeWidget_Item(self.Shapes_GroupBox_TreeWidget,
                                                                 self.Shapes_GroupBox_Checkbox_SelectAll.checkState(),
                                                                 inputLoadName, pts,
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

    def viewLoadShapes(self):

        #Limpando
        self.graphWidget.clear()
        ##Definindo o X


        plot_x = [self.nStepSizeDef * ctd for ctd in range(0,self.nPointsLoadDef)]

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add Axis Labels
        self.graphWidget.setLabel('left', 'Demanda', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Tempo (' + self.nStepSizeTimeDef[0] + ")", color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        #self.graphWidget.setXRange(0, max(plot_x), padding=0)
        #self.graphWidget.setYRange(20, 55, padding=0)

        countSelected = 0
        for ctd in range(0, self.Shapes_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.Shapes_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:

                pen = pyqtgraph.mkPen(color = Item.getColorRGB())

                if self.Shapes_GroupBox_Checkbox_Normalize.checkState() == Qt.Checked:

                    pointsList = Item.getPointsList()
                    pointsList[:] = [x / max(pointsList) for x in pointsList]
                else:
                    pointsList = Item.getPointsList()

                self.graphWidget.plot(plot_x, pointsList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())

                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Carga', "Nenhuma curva selecionada para visualização!")



class Config_LoadShape_Shapes_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, check, name, points, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_LoadShape_Shapes_GroupBox_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:


        self.setText(0, unidecode.unidecode(name.replace(" ", "_")))
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
        self.setText(2, points)

    @property
    def name(self):
        return self.text(0)

    def getPoints(self):
        return self.text(2)

    def getPointsList(self):
        points = [float(x) for x in self.text(2).split(',')]
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


