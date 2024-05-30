from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QPushButton, QCheckBox, QLabel, QDoubleSpinBox
from PyQt5.QtCore import Qt

import opendss.class_opendss
import opendss.storage.class_select_dispatch_curve
import opendss.storage.class_select_price_curve
import opendss.storage.class_config_storagecontroller
import config as cfg

class C_ActPow_Default_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Deafult da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Default da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.DefaultParameters = {}

        self.Select_DispCurve = opendss.storage.class_select_dispatch_curve.C_Config_DispCurve_Dialog()
        self.Select_DispCurveFile = opendss.storage.class_select_dispatch_curve

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira os parâmetros")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)

        self.ChargeTrigger_Label = QLabel("Charge Trigger")
        self.Dialog_Layout.addWidget(self.ChargeTrigger_Label, 2, 1, 1, 1)
        self.ChargeTrigger_DoubleSpinBox = QDoubleSpinBox()
        self.ChargeTrigger_DoubleSpinBox.setRange(0.0, 1000.0)
        self.ChargeTrigger_DoubleSpinBox.setDecimals(3)
        self.ChargeTrigger_DoubleSpinBox.setButtonSymbols(2)
        self.Dialog_Layout.addWidget(self.ChargeTrigger_DoubleSpinBox, 2, 2, 1, 1)
        self.DischargeTrigger_Label = QLabel("Discharge Trigger")
        self.Dialog_Layout.addWidget(self.DischargeTrigger_Label, 3, 1, 1, 1)
        self.DischargeTrigger_DoubleSpinBox = QDoubleSpinBox()
        self.DischargeTrigger_DoubleSpinBox.setRange(0.0, 1000.0)
        self.DischargeTrigger_DoubleSpinBox.setDecimals(3)
        self.DischargeTrigger_DoubleSpinBox.setButtonSymbols(2)
        self.Dialog_Layout.addWidget(self.DischargeTrigger_DoubleSpinBox, 3, 2, 1, 1)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 4, 1, 1, 1)
        self.TimeTrigger_DoubleSpinBox = QDoubleSpinBox()
        self.TimeTrigger_DoubleSpinBox.setRange(0.0, 1000.0)
        self.TimeTrigger_DoubleSpinBox.setDecimals(3)
        self.TimeTrigger_DoubleSpinBox.setValue(2.00)
        self.TimeTrigger_DoubleSpinBox.setButtonSymbols(2)
        self.TimeTrigger_DoubleSpinBox.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_DoubleSpinBox, 4, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de despacho")
        self.DispatchCurve_Btn.clicked.connect(self.selectDispCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 5, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptDefault)
        self.Dialog_Layout.addWidget(self.OK_Btn, 6, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelDefault)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 6, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_DoubleSpinBox.setEnabled(True)
        else:
            self.TimeTrigger_DoubleSpinBox.setEnabled(False)

    def selectDispCurve(self):
        self.Select_DispCurve.show()

    def acceptDefault(self):
        self.DefaultParameters = {}
        self.DefaultParameters["ChargeTrigger"] = self.ChargeTrigger_DoubleSpinBox.text().replace(",", ".")
        self.DefaultParameters["DischargeTrigger"] = self.DischargeTrigger_DoubleSpinBox.text().replace(",", ".")
        if self.TimeTrigger_DoubleSpinBox.isEnabled():
            self.DefaultParameters["TimeChargeTrigger"] = self.TimeTrigger_DoubleSpinBox.text().replace(",", ".")
        self.DefaultParameters.update(self.Select_DispCurve.dataDispCurve)
        self.close()

    def cancelDefault(self):
        self.clearParameters()
        self.close()

    def clearParameters(self):
        self.ChargeTrigger_DoubleSpinBox.setValue(0.0)
        self.DischargeTrigger_DoubleSpinBox.setValue(0.0)
        self.TimeTrigger_CheckBox.setChecked(False)
        self.TimeTrigger_DoubleSpinBox.setEnabled(False)
        self.TimeTrigger_DoubleSpinBox.setValue(2.0)