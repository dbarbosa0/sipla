from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QRadioButton, QButtonGroup
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
import opendss.storage.class_config_storagecontroller
import config as cfg
import unidecode

class C_ActPow_LoadLevel_DispMode_Dialog(QDialog): ## Classe Dialog Despacho LoadLevel da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho LoadLevel da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.LoadLevelParameters = {}

        self.InitUI()

        self.Select_PriceCurve = opendss.storage.class_select_price_curve.C_Config_PriceCurve_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.ChargeTrigger_Label = QLabel("Charge Trigger")
        self.Dialog_Layout.addWidget(self.ChargeTrigger_Label, 2, 1, 1, 1)
        self.ChargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.ChargeTrigger_LineEdit, 2, 2, 1, 1)
        self.DischargeTrigger_Label = QLabel("Discharge Trigger")
        self.Dialog_Layout.addWidget(self.DischargeTrigger_Label, 3, 1, 1, 1)
        self.DischargeTrigger_LineEdit = QLineEdit()
        self.Dialog_Layout.addWidget(self.DischargeTrigger_LineEdit, 3, 2, 1, 1)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 4, 1, 1, 1)
        self.TimeTrigger_LineEdit = QLineEdit()
        self.TimeTrigger_LineEdit.setText("2.00")
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_LineEdit, 4, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de preço")
        self.DispatchCurve_Btn.clicked.connect(self.selectPriceCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 5, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptLoadLevel)
        self.Dialog_Layout.addWidget(self.OK_Btn, 6, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelLoadLevel)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 6, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_LineEdit.setEnabled(True)
        else:
            self.TimeTrigger_LineEdit.setEnabled(False)

    def selectPriceCurve(self):
        self.Select_PriceCurve.show()

    def acceptLoadLevel(self):
        self.LoadLevelParameters = {}
        self.LoadLevelParameters["ChargeTrigger"] = self.ChargeTrigger_LineEdit.text()
        self.LoadLevelParameters["DischargeTrigger"] = self.DischargeTrigger_LineEdit.text()
        if self.TimeTrigger_LineEdit.isEnabled():
            self.LoadLevelParameters["TimeChargeTrigger"] = self.TimeTrigger_LineEdit.text()
        self.LoadLevelParameters.update(self.Select_PriceCurve.dataPriceCurve)
        self.close()

    def cancelLoadLevel(self):
        self.clearParameters()
        self.close()

    def clearParameters(self):
        self.ChargeTrigger_LineEdit.setText("")
        self.DischargeTrigger_LineEdit.setText("")
        self.TimeTrigger_CheckBox.setChecked(False)
        self.TimeTrigger_LineEdit.setEnabled(False)
        self.TimeTrigger_LineEdit.setText("2.00")