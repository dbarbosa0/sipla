from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QPushButton, QCheckBox, QLabel, QDoubleSpinBox
from PyQt5.QtCore import Qt

import opendss.class_opendss
import opendss.storage.class_select_dispatch_curve
import opendss.storage.class_select_price_curve
import opendss.storage.class_config_storagecontroller
import config as cfg

class C_ActPow_Follow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho Follow da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho Follow da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.FollowParameters = {}

        self.InitUI()

        self.Select_DispCurve = opendss.storage.class_select_dispatch_curve.C_Config_DispCurve_Dialog()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.Dialog_Layout = QGridLayout()
        self.Label = QLabel("Insira o parâmetro")
        self.Dialog_Layout.addWidget(self.Label, 1, 1, 1, 2)
        self.TimeTrigger_CheckBox = QCheckBox("Time Charge Trigger")
        self.TimeTrigger_CheckBox.clicked.connect(self.EnableDisableTimeTrigger)
        self.Dialog_Layout.addWidget(self.TimeTrigger_CheckBox, 2, 1, 1, 1)
        self.TimeTrigger_DoubleSpinBox = QDoubleSpinBox()
        self.TimeTrigger_DoubleSpinBox.setRange(0.0, 1000.0)
        self.TimeTrigger_DoubleSpinBox.setDecimals(3)
        self.TimeTrigger_DoubleSpinBox.setValue(2.00)
        self.TimeTrigger_DoubleSpinBox.setButtonSymbols(2)
        self.TimeTrigger_DoubleSpinBox.setEnabled(False)
        self.Dialog_Layout.addWidget(self.TimeTrigger_DoubleSpinBox, 2, 2, 1, 1)
        self.DispatchCurve_Btn = QPushButton("Selecionar curva de despacho")
        self.DispatchCurve_Btn.clicked.connect(self.selectDispCurve)
        self.Dialog_Layout.addWidget(self.DispatchCurve_Btn, 3, 1, 1, 2)
        # Botão OK
        self.OK_Btn = QPushButton("OK")
        self.OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.OK_Btn.clicked.connect(self.acceptFollow)
        self.Dialog_Layout.addWidget(self.OK_Btn, 4, 1, 1, 1)
        # Botao Cancelar
        self.Cancel_Btn = QPushButton("Cancelar")
        self.Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Cancel_Btn.clicked.connect(self.cancelFollow)
        self.Dialog_Layout.addWidget(self.Cancel_Btn, 4, 2, 1, 1)

        self.setLayout(self.Dialog_Layout)

    def EnableDisableTimeTrigger(self):
        if self.TimeTrigger_CheckBox.isChecked():
            self.TimeTrigger_DoubleSpinBox.setEnabled(True)
        else:
            self.TimeTrigger_DoubleSpinBox.setEnabled(False)

    def selectDispCurve(self):
        self.Select_DispCurve.show()

    def acceptFollow(self):
        self.FollowParameters = {}
        self.FollowParameters.update(self.Select_DispCurve.dataDispCurve)
        if self.TimeTrigger_DoubleSpinBox.isEnabled():
            self.FollowParameters["TimeChargeTrigger"] = self.TimeTrigger_DoubleSpinBox.text().replace(",", ".")
        self.close()

    def cancelFollow(self):
        self.clearParameters()
        self.close()

    def clearParameters(self):
        self.TimeTrigger_CheckBox.setChecked(False)
        self.TimeTrigger_DoubleSpinBox.setEnabled(False)
        self.TimeTrigger_DoubleSpinBox.setValue(2.00)
