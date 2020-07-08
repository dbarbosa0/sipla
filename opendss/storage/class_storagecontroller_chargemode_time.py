from PyQt5.QtGui import QColor, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QRadioButton, QButtonGroup, QSpinBox
from PyQt5.QtCore import Qt

import csv
import random
import pathlib
import platform
import pyqtgraph
import class_exception

import opendss.class_opendss
import opendss.storage.class_select_dispatch_curve
import opendss.storage.class_select_price_curve
import opendss.storage.class_active_pow_dispmode_dialog
import opendss.storage.class_insert_storage_dialog
import config as cfg
import unidecode

class C_ActPow_Charge_Time_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Charge Time da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Time da Potência Ativa"
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
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.timeChargeTrigger = QLabel("Charge Trigger:")
        self.Dialog_Layout.addWidget(self.timeChargeTrigger, 2, 1, 1, 1)
        self.timeChargeTrigger_LineEdit = QLineEdit()
        self.LineEditsValidos = QDoubleValidator()
        self.LineEditsValidos.setBottom(0.1)
        self.timeChargeTrigger_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.timeChargeTrigger_LineEdit, 2, 2, 1, 1)
        self.RateCharge_Label = QLabel("Taxa de carregamento (%):")
        self.Dialog_Layout.addWidget(self.RateCharge_Label, 3, 1, 1, 1)
        self.RateCharge_LineEdit = QLineEdit()
        self.RateCharge_LineEdit.setValidator(self.LineEditsValidos)
        self.Dialog_Layout.addWidget(self.RateCharge_LineEdit, 3, 2, 1, 1)
        ### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelTime)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptTime)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 4, 1, 1, 3)
        self.setLayout(self.Dialog_Layout)

    def gettimeChargeTrigger(self):
        return self.timeChargeTrigger_LineEdit.text()
    def getRateCharge(self):
        return self.RateCharge_LineEdit.text()

    def verificaLineEdits(self):
        if not self.timeChargeTrigger_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para o Charge Trigger não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        elif not self.RateCharge_LineEdit.hasAcceptableInput():
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "O valor para da a Taxa de carregamento não é um valor válido!",
                        QMessageBox.Ok).exec()
            return False
        else:
            return True

    def acceptTime(self):
        if self.verificaLineEdits():
            self.ChargeMode["ChargeMode"] = "Time"
            self.ChargeMode["timeChargeTrigger"] = self.gettimeChargeTrigger()
            self.ChargeMode["%RateCharge"] = self.getRateCharge()
            self.close()
    def cancelTime(self):
        self.close()

    def clearParameters(self):
        self.timeChargeTrigger_LineEdit.setText("")
        self.RateCharge_LineEdit.setText("")

    def updateDialog(self):
        self.clearParameters()
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                if "timeChargeTrigger" in ctd:
                    self.timeChargeTrigger_LineEdit.setText(ctd["timeChargeTrigger"])
                    self.RateCharge_LineEdit.setText(ctd["%RateCharge"])
