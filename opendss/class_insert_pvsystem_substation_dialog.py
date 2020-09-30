from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QRadioButton, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sys
import opendss.class_opendss
import config as cfg


class C_Insert_PVSystem_Substation_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "PVSystem Substation"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.adjustSize()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.PVSystem_List = []

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        # GroupBox Substation Config
        self.PVSystem_GroupBox_Substation = QGroupBox("Informações do Transformador")

        self.PVSystem_GroupBox_Substation_Label = QLabel("Barras do Sistemas com Conexão Fotovoltaica")
        self.PVSystem_GroupBox_Substation_ComboBox = QComboBox()

        self.PVSystem_GroupBox_Substation_Layout = QGridLayout()
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_ComboBox, 0, 1, 1, 3)

        self.PVSystem_GroupBox_Substation.setLayout(self.PVSystem_GroupBox_Substation_Layout)
        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_Substation)

        # Btns - GroupBox PVSystem Config
        self.PVSystem_GroupBox_Substation_Remove_Btn = QPushButton("Remover")
        self.PVSystem_GroupBox_Substation_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.PVSystem_GroupBox_Substation_Remove_Btn.clicked.connect(self.removePVSystem)
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_Remove_Btn, 1, 1, 1, 1)

        self.PVSystem_GroupBox_Substation_Edit_Btn = QPushButton("Editar")
        self.PVSystem_GroupBox_Substation_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.PVSystem_GroupBox_Substation_Edit_Btn.clicked.connect(self.editPVSystem)
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_Edit_Btn, 1, 2, 1, 1)

        self.PVSystem_GroupBox_Substation_Add_Btn = QPushButton("Adicionar")
        self.PVSystem_GroupBox_Substation_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.PVSystem_GroupBox_Substation_Add_Btn.clicked.connect(self.add_pvsystem)
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_Add_Btn, 1, 3, 1, 1)

        # Substation Data
        self.PVSystem_GroupBox_Substation_data = QGroupBox("Configuração do PVSystem")
        self.PVSystem_GroupBox_Substation_data_Layout = QGridLayout()
        self.PVSystem_GroupBox_Substation_data.setVisible(False)

        #  GroupBox PVSystem Data
        #  Labels
        self.PVSystem_Substation_Transf_Name_Label = QLabel("Nome:")
        self.PVSystem_Substation_Transf_Phases_Label = QLabel("Nº Fases:")
        self.PVSystem_Substation_Transf_XHL_Label = QLabel("XHL(%)")
        self.PVSystem_Substation_Transf_Primary_Label = QLabel("Enrolamento Primário")
        self.PVSystem_Substation_Transf_Bus1_Label = QLabel("Barra de conexão do Primário")
        self.PVSystem_Substation_Transf_VPrimary_Label = QLabel("Tensão no Primário")
        self.PVSystem_Substation_Transf_KVAPrimary_Label = QLabel("Potência no Primário")
        self.PVSystem_Substation_Transf_ConnPrimary_Label = QLabel("Tipo de conexão do Primário")
        self.PVSystem_Substation_Transf_Second_Label = QLabel("Enrolamento Secundário")
        self.PVSystem_Substation_Transf_Bus2_Label = QLabel("Barra de conexão do Secundário")
        self.PVSystem_Substation_Transf_VSecond_Label = QLabel("Tensão no Secundário")
        self.PVSystem_Substation_Transf_KVASecond_Label = QLabel("Potência no Secundário")
        self.PVSystem_Substation_Transf_ConnSecond_Label = QLabel("Tipo de conexão do Secundário")

        # LineEdits
        self.PVSystem_Substation_Transf_Name = QLineEdit()
        self.PVSystem_Substation_Transf_XHL = QLineEdit()
        self.PVSystem_Substation_Transf_VPrimary = QLineEdit()
        self.PVSystem_Substation_Transf_KVAPrimary = QLineEdit()
        self.PVSystem_Substation_Transf_VSecond = QLineEdit()
        self.PVSystem_Substation_Transf_KVASecond = QLineEdit()

        # Comboboxs
        self.PVSystem_Substation_Transf_Phases_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_Phases_ComboBox.addItems(["1", "3"])
        self.PVSystem_Substation_Transf_Primary_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_Primary_ComboBox.addItems(["1"])
        self.PVSystem_Substation_Transf_Bus1_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_Bus1_ComboBox.addItems(["Listar Barras PVSystem"])
        self.PVSystem_Substation_Transf_ConnPrimary_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_ConnPrimary_ComboBox.addItems(["wye", "delta"])
        self.PVSystem_Substation_Transf_Second_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_Second_ComboBox.addItems(["2"])
        self.PVSystem_Substation_Transf_Bus2_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_Bus2_ComboBox.addItems(["Listar Barras PVSystem"])
        self.PVSystem_Substation_Transf_ConnSecond_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_ConnSecond_ComboBox.addItems(["wye", "delta"])




        # Add Widgets and Layouts
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Name_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Name, 0, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Phases_Label, 1, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Phases_ComboBox, 1, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_XHL_Label, 2, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_XHL, 2, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Primary_Label, 3, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Primary_ComboBox, 3, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Bus1_Label, 4, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Bus1_ComboBox, 4, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_VPrimary_Label, 5, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_VPrimary, 5, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_KVAPrimary_Label, 6, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_KVAPrimary, 6, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_ConnPrimary_Label, 7, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_ConnPrimary_ComboBox, 7, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Second_Label, 8, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Second_ComboBox, 8, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Bus2_Label, 9, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_Bus2_ComboBox, 9, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_VSecond_Label, 10, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_VSecond, 10, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_KVASecond_Label, 11, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_KVASecond, 11, 1, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_ConnSecond_Label, 12, 0, 1, 1)
        self.PVSystem_GroupBox_Substation_data_Layout.addWidget(self.PVSystem_Substation_Transf_ConnSecond_ComboBox, 12, 1, 1, 1)


        self.PVSystem_GroupBox_Substation_data.setLayout(self.PVSystem_GroupBox_Substation_data_Layout)
        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_Substation_data)
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
        self.PVSystem_GroupBox_Substation_data.setVisible(True)

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
        self.PVSystem_GroupBox_Substation_data.setVisible(False)

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
