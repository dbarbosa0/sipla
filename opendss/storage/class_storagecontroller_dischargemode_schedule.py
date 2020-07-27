from PyQt5.QtGui import QColor, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, \
    QPushButton, QMessageBox, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt

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
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeDischargeTrigger = QLabel("Discharge Trigger:")
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger, 2, 1, 1, 1)
        self.timeDischargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeDischargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeDischargeTrigger_LineEdit, 2, 2, 1, 1)
        self.Tup_Label = QLabel("Duração da subida da rampa:")
        self.Dialog_Layout.addWidget(self.Tup_Label, 3, 1, 1, 1)
        self.Tup_LineEdit = QLineEdit()
        self.Tup_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Tup_LineEdit, 3, 2, 1, 1)
        self.Tflat_Label = QLabel("Duração do platô:")
        self.Dialog_Layout.addWidget(self.Tflat_Label, 4, 1, 1, 1)
        self.Tflat_LineEdit = QLineEdit()
        self.Tflat_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Tflat_LineEdit, 4, 2, 1, 1)
        self.Tdn_Label = QLabel("Duração da descida da rampa:")
        self.Dialog_Layout.addWidget(self.Tdn_Label, 5, 1, 1, 1)
        self.Tdn_LineEdit = QLineEdit()
        self.Tdn_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.Tdn_LineEdit, 5, 2, 1, 1)
        self.RateDischarge_Label = QLabel("Taxa de descarregamento (%):")
        self.Dialog_Layout.addWidget(self.RateDischarge_Label, 6, 1, 1, 1)
        self.RateDischarge_LineEdit = QLineEdit()
        self.RateDischarge_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.RateDischarge_LineEdit, 6, 2, 1, 1)
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

    def gettimeDischargeTrigger(self):
        return self.timeDischargeTrigger_LineEdit.text()
    def getTup(self):
        return self.Tup_LineEdit.text()
    def getTflat(self):
        return self.Tflat_LineEdit.text()
    def getTdn(self):
        return self.Tdn_LineEdit.text()
    def getRateDischarge(self):
        return self.RateDischarge_LineEdit.text()

    def verificaLineEdits(self):
        if not self.timeDischargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para o Discharge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Tup_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Duração da subida da rampa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Tflat_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Duração do platô não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.Tdn_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da Duração da descida da rampa não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.RateDischarge_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Taxa de descarregamento não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptSchedule(self):
        if self.verificaLineEdits():
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
        self.timeDischargeTrigger_LineEdit.setText("")
        self.Tup_LineEdit.setText("")
        self.Tflat_LineEdit.setText("")
        self.Tdn_LineEdit.setText("")
        self.RateDischarge_LineEdit.setText("")

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeDischargeTrigger" in ctd:
                    self.timeDischargeTrigger_LineEdit.setText(ctd["timeDischargeTrigger"])
                    self.Tup_LineEdit.setText(ctd["Tup"])
                    self.Tflat_LineEdit.setText(ctd["Tflat"])
                    self.Tdn_LineEdit.setText(ctd["Tdn"])
                    self.RateDischarge_LineEdit.setText(ctd["%RatekW"])

