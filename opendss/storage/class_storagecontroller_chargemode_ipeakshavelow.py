from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QLabel, QComboBox, QHBoxLayout, QDoubleSpinBox
from PyQt5.QtCore import Qt


import config as cfg

class C_ActPow_Charge_IPeakShaveLow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Charge IPeakShaveLow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho I-PeakShaveLow da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self._StorageControllersTemporario = []
        self._StorControl_GroupBox_Selection_ComboBox = 0

        self.InitUI()
        self.ChargeMode = {}

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
        self.setFixedWidth(50)
        self.setFixedHeight(40)

        self.kampsTargetLow_Label = QLabel("Corrente alvo (kAmps):")
        self.kampsTargetLow_Label.setToolTip("\
A frota de Storages é carregada a fim de manter a corrente no elemento monitorado abaixo da Potência Alvo ou\n\
dentro da faixa aceitável.")
        self.Dialog_Layout.addWidget(self.kampsTargetLow_Label, 2, 1, 1, 1)
        self.kampsTargetLow_DoubleSpinBox = QDoubleSpinBox()
        self.kampsTargetLow_DoubleSpinBox.setButtonSymbols(2)
        self.kampsTargetLow_DoubleSpinBox.setDecimals(3)
        self.kampsTargetLow_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.kampsTargetLow_DoubleSpinBox, 2, 2, 1, 2)
        self.BandLow_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.BandLow_Label, 3, 1, 1, 1)
        self.BandLow_DoubleSpinBox = QDoubleSpinBox()
        self.BandLow_DoubleSpinBox.setButtonSymbols(2)
        self.BandLow_DoubleSpinBox.setDecimals(3)
        self.BandLow_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.BandLow_DoubleSpinBox, 3, 2, 1, 1)
        self.BandLow_Unit_ComboBox = QComboBox()
        self.BandLow_Unit_ComboBox.addItems(["% kAmps", "kAmps"])
        self.Dialog_Layout.addWidget(self.BandLow_Unit_ComboBox, 3, 3, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelIPeakShaveLow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptIPeakShaveLow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)
        self.setFixedWidth(400)
        self.setFixedHeight(140)

    def getkampsTargetLow(self):
        return self.kampsTargetLow_DoubleSpinBox.text().replace(",", ".")
    def getBandLowUnit(self):
        return self.BandLow_Unit_ComboBox.currentText()
    def getBandWidthLow(self):
        return self.BandLow_DoubleSpinBox.text().replace(",", ".")

    def acceptIPeakShaveLow(self):
        self.ChargeMode["ChargeMode"] = "I-PeakShaveLow"
        self.ChargeMode["kWTargetLow"] = self.getkampsTargetLow()
        if self.getBandLowUnit() == "kW":
            self.ChargeMode["kWBandLow"] = self.getBandWidthLow()
        else:
            self.ChargeMode["%kWBandLow"] = self.getBandWidthLow()
        self.close()

    def cancelIPeakShaveLow(self):
        self.close()

    def clearParameters(self):
        self.kampsTargetLow_DoubleSpinBox.setValue(0.0)
        self.BandLow_DoubleSpinBox.setValue(0.0)
        self.BandLow_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "kWTargetLow" in ctd:
                    self.kampsTargetLow_DoubleSpinBox.setValue(float(ctd["kWTargetLow"]))
                if "kWBandLow" in ctd:
                    self.BandLow_DoubleSpinBox.setValue(float(ctd["kWBandLow"]))
                    self.BandLow_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.BandLow_DoubleSpinBox.setValue(float(ctd["%kWBandLow"]))
                    self.BandLow_Unit_ComboBox.setCurrentIndex(1)

