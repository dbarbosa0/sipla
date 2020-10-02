from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QRadioButton, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QTabWidget, QLabel, QComboBox, QDesktopWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sys
import opendss.class_opendss
import config as cfg
#from opendss.class_insert_pvsystem_config_dialog import C_Config_PVSystem_Dialog

class C_Insert_PVSystem_Substation_Dialog(QDialog):
    def __init__(self, pvsubs_parents):
        super().__init__()

        self.titleWindow = "PVSystem Substation"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.adjustSize()
        self.substation_parents = pvsubs_parents
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.Exist_Subs_Names = []
        self.Subs_List = []


        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()# Layout da Dialog

        #print(self._teste)
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
        self.PVSystem_GroupBox_Substation_Remove_Btn.clicked.connect(self.remove_substation)
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_Remove_Btn, 1, 1, 1, 1)

        self.PVSystem_GroupBox_Substation_Edit_Btn = QPushButton("Editar")
        self.PVSystem_GroupBox_Substation_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.PVSystem_GroupBox_Substation_Edit_Btn.clicked.connect(self.edit_substation)
        self.PVSystem_GroupBox_Substation_Layout.addWidget(self.PVSystem_GroupBox_Substation_Edit_Btn, 1, 2, 1, 1)

        self.PVSystem_GroupBox_Substation_Add_Btn = QPushButton("Adicionar")
        self.PVSystem_GroupBox_Substation_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.PVSystem_GroupBox_Substation_Add_Btn.clicked.connect(self.add_substation)
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
        self.PVSystem_Substation_Transf_ConnPrimary_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_ConnPrimary_ComboBox.addItems(["wye", "delta"])
        self.PVSystem_Substation_Transf_Second_ComboBox = QComboBox()
        self.PVSystem_Substation_Transf_Second_ComboBox.addItems(["2"])
        self.PVSystem_Substation_Transf_Bus2_ComboBox = QComboBox()
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

    def add_substation(self):
        self.update_dialog()
        self.PVSystem_GroupBox_Substation_data.setVisible(True)
        self.centralize()

    def edit_substation(self):
        pass

    def remove_substation(self):
        pass

    def Accept(self):
        self.loadPVSystem()
        self.PVSystem_GroupBox_Substation_data.setVisible(False)
        self.adjustSize()
        self.close()
        self.clearPVConfigParameters()
        print(self.substation_parents.PVSystem_List)

    def update_dialog(self):
        self.AllBus = self.OpenDSS.getBusList()
        self.PVSystem_Substation_Transf_Bus1_ComboBox.addItems(self.AllBus)
        self.PVSystem_Substation_Transf_Bus2_ComboBox.addItems(self.substation_parents.Exist_PV_Names)

    # Gets

    def get_Substation_Name(self):
        return self.PVSystem_Substation_Transf_Name.text()

    def get_XHL(self):
        return self.PVSystem_Substation_Transf_XHL.text()

    def get_VPrimary(self):
        return self.PVSystem_Substation_Transf_VPrimary.text()

    def get_KVAPrimary(self):
        return self.PVSystem_Substation_Transf_KVAPrimary.text()

    def get_VSecond(self):
        return self.PVSystem_Substation_Transf_VSecond.text()

    def get_KVASecond(self):
        return self.PVSystem_Substation_Transf_KVASecond.text()

    def get_Trafo_Phases(self):
        return self.PVSystem_Substation_Transf_Phases_ComboBox.currentText()

    def get_Primary(self):
        return self.PVSystem_Substation_Transf_Primary_ComboBox.currentText()

    def get_Bus1(self):
        return self.PVSystem_Substation_Transf_Bus1_ComboBox.currentText()

    def get_ConnPrimary(self):
        return self.PVSystem_Substation_Transf_ConnPrimary_ComboBox.currentText()

    def get_Second(self):
        return self.PVSystem_Substation_Transf_Second_ComboBox.currentText()

    def get_Bus2(self):
        return self.PVSystem_Substation_Transf_Bus2_ComboBox.currentText()

    def get_ConnSecond(self):
        return self.PVSystem_Substation_Transf_ConnSecond_ComboBox.currentText()

    def loadPVSystem(self):
        self.Substation_Data = {}
        self.Substation_Data['Name'] = self.get_Substation_Name()
        self.Substation_Data['Phases'] = self.get_Trafo_Phases()
        self.Substation_Data['Xhl'] = self.get_XHL()
        self.Substation_Data['wdg1'] = self.get_Primary()
        self.Substation_Data['bus1'] = self.get_Bus1()
        self.Substation_Data['kv1'] = self.get_VPrimary()
        self.Substation_Data['kva1'] = self.get_KVAPrimary()
        self.Substation_Data['conn1'] = self.get_ConnPrimary()
        self.Substation_Data['wdg2'] = self.get_Second()
        self.Substation_Data['bus2'] = self.get_Bus2()
        self.Substation_Data['kv2'] = self.get_VSecond()
        self.Substation_Data['kva2'] = self.get_KVASecond()
        self.Substation_Data['conn2'] = self.get_ConnSecond()

        if self.PVSystem_Substation_Transf_Name.text() not in self.Exist_Subs_Names and not self.PVSystem_Substation_Transf_Name.text().isspace() and self.PVSystem_Substation_Transf_Name.text() != '':
            self.Subs_List.append(self.Substation_Data.copy())
            self.Exist_Subs_Names.append(self.get_Substation_Name())
        else:
            msg = QMessageBox()
            msg.information(self, 'Valores inválidos',
                            "Preencha todos os campos!\n Os valores estão inválidos ou não foram preenchidos")
        return self.Exist_Subs_Names

    def clearPVConfigParameters(self):
        self.PVSystem_Substation_Transf_Name.clear()
        self.PVSystem_Substation_Transf_XHL.clear()
        self.PVSystem_Substation_Transf_VPrimary.clear()
        self.PVSystem_Substation_Transf_KVAPrimary.clear()
        self.PVSystem_Substation_Transf_VSecond.clear()
        self.PVSystem_Substation_Transf_KVASecond.clear()
        self.PVSystem_Substation_Transf_Phases_ComboBox.clear()
        self.PVSystem_Substation_Transf_Primary_ComboBox.clear()
        self.PVSystem_Substation_Transf_Bus1_ComboBox.clear()
        self.PVSystem_Substation_Transf_ConnPrimary_ComboBox.clear()
        self.PVSystem_Substation_Transf_Second_ComboBox.clear()
        self.PVSystem_Substation_Transf_Bus2_ComboBox.clear()
        self.PVSystem_Substation_Transf_ConnSecond_ComboBox.clear()

    def centralize(self):
        qr = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerpoint)
        self.move(qr.topLeft())


    def exec_pvsystem(self):
        self.memoFileDevices = []
        for ctd in self.substation_parents.PVSystem_List:
            print(ctd)