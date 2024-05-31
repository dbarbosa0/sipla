from PyQt6.QtGui import QIcon, QDoubleValidator
from PyQt6.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QLabel, QLineEdit, QComboBox, QHBoxLayout, QDoubleSpinBox, QAbstractSpinBox
from PyQt6.QtCore import Qt

import config as cfg

class C_ActPow_Discharge_IPeakShave_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge IPeakShave da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho I-PeakShave da Potência Ativa"
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
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.kampsTarget_Label = QLabel("Corrente alvo (kAmps):")
        self.kampsTarget_Label.setToolTip("\
A frota de Storages é despachada a fim de manter a corrente no elemento monitorado abaixo da Corrente Alvo ou\n\
dentro da faixa aceitável.")
        self.Dialog_Layout.addWidget(self.kampsTarget_Label, 2, 1, 1, 1)
        self.kampsTarget_DoubleSpinBox = QDoubleSpinBox()
        self.kampsTarget_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.kampsTarget_DoubleSpinBox.setDecimals(3)
        self.kampsTarget_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.kampsTarget_DoubleSpinBox, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_DoubleSpinBox = QDoubleSpinBox()
        self.Band_DoubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.Band_DoubleSpinBox.setDecimals(3)
        self.Band_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.Band_DoubleSpinBox, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["% kAmps", "kAmps"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelIPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptIPeakShave)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)
        self.setFixedWidth(400)
        self.setFixedHeight(140)

    def getkampsTarget(self):
        return self.kampsTarget_DoubleSpinBox.text().replace(",", ".")
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText()
    def getBandWidth(self):
        return self.Band_DoubleSpinBox.text().replace(",", ".")

    def acceptIPeakShave(self):
        self.DischargeMode["DischargeMode"] = "I-PeakShave"
        self.DischargeMode["kWTarget"] = self.getkampsTarget()
        if self.getBandUnit() == "kW":
            self.DischargeMode["kWBand"] = self.getBandWidth()
        else:
            self.DischargeMode["%kWBand"] = self.getBandWidth()
        self.close()

    def cancelIPeakShave(self):
        self.close()

    def clearParameters(self):
        self.kampsTarget_DoubleSpinBox.setValue(0)
        self.Band_DoubleSpinBox.setValue(0)
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTarget" in ctd:
                    self.kampsTarget_DoubleSpinBox.setValue(float(ctd["kWTarget"]))
                if "kWBandLow" in ctd:
                    self.Band_DoubleSpinBox.setValue(float(ctd["kWBand"]))
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.Band_DoubleSpinBox.setValue(float(ctd["%kWBand"]))
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

