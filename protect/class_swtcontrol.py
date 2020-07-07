from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QComboBox, QLineEdit, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import unidecode

import opendss.class_conn
import opendss.class_opendss
import config as cfg


class SwtControl(QWidget):

    def __init__(self):
        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Edit_SwtControl = EditSwtControl(self)
        self.SwtControlSettings_GroupBox = QGroupBox('Selecionar Switch')
        self.SwtControlSettings_GroupBox_Layout = QVBoxLayout()
        self.SwtControlSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.SwtControlSelect_Combobox = QComboBox()
        self.SwtControlSelect_Combobox.setMaximumWidth(150)
        self.SwtControlSettings_GroupBox_Layout.addWidget(self.SwtControlSelect_Combobox)

        self.ElementList = []
        self.AddSwtControlDataInfo = []
        self.SwtControlDataInfo = []
        self.loadDatabaseFlag = False
        self.flag = False

        #  Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.Remover_Btn.clicked.connect(self.Edit_SwtControl.removeSwtControl)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.Edit_Btn.clicked.connect(self.Edit_SwtControl.editSwtControl(self.SwtControlSelect_Combobox.currentText))
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.Add_Btn.clicked.connect(self.Edit_SwtControl.addSwtControl())
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.SwtControlSettings_GroupBox.setLayout(self.SwtControlSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.SwtControlSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def load_SwtControlInfo(self):
        SwtControlSelected = self.SwtControlSelect_Combobox.currentText()
        for item in self.SwtControlDataInfo:
            if item["Name"] == SwtControlSelected:

                self.Edit_SwtControl.SwtControlName_LineEdit.setText(item["Name"])

                if item["Action"] == 'close':
                    self.Edit_SwtControl.Action_ComboBox.setCurrentIndex(1)
                else:
                    self.Edit_SwtControl.Action_ComboBox.setCurrentIndex(0)

                self.Edit_SwtControl.Delay_LineEdit.setText(item["Delay"])

                if item["Enabled"] == 'yes' or item["Enabled"] == '':
                    self.Edit_SwtControl.Enable_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_SwtControl.Enable_ComboBox.setCurrentIndex(1)

                if item["Lock"] == 'yes':
                    self.Edit_SwtControl.Lock_ComboBox.setCurrentIndex(0)
                else:
                    self.Edit_SwtControl.Lock_ComboBox.setCurrentIndex(1)

                self.Edit_SwtControl.Normal_ComboBox.setCurrentText(item["Normal"])
                self.Edit_SwtControl.Reset_ComboBox.setCurrentText(item["Reset"])
                self.Edit_SwtControl.State_ComboBox.setCurrentText(item["State"])

                self.Edit_SwtControl.SwitchedObj_ComboBox.setCurrentText(item["SwitchedObj"])
                self.Edit_SwtControl.SwitchedTerm_ComboBox.setCurrentText(item["SwitchedTerm"])

    def load_SwtControlsDatabase(self):
        databaseSwtControldict = {}
        databaseSwtControl = self.OpenDSS.getSwtControlList()
        # print(databaseSwtControl)
        # Se trocar de subestação

        # Caso seja encontrado algum Switch que ainda pertence ao database, ou seja, se não foi trocado de subestação
        try:
            for item in databaseSwtControl:
                for item2 in self.SwtControlDataInfo:
                    if item.split(" SwitchedObj=")[0].split("New SwtControl.")[1] == item2["Name"]:
                        self.flag = True
                        return
                    else:
                        self.flag = False
        except IndexError:
            pass

        # Caso algum Switch tenha sido adicionado
        if self.AddSwtControlDataInfo:
            self.flag = True

        # Caso não haja Switches adicionados ou do database:
        if not self.flag:
            self.loadDatabaseFlag = False
            self.SwtControlDataInfo.clear()
            self.AddSwtControlDataInfo.clear()

        # Caso a lista de Switches esteja vazia:
        if not self.SwtControlDataInfo and not self.loadDatabaseFlag:
            for item in databaseSwtControl:
                databaseSwtControldict["Device"] = 'SwtControl'
                databaseSwtControldict["Name"] = item.split(" SwitchedObj=")[0].split("New Swtcontrol.")[1]
                # Basic
                if item.split(" lock=")[0].split("Action=")[1] == 'c':
                    databaseSwtControldict["Action"] = 'close'
                else:
                    databaseSwtControldict["Action"] = 'open'

                databaseSwtControldict["Delay"] = ''
                databaseSwtControldict["Enabled"] = ''
                databaseSwtControldict["Lock"] = item.split(" lock=")[1]
                databaseSwtControldict["Normal"] = ''
                databaseSwtControldict["Reset"] = ''
                databaseSwtControldict["State"] = ''
                # Connections
                databaseSwtControldict["SwitchedObj"] = item.split(" SwitchedTerm=")[0].split("SwitchedObj=")[1]
                databaseSwtControldict["SwitchedTerm"] = item.split(" Action=")[0].split("SwitchedTerm=")[1]
                self.SwtControlDataInfo.append(databaseSwtControldict.copy())

            self.loadDatabaseFlag = True

    def updateProtectDialog(self):
        self.load_SwtControlsDatabase()
        # Carregando a ElementList para ser usada na Edit Dialog
        self.ElementList = self.OpenDSS.getElementList()
        self.SwtControlSelect_Combobox.clear()
        for dicio in self.SwtControlDataInfo:
            self.SwtControlSelect_Combobox.addItem(dicio["Name"], dicio["Name"])


class EditSwtControl(QDialog):
    def __init__(self, SwtControl_parent):
        super().__init__()
        self.datainfo = {}
        self.titleWindow = "Blank"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.SwtControl_parent = SwtControl_parent
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825, 170)
        self.Dialog_Layout = QVBoxLayout()
        self.SwtControlInfo()
        self.Btns()
        self.setLayout(self.Dialog_Layout)

    def SwtControlInfo(self):
        # Parâmetros Intrínsecos do Switch
        self.Edit_SwtControl_GroupBox = QGroupBox('Geral')
        self.Edit_SwtControl_GroupBox_Layout = QGridLayout()
        self.Edit_SwtControl_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.SwtControlName_LineEdit = QLineEdit()
        self.SwtControlName_LineEdit_Label = QLabel("Dispositivo")
        self.SwtControlName_LineEdit.setMaximumWidth(150)

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

        self.Locklist = ['Sim', 'Não']
        self.Locklist_data = ['yes', 'no']
        self.Lock_ComboBox = QComboBox()
        self.Lock_ComboBox.setMaximumWidth(150)
        self.Lock_ComboBox_Label = QLabel("Lock")
        for index, item in enumerate(self.Locklist):
            self.Lock_ComboBox.addItem(item, self.Locklist_data[index])

        self.Normallist = ['Aberto', 'Fechado']
        self.Normallist_data = ['Open', 'Closed']
        self.Normal_ComboBox = QComboBox()
        self.Normal_ComboBox.setMaximumWidth(150)
        self.Normal_ComboBox_Label = QLabel("Normal State")
        for index, item in enumerate(self.Normallist):
            self.Normal_ComboBox.addItem(item, self.Normallist_data[index])

        self.Resetlist = ['Sim', 'Não']
        self.Resetlist_data = ['yes', 'no']
        self.Reset_ComboBox = QComboBox()
        self.Reset_ComboBox.setMaximumWidth(150)
        self.Reset_ComboBox_Label = QLabel("Reset")
        for index, item in enumerate(self.Resetlist):
            self.Reset_ComboBox.addItem(item, self.Resetlist_data[index])

        self.Statelist = ['Aberto', 'Fechado']
        self.Statelist_data = ['Open', 'Closed']
        self.State_ComboBox = QComboBox()
        self.State_ComboBox.setMaximumWidth(150)
        self.State_ComboBox_Label = QLabel("State")
        for index, item in enumerate(self.Statelist):
            self.State_ComboBox.addItem(item, self.Statelist_data[index])

        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.SwtControlName_LineEdit_Label, 0, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.SwtControlName_LineEdit, 0, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Action_ComboBox_Label, 1, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Action_ComboBox, 1, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Delay_LineEdit_Label, 2, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Delay_LineEdit, 2, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Enable_ComboBox_Label, 3, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Enable_ComboBox, 3, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Lock_ComboBox_Label, 4, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Lock_ComboBox, 4, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Normal_ComboBox_Label, 5, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Normal_ComboBox, 5, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Reset_ComboBox_Label, 6, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.Reset_ComboBox, 6, 1)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.State_ComboBox_Label, 7, 0)
        self.Edit_SwtControl_GroupBox_Layout.addWidget(self.State_ComboBox, 7, 1)

        self.Edit_SwtControl_GroupBox.setLayout(self.Edit_SwtControl_GroupBox_Layout)

        # Parâmetros de conexões do Switch
        self.Conn_SwtControl_GroupBox = QGroupBox('Conexões ')
        self.Conn_SwtControl_GroupBox_Layout = QGridLayout()
        self.Conn_SwtControl_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.SwitchedObj_ComboBox = QComboBox()
        self.SwitchedObj_ComboBox.setMinimumWidth(150)
        self.SwitchedObj_ComboBox_Label = QLabel("Elemento Chaveado")

        self.SwitchedTermList = ['1', '2']
        self.SwitchedTerm_ComboBox = QComboBox()
        self.SwitchedTerm_ComboBox.setMaximumWidth(150)
        self.SwitchedTerm_ComboBox_Label = QLabel("Terminal Chaveado")
        for index, item in enumerate(self.SwitchedTermList):
            self.SwitchedTerm_ComboBox.addItem(item, item)

        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox_Label, 1, 0, 1, 1)
        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedObj_ComboBox, 1, 1, 1, 1)
        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox_Label, 1, 2, 1, 1)
        self.Conn_SwtControl_GroupBox_Layout.addWidget(self.SwitchedTerm_ComboBox, 1, 3, 1, 1)
        self.Conn_SwtControl_GroupBox.setLayout(self.Conn_SwtControl_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_SwtControl_GroupBox)
        self.Dialog_Layout.addWidget(self.Conn_SwtControl_GroupBox)

    def Btns(self):
        self.btngroupbox_layout = QHBoxLayout()
        self.Ok_Btn = QPushButton("Ok")
        self.Ok_Btn.setMaximumWidth(150)
        self.Ok_Btn.clicked.connect(self.AcceptAddEditSwtControl)

        self.btngroupbox_layout.addWidget(self.Ok_Btn)

        self.Dialog_Layout.addLayout(self.btngroupbox_layout)

    def editSwtControl(self, get_name):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Editar Switch {get_name()}'
            self.setWindowTitle(self.titleWindow)

            self.SwtControlName_LineEdit.setEnabled(False)
            self.show()
            self.updateEditDialog()
            self.SwtControl_parent.load_SwtControlInfo()
            self.SwtControl_parent.load_SwtControlsDatabase()

        return process

    def addSwtControl(self):
        ## Pro gamer movement pra poder usar argumentos dentro do " .connect "
        def process():
            self.titleWindow = f' Adicionar Switch'
            self.setWindowTitle(self.titleWindow)

            self.SwtControlName_LineEdit.setEnabled(True)
            self.show()
            self.clearSwtControlParameters()
            self.updateEditDialog()

        return process

    def removeSwtControl(self):
        for ctd in self.SwtControl_parent.SwtControlDataInfo:
            if ctd["Name"] == self.SwtControl_parent.SwtControlSelect_Combobox.currentText():
                self.SwtControl_parent.SwtControlDataInfo.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Switch",
                            "Switch " + ctd["Name"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
        self.clearSwtControlParameters()

        self.SwtControl_parent.SwtControlSelect_Combobox.clear()
        for dicio in self.SwtControl_parent.SwtControlDataInfo:
            self.SwtControl_parent.SwtControlSelect_Combobox.addItem(dicio["Name"], dicio["Name"])

    def loadParameters(self):
        self.datainfo["Device"] = 'SwtControl'
        self.datainfo["Name"] = get_lineedit(self.SwtControlName_LineEdit)
        ## Basic
        self.datainfo["Action"] = get_combobox(self.Action_ComboBox)
        self.datainfo["Delay"] = get_lineedit(self.Delay_LineEdit)
        self.datainfo["Enabled"] = get_combobox(self.Enable_ComboBox)
        self.datainfo["Lock"] = get_combobox(self.Lock_ComboBox)
        self.datainfo["Normal"] = get_combobox(self.Normal_ComboBox)
        self.datainfo["Reset"] = get_combobox(self.Reset_ComboBox)
        self.datainfo["State"] = get_combobox(self.State_ComboBox)

        #  Connections
        self.datainfo["SwitchedObj"] = get_combobox(self.SwitchedObj_ComboBox)
        self.datainfo["SwitchedTerm"] = get_combobox(self.SwitchedTerm_ComboBox)

    def AcceptAddEditSwtControl(self):  # Dá para otimizar e muito // Somente um teste

        datainfo = {"Device": 'SwtControl',
                    "Name": unidecode.unidecode(get_lineedit(self.SwtControlName_LineEdit).replace(" ", "_")),
                    "Action": get_combobox(self.Action_ComboBox), "Delay": get_lineedit(self.Delay_LineEdit),
                    "Enabled": get_combobox(self.Enable_ComboBox), "Lock": get_combobox(self.Lock_ComboBox),
                    "Normal": get_combobox(self.Normal_ComboBox), "Reset": get_combobox(self.Reset_ComboBox),
                    "State": get_combobox(self.State_ComboBox), "SwitchedObj": get_combobox(self.SwitchedObj_ComboBox),
                    "SwitchedTerm": get_combobox(self.SwitchedTerm_ComboBox)}
        ## Basic
        #  Connections

        if self.SwtControlName_LineEdit.isEnabled():
            ctdExist = False
            for ctd in self.SwtControl_parent.SwtControlDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ctdExist = True
            if not ctdExist:
                self.SwtControl_parent.SwtControlDataInfo.append(datainfo)
                self.SwtControl_parent.AddSwtControlDataInfo.append(datainfo)
                QMessageBox(QMessageBox.Information, "Switch",
                            "Switch " + datainfo["Name"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Switch",
                            "Switch " + datainfo["Name"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.SwtControl_parent.SwtControlDataInfo:
                if ctd["Name"] == datainfo["Name"]:
                    ## Basic
                    ctd["Action"] = datainfo["Action"]
                    ctd["Delay"] = datainfo["Delay"]
                    ctd["Enabled"] = datainfo["Enabled"]
                    ctd["Lock"] = datainfo["Lock"]
                    ctd["Normal"] = datainfo["Normal"]
                    ctd["Reset"] = datainfo["Reset"]
                    ctd["State"] = datainfo["State"]

                    #  Connections
                    ctd["SwitchedObj"] = datainfo["SwitchedObj"]
                    ctd["SwitchedTerm"] = datainfo["SwitchedTerm"]

                    QMessageBox(QMessageBox.Information, "Switch",
                                "Switch " + ctd["Name"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.SwtControl_parent.updateProtectDialog()
        self.adjustSize()
        self.close()

    def clearSwtControlParameters(self):
        self.SwtControlName_LineEdit.setText("")
        ## Basic
        self.Action_ComboBox.setCurrentIndex(0)
        self.Delay_LineEdit.setText("")
        self.Enable_ComboBox.setCurrentIndex(0)
        self.Lock_ComboBox.setCurrentIndex(0)
        self.Normal_ComboBox.setCurrentIndex(0)
        self.Reset_ComboBox.setCurrentIndex(0)
        self.State_ComboBox.setCurrentIndex(0)

        self.SwitchedObj_ComboBox.setCurrentIndex(0)
        self.SwitchedTerm_ComboBox.setCurrentIndex(0)

    def updateEditDialog(self):
        self.SwitchedObj_ComboBox.clear()

        for index, item in enumerate(self.SwtControl_parent.ElementList):
            self.SwitchedObj_ComboBox.addItem(item, item)


def get_lineedit(lineedit):
    return lineedit.text()


def get_combobox(combobox):
    return str(combobox.itemData(combobox.currentIndex()))