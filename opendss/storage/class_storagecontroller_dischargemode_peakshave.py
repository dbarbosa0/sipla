from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QLabel, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt

import config as cfg

class C_ActPow_Discharge_PeakShave_DispMode_Dialog(QDialog):# Classe Dialog Despacho Discharge PeakShave da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho PeakShave da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()

        self.DischargeMode = {}

    @property
    def StorageControllersTemporario(self):
        return self._StorageControllersTemporario

    @StorageControllersTemporario.setter
    def StorageControllersTemporario(self, value):
        self._StorageControllersTemporario = value

    @property
    def StorControl_GroupBox_Selection_ComboBox(self):
        return self._StorControl_GroupBox_Selection_ComboBox

    @StorControl_GroupBox_Selection_ComboBox.setter
    def StorControl_GroupBox_Selection_ComboBox(self, value):
        self._StorControl_GroupBox_Selection_ComboBox = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kWTarget_Label = QLabel("Pot. alvo (kW):")
        self.Dialog_Layout.addWidget(self.kWTarget_Label, 2, 1, 1, 1)
        self.kWTarget_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.kWTarget_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kWTarget_LineEdit, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_LineEdit = QLineEdit()
        self.Band_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Band_LineEdit, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["kW", "% kW"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def getkWTarget(self):
        return self.kWTarget_LineEdit.text()
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText()
    def getBandWidth(self):
        return self.Band_LineEdit.text()

    def verificaLineEdits(self):
        if not self.kWTarget_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Potência alvo (kW) não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Band_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptPeakShave(self):
        if self.verificaLineEdits():
            self.DischargeMode["DischargeMode"] = "PeakShave"
            self.DischargeMode["kWTarget"] = self.getkWTarget()
            if self.getBandUnit() == "kW":
                self.DischargeMode["kWBand"] = self.getBandWidth()
            else:
                self.DischargeMode["%kWBand"] = self.getBandWidth()
            self.close()
    def cancelPeakShave(self):
        self.close()

    def clearParameters(self):
        self.kWTarget_LineEdit.setText("")
        self.Band_LineEdit.setText("")
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTarget" in ctd:
                    self.kWTarget_LineEdit.setText(ctd["kWTarget"])
                if "kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["%kWBand"])
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

