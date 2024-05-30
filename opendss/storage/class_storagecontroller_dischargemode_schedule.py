from PyQt6.QtGui import QColor, QIcon, QDoubleValidator
from PyQt6.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QLabel, QHBoxLayout, QDoubleSpinBox
from PyQt6.QtCore import Qt

import config as cfg

class C_ActPow_Discharge_Schedule_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge Schedule da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Schedule da Potência Ativa"
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

        self.timeDischargeTrigger = QLabel("Discharge Trigger:")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger, 2, 1, 1, 1)
        self.timeDischargeTrigger_DoubleSpinBox = QDoubleSpinBox()
        self.timeDischargeTrigger_DoubleSpinBox.setButtonSymbols(2)
        self.timeDischargeTrigger_DoubleSpinBox.setDecimals(3)
        self.timeDischargeTrigger_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_DoubleSpinBox, 2, 2, 1, 1)
        self.Tup_Label = QLabel("Duração da subida da rampa:")
        self.Dialog_Layout.addWidget(self.Tup_Label, 3, 1, 1, 1)
        self.Tup_DoubleSpinBox = QDoubleSpinBox()
        self.Tup_DoubleSpinBox.setButtonSymbols(2)
        self.Tup_DoubleSpinBox.setDecimals(3)
        self.Tup_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.Tup_DoubleSpinBox, 3, 2, 1, 1)
        self.Tflat_Label = QLabel("Duração do platô:")
        self.Dialog_Layout.addWidget(self.Tflat_Label, 4, 1, 1, 1)
        self.Tflat_DoubleSpinBox = QDoubleSpinBox()
        self.Tflat_DoubleSpinBox.setButtonSymbols(2)
        self.Tflat_DoubleSpinBox.setDecimals(3)
        self.Tflat_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.Tflat_DoubleSpinBox, 4, 2, 1, 1)
        self.Tdn_Label = QLabel("Duração da descida da rampa:")
        self.Dialog_Layout.addWidget(self.Tdn_Label, 5, 1, 1, 1)
        self.Tdn_DoubleSpinBox = QDoubleSpinBox()
        self.Tdn_DoubleSpinBox.setButtonSymbols(2)
        self.Tdn_DoubleSpinBox.setDecimals(3)
        self.Tdn_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.Tdn_DoubleSpinBox, 5, 2, 1, 1)
        self.RateDischarge_Label = QLabel("Taxa de descarregamento (%):")
        self.Dialog_Layout.addWidget(self.RateDischarge_Label, 6, 1, 1, 1)
        self.RateDischarge_DoubleSpinBox = QDoubleSpinBox()
        self.RateDischarge_DoubleSpinBox.setButtonSymbols(2)
        self.RateDischarge_DoubleSpinBox.setDecimals(3)
        self.RateDischarge_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.RateDischarge_DoubleSpinBox, 6, 2, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelSchedule)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptSchedule)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 7, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)
        self.setFixedWidth(400)
        self.setFixedHeight(140)

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_DoubleSpinBox.text().replace(",", ".")
    def getTup(self):
        return self.Tup_DoubleSpinBox.text().replace(",", ".")
    def getTflat(self):
        return self.Tflat_DoubleSpinBox.text().replace(",", ".")
    def getTdn(self):
        return self.Tdn_DoubleSpinBox.text().replace(",", ".")
    def getRateDischarge(self):
        return self.RateDischarge_DoubleSpinBox.text().replace(",", ".")

    def acceptSchedule(self):
        self.DischargeMode["DischargeMode"] = "Schedule"
        self.DischargeMode["timeDischargeTrigger"] = self.gettimeDischargeTrigger()
        self.DischargeMode["Tup"] = self.getTup()
        self.DischargeMode["Tflat"] = self.getTflat()
        self.DischargeMode["Tdn"] = self.getTdn()
        self.DischargeMode["%RatekW"] = self.getRateDischarge()
        self.close()

    def cancelSchedule(self):
        self.close()

    def clearParameters(self):
        self.timeDischargeTrigger_DoubleSpinBox.setValue(0)
        self.Tup_DoubleSpinBox.setValue(0)
        self.Tflat_DoubleSpinBox.setValue(0)
        self.Tdn_DoubleSpinBox.setValue(0)
        self.RateDischarge_DoubleSpinBox.setValue(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_DoubleSpinBox.setValue(float(ctd["timeDischargeTrigger"]))
                    self.Tup_DoubleSpinBox.setValue(float(ctd["Tup"]))
                    self.Tflat_DoubleSpinBox.setValue(float(ctd["Tflat"]))
                    self.Tdn_DoubleSpinBox.setValue(float(ctd["Tdn"]))
                    self.RateDischarge_DoubleSpinBox.setValue(float(ctd["%RatekW"]))

