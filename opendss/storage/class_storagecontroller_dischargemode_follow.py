from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QCheckBox, QLabel, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt

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
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeDischargeTrigger_Label = QLabel("Discharge Trigger:")
        self.timeDischargeTrigger_Label.setToolTip("\
Ao atingir o horário do Discharge Trigger, a frota de Storages é despachada a fim de manter a potência no \n\
elemento monitorado abaixo da Potência medida no momento do Trigger ou dentro da faixa aceitável.")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_Label, 2, 1, 1, 1)
        self.timeDischargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeDischargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_LineEdit, 2, 2, 1, 2)
        self.Band_Label = QLabel("Largura da faixa:")
        self.Dialog_Layout.addWidget(self.Band_Label, 3, 1, 1, 1)
        self.Band_LineEdit = QLineEdit()
        self.Band_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Band_LineEdit, 3, 2, 1, 1)
        self.Band_Unit_ComboBox = QComboBox()
        self.Band_Unit_ComboBox.addItems(["% kW", "kW"])
        self.Dialog_Layout.addWidget(self.Band_Unit_ComboBox, 3, 3, 1, 1)
        self.kWThreshold_CheckBox = QCheckBox("Carga mínima para ativar\ndescarregamento:")
        self.kWThreshold_CheckBox.clicked.connect(self.EnableDisablekWThreshold)
        self.Dialog_Layout.addWidget(self.kWThreshold_CheckBox, 4, 1, 1, 1)
        self.kWThreshold_LineEdit = QLineEdit()
        self.kWThreshold_LineEdit.setEnabled(False)
        self.kWThreshold_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.kWThreshold_LineEdit, 4, 2, 1, 2)
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

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_LineEdit.text()
    def getBandUnit(self):
        return self.Band_Unit_ComboBox.currentText()
    def getBandWidth(self):
        return self.Band_LineEdit.text()
    def getkWThreshold(self):
        return self.kWThreshold_LineEdit.text()

    def EnableDisablekWThreshold(self):
        if self.kWThreshold_CheckBox.isChecked():
            self.kWThreshold_LineEdit.setEnabled(True)
        else:
            self.kWThreshold_LineEdit.setEnabled(False)

    def verificaLineEdits(self):
        if not self.timeDischargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para o Discharge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Band_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller","O valor da Largura da faixa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif self.kWThreshold_CheckBox.isChecked():
                if not self.kWThreshold_LineEdit.hasAcceptableInput():
                    QMessageBox(QMessageBox.Warning, "Storage Controller","O valor para a Carga mínima não é um valor válido!",
                                QMessageBox.Ok).exec()
                    return False
        else:
            return True

    def acceptFollow(self):
        if self.verificaLineEdits():
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
        self.timeDischargeTrigger_LineEdit.setText("")
        self.kWThreshold_LineEdit.setText("")
        self.kWThreshold_CheckBox.setChecked(False)
        self.Band_LineEdit.setText("")
        self.Band_Unit_ComboBox.setCurrentIndex(0)

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_LineEdit.setText(ctd["timeDischargeTrigger"])
                if "kWThreshold" in ctd:
                    self.kWThreshold_LineEdit.setText(ctd["kWThreshold"])
                if "kWBand" in ctd:
                    self.Band_LineEdit.setText(ctd["kWBandLow"])
                    self.Band_Unit_ComboBox.setCurrentIndex(0)
                elif "%kWBandLow" in ctd:
                    self.Band_LineEdit.setText(ctd["%kWBandLow"])
                    self.Band_Unit_ComboBox.setCurrentIndex(1)

