from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QRadioButton, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sys
import opendss.class_opendss
import config as cfg


class C_Insert_PVSystem_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "PVSystem"
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

        # GroupBox PVSystem Config
        self.PVSystem_GroupBox_PVconfig = QGroupBox("Configuração")
        self.PVSystem_GroupBox_PVconfig_Label = QLabel("Sistemas Fotovoltaicos Existentes")
        self.PVSystem_GroupBox_PVconfig_ComboBox = QComboBox()

        # GroupBox PVSystem Layout
        self.PVSystem_GroupBox_PVconfig_Layout = QGridLayout()
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_ComboBox, 0, 1, 1, 3)
        self.PVSystem_GroupBox_PVconfig.setLayout(self.PVSystem_GroupBox_PVconfig_Layout)

        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_PVconfig)

        ##### Btns
        self.PVSystem_GroupBox_PVconfig_Remove_Btn = QPushButton("Remover")
        self.PVSystem_GroupBox_PVconfig_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.PVSystem_GroupBox_PVconfig_Remove_Btn.clicked.connect(self.removePVSystem)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Remove_Btn,1,1,1,1)

        self.PVSystem_GroupBox_PVconfig_Edit_Btn = QPushButton("Editar")
        self.PVSystem_GroupBox_PVconfig_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.PVSystem_GroupBox_PVconfig_Edit_Btn.clicked.connect(self.editPVSystem)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Edit_Btn,1,2,1,1)

        self.PVSystem_GroupBox_PVconfig_Add_Btn = QPushButton("Adicionar")
        self.PVSystem_GroupBox_PVconfig_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.PVSystem_GroupBox_PVconfig_Add_Btn.clicked.connect(self.addPVSystem)
        self.PVSystem_GroupBox_PVconfig_Layout.addWidget(self.PVSystem_GroupBox_PVconfig_Add_Btn,1,3,1,1)

        # PVSystem Data

        self.PVSystem_GroupBox_PVdata = QGroupBox("Configuração do Medidor de Energia")
        self.PVSystem_GroupBox_PVdata.setVisible(False)

        #  GroupBox PVSystem Data
        #  Labels
        self.PVSystem_PVdata_Name_Label = QLabel("Nome:")
        self.PVSystem_PVdata_PTCurve_Label = QLabel("Curva P-t:")
        self.PVSystem_PVdata_PTnpts_Label = QLabel("Npts Curva P-t:")
        self.PVSystem_PVdata_EffCurve_Label = QLabel("Curva Eff-P:")
        self.PVSystem_PVdata_Effnpts_Label = QLabel("Npts Curve Eff-P:")
        self.PVSystem_PVdata_IrradCurve_Label = QLabel("Curva de Irradiação:")
        self.PVSystem_PVdata_Irradnpts_Label = QLabel("Npts Curva de Irrad.:")
        self.PVSystem_PVdata_TempCurve_Label = QLabel("Curva de Temperatura:")
        self.PVSystem_PVdata_Tempnpts_Label = QLabel("Npts Curva de Temp.:")
        self.PVSystem_PVdata_Phases_Label = QLabel("Nº Fases:")
        self.PVSystem_PVdata_Voltage_Label = QLabel("Tensão do Painel (kV):")

        self.PVSystem_PVdata_LineLosses_Label = QLabel("LineLosses:")
        self.PVSystem_PVdata_Losses_Label = QLabel("Losses:")
        self.PVSystem_PVdata_SeqLosses_Label = QLabel("SeqLosses:")
        self.PVSystem_PVdata_VbaseLosses_Label = QLabel("VbaseLosses:")
        self.PVSystem_PVdata_XfmrLosses_Label = QLabel("XfmrLosses:")
        self.PVSystem_PVdata_LocalOnly_Label = QLabel("LocalOnly:")
        self.PVSystem_PVdata_PhaseVoltageReport_Label = QLabel("PhaseVoltageReport:")
        self.PVSystem_PVdata_Enabled_Label = QLabel("Enabled:")
        self.PVSystem_PVdata_Action_Label = QLabel("Action:")

        self.Dialog_Layout.addLayout(QHBoxLayout())
        self.setLayout(self.Dialog_Layout)


    def removePVSystem(self):
        pass

    def addPVSystem(self):
        pass

    def editPVSystem(self):
        pass


'''
        #Teste button
        self.radiobutton_layout = QGridLayout()
        self.radiobutton = QRadioButton("Por Barra")
        self.radiobutton.setChecked(True)
        self.radiobutton.name = "Australia"
        self.radiobutton.toggled.connect(self.onClicked)
        self.radiobutton_layout.addWidget(self.radiobutton, 0, 0)

        self.radiobutton = QRadioButton("Randomico")
        self.radiobutton.country = "China"
        self.radiobutton.toggled.connect(self.onClicked)
        self.radiobutton_layout.addWidget(self.radiobutton, 0, 1)

        self.radiobutton = QRadioButton("randomico")
        self.radiobutton.country = "Japan"
        self.radiobutton.toggled.connect(self.onClicked)
        self.radiobutton_layout.addWidget(self.radiobutton, 0, 2)

        #self.PVSystem_Groupbox_Insert_config_Layout.addWidget(self.radiobutton_layout, 0, 1)



    def onClicked(self):
        self.radiobutton = self.sender()
        if self.radiobutton.isChecked():
            print("Country is %s" % (self.radiobutton.country))
'''


# Teste do button


# self.loadDefaultParameters()

