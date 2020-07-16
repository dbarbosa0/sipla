import csv

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QComboBox, QLineEdit, QWidget, QLabel, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import unidecode
import platform

import class_exception
import opendss.class_conn
import opendss.class_opendss
import prodist.tcapelofu
import config as cfg
import pyqtgraph

class Fuse(QWidget):

    def __init__(self):
        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Fuse = EditFuse(self)
        self.FuseSettings_GroupBox = QGroupBox('Selecionar Fusível')
        self.FuseSettings_GroupBox_Layout = QVBoxLayout()
        self.FuseSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.FuseSelect_Combobox = QComboBox()
        self.FuseSelect_Combobox.setMaximumWidth(150)
        self.FuseSettings_GroupBox_Layout.addWidget(self.FuseSelect_Combobox)

        self.ElementList = []
        self.AddFuseDataInfo = []
        self.FuseDataInfo = []
        self.loadDatabaseFlag = False
        self.flag = False

        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_Fuse.removeFuse)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.Edit_Btn.clicked.connect(self.Edit_Fuse.editFuse(self.FuseSelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.Add_Btn.clicked.connect(self.Edit_Fuse.addFuse())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.FuseSettings_GroupBox.setLayout(self.FuseSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.FuseSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_FuseInfo(self):
        FuseSelected = self.FuseSelect_Combobox.currentText()
        for item in self.FuseDataInfo:
            if item["Name"] == FuseSelected:

                self.Edit_Fuse.FuseName_LineEdit.setText(item["Name"])
                self.Edit_Fuse.Action_ComboBox.setCurrentText(item["Action"])
                self.Edit_Fuse.Delay_LineEdit.setText(item["Delay"])

                if item["Enabled"] == 'yes' or item["Enabled"] == '':
                    self.Edit_Fuse.Enable_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_Fuse.Enable_ComboBox.setCurrentIndex(1)

                self.Edit_Fuse.MonitObj_ComboBox.setCurrentText(item["MonitoredObj"])
                self.Edit_Fuse.SwitchedObj_ComboBox.setCurrentText(item["SwitchedObj"])
                self.Edit_Fuse.MonitTerm_ComboBox.setCurrentText(item["MonitoredTerm"])
                self.Edit_Fuse.SwitchedTerm_ComboBox.setCurrentText(item["SwitchedTerm"])

                self.Edit_Fuse.FuseCurve_ComboBox.setCurrentText(item["FuseCurve"])
                self.Edit_Fuse.RatedCurrent_LineEdit.setText(item["RatedCurrent"])

    def load_FusesDatabase(self):
        databaseFusedict = {}
        databaseFuse = self.OpenDSS.getFuseList()
        # print(databaseFuse)
        # Se trocar de subestação

        # Caso seja encontrado algum Fusível que ainda pertence ao database, ou seja, se não foi trocado de subestação
        try:
            for item in databaseFuse:
                for item2 in self.FuseDataInfo:
                    if item.split(" MonitoredObj=")[0].split("New Fuse.")[1] == item2["Name"]:
                        self.flag = True
                        return
                    else:
                        self.flag = False
        except IndexError:
            pass

        # Caso algum Fusível tenha sido adicionado
        if self.AddFuseDataInfo:
            self.flag = True

        # Caso não haja Fusíveles adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.FuseDataInfo.clear()
            self.AddFuseDataInfo.clear()

        # Caso a lista de Fusíveis esteja vazia:
        if not self.FuseDataInfo and not self.loadDatabaseFlag:
            for item in databaseFuse:
                databaseFusedict["Device"] = 'Fuse'
                databaseFusedict["Name"] = item.split(" MonitoredObj=")[0].split("New Fuse.")[1]
                # Basic
                databaseFusedict["Action"] = ''
                databaseFusedict["Delay"] = ''
                databaseFusedict["Enabled"] = ''
                # Connections
                databaseFusedict["MonitoredObj"] = item.split(" SwitchedObj=")[0].split("MonitoredObj=")[1]
                databaseFusedict["MonitoredTerm"] = ''
                databaseFusedict["SwitchedObj"] = item.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
                databaseFusedict["SwitchedTerm"] = item.split(" FuseCurve=")[0].split("SwitchedTerm=")[1]
                # TCC Curves
                databaseFusedict["FuseCurve"] = item.split(" RatedCurrent=")[0].split("FuseCurve=")[1]
                databaseFusedict["RatedCurrent"] = item.split(" RatedCurrent=")[1]

                self.FuseDataInfo.append(databaseFusedict.copy())

            self.loadDatabaseFlag = True

    def updateProtectDialog(self):
        self.load_FusesDatabase()
        # Carregando a ElementList para ser usada na Edit Dialog
        self.ElementList = self.OpenDSS.getElementList()
        self.FuseSelect_Combobox.clear()
        for dicio in self.FuseDataInfo:
            self.FuseSelect_Combobox.addItem(dicio["Name"], dicio["Name"])
        print(f'FuseS:{len(self.FuseDataInfo)}')


class EditFuse(QDialog):
    def __init__(self, Fuse_parent):
        super().__init__()
        self.ImportedCurves = []
        self.curvelist = [""]
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.Fuse_parent = Fuse_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(860, 170)
        self.Dialog_Layout = QVBoxLayout()
        self.TesteDialog_Layout = QHBoxLayout()
        self.FuseInfo()
        self.Btns()
        self.setLayout(self.TesteDialog_Layout)
        self.PlotState = True

    def FuseInfo(self):
        # Parâmetros Intrínsecos do Fusível
        self.Edit_Fuse_GroupBox = QGroupBox('Geral')
        self.Edit_Fuse_GroupBox_Layout = QGridLayout()
        self.Edit_Fuse_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.FuseName_LineEdit = QLineEdit()
        self.FuseName_LineEdit_Label = QLabel("Dispositivo")
        self.FuseName_LineEdit.setMaximumWidth(150)

        self.actionlist = ['Aberto', 'Fechado']
        self.actionlist_data = ['Open', 'Closed']
        self.Action_ComboBox = QComboBox()
        self.Action_ComboBox.setMaximumWidth(150)
        self.Action_ComboBox_Label = QLabel("Action")
        for index, item in enumerate(self.actionlist):
            self.Action_ComboBox.addItem(item, self.actionlist_data[index])

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setMaximumWidth(150)
        self.Delay_LineEdit_Label = QLabel("Delay")

        self.enablelist = ['Sim', 'Não']
        self.enablelist_data = ['yes', 'no']
        self.Enable_ComboBox = QComboBox()
        self.Enable_ComboBox.setMaximumWidth(150)
        self.Enable_ComboBox_Label = QLabel("Habilitado")
        for index, item in enumerate(self.enablelist):
            self.Enable_ComboBox.addItem(item, self.enablelist_data[index])

        self.Edit_Fuse_GroupBox_Layout.addWidget(self.FuseName_LineEdit_Label, 0, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.FuseName_LineEdit, 0, 1)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 1, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Action_ComboBox, 1, 1)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 2, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Delay_LineEdit, 2, 1)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 3, 0)
        self.Edit_Fuse_GroupBox_Layout.addWidget(self.Enable_ComboBox, 3, 1)

        self.Edit_Fuse_GroupBox.setLayout(self.Edit_Fuse_GroupBox_Layout)

        # Parâmetros de conexões do Fusível
        self.Conn_Fuse_GroupBox = QGroupBox('Conexões ')
        self.Conn_Fuse_GroupBox_Layout = QGridLayout()
        self.Conn_Fuse_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.MonitObj_ComboBox = QComboBox()
        self.MonitObj_ComboBox.setMinimumWidth(150)
        self.MonitObj_ComboBox_Label = QLabel("Elemento Monitorado")

        self.MonitTermList = ['1', '2']
        self.MonitTerm_ComboBox = QComboBox()
        # self.MonitTerm_ComboBox.setMaximumWidth(150)
        self.MonitTerm_ComboBox_Label = QLabel("Terminal Monitorado")
        for index, item in enumerate(self.MonitTermList):
            self.MonitTerm_ComboBox.addItem(item, item)

        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMinimumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitObj_ComboBox_Label, 0, 0, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitObj_ComboBox, 0, 1, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox_Label, 0, 2, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox, 0, 3, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_Fuse_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
        self.Conn_Fuse_GroupBox.setLayout(self.Conn_Fuse_GroupBox_Layout)

        # Curvas TCC
        self.TCCCurves_Fuse_GroupBox = QGroupBox('Curvas TCC')
        self.TCCCurves_Fuse_GroupBox_Layout = QGridLayout()
        self.TCCCurves_Fuse_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.FuseCurveList = self.curvelist
        self.FuseCurve_ComboBox = QComboBox()
        self.FuseCurve_ComboBox.setMaximumWidth(150)
        self.FuseCurve_ComboBox_Label = QLabel("Fuse Curve")
        for index, item in enumerate(self.FuseCurveList):
            self.FuseCurve_ComboBox.addItem(item, item)

        self.RatedCurrent_LineEdit = QLineEdit()
        self.RatedCurrent_LineEdit.setMaximumWidth(50)
        self.RatedCurrent_LineEdit.setPlaceholderText("1.0")
        self.RatedCurrent_LineEdit_Label = QLabel("Rated Current")

        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.FuseCurve_ComboBox_Label, 0, 0, 1, 1)
        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.FuseCurve_ComboBox, 0, 1, 1, 1)
        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.RatedCurrent_LineEdit_Label, 0, 2, 1, 1)
        self.TCCCurves_Fuse_GroupBox_Layout.addWidget(self.RatedCurrent_LineEdit, 0, 3, 1, 1)

        self.TCCCurves_Fuse_GroupBox.setLayout(self.TCCCurves_Fuse_GroupBox_Layout)

        self.graphWidget = pyqtgraph.PlotWidget()
        self.graphWidget.setHidden(True)

        self.Dialog_Layout.addWidget(self.Edit_Fuse_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Fuse_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Fuse_GroupBox)

        self.TesteDialog_Layout.addLayout(self.Dialog_Layout)
        self.TesteDialog_Layout.addWidget(self.graphWidget)

    def ImportCurve(self):
        try:
            dataCSV = {} #Dicionário para as variáveis
            pointsXList = []
            pointsYList = []
            self.FuseCurve_ComboBox.clear()
            self.FuseCurve_ComboBox.addItem("","")
            self.filename = QFileDialog.getOpenFileName(self, 'Open CSV file',
                                                "", "CSV files (*.csv)")
                                                #str(pathlib.Path.home()), "CSV files (*.csv)")

            if platform.system() == "Windows":
                fname = self.filename[0].replace('/', '\\')
            else:
                fname = self.filename[0]

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
                        self.curvelist.append(key)
                        string = "new TCC_Curve." + key + " npts=" + str(len(pointsXList)) +\
                                 " c_array=("  + str(pointsXList).strip('[]').replace("'","").replace("," , " ") +\
                            ") t_array=(" + str(pointsYList).strip('[]').replace("'","").replace("," , " ") + ")"
                        self.ImportedCurves.append(string)
                        print(string)

                    pointsXList = []
                    pointsYList = []
                    self.FuseCurve_ComboBox.addItem(key,key)

        except:
            class_exception.ExecConfigOpenDSS("Erro ao importar a(s) Curva(s) TCC!","Verifique o arquivo CSV!")

    def viewCurve(self):
        dataCSV = {}
        pointsXList = []
        pointsYList = []
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
        pen = pyqtgraph.mkPen(color = 'b')
        self.PlotState = not self.PlotState

        if not self.PlotState and self.filename:

            if platform.system() == "Windows":
                fname = self.filename[0].replace('/', '\\')
            else:
                fname = self.filename[0]

            with open(fname, 'r', newline='') as file:
                csv_reader_object = csv.reader(file)
                # if csv.Sniffer().has_header:
                name_col = next(csv_reader_object)

                for row in name_col:
                    dataCSV[row] = []

                for row in csv_reader_object:  ##Varendo todas as linhas
                    for ndata in range(0, len(name_col)):  ## Varendo todas as colunas
                        dataCSV[name_col[ndata]].append(row[ndata])

                try:
                    for key, values in dataCSV.items():
                        if key == get_combobox(self.FuseCurve_ComboBox):
                            for value in values:
                                if value:
                                    if self.RatedCurrent_LineEdit.text() == '':
                                        m = float(value.split(';')[0])
                                    else:
                                        m = float(value.split(';')[0])*float(self.RatedCurrent_LineEdit.text())
                                    pointsXList.append(m)
                                    pointsYList.append(float(value.split(';')[1]))

                            name = 'Curva ' + key

                    print(pointsXList,pointsYList)
                    bluergb = (0, 0, 255, 255)
                    self.graphWidget.plot(pointsXList, pointsYList, name=name, pen=pen, symbol='o', symbolSize=10, symbolBrush=bluergb)
                except ValueError:
                    QMessageBox(QMessageBox.Warning, "Curva TCC - Fusível", "Erro ao carregar curva.", QMessageBox.Ok).exec()
                    self.PlotState = not self.PlotState

        if not self.PlotState:
             self.setFixedWidth(900)
             self.move(325,170)
        else:
            # self.resize(200, 200)
            self.setFixedWidth(440)
            self.move(860, 170)
        self.graphWidget.setHidden(self.PlotState)

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.AcceptAddEditFuse)

        self.ViewTCC_Btn = QPushButton("Visualizar TCC")
        self.ViewTCC_Btn.setMaximumWidth(150)
        self.ViewTCC_Btn.clicked.connect(self.viewCurve)

        self.ImportTCC_Btn = QPushButton("Importar TCC")
        self.ImportTCC_Btn.setMaximumWidth(150)
        self.ImportTCC_Btn.clicked.connect(self.ImportCurve)

        self.btngroupbox_layout.addWidget(self.ImportTCC_Btn)
        self.btngroupbox_layout.addWidget(self.ViewTCC_Btn)
        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def editFuse(self, get_name):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar Fusível {get_name()}'
            self.setWindowTitle(self.titleWindow)

            self.FuseName_LineEdit.setEnabled(False)
            self.show()
            self.updateEditDialog()
            self.Fuse_parent.load_FuseInfo()
            self.Fuse_parent.load_FusesDatabase()

            self.graphWidget.setHidden(True)
            self.setFixedWidth(440)
            self.move(860, 170)

        return process

    def addFuse(self):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar Fusível'
            self.setWindowTitle(self.titleWindow)

            self.FuseName_LineEdit.setEnabled(True)
            self.show()
            self.clearFuseParameters()
            self.updateEditDialog()

            self.graphWidget.setHidden(True)
            self.setFixedWidth(440)
            self.move(860, 170)

        return process

    def removeFuse(self):
        for ctd in self.Fuse_parent.FuseDataInfo:
            if ctd["Name"] == self.Fuse_parent.FuseSelect_Combobox.currentText():
                self.Fuse_parent.FuseDataInfo.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Fusível",
                            "Fusível " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
        self.clearFuseParameters()

        self.Fuse_parent.FuseSelect_Combobox.clear()
        for dicio in self.Fuse_parent.FuseDataInfo:
            self.Fuse_parent.FuseSelect_Combobox.addItem(dicio["Name"], dicio["Name"])

    def loadParameters(self):
        self.datainfo["Device"] = 'Fuse'
        self.datainfo["Name"] = get_lineedit(self.FuseName_LineEdit)
        ## Basic
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)

        #  Connections
        self.datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        self.datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        #  TCC Curves
        self.datainfo["FuseCurve"] = get_combobox(self.FuseCurve_ComboBox)
        self.datainfo["RatedCurrent"] = get_lineedit(self.RatedCurrent_LineEdit)

    def AcceptAddEditFuse(self):  # Dá para otimizar e muito // Somente um teste

        datainfo = {"Device": 'Fuse',
                    "Name": unidecode.unidecode(get_lineedit(self.FuseName_LineEdit).replace(" ", "_")),
                    "Action": get_combobox(self.Action_ComboBox), "Delay": get_lineedit(self.Delay_LineEdit),
                    "Enabled": get_combobox(self.Enable_ComboBox), "MonitoredObj": get_combobox(self.MonitObj_ComboBox),
                    "MonitoredTerm": get_combobox(self.MonitTerm_ComboBox),
                    "SwitchedObj": get_combobox(self.SwitchedObj_ComboBox),
                    "SwitchedTerm": get_combobox(self.SwitchedTerm_ComboBox),
                    "FuseCurve": get_combobox(self.FuseCurve_ComboBox),
                    "RatedCurrent": get_lineedit(self.RatedCurrent_LineEdit)}
        ## Basic
        #  Connections

        #  TCC Curves

        if self.FuseName_LineEdit.isEnabled():
            ctdExist = False
            for ctd in self.Fuse_parent.FuseDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.Fuse_parent.FuseDataInfo.append(datainfo)
                self.Fuse_parent.AddFuseDataInfo.append(datainfo)
                QMessageBox(QMessageBox.Information, "Fusível",
                            "Fusível " + datainfo["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Fusível",
                            "Fusível " + datainfo["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.Fuse_parent.FuseDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ## Basic
                    ctd["Action"] = datainfo["Action"]
                    ctd["Delay"] = datainfo["Delay"]
                    ctd["Enabled"] = datainfo["Enabled"]

                    #  Connections
                    ctd["MonitoredObj"] = datainfo["MonitoredObj"]
                    ctd["MonitoredTerm"] = datainfo["MonitoredTerm"]
                    ctd["SwitchedObj"] = datainfo["SwitchedObj"]
                    ctd["SwitchedTerm"] = datainfo["SwitchedTerm"]
                    #  TCC Curves
                    #  Phase
                    ctd["FuseCurve"] = datainfo["FuseCurve"]
                    ctd["RatedCurrent"] = datainfo["RatedCurrent"]

                    QMessageBox(QMessageBox.Information, "Fusível",
                                "Fusível " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.Fuse_parent.updateProtectDialog()
        self.adjustSize()
        self.close()

    def clearFuseParameters(self):
        self.FuseName_LineEdit.setText("")
        ## Basic
        self.Action_ComboBox.setCurrentIndex(0)
        self.Delay_LineEdit.setText("")
        self.Enable_ComboBox.setCurrentIndex(0)

        self.MonitObj_ComboBox.setCurrentIndex(0)
        self.MonitTerm_ComboBox.setCurrentIndex(0)
        self.SwitchedObj_ComboBox.setCurrentIndex(0)
        self.SwitchedTerm_ComboBox.setCurrentIndex(0)

        self.FuseCurve_ComboBox.setCurrentIndex(0)
        self.RatedCurrent_LineEdit.setText("")

    def updateEditDialog(self):
        self.MonitObj_ComboBox.clear()
        self.SwitchedObj_ComboBox.clear()

        for index, item in enumerate(self.Fuse_parent.ElementList):
            self.MonitObj_ComboBox.addItem(item, item)
            self.SwitchedObj_ComboBox.addItem(item, item)

def get_lineedit(lineedit):
    return lineedit.text()


def get_combobox(combobox):
    return str(combobox.itemData(combobox.currentIndex()))