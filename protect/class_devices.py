# Carvalho Tag
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QTabWidget, QComboBox, QLineEdit, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt

import opendss.class_conn
import opendss.class_opendss
import config as cfg


class C_Devices_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Dispositivos de proteção"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        # self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)

        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        self.TabWidget = QTabWidget()
        self.TabRecloser = Recloser()

        self.TabWidget.addTab(self.TabRecloser, "Recloser")
        self.Dialog_Layout.addWidget(self.TabWidget)

        #  Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 0)

        self.setLayout(self.Dialog_Layout)

    def Accept(self):
        self.close()


# Método "estático", não precisa estar dentro de alguma classe
def get_lineedit(lineedit):
    return lineedit.text()


def get_combobox(combobox):
    return str(combobox.itemData(combobox.currentIndex()))


def gen_recloserString(datainfo, device="GenericDevice"):
    string = "Edit " + device + "." + datainfo.get("Name")
    keys = list(datainfo.keys())
    for key in keys:
        if datainfo.get(key) != '' and key != "Name":
            string += ' ' + key + '=' + datainfo.get(key)

    print(string)


class Recloser(QWidget):

    def __init__(self):
        super().__init__()
        self.TCClist = ['A', 'B', 'C', 'D', 'E']
        self.TCClist_data = ['1', '2', '3', '4', '5']

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_Recloser = EditRecloser(self)
        self.RecloserSettings_GroupBox = QGroupBox('Selecionar Religador')
        self.RecloserSettings_GroupBox_Layout = QVBoxLayout()
        self.RecloserSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RecloserSelect_Combobox = QComboBox()
        self.RecloserSelect_Combobox.setMaximumWidth(150)
        self.RecloserSettings_GroupBox_Layout.addWidget(self.RecloserSelect_Combobox)
        self.RecloserNameList = []
        self.ElementList = []
        self.Edit_RECDataInfo = []
        self.Add_RECDataInfo = []


        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        # self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        # self.Remover_Btn.clicked.connect(self.dialog)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        # self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        # self.Edit_Btn.setFixedWidth(80)
        self.Edit_Btn.clicked.connect(self.Edit_Recloser.edit_exec(self.RecloserSelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        # self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        # self.Add_Btn.setFixedWidth(80)
        self.Add_Btn.clicked.connect(self.Edit_Recloser.add_exec())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.RecloserSettings_GroupBox.setLayout(self.RecloserSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.RecloserSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def updateDialog(self):
        self.RecloserSelect_Combobox.clear()
        list = self.OpenDSS.getRecloserList()
        if len(list) > 0:
            RecloserList = self.RecloserNameList
        else:
            RecloserList = ['None', 'None']

        for index, item in enumerate(RecloserList):
            self.RecloserSelect_Combobox.addItem(item, item)

        self.ElementList = self.OpenDSS.getElementList()

    def gen_RecloserNameList(self):
        list = self.OpenDSS.getRecloserList()
        if len(list) > 0:
            for item in list:
                if item not in self.RecloserNameList:
                    self.RecloserNameList.append(item.split(" MonitoredObj=")[0].split("New Recloser.")[1])

    def load_RecloserInfo(self):
        self.recloserString = 'New Recloser.F00378 MonitoredObj=Line.F00378 SwitchedObj=Line.F00378 SwitchedTerm=2 action=c'
        recloserSelected = "Recloser." + self.RecloserSelect_Combobox.currentText()
        Recloserlist = self.OpenDSS.getRecloserList()
        for item in Recloserlist:
            if recloserSelected in item:
                self.recloserString = item

        print(self.recloserString)
        if self.recloserString.split(" action=")[1] == 'c':
            self.Edit_Recloser.Action_ComboBox.setCurrentIndex(1)
        else:
            self.Edit_Recloser.Action_ComboBox.setCurrentIndex(0)

        MonitObj = self.recloserString.split(" SwitchedObj=")[0].split("MonitoredObj=")[1]
        self.Edit_Recloser.MonitObj_ComboBox.setCurrentText(MonitObj)
        SwitchedObj = self.recloserString.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
        self.Edit_Recloser.SwitchedObj_ComboBox.setCurrentText(SwitchedObj)
        SwitchedTerm = self.recloserString.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
        self.Edit_Recloser.MonitTerm_ComboBox.setCurrentText(SwitchedTerm)
        self.Edit_Recloser.SwitchedTerm_ComboBox.setCurrentText(SwitchedTerm)


class EditRecloser(QDialog):
    def __init__(self, recloser_parent):
        super().__init__()
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.recloser_parent = recloser_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.EditFlag = False
        self.AddFlag = False

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825, 0)  ##Resolução 1366x768
        self.Dialog_Layout = QVBoxLayout()
        self.RecInfo()
        self.Btns()
        self.setLayout(self.Dialog_Layout)

    def RecInfo(self):
        # Parâmetros Intrínsecos do religador
        self.Edit_Recloser_GroupBox = QGroupBox('Geral')
        self.Edit_Recloser_GroupBox_Layout = QGridLayout()
        self.Edit_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RecloserName_LineEdit = QLineEdit()
        self.RecloserName_LineEdit_Label = QLabel("Dispositivo")
        self.RecloserName_LineEdit.setMaximumWidth(150)

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

        self.NumFast_LineEdit = QLineEdit()
        self.NumFast_LineEdit.setMaximumWidth(150)
        self.NumFast_LineEdit_Label = QLabel("Fast Shots")

        self.Shots_LineEdit = QLineEdit()
        self.Shots_LineEdit.setMaximumWidth(150)
        self.Shots_LineEdit_Label = QLabel("Total Shots")

        self.RecloserIntervals_LineEdit = QLineEdit()
        self.RecloserIntervals_LineEdit.setPlaceholderText("Ex: 2,2,5,5")
        self.RecloserIntervals_LineEdit.setMaximumWidth(150)
        self.RecloserIntervals_LineEdit_Label = QLabel("RecloserIntervals")

        self.ResetTime_LineEdit = QLineEdit()
        self.ResetTime_LineEdit_Label = QLabel("ResetTime")
        self.ResetTime_LineEdit.setMaximumWidth(150)

        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserName_LineEdit_Label, 0, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserName_LineEdit, 0, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 1, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_ComboBox, 1, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 2, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit, 2, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 3, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Enable_ComboBox, 3, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Shots_LineEdit_Label, 4, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Shots_LineEdit, 4, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.NumFast_LineEdit_Label, 5, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.NumFast_LineEdit, 5, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserIntervals_LineEdit_Label, 6, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.RecloserIntervals_LineEdit, 6, 1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.ResetTime_LineEdit_Label, 7, 0)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.ResetTime_LineEdit, 7, 1)
        self.Edit_Recloser_GroupBox.setLayout(self.Edit_Recloser_GroupBox_Layout)

        # Parâmetros de conexões do religador
        self.Conn_Recloser_GroupBox = QGroupBox('Conexões ')
        self.Conn_Recloser_GroupBox_Layout = QGridLayout()
        self.Conn_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

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

        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitObj_ComboBox_Label, 0, 0, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitObj_ComboBox, 0, 1, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox_Label, 0, 2, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.MonitTerm_ComboBox, 0, 3, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_Recloser_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
        self.Conn_Recloser_GroupBox.setLayout(self.Conn_Recloser_GroupBox_Layout)

        # Curvas TCC
        self.TCCCurves_Recloser_GroupBox = QGroupBox('Curvas TCC')
        self.TCCCurves_Recloser_GroupBox_Layout = QGridLayout()
        self.TCCCurves_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.GroundDelayList = ['a', 'b', 'c', 'd']
        self.GroundDelay_ComboBox = QComboBox()
        self.GroundDelay_ComboBox.setMaximumWidth(150)
        self.GroundDelay_ComboBox_Label = QLabel("Ground Delayed")
        for index, item in enumerate(self.GroundDelayList):
            self.GroundDelay_ComboBox.addItem(item, item)

        self.GroundFastList = ['A', 'B', 'C', 'D']
        self.GroundFast_ComboBox = QComboBox()
        self.GroundFast_ComboBox.setMaximumWidth(150)
        self.GroundFast_ComboBox_Label = QLabel("Ground Fast")
        for index, item in enumerate(self.GroundFastList):
            self.GroundFast_ComboBox.addItem(item, item)

        self.GroundTrip_LineEdit = QLineEdit()
        self.GroundTrip_LineEdit.setMaximumWidth(50)
        self.GroundTrip_LineEdit.setPlaceholderText("1.0")
        self.GroundTrip_LineEdit_Label = QLabel("Ground Multiplier Amps")

        self.GroundDelayTimeDial_LineEdit = QLineEdit()
        self.GroundDelayTimeDial_LineEdit.setMaximumWidth(50)
        self.GroundDelayTimeDial_LineEdit.setPlaceholderText("1.0")
        self.GroundDelayTimeDial_LineEdit_Label = QLabel("Time dial - Ground Delayed")

        self.GroundFastTimeDial_LineEdit = QLineEdit()
        self.GroundFastTimeDial_LineEdit.setMaximumWidth(50)
        self.GroundFastTimeDial_LineEdit.setPlaceholderText("1.0")
        self.GroundFastTimeDial_LineEdit_Label = QLabel("Time dial - Ground Fast")

        self.PhaseDelayList = ['aaa', 'bbb', 'ccc', 'ddd']
        self.PhaseDelay_ComboBox = QComboBox()
        self.PhaseDelay_ComboBox.setMaximumWidth(150)
        self.PhaseDelay_ComboBox_Label = QLabel("Phase Delayed")
        for index, item in enumerate(self.PhaseDelayList):
            self.PhaseDelay_ComboBox.addItem(item, item)

        self.PhaseFastList = ['AAA', 'BBB', 'CCC', 'DDD']
        self.PhaseFast_ComboBox = QComboBox()
        self.PhaseFast_ComboBox.setMaximumWidth(150)
        self.PhaseFast_ComboBox_Label = QLabel("Phase Fast")
        for index, item in enumerate(self.PhaseFastList):
            self.PhaseFast_ComboBox.addItem(item, item)

        self.PhaseTrip_LineEdit = QLineEdit()
        self.PhaseTrip_LineEdit.setMaximumWidth(50)
        self.PhaseTrip_LineEdit.setPlaceholderText("1.0")
        self.PhaseTrip_LineEdit_Label = QLabel("Phase Multiplier Amps")

        self.PhaseDelayTimeDial_LineEdit = QLineEdit()
        self.PhaseDelayTimeDial_LineEdit.setMaximumWidth(50)
        self.PhaseDelayTimeDial_LineEdit.setPlaceholderText("1.0")
        self.PhaseDelayTimeDial_LineEdit_Label = QLabel("Time dial - Phase Delayed")

        self.PhaseFastTimeDial_LineEdit = QLineEdit()
        self.PhaseFastTimeDial_LineEdit.setMaximumWidth(50)
        self.PhaseFastTimeDial_LineEdit.setPlaceholderText("1.0")
        self.PhaseFastTimeDial_LineEdit_Label = QLabel("Time dial - Phase Fast")

        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit_Label, 0, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseTrip_LineEdit, 0, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelayTimeDial_LineEdit_Label, 1, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelayTimeDial_LineEdit, 1, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelay_ComboBox_Label, 1, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseDelay_ComboBox, 1, 1, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFastTimeDial_LineEdit_Label, 2, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFastTimeDial_LineEdit, 2, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFast_ComboBox_Label, 2, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.PhaseFast_ComboBox, 2, 1, 1, 1)

        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit_Label, 4, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundTrip_LineEdit, 4, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelayTimeDial_LineEdit_Label, 5, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelayTimeDial_LineEdit, 5, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelay_ComboBox_Label, 5, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundDelay_ComboBox, 5, 1, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFastTimeDial_LineEdit_Label, 6, 2, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFastTimeDial_LineEdit, 6, 3, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFast_ComboBox_Label, 6, 0, 1, 1)
        self.TCCCurves_Recloser_GroupBox_Layout.addWidget(self.GroundFast_ComboBox, 6, 1, 1, 1)

        self.TCCCurves_Recloser_GroupBox.setLayout(self.TCCCurves_Recloser_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_Recloser_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_Recloser_GroupBox)
        self.Dialog_Layout.addWidget(self.TCCCurves_Recloser_GroupBox)

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.exec_okBtn)

        self.AddTCC_Btn = QPushButton("Add TCC Curve")
        self.AddTCC_Btn.setMaximumWidth(150)
        # self.AddTCC_Btn.clicked.connect(self.recloser_parent.RecloserList)

        self.btngroupbox_layout.addWidget(self.AddTCC_Btn)
        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def edit_exec(self, get_name):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar religador {get_name()}'
            self.RecloserName_LineEdit.setEnabled(False)
            self.setWindowTitle(self.titleWindow)
            self.show()
            self.updateDialog()
            self.RecloserName_LineEdit.setText(self.titleWindow.split(" Editar religador ")[1])
            self.recloser_parent.load_RecloserInfo()
            self.EditFlag = True
            self.AddFlag = False
        return process

    def add_exec(self):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar religador'
            self.RecloserName_LineEdit.setEnabled(True)
            self.setWindowTitle(self.titleWindow)
            self.show()
            self.updateDialog()
            self.RecloserName_LineEdit.clear()
            self.EditFlag = False
            self.AddFlag = True

        return process

    def exec_okBtn(self):
        if self.AddFlag:
            if get_lineedit(self.RecloserName_LineEdit) in self.recloser_parent.RecloserNameList:
                QMessageBox(QMessageBox.Warning, "Energy Meter", "Religador já existe",
                            QMessageBox.Ok).exec()
                return
            elif self.AddFlag and get_lineedit(self.RecloserName_LineEdit) == '':
                QMessageBox(QMessageBox.Warning, "Energy Meter", "Escolha um nome para o religador",
                            QMessageBox.Ok).exec()
                return
            # Armazena os parametros em datainfo
            self.loadParameters()
            # Gera a string Edit do recloser
            gen_recloserString(self.datainfo, "Recloser")
            # Adiciona na lista de religadores editados
            self.recloser_parent.Add_RECDataInfo.append(self.datainfo)
            self.recloser_parent.RecloserNameList.append(self.datainfo["Name"])

        if self.EditFlag:
            # Armazena os parametros em datainfo
            self.loadParameters()
            # Gera a string Edit do recloser
            gen_recloserString(self.datainfo, "Recloser")
            # Adiciona na lista de religadores editados
            self.recloser_parent.Edit_RECDataInfo.append(self.datainfo)

        self.close()
        self.EditFlag = False
        self.AddFlag = False
        print(f'Add_RECDataInfo: {self.recloser_parent.Add_RECDataInfo}')
        print(f'Edit_RECDataInfo: {self.recloser_parent.Edit_RECDataInfo}')
        print(f'RecloserNameList: {self.recloser_parent.RecloserNameList}')
        self.recloser_parent.updateDialog()

    def loadParameters(self):
        self.datainfo["Name"] = get_lineedit(self.RecloserName_LineEdit)
        ## Basic
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        self.datainfo["Shots"] = get_lineedit(self.Shots_LineEdit)
        self.datainfo["NumFast"] = get_lineedit(self.NumFast_LineEdit)
        self.datainfo["RecloseIntervals"] = get_lineedit(self.RecloserIntervals_LineEdit)
        self.datainfo["Reset"] = get_lineedit(self.ResetTime_LineEdit)

        #  Connections
        self.datainfo["MonitoredObj"] = get_combobox(self.MonitObj_ComboBox)
        self.datainfo["MonitoredTerm"] = get_combobox(self.MonitTerm_ComboBox)
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

        #  TCC Curves
        #  Phase
        self.datainfo["PhaseDelayed"] = get_combobox(self.PhaseDelay_ComboBox)
        self.datainfo["PhaseFast"] = get_combobox(self.PhaseFast_ComboBox)
        self.datainfo["PhaseTrip"] = get_lineedit(self.PhaseTrip_LineEdit)
        self.datainfo["TDPhDelayed"] = get_lineedit(self.PhaseDelayTimeDial_LineEdit)
        self.datainfo["TDPhFast"] = get_lineedit(self.PhaseFastTimeDial_LineEdit)
        #  Ground
        self.datainfo["GroundDelayed"] = get_combobox(self.GroundDelay_ComboBox)
        self.datainfo["GroundFast"] = get_combobox(self.GroundFast_ComboBox)
        self.datainfo["GroundTrip"] = get_lineedit(self.GroundTrip_LineEdit)
        self.datainfo["TDGrDelayed"] = get_lineedit(self.GroundDelayTimeDial_LineEdit)
        self.datainfo["TDGrFast"] = get_lineedit(self.GroundFastTimeDial_LineEdit)

        # print(self.datainfo)

    def updateDialog(self):
        self.MonitObj_ComboBox.clear()
        self.SwitchedObj_ComboBox.clear()
        if len(self.recloser_parent.ElementList) > 0:
            ElementList = self.recloser_parent.ElementList
        else:
            ElementList = ['', 'None']

        for index, item in enumerate(ElementList):
            self.MonitObj_ComboBox.addItem(item, item)
            self.SwitchedObj_ComboBox.addItem(item, item)
