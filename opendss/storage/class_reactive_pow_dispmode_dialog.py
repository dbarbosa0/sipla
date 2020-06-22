from PyQt5.QtGui import  QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QPushButton, QLabel, QLineEdit, \
    QHBoxLayout,  QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt

import config as cfg

class C_Reactive_Pow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho da Potencia Reativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho da Potência Reativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.ReactPow = {}

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()

        self.Dialog_Label = QLabel("Selecione um modo")
        self.Dialog_Layout.addWidget(self.Dialog_Label, 1, 1, 1, 2)

        self.BtnGroup = QButtonGroup()

        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)

        # "FP Constante"
        self.FPConst_RadioBtn = QRadioButton("FP Constante:")
        self.FPConst_RadioBtn.setChecked(True)
        self.FPConst_RadioBtn.clicked.connect(self.FPConst)
        self.Dialog_Layout.addWidget(self.FPConst_RadioBtn, 2, 1, 1, 1)
        self.FPConst_LineEdit = QLineEdit()
        self.FPConst_LineEdit.setValidator(self.LineEditsValidos)
        self.FPConst_LineEdit.setText("1.0")
        self.Dialog_Layout.addWidget(self.FPConst_LineEdit, 2, 2, 1, 1)

        # Radio Btn "kVar Constante"
        self.kvarConst_RadioBtn = QRadioButton("kVar Constante:")
        self.kvarConst_RadioBtn.setChecked(False)
        self.kvarConst_RadioBtn.clicked.connect(self.kvarConst)
        self.Dialog_Layout.addWidget(self.kvarConst_RadioBtn, 3, 1, 1, 1)
        self.kvarConst_LineEdit = QLineEdit()
        self.kvarConst_LineEdit.setEnabled(False)
        self.kvarConst_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kvarConst_LineEdit, 3, 2, 1, 1)

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

        self.Dialog_Layout.addItem(self.Dialog_Btn_Layout, 4, 1, 1, 2)

        self.setLayout(self.Dialog_Layout)

    def FPConst(self):
        self.kvarConst_LineEdit.setEnabled(False)
        self.FPConst_LineEdit.setEnabled(True)

    def kvarConst(self):
        self.FPConst_LineEdit.setEnabled(False)
        self.kvarConst_LineEdit.setEnabled(True)

    def acceptDespachoPotReat(self):
        if self.FPConst_RadioBtn.isChecked():
            self.ReactPow = {}
            self.ReactPow["FP"] = self.FPConst_LineEdit.text()
        if self.kvarConst_RadioBtn.isChecked():
            self.ReactPow = {}
            self.ReactPow["kvar"] = self.kvarConst_LineEdit.text()
        self.close()

    def cancelDespachoPotReat(self):
        self.close()