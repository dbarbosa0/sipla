from PyQt6.QtGui import QIcon, QDoubleValidator
from PyQt6.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QCheckBox, QLabel, QLineEdit, QComboBox, QHBoxLayout, QDoubleSpinBox
from PyQt6.QtCore import Qt

import config as cfg

class C_ActPow_Discharge_Follow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Discharge Follow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Follow da Potência Ativa"
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

        self.timeDischargeTrigger_Label = QLabel("Discharge Trigger:")
        self.timeDischargeTrigger_Label.setToolTip("\
Ao atingir o horário do Discharge Trigger, a frota de Storages é despachada a fim de manter a potência no \n\
elemento monitorado abaixo da Potência medida no momento do Trigger ou dentro da faixa aceitável.")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_Label, 2, 1, 1, 1)
        self.timeDischargeTrigger_DoubleSpinBox = QDoubleSpinBox()
        self.timeDischargeTrigger_DoubleSpinBox.setButtonSymbols(2)
        self.timeDischargeTrigger_DoubleSpinBox.setDecimals(3)
        self.timeDischargeTrigger_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_DoubleSpinBox, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_DoubleSpinBox = QDoubleSpinBox()
        self.Band_DoubleSpinBox.setButtonSymbols(2)
        self.Band_DoubleSpinBox.setDecimals(3)
        self.Band_DoubleSpinBox.setRange(0.001, 999999999)
        self.Dialog_Layout.addWidget(self.Band_DoubleSpinBox, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["% kW", "kW"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        self.kWThreshold_CheckBox = QCheckBox("kWThreshold:")
        self.kWThreshold_CheckBox.clicked.connect(self.EnableDisablekWThreshold)
        self.Dialog_Layout.addWidget(self.kWThreshold_CheckBox, 4, 1, 1, 1)
        self.kWThreshold_DoubleSpinBox = QDoubleSpinBox()
        self.kWThreshold_DoubleSpinBox.setButtonSymbols(2)
        self.kWThreshold_DoubleSpinBox.setDecimals(3)
        self.kWThreshold_DoubleSpinBox.setRange(0.001, 999999999)
        self.kWThreshold_DoubleSpinBox.setEnabled(False)
        self.Dialog_Layout.addWidget(self.kWThreshold_DoubleSpinBox, 4, 2, 1, 2)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelFollow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptFollow)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 5, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)
        self.setFixedWidth(400)
        self.setFixedHeight(140)

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_DoubleSpinBox.text().replace(",", ".")
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText().replace(",", ".")
    def getBandWidth(self):
        return self.Band_DoubleSpinBox.text()
    def getkWThreshold(self):
        return self.kWThreshold_DoubleSpinBox.text().replace(",", ".")

    def EnableDisablekWThreshold(self):
        if self.kWThreshold_CheckBox.isChecked():
            self.kWThreshold_DoubleSpinBox.setEnabled(True)
        else:
            self.kWThreshold_DoubleSpinBox.setEnabled(False)

    def acceptFollow(self):
        self.DischargeMode["DischargeMode"] = "Follow"
        self.DischargeMode["timeDischargeTrigger"] = self.gettimeDischargeTrigger()
        if self.getBandUnit() == "kW":
            self.DischargeMode["kWBand"] = self.getBandWidth()
        else:
            self.DischargeMode["%kWBand"] = self.getBandWidth()
        if self.kWThreshold_CheckBox.isChecked():
            self.DischargeMode["kWThreshold"] = self.getkWThreshold()
        self.close()

    def cancelFollow(self):
        self.close()

    def clearParameters(self):
        self.timeDischargeTrigger_DoubleSpinBox.setValue(0)
        self.kWThreshold_DoubleSpinBox.setValue(0)
        self.kWThreshold_CheckBox.setChecked(False)
        self.Band_DoubleSpinBox.setValue(0)
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_DoubleSpinBox.setValue(float(ctd["timeDischargeTrigger"]))
                if "kWThreshold" in ctd:
                    self.kWThreshold_DoubleSpinBox.setValue(float(ctd["kWThreshold"]))
                if "kWBand" in ctd:
                    self.Band_DoubleSpinBox.setValue(float(ctd["kWBandLow"]))
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.Band_DoubleSpinBox.setValue(float(ctd["%kWBandLow"]))
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

