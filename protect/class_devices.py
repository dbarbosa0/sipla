# Carvalho Tag
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QGridLayout, QHBoxLayout, \
    QPushButton, QVBoxLayout, QTabWidget, QComboBox, QLineEdit,  QWidget, QMessageBox
from PyQt5.QtCore import Qt

import configparser
import class_exception
import opendss.class_conn
import opendss.class_opendss
import config as cfg

class C_Devices_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Dispositivos de proteção"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.SCDataInfo = [] ## Vetor com todos os dicionários para faltas  - Com

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

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 0)

        self.setLayout(self.Dialog_Layout)
    def saveDefaultParameters(self):
        try:
            config = configparser.ConfigParser()
            ## Basic
            config['FltConfigBasic'] = {}
            config['FltConfigBasic']['FltBus'] = self.get_combobox(self.TabBasic.FltBus_GroupBox_ComboBox)
            config['FltConfigBasic']['FltPhases'] = self.get_combobox(self.TabBasic.FltPhases_GroupBox_ComboBox)
            config['FltConfigBasic']['FltRst'] = self.get_lineedit(self.TabBasic.FltResistance_GroupBox_LineEdit)
            config['FltConfigBasic']['FltType'] = self.get_combobox(self.TabBasic.FltType_GroupBox_ComboBox)
            config['FltConfigBasic']['FltTime'] = self.get_lineedit(self.TabBasic.FltTime_GroupBox_LineEdit)
            config['FltConfigBasic']['FltBus2'] = self.get_combobox(self.TabBasic.FltBus2_GroupBox_ComboBox)

            config['FltConfigAdvanced'] = {}
            config['FltConfigAdvanced']['FltBaseFreq'] = self.get_combobox(self.TabAdvanced.FltBaseFreq_GroupBox_ComboBox)
            config['FltConfigAdvanced']['FltRstDev'] = self.get_lineedit(self.TabAdvanced.FltRstDev_GroupBox_LineEdit)
            config['FltConfigAdvanced']['FltRepair'] = self.get_lineedit(self.TabAdvanced.FltRepair_GroupBox_LineEdit)

            with open('scanconfig.ini', 'w') as configfile:
                config.write(configfile)

            QMessageBox(QMessageBox.Information, "SC Analyze Configuration", "Configurações Salvas com Sucesso!",
                        QMessageBox.Ok).exec()

        except:
            raise class_exception.ExecConfigOpenDSS("Configuração da Análise de Curto Circuito", "Erro ao salvar parâmetros!")

    def get_lineedit(self, lineedit):
        self.lineedit = lineedit.text()
        return self.lineedit

    def get_combobox(self, combobox):
        ## itemData corresponde à tag do item selecionado no combobox. "None" aparece quando não há nada no combobox
        ## currentIndex indica o índice do item selecionado
        self.combobox = str(combobox.itemData(combobox.currentIndex()))
        return self.combobox

    def Accept(self):
        self.close()


class Recloser(QWidget):
    def __init__(self):
        super().__init__()

        self.TCClist = ['A', 'B', 'C', 'D', 'E']
        self.TCClist_data = ['1', '2', '3', '4', '5']

        self.Edit_Recloser = EditRecloser()
        self.RecloserSettings_GroupBox = QGroupBox('Selecionar Religador')
        self.RecloserSettings_GroupBox_Layout = QVBoxLayout()
        self.RecloserSettings_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.RecloserSelect_Combobox = QComboBox()
        self.RecloserSelect_Combobox.setMaximumWidth(150)
        self.RecloserSettings_GroupBox_Layout.addWidget(self.RecloserSelect_Combobox)


        ##### Btns
        self.Tab_Btns_Layout = QHBoxLayout()
        self.Tab_Btns_Layout.setAlignment(Qt.AlignCenter)

        self.Remover_Btn = QPushButton("Remover")
        #self.Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        #self.Remover_Btn.clicked.connect(self.dialog)
        self.Tab_Btns_Layout.addWidget(self.Remover_Btn)

        self.Edit_Btn = QPushButton("Editar")
        #self.Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        #self.Edit_Btn.setFixedWidth(80)
        self.Edit_Btn.clicked.connect(self.Edit_Recloser.show)
        self.Tab_Btns_Layout.addWidget(self.Edit_Btn)

        self.Add_Btn = QPushButton("Adicionar")
        #self.Add_Btn.setIcon(QIcon('img/icon_add.png'))
        #self.Add_Btn.setFixedWidth(80)
        #self.Add_Btn.clicked.connect(self.addMonitor)
        self.Tab_Btns_Layout.addWidget(self.Add_Btn)

        self.RecloserSettings_GroupBox.setLayout(self.RecloserSettings_GroupBox_Layout)
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.RecloserSettings_GroupBox)
        self.Tab_layout.addLayout(self.Tab_Btns_Layout)
        self.setLayout(self.Tab_layout)

    def updateDialog(self):
        self.RecloserSelect_Combobox.clear()
        RecloserList = ['Religador A', 'Religador B', 'Religador C', 'Religador D', 'Religador E']
        for index, item in enumerate(RecloserList):
            self.RecloserSelect_Combobox.addItem(item, item)

    def enlarge_window(self):
        self.setGeometry(0, 0, 100,100)

class EditRecloser(QDialog):
    def __init__(self):
        super().__init__()
        self.titleWindow = "Editar religador"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(200, 200)
        self.move(825,238) ##Resolução 1366x768
        self.Dialog_Layout = QVBoxLayout()

        self.Edit_Recloser_GroupBox = QGroupBox('Religador Selecionado')
        self.Edit_Recloser_GroupBox_Layout = QGridLayout()
        self.Edit_Recloser_GroupBox_Layout.setAlignment(Qt.AlignCenter)

        self.Action_LineEdit = QLineEdit()
        self.Action_LineEdit.setPlaceholderText('Ex: 0.0001')
        self.Action_LineEdit.setMaximumWidth(150)

        self.Delay_LineEdit = QLineEdit()
        self.Delay_LineEdit.setPlaceholderText('Ex: 0.0001')
        self.Delay_LineEdit.setMaximumWidth(150)



        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Action_LineEdit,0,0,1,1)
        self.Edit_Recloser_GroupBox_Layout.addWidget(self.Delay_LineEdit, 0, 1, 1, 3)

        self.Edit_Recloser_GroupBox.setLayout(self.Edit_Recloser_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.Edit_Recloser_GroupBox)
        self.setLayout(self.Dialog_Layout)