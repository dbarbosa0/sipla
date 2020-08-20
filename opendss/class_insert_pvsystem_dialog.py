from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QRadioButton, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sys
import opendss.class_opendss
import config as cfg
from opendss.PVSystem.class_pvsystem_effcurve_dialog import C_Config_EffCurve_Dialog
from opendss.PVSystem.class_pvsystem_effcurve_import import C_Eff_Curve_Import

from opendss.PVSystem.class_pvsystem_irradcurve_dialog import C_Config_IrradCurve_Dialog
from opendss.PVSystem.class_pvsystem_irradcurve_import import C_Irrad_Curve_Import

from opendss.PVSystem.class_pvsystem_ptcurve_dialog import C_Config_PTCurve_Dialog
from opendss.PVSystem.class_pvsystem_ptcurve_import import C_PT_Curve_Import

from opendss.PVSystem.class_pvsystem_tempcurve_dialog import C_Config_TempCurve_Dialog
from opendss.PVSystem.class_pvsystem_tempcurve_import import C_Temp_Curve_Import


class C_Insert_PVSystem_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "PVSystem"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.adjustSize()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.effcurve = C_Config_EffCurve_Dialog()
        self.irradcurve = C_Config_IrradCurve_Dialog()
        self.ptcurve = C_Config_PTCurve_Dialog()
        self.tempcurve = C_Config_TempCurve_Dialog()

        self.select_effcurve = C_Eff_Curve_Import()
        self.select_irradcurve = C_Irrad_Curve_Import()
        self.select_ptcurve = C_PT_Curve_Import()
        self.select_tempcurve = C_Temp_Curve_Import()

        self.PVSystem_List = []

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        # GroupBox Curves Config
        self.PVSystem_GroupBox_Import_Curves = QGroupBox("Importando Curvas")

        self.PVSystem_Import_PTCurve_Label = QLabel("Carregar Curva Potencia x Tempo")
        self.PVSystem_Import_PTCurve_Btn = QPushButton("PT Curve")
        self.PVSystem_Import_EffCurve_Label = QLabel("Carregar Curva Eficiência x Potencia")
        self.PVSystem_Import_EffCurve_Btn = QPushButton("Eff Curve")
        self.PVSystem_Import_TempCurve_Label = QLabel("Carregar Curva Temperatura")
        self.PVSystem_Import_TempCurve_Btn = QPushButton("Temp Curve")
        self.PVSystem_Import_IrradCurve_Label = QLabel("Carregar Curva de Irradiação")
        self.PVSystem_Import_IrradCurve_Btn = QPushButton("Irrad Curve")

        self.PVSystem_GroupBox_Import_Curves_Layout = QGridLayout()
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_PTCurve_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_PTCurve_Btn, 0, 1, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_EffCurve_Label, 1, 0, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_EffCurve_Btn, 1, 1, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_TempCurve_Label, 2, 0, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_TempCurve_Btn, 2, 1, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_IrradCurve_Label, 3, 0, 1, 1)
        self.PVSystem_GroupBox_Import_Curves_Layout.addWidget(self.PVSystem_Import_IrradCurve_Btn, 3, 1, 1, 1)

        self.PVSystem_GroupBox_Import_Curves.setLayout(self.PVSystem_GroupBox_Import_Curves_Layout)
        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_Import_Curves)

        # GroupBox Curves Config Buttons - Actions
        self.PVSystem_Import_EffCurve_Btn.clicked.connect(self.effcurve.show)
        self.PVSystem_Import_IrradCurve_Btn.clicked.connect(self.irradcurve.show)
        self.PVSystem_Import_PTCurve_Btn.clicked.connect(self.ptcurve.show)
        self.PVSystem_Import_TempCurve_Btn.clicked.connect(self.tempcurve.show)

        # GroupBox PVSystem Config
        self.PVSystem_GroupBox_PVconfig = QGroupBox("Inserindo PVSystem")

        self.PVSystem_GroupBox_PVconfig_Label = QLabel("Sistemas Fotovoltaicos Existentes")
        self.PVSystem_GroupBox_PVconfig_ComboBox = QComboBox()

        self.PVSystem_GroupBox_PVconfig_Layout = QGridLayout()
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_ComboBox, 0, 1, 1, 3)

        self.PVSystem_GroupBox_PVconfig.setLayout(self.PVSystem_GroupBox_PVconfig_Layout)
        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_PVconfig)

        # Btns - GroupBox PVSystem Config
        self.PVSystem_GroupBox_PVconfig_Remove_Btn = QPushButton("Remover")
        self.PVSystem_GroupBox_PVconfig_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.PVSystem_GroupBox_PVconfig_Remove_Btn.clicked.connect(self.removePVSystem)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Remove_Btn, 1, 1, 1, 1)

        self.PVSystem_GroupBox_PVconfig_Edit_Btn = QPushButton("Editar")
        self.PVSystem_GroupBox_PVconfig_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.PVSystem_GroupBox_PVconfig_Edit_Btn.clicked.connect(self.editPVSystem)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Edit_Btn, 1, 2, 1, 1)

        self.PVSystem_GroupBox_PVconfig_Add_Btn = QPushButton("Adicionar")
        self.PVSystem_GroupBox_PVconfig_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.PVSystem_GroupBox_PVconfig_Add_Btn.clicked.connect(self.add_pvsystem)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Add_Btn, 1, 3, 1, 1)

        # PVSystem Data
        self.PVSystem_GroupBox_PVdata = QGroupBox("Configuração do PVSystem")
        self.PVSystem_GroupBox_PVdata_Layout = QGridLayout()
        self.PVSystem_GroupBox_PVdata.setVisible(False)

        #  GroupBox PVSystem Data
        #  Labels
        self.PVSystem_PVdata_Name_Label = QLabel("Nome:")
        self.PVSystem_PVdata_PTCurve_Label = QLabel("Curva P-t:")
        self.PVSystem_PVdata_EffCurve_Label = QLabel("Curva Eff-P:")
        self.PVSystem_PVdata_IrradCurve_Label = QLabel("Curva de Irradiação:")
        self.PVSystem_PVdata_TempCurve_Label = QLabel("Curva de Temperatura:")
        self.PVSystem_PVdata_Phases_Label = QLabel("Nº Fases:")
        self.PVSystem_PVdata_Voltage_Label = QLabel("Tensão do Painel (kV):")
        self.PVSystem_PVdata_Irrad_Label = QLabel("Irradiação Nominal (normalizada):")
        self.PVSystem_PVdata_Ppmp_Label = QLabel("Máxima Potência (kVA):")
        self.PVSystem_PVdata_Temp_Label = QLabel("Temperatura de Operação:")
        self.PVSystem_PVdata_PF_Label = QLabel("Fator de Potência:")

        # LineEdits
        self.PVSystem_PVdata_Name = QLineEdit()
        self.PVSystem_PVdata_Voltage = QLineEdit()
        self.PVSystem_PVdata_Irrad = QLineEdit()
        self.PVSystem_PVdata_Ppmp = QLineEdit()
        self.PVSystem_PVdata_Temp = QLineEdit()
        self.PVSystem_PVdata_PF = QLineEdit()

        # Comboboxs
        self.PVSystem_PVdata_PTCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_PTCurve_ComboBox.addItems(["Default"])
        self.PVSystem_PVdata_EffCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_EffCurve_ComboBox.addItems(["Default"])
        self.PVSystem_PVdata_IrradCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_IrradCurve_ComboBox.addItems(["Default"])
        self.PVSystem_PVdata_TempCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_TempCurve_ComboBox.addItems(["Default"])
        self.PVSystem_PVdata_Phases_ComboBox = QComboBox()
        self.PVSystem_PVdata_Phases_ComboBox.addItems(["1", "3"])

        # Add Widgets and Layouts
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Name_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Name, 0, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_PTCurve_Label, 1, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_PTCurve_ComboBox, 1, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_EffCurve_Label, 2, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_EffCurve_ComboBox, 2, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_IrradCurve_Label, 3, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_IrradCurve_ComboBox, 3, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_TempCurve_Label, 4, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_TempCurve_ComboBox, 4, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Phases_Label, 5, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Phases_ComboBox, 5, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Voltage_Label, 6, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Voltage, 6, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Irrad_Label, 7, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Irrad, 7, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Ppmp_Label, 8, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Ppmp, 8, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Temp_Label, 9, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Temp, 9, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_PF_Label, 10, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_PF, 10, 1, 1, 1)

        self.PVSystem_GroupBox_PVdata.setLayout(self.PVSystem_GroupBox_PVdata_Layout)
        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_PVdata)
        self.Dialog_Layout.addLayout(QVBoxLayout())
        self.setLayout(self.Dialog_Layout)

        # Buttons Ok and Cancel
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout)

        self.setLayout(self.Dialog_Layout)

    def removePVSystem(self):
        pass

    def add_pvsystem(self):
        self.PVSystem_GroupBox_PVdata.setVisible(True)

    def add_eff_curve(self):
        self.effcurve.show()

    def add_irrad_curve(self):
        self.irradcurve.show()

    def add_pt_curve(self):
        self.ptcurve.show()

    def add_temp_curve(self):
        self.tempcurve.show()

    def editPVSystem(self):
        pass

    def Accept(self):
        self.PVSystem_GroupBox_PVdata.setVisible(False)

    # Gets

    def get_PVSystem_Name(self):
        return self.PVSystem_PVdata_Name.text()

    def get_PTCurve(self):
        return self.PVSystem_PVdata_PTCurve_ComboBox.currentText()

    def get_EffCurve(self):
        return self.PVSystem_PVdata_EffCurve_ComboBox.currentText()

    def get_IrradCurve(self):
        return self.PVSystem_PVdata_IrradCurve_ComboBox.currentText()

    def get_TempCurve(self):
        return self.PVSystem_PVdata_TempCurve_ComboBox.currentText()

    def get_Phases(self):
        return self.PVSystem_PVdata_Phases_ComboBox.currentText()

    def get_Nominal_Voltage(self):
        return self.PVSystem_PVdata_Voltage.text()

    def get_Nominal_Irradiance(self):
        return self.PVSystem_PVdata_Irrad.text()

    def get_Nominal_Power(self):
        return self.PVSystem_PVdata_Ppmp.text()

    def get_Nominal_Temp(self):
        return self.PVSystem_PVdata_Temp.text()

    def get_Power_Factor(self):
        return self.PVSystem_PVdata_PF.text()


# self.loadDefaultParameters()
