from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QLabel, QComboBox, QSpinBox
from PyQt5.QtCore import Qt

import csv
import random
import pathlib
import platform
import pyqtgraph
import config as cfg
import class_exception
import unidecode



class C_Config_PriceCurve_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Seleção da Curva de Preço"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.dataPriceCurve = {}

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        #self.resize(800, 500)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)

        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ##### Config parametros iniciais
        self.Daily_GroupBox = QGroupBox("Parâmetros para a curva")
        self.Daily_GroupBox_Layout = QGridLayout()

        self.Daily_GroupBox_Stepsize_Label = QLabel("Set Stepsize:")
        self.Daily_GroupBox_Layout.addWidget(self.Daily_GroupBox_Stepsize_Label, 1, 1, 1, 1)
        self.Daily_GroupBox_Stepsize_SpinBox = QSpinBox()
        self.Daily_GroupBox_Stepsize_SpinBox.setValue(1)
        self.Daily_GroupBox_Layout.addWidget(self.Daily_GroupBox_Stepsize_SpinBox, 1, 2, 1, 1)

        self.Daily_GroupBox_Number_Label = QLabel("Set Number:")
        self.Daily_GroupBox_Layout.addWidget(self.Daily_GroupBox_Number_Label, 2, 1, 1, 1)
        self.Daily_GroupBox_Number_SpinBox = QSpinBox()
        self.Daily_GroupBox_Number_SpinBox.setValue(24)
        self.Daily_GroupBox_Layout.addWidget(self.Daily_GroupBox_Number_SpinBox, 2, 2, 1, 2)

        self.Daily_GroupBox_Stepsize_ComboBox = QComboBox()
        self.Daily_GroupBox_Stepsize_ComboBox.addItems(["sec", "min", "hr"])
        self.Daily_GroupBox_Stepsize_ComboBox.setCurrentText("hr")
        self.Daily_GroupBox_Layout.addWidget(self.Daily_GroupBox_Stepsize_ComboBox, 1, 3, 1, 1)

        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.CancelParameters)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.AcceptParameters)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Daily_GroupBox_Layout.addLayout(self.Dialog_Btns_Layout, 3, 1, 1, 3)

        self.Daily_GroupBox.setLayout(self.Daily_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Daily_GroupBox, 1, 0, 1, 1)
        ######################################################################
        ##### PriceCurve
        self.PriceCurve_GroupBox = QGroupBox("Curvas de Preço")
        self.PriceCurve_GroupBox.setFixedWidth(400)
        self.PriceCurve_GroupBox.setVisible(False)

        self.PriceCurve_GroupBox_Layout = QGridLayout()
        self.PriceCurve_GroupBox_TreeWidget = QTreeWidget()
        self.PriceCurve_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Cor', 'Pontos'])
        self.PriceCurve_GroupBox_TreeWidget.setColumnWidth(1, 20)
        self.PriceCurve_GroupBox_Layout.addWidget(self.PriceCurve_GroupBox_TreeWidget, 1, 1, 1, 2)

        self.PriceCurve_GroupBox_Remover_Btn = QPushButton("Remover")
        self.PriceCurve_GroupBox_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.PriceCurve_GroupBox_Remover_Btn.setFixedWidth(80)
        self.PriceCurve_GroupBox_Remover_Btn.clicked.connect(self.removePriceCurve)
        self.PriceCurve_GroupBox_Layout.addWidget(self.PriceCurve_GroupBox_Remover_Btn,3,1,1,1)

        self.PriceCurve_GroupBox_Adicionar_Btn = QPushButton("Adicionar")
        self.PriceCurve_GroupBox_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.PriceCurve_GroupBox_Adicionar_Btn.setFixedWidth(80)
        self.PriceCurve_GroupBox_Adicionar_Btn.clicked.connect(self.addPriceCurve)
        self.PriceCurve_GroupBox_Layout.addWidget(self.PriceCurve_GroupBox_Adicionar_Btn,3,2,1,1)


        #########################################################

        self.PriceCurve_GroupBox_Import_Btn = QPushButton("Importar")
        self.PriceCurve_GroupBox_Import_Btn.setIcon(QIcon('img/icon_import_csv.png'))
        #self.PriceCurve_GroupBox_Import_Btn.setFixedWidth(80)
        self.PriceCurve_GroupBox_Import_Btn.clicked.connect(self.csvImport)
        self.PriceCurve_GroupBox_Layout.addWidget(self.PriceCurve_GroupBox_Import_Btn,4,1,1,1)

        self.PriceCurve_GroupBox_Export_Btn = QPushButton("Exportar")
        self.PriceCurve_GroupBox_Export_Btn.setIcon(QIcon('img/icon_export_csv.png'))
        #self.PriceCurve_GroupBox_Export_Btn.setFixedWidth(80)
        self.PriceCurve_GroupBox_Export_Btn.clicked.connect(self.csvExport)
        self.PriceCurve_GroupBox_Layout.addWidget(self.PriceCurve_GroupBox_Export_Btn,4,2,1,1)

        self.PriceCurve_GroupBox.setLayout(self.PriceCurve_GroupBox_Layout)
        #########################################################

        self.PriceCurve_GroupBox_Show_Btn = QPushButton("Visualizar")
        self.PriceCurve_GroupBox_Show_Btn.setIcon(QIcon('img/icon_line.png'))
        #self.PriceCurve_GroupBox_Show_Btn.setFixedWidth(100)
        self.PriceCurve_GroupBox_Show_Btn.clicked.connect(self.viewPriceCurve)
        self.PriceCurve_GroupBox_Layout.addWidget(self.PriceCurve_GroupBox_Show_Btn,5,1,1,2)


        self.Dialog_Layout.addWidget(self.PriceCurve_GroupBox, 1, 1, 1, 1)

        ##############################################################################################

        ##### PriceCurve
        self.View_GroupBox = QGroupBox("Visualizar a(s) Curva(s) de Preço")
        self.View_GroupBox.setVisible(False)
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
        self.Dialog_Btns_Cancel_Btn.setVisible(False)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Ok_Btn.setVisible(False)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 2, 3, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def AcceptParameters(self):
        self.PriceCurve_GroupBox.setVisible(True)
        self.View_GroupBox.setVisible(True)
        self.Dialog_Btns_Cancel_Btn.setVisible(True)
        self.Dialog_Btns_Ok_Btn.setVisible(True)
        self.Daily_GroupBox.setVisible(False)
        self.adjustSize()

    def CancelParameters(self):
        self.close()

    def nPointsLoadDef(self):
        return self.Daily_GroupBox_Number_SpinBox.value()

    def nStepSizeDef(self):
        return self.Daily_GroupBox_Stepsize_SpinBox.value()

    def nStepSizeTimeDef(self):
        return self.Daily_GroupBox_Stepsize_ComboBox.currentText()

    def Cancel(self):
        self.PriceCurve_GroupBox_TreeWidget.clear()
        self.graphWidget.clear()
        self.PriceCurve_GroupBox.setVisible(False)
        self.View_GroupBox.setVisible(False)
        self.Dialog_Btns_Cancel_Btn.setVisible(False)
        self.Dialog_Btns_Ok_Btn.setVisible(False)
        self.Daily_GroupBox.setVisible(True)
        self.adjustSize()

    def Accept(self):
        self.setDataPriceCurve()
        self.close()

    def setDataPriceCurve(self):
        self.dataPriceCurve = {}
        self.dataPriceCurve["npts"] = self.nPointsLoadDef()
        if self.nStepSizeTimeDef() == "sec":
            self.dataPriceCurve["sinterval"] = self.nStepSizeDef()
        elif self.nStepSizeTimeDef() == "min":
            self.dataPriceCurve["minterval"] = self.nStepSizeDef()
        elif self.nStepSizeTimeDef() == "hr":
            self.dataPriceCurve["interval"] = self.nStepSizeDef()

        checkCont = 0
        try:
            for ctd in range(0, self.PriceCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.PriceCurve_GroupBox_TreeWidget.topLevelItem(ctd)
                if Item.checkState(0) == Qt.Checked:
                    checkCont += 1
                    if checkCont > 1:
                        raise class_exception.ExecConfigOpenDSS("Erro na seleção da Curva de Preço ",
                                                                "Selecione somente uma curva!")
                    elif checkCont == 0:
                        raise class_exception.ExecConfigOpenDSS("Erro na seleção da Curva de Preço ",
                                                                "Selecione ao menos uma curva!")
                    else:
                        if self.checkPriceCurve(Item.name, Item.getPoints()):
                            price = Item.getPointsList()
                            self.dataPriceCurve["PriceCurveName"] = Item.name
                            self.dataPriceCurve["price"] = price
                        else:
                            raise class_exception.ExecConfigOpenDSS("Erro na verificação da Curva de Preço " \
                                             + Item.name + " !","Verifique se todos os " + self.nPointsLoadDef() + " pontos estão presentes!")
        except:
            pass

    def csvExport(self):
        fname = QFileDialog.getSaveFileName(self, 'Open CSV file',
                                            str(pathlib.Path.home()), "CSV files (*.csv)")

        if platform.system() == "Windows":
            fname = fname[0].replace('/', '\\')
        else:
            fname = fname[0]

        self.setDataPriceCurve()


        with open(str(fname), 'w' , newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            rowText = []
            for nameShape in self.dataPriceCurve:
                rowText.append(nameShape)

            writer.writerow(rowText)

            for ctdPoints in range(0, self.nPointsLoadDef()):
                rowText.clear()
                for dataShape in self.dataPriceCurve:
                    rowText.append(self.dataPriceCurve[dataShape][ctdPoints])
                writer.writerow(rowText)



    def csvImport(self):
        try:
            dataCSV = {} #Dicionário para as variáveis

            fname = QFileDialog.getOpenFileName(self, 'Open CSV file',
                                                "StorageCurves", "CSV files (*.csv)")
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
                    if self.checkPriceCurve(ctd, str(dataCSV[ctd]).strip('[]').replace("'","")):
                        Config_PriceCurve_GroupBox_TreeWidget_Item(self.PriceCurve_GroupBox_TreeWidget,
                                                                        ctd, str(dataCSV[ctd]).strip('[]').replace("'",""),
                                                                        cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])

        except:
            class_exception.ExecConfigOpenDSS("Erro ao importar a(s) Curva(s) de Preço!","Verifique o arquivo CSV!")

    def removePriceCurve(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Você deseja remover a(s) curva(s) selecionada(s)?")
        msg.setWindowTitle('Curvas de Preço')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()

        contChecked = 0
        if retval == QMessageBox.Yes:
            for ctd in range(self.PriceCurve_GroupBox_TreeWidget.topLevelItemCount() -1 , -1, -1):

                Item = self.PriceCurve_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.checkState(0) == Qt.Checked:
                    self.PriceCurve_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                    contChecked += 1

            if contChecked > 0:
                msg.information(self, 'Curvas de Preço', str(contChecked) + " curva(s) de Preço removida(s)!")
            else:
                msg.information(self, 'Curvas de Preço', "Nenhuma curva de Preço selecionada!")

        else:
            msg.information(self, 'Curvas de Preço', "Nenhuma curva de Preço foi removida!")

    def addPriceCurve(self):

        inputPriceCurveName, inputOk = QInputDialog.getText(self, 'Curva de Preço', 'Entre com o nome da nova Curva de Preço:')

        if inputOk:
            countName = 0
            for ctd in range(0, self.PriceCurve_GroupBox_TreeWidget.topLevelItemCount()):

                Item = self.PriceCurve_GroupBox_TreeWidget.topLevelItem(ctd)

                if Item.name == str(inputPriceCurveName):
                    countName += 1

            if countName == 0:
                pts = [0 for ctd in range(0,self.nPointsLoadDef())]
                pts = str(pts).strip('[]').replace("'","")
                Config_PriceCurve_GroupBox_TreeWidget_Item(self.PriceCurve_GroupBox_TreeWidget,
                                                                 inputPriceCurveName, pts,
                                                                 cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
            else:
                msg = QMessageBox()
                msg.information(self, 'Curvas de Preço', "Não foi possível adicionar a curva de Preço!\nCurva de Preço já existente!")

    def checkPriceCurve(self, namePriceCurve, pointsPriceCurve):

        msgText = ''
        pointsPriceCurve = pointsPriceCurve.split(',')

        if len(pointsPriceCurve) != self.nPointsLoadDef():
            msgText += "Número de pontos da curva " + namePriceCurve + " está diferente do definido na configuração! \n"
        else:
            for ctd in pointsPriceCurve:
                try:
                    float(ctd)
                except:
                    msgText += "O item: " + ctd + " não é float! Verifique a curva de Preço!"

        if msgText != "":
            msg = QMessageBox()
            msg.information(self, 'Curvas de Preço',
                            "Não foi possível adicionar a curva de Preço:\n" + msgText)
            return False
        else:
            return True

    def viewPriceCurve(self):

        #Limpando
        self.graphWidget.clear()
        ##Definindo o X


        plot_x = [self.nStepSizeDef() * ctd for ctd in range(0,self.nPointsLoadDef())]

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add Axis Labels
        self.graphWidget.setLabel('left', 'Demanda', color='red', size=20)
        self.graphWidget.setLabel('bottom', 'Tempo (' + self.nStepSizeTimeDef()[0] + ")", color='red', size=20)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        #self.graphWidget.setXRange(0, max(plot_x), padding=0)
        #self.graphWidget.setYRange(20, 55, padding=0)

        countSelected = 0
        for ctd in range(0, self.PriceCurve_GroupBox_TreeWidget.topLevelItemCount()):

            Item = self.PriceCurve_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:

                pen = pyqtgraph.mkPen(color = Item.getColorRGB())
                pointsList = Item.getPointsList()

                self.graphWidget.plot(plot_x, pointsList, name=Item.name, pen=pen, symbol='o', symbolSize=10, symbolBrush=Item.getColorRGB())
                print(Item.getColorRGB())
                countSelected += 1

        if countSelected == 0:
            msg = QMessageBox()
            msg.information(self, 'Curvas de Preço', "Nenhuma curva selecionada para visualização!")



class Config_PriceCurve_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, points, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(Config_PriceCurve_GroupBox_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:


        self.setText(0, unidecode.unidecode(name.replace(" ", "_")))
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        self.setCheckState(0, Qt.Unchecked)

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