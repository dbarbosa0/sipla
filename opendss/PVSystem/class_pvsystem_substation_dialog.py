from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QLineEdit, QLabel, QDoubleSpinBox, QComboBox, QHBoxLayout, \
    QPushButton, QMessageBox

from PyQt5.QtCore import Qt

import unidecode
import config as cfg

class Subestacao(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Configurar Subestação"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.dataSubestacao = {}

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(400, 475)

        ##Layout principal
        self.Dialog_Layout = QGridLayout()  # Layout da Dialog

        ################################### GroupBox Subestação #################################################
        self.Subestacao_GroupBox_PVdata = QGroupBox()
        self.Subestacao_GroupBox_PVdata_Layout = QGridLayout()

        ### Botões das Configurações
        self.Config_Btns_Layout = QHBoxLayout()
        self.Config_Btns_Layout.setAlignment(Qt.AlignRight)
        # Botao Restaurar Default
        self.Config_Btns_Default_Btn = QPushButton("Restaurar Default")  # Botão Default dentro do GroupBox
        self.Config_Btns_Default_Btn.setFixedHeight(30)
        self.Config_Btns_Default_Btn.setFixedWidth(150)
        self.Config_Btns_Default_Btn.clicked.connect(self.restauradefault)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Default_Btn)
        # Botão OK
        self.Config_Btns_OK_Btn = QPushButton("OK")  # Botão Ok dentro do GroupBox
        self.Config_Btns_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Config_Btns_OK_Btn.setFixedHeight(30)
        self.Config_Btns_OK_Btn.clicked.connect(self.AcceptSubstation)
        self.Config_Btns_OK_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_OK_Btn)
        # Botao Cancelar
        self.Config_Btns_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Config_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Config_Btns_Cancel_Btn.setFixedHeight(30)
        self.Config_Btns_Cancel_Btn.clicked.connect(self.CancelSubstation)
        self.Config_Btns_Cancel_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Cancel_Btn)

        #  Labels
        self.Subestacao_Name_Label = QLabel("Nome da Subestação:")
        self.Subestacao_XHL_Label = QLabel("XHL(%)")
        self.Subestacao_Bus1_Label = QLabel("Barra de conexão do Primário")
        self.Subestacao_VPrimary_Label = QLabel("Tensão no Primário")
        self.Subestacao_KVAPrimary_Label = QLabel("Potência no Primário")
        self.Subestacao_ConnPrimary_Label = QLabel("Tipo de conexão do Primário")
        self.Subestacao_Bus2_Label = QLabel("Barra de conexão do Secundário")
        self.Subestacao_VSecond_Label = QLabel("Tensão no Secundário")
        self.Subestacao_KVASecond_Label = QLabel("Potência no Secundário")
        self.Subestacao_ConnSecond_Label = QLabel("Tipo de conexão do Secundário")

        # LineEdits
        self.Subestacao_Name = QLineEdit()
        self.Subestacao_XHL = QDoubleSpinBox()
        self.Subestacao_XHL.setDecimals(2)
        self.Subestacao_XHL.setRange(0.01, 1000)
        self.Subestacao_XHL.setToolTip("Aceita valores entre 0,00 e 1000")
        self.Subestacao_XHL.setButtonSymbols(2)
        self.Subestacao_XHL.setValue(4.6)
        self.Subestacao_Bus1_LineEdit = QLineEdit()
        self.Subestacao_VPrimary = QDoubleSpinBox()
        self.Subestacao_VPrimary.setDecimals(2)
        self.Subestacao_VPrimary.setRange(0.01, 1000)
        self.Subestacao_VPrimary.setToolTip("Aceita valores entre 0,01 e 1000")
        self.Subestacao_VPrimary.setButtonSymbols(2)
        self.Subestacao_VPrimary.setValue(4.6)
        self.Subestacao_KVAPrimary = QDoubleSpinBox()
        self.Subestacao_KVAPrimary.setDecimals(2)
        self.Subestacao_KVAPrimary.setRange(0.01, 1000)
        self.Subestacao_KVAPrimary.setToolTip("Aceita valores entre 0,01 e 1000")
        self.Subestacao_KVAPrimary.setButtonSymbols(2)
        self.Subestacao_KVAPrimary.setValue(4.6)
        self.Subestacao_VSecond = QDoubleSpinBox()
        self.Subestacao_VSecond.setDecimals(2)
        self.Subestacao_VSecond.setRange(0.01, 1000)
        self.Subestacao_VSecond.setToolTip("Aceita valores entre 0,01 e 1000")
        self.Subestacao_VSecond.setButtonSymbols(2)
        self.Subestacao_VSecond.setValue(4.6)
        self.Subestacao_KVASecond = QDoubleSpinBox()
        self.Subestacao_KVASecond.setDecimals(2)
        self.Subestacao_KVASecond.setRange(0.01, 1000)
        self.Subestacao_KVASecond.setToolTip("Aceita valores entre 0,01 e 1000")
        self.Subestacao_KVASecond.setButtonSymbols(2)
        self.Subestacao_KVASecond.setValue(4.6)

        # Comboboxs
        self.Subestacao_ConnPrimary_ComboBox = QComboBox()
        self.Subestacao_ConnPrimary_ComboBox.addItems(["wye", "delta"])
        self.Subestacao_Bus2_ComboBox = QComboBox()
        self.Subestacao_ConnSecond_ComboBox = QComboBox()
        self.Subestacao_ConnSecond_ComboBox.addItems(["wye", "delta"])

        # Add Widgets and Layouts
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_Name_Label, 0, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_Name, 0, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_XHL_Label, 1, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_XHL, 1, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_Bus1_Label, 2, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_Bus1_LineEdit, 2, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_VPrimary_Label, 3, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_VPrimary, 3, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_KVAPrimary_Label, 4, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_KVAPrimary, 4, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_ConnPrimary_Label, 5, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_ConnPrimary_ComboBox, 5, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_Bus2_Label, 6, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_Bus2_ComboBox, 6, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_VSecond_Label, 7, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_VSecond, 7, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_KVASecond_Label, 8, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_KVASecond, 8, 1, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_ConnSecond_Label, 9, 0, 1, 1)
        self.Subestacao_GroupBox_PVdata_Layout.addWidget(self.Subestacao_ConnSecond_ComboBox, 9, 1, 1, 1)

        self.Dialog_Layout.addLayout(self.Config_Btns_Layout, 1, 1, 1, 1)

        self.Subestacao_GroupBox_PVdata.setLayout(self.Subestacao_GroupBox_PVdata_Layout)
        self.Dialog_Layout.addWidget(self.Subestacao_GroupBox_PVdata, 0, 1, 1, 1)
        self.setLayout(self.Dialog_Layout)

    def restauradefault(self):
        self.clearSubstationParameters()
        self.defaultSubstationParameters()

    def AcceptSubstation(self):
        if self.get_Bus1() == '':
            msg = QMessageBox()
            msg.information(self, "Inserir Subestação", "Adicione um nome a barra de conexão do primário")

        else:
            if self.get_Substation_Name() == '':
                msg = QMessageBox()
                msg.information(self, "Inserir Subestação", "Adicione um nome a Subestação")

            else:
                self.dataSubestacao["subsname"] = self.get_Substation_Name()
                self.dataSubestacao["xhl"] = self.get_XHL()
                self.dataSubestacao["bus1"] = self.get_Bus1()
                self.dataSubestacao["kv1"] = self.get_VPrimary()
                self.dataSubestacao["kva1"] = self.get_KVAPrimary()
                self.dataSubestacao["conn1"] = self.get_ConnPrimary()
                self.dataSubestacao["bus2"] = self.get_Bus2()
                self.dataSubestacao["kv2"] = self.get_VSecond()
                self.dataSubestacao["kva2"] = self.get_KVASecond()
                self.dataSubestacao["conn2"] = self.get_ConnSecond()
                self.close()

    def CancelSubstation(self):
        self.clearSubstationParameters()
        self.defaultSubstationParameters()
        self.close()

    def clearSubstationParameters(self):
        self.Subestacao_Name.clear()
        self.Subestacao_XHL.clear()
        self.Subestacao_Bus1_LineEdit.clear()
        self.Subestacao_VPrimary.clear()
        self.Subestacao_KVAPrimary.clear()
        self.Subestacao_ConnPrimary_ComboBox.setCurrentIndex(0)
        self.Subestacao_Bus2_ComboBox.setCurrentIndex(0)
        self.Subestacao_VSecond.clear()
        self.Subestacao_KVASecond.clear()
        self.Subestacao_ConnSecond_ComboBox.setCurrentIndex(0)

    def defaultSubstationParameters(self):
        self.Subestacao_Name.setText("")
        self.Subestacao_XHL.setValue(5.75)
        self.Subestacao_Bus1_LineEdit.setText("")
        self.Subestacao_VPrimary.setValue(0.48)
        self.Subestacao_KVAPrimary.setValue(750)
        self.Subestacao_ConnPrimary_ComboBox.setCurrentIndex(0)
        self.Subestacao_Bus2_ComboBox.setCurrentIndex(0)
        self.Subestacao_VSecond.setValue(4.16)
        self.Subestacao_KVASecond.setValue(750)
        self.Subestacao_ConnSecond_ComboBox.setCurrentIndex(0)

    # Gets

    def get_Substation_Name(self):
        return unidecode.unidecode(self.Subestacao_Name.text().strip().replace(" ", "_"))

    def get_XHL(self):
        return self.Subestacao_XHL.text().replace(",", ".")

    def get_VPrimary(self):
        return self.Subestacao_VPrimary.text().replace(",", ".")

    def get_KVAPrimary(self):
        return self.Subestacao_KVAPrimary.text().replace(",", ".")

    def get_VSecond(self):
        return self.Subestacao_VSecond.text().replace(",", ".")

    def get_KVASecond(self):
        return self.Subestacao_KVASecond.text().replace(",", ".")

    def get_Bus1(self):
        return unidecode.unidecode(self.Subestacao_Bus1_LineEdit.text().strip().replace(" ", "_"))

    def get_ConnPrimary(self):
        return self.Subestacao_ConnPrimary_ComboBox.currentText()

    def get_Bus2(self):
        return self.Subestacao_Bus2_ComboBox.currentText()

    def get_ConnSecond(self):
        return self.Subestacao_ConnSecond_ComboBox.currentText()