from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QVBoxLayout, \
    QPushButton, QLabel, QHBoxLayout,  QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt

import config as cfg

class C_Reactive_Pow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho da Potencia Reativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho da Potência Reativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

        # self.OpenDSS = opendss.class_opendss.C_OpenDSS()


    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QVBoxLayout()

        self.Dialog_Label = QLabel("Selecione um modo")
        self.Dialog_Layout.addWidget(self.Dialog_Label)

        self.BtnGroup = QButtonGroup()

        ################# GroupBox Auto Despacho #########################
        self.AutoDespacho_GroupBox = QGroupBox("Auto Despacho")
        #self.AutoDespacho_GroupBox.setFixedWidth(175)
        self.AutoDespacho_GroupBox_Layout = QVBoxLayout()

        # Radio Btn "FP Constante"
        self.AutoDespacho_GroupBox_Layout_FPConst_RadioBtn = QRadioButton("FP Constante")
        self.AutoDespacho_GroupBox_Layout_FPConst_RadioBtn.setChecked(False)
        self.AutoDespacho_GroupBox_Layout_FPConst_RadioBtn.clicked.connect(self.ReactPowFPConst)
        self.AutoDespacho_GroupBox_Layout.addWidget(self.AutoDespacho_GroupBox_Layout_FPConst_RadioBtn)
        self.BtnGroup.addButton(self.AutoDespacho_GroupBox_Layout_FPConst_RadioBtn)
        # Radio Btn "kVar Constante"
        self.AutoDespacho_GroupBox_Layout_kvarConst_RadioBtn = QRadioButton("kVar Constante")
        self.AutoDespacho_GroupBox_Layout_kvarConst_RadioBtn.setChecked(False)
        self.AutoDespacho_GroupBox_Layout_kvarConst_RadioBtn.clicked.connect(self.ReactPowkvarConst)
        self.AutoDespacho_GroupBox_Layout.addWidget(self.AutoDespacho_GroupBox_Layout_kvarConst_RadioBtn)
        self.BtnGroup.addButton(self.AutoDespacho_GroupBox_Layout_kvarConst_RadioBtn)

        self.AutoDespacho_GroupBox.setLayout(self.AutoDespacho_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.AutoDespacho_GroupBox)

        ################# GroupBox Inversor Cntroller #########################
        self.InvCont_GroupBox = QGroupBox("Inversor Controller")
        #self.InvCont_GroupBox.setFixedWidth(175)
        self.InvCont_GroupBox_Layout = QVBoxLayout()

        # Radio Btn "Volt-Var"
        self.InvCont_GroupBox_Layout_VV_RadioBtn = QRadioButton("Volt - Var")
        self.InvCont_GroupBox_Layout_VV_RadioBtn.setChecked(False)
        self.InvCont_GroupBox_Layout_VV_RadioBtn.clicked.connect(self.ReactPowVV)
        self.InvCont_GroupBox_Layout.addWidget(self.InvCont_GroupBox_Layout_VV_RadioBtn)
        self.BtnGroup.addButton(self.InvCont_GroupBox_Layout_VV_RadioBtn)
        # Radio Btn "Dynamic Reactive Current"
        self.InvCont_GroupBox_Layout_DRC_RadioBtn = QRadioButton("Dynamic Reactive Current")
        self.InvCont_GroupBox_Layout_DRC_RadioBtn.setChecked(False)
        self.InvCont_GroupBox_Layout_DRC_RadioBtn.clicked.connect(self.ReactPowDRC)
        self.InvCont_GroupBox_Layout.addWidget(self.InvCont_GroupBox_Layout_DRC_RadioBtn)
        self.BtnGroup.addButton(self.InvCont_GroupBox_Layout_DRC_RadioBtn)
        # Radio Btn "Volt-Var e Dynamic Reactive Current"
        self.InvCont_GroupBox_Layout_VVeDRC_RadioBtn = QRadioButton("Volt - Var e Dynamic Reactive Current")
        self.InvCont_GroupBox_Layout_VVeDRC_RadioBtn.setChecked(False)
        self.InvCont_GroupBox_Layout_VVeDRC_RadioBtn.clicked.connect(self.ReactPowVVeDRC)
        self.InvCont_GroupBox_Layout.addWidget(self.InvCont_GroupBox_Layout_VVeDRC_RadioBtn)
        self.BtnGroup.addButton(self.InvCont_GroupBox_Layout_VVeDRC_RadioBtn)
        # Radio Btn "Volt-Var e Volt-Watt"
        self.InvCont_GroupBox_Layout_VVeVW_RadioBtn = QRadioButton("Volt - Var e Volt - Watt")
        self.InvCont_GroupBox_Layout_VVeVW_RadioBtn.setChecked(False)
        self.InvCont_GroupBox_Layout_VVeVW_RadioBtn.clicked.connect(self.ReactPowVVeVW)
        self.InvCont_GroupBox_Layout.addWidget(self.InvCont_GroupBox_Layout_VVeVW_RadioBtn)
        self.BtnGroup.addButton(self.InvCont_GroupBox_Layout_VVeVW_RadioBtn)

        self.InvCont_GroupBox.setLayout(self.InvCont_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.InvCont_GroupBox)

        #### Botões do Dialog
        self.Dialog_Btn_Layout = QHBoxLayout()
        # Botão OK
        self.Dialog_Btn_OK_Btn = QPushButton("OK")
        self.Dialog_Btn_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btn_OK_Btn.clicked.connect(self.acceptDespachoPotReat)
        self.Dialog_Btn_Layout.addWidget(self.Dialog_Btn_OK_Btn)
        # Botao Cancelar
        self.Dialog_Btn_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btn_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btn_Cancel_Btn.clicked.connect(self.cancelDespachoPotReat)
        self.Dialog_Btn_Layout.addWidget(self.Dialog_Btn_Cancel_Btn)

        self.Dialog_Layout.addItem(self.Dialog_Btn_Layout)

        self.setLayout(self.Dialog_Layout)

    def ReactPowFPConst(self):
        pass

    def ReactPowkvarConst(self):
        pass

    def ReactPowVV(self):
        pass

    def ReactPowDRC(self):
        pass

    def ReactPowVVeDRC(self):
        pass

    def ReactPowVVeVW(self):
        pass

    def acceptDespachoPotReat(self):
        pass

    def cancelDespachoPotReat(self):
        pass