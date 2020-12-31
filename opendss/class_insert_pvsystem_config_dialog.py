from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QCheckBox, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QTabWidget, QLabel, QComboBox, QDesktopWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg
import main_toolbar

from opendss.PVSystem.class_pvsystem_effcurve_dialog import C_Config_EffCurve_Dialog
from opendss.PVSystem.class_pvsystem_effcurve_import import C_Eff_Curve_Import

from opendss.PVSystem.class_pvsystem_irradcurve_dialog import C_Config_IrradCurve_Dialog
from opendss.PVSystem.class_pvsystem_irradcurve_import import C_Irrad_Curve_Import

from opendss.PVSystem.class_pvsystem_ptcurve_dialog import C_Config_PTCurve_Dialog
from opendss.PVSystem.class_pvsystem_ptcurve_import import C_PT_Curve_Import

from opendss.PVSystem.class_pvsystem_tempcurve_dialog import C_Config_TempCurve_Dialog
from opendss.PVSystem.class_pvsystem_tempcurve_import import C_Temp_Curve_Import

from opendss.class_insert_pvsystem_substation_dialog import C_Insert_PVSystem_Substation_Dialog


class C_Config_PVSystem_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.pvsubstation_parents = C_Insert_PVSystem_Substation_Dialog(self)
        self.titleWindow = "PVSystem Config"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.adjustSize()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Main_Toolbar = main_toolbar.C_MenuToolBar()

        self.effcurve = C_Config_EffCurve_Dialog()
        self.irradcurve = C_Config_IrradCurve_Dialog()
        self.ptcurve = C_Config_PTCurve_Dialog()
        self.tempcurve = C_Config_TempCurve_Dialog()

        self.select_effcurve = C_Eff_Curve_Import()
        self.select_irradcurve = C_Irrad_Curve_Import()
        self.select_ptcurve = C_PT_Curve_Import()
        self.select_tempcurve = C_Temp_Curve_Import()

        self.PVSystem_List = []
        self.Exist_PV_Names = []

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
        self.PVSystem_GroupBox_PVconfig = QGroupBox("Configurando PVSystem")

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

        #  Buttons
        self.PVSystem_PVdata_Multi_Button = QCheckBox("")
        self.PVSystem_PVdata_Multi_Button.stateChanged.connect(self.MultiPVs)

        #  Labels
        self.PVSystem_PVdata_Name_Label = QLabel("Nome:")
        self.PVSystem_PVdata_PTCurve_Label = QLabel("Curva P-t:")
        self.PVSystem_PVdata_EffCurve_Label = QLabel("Curva Eff-P:")
        self.PVSystem_PVdata_IrradCurve_Label = QLabel("Curva de Irradiação:")
        self.PVSystem_PVdata_TempCurve_Label = QLabel("Curva de Temperatura:")
        self.PVSystem_PVdata_Phases_Label = QLabel("Nº Fases:")
        self.PVSystem_PVdata_Voltage_Label = QLabel("Tensão do Painel (kV):")
        self.PVSystem_PVdata_Irrad_Label = QLabel("Irradiação Nominal (normalizada):")
        self.PVSystem_PVdata_Ppmp_Label = QLabel("Potência MPPT (W):")
        self.PVSystem_PVdata_Temp_Label = QLabel("Temperatura de Operação:")
        self.PVSystem_PVdata_PF_Label = QLabel("Fator de Potência:")
        self.PVSystem_PVdata_Cutin_Label = QLabel("%Cutin")
        self.PVSystem_PVdata_Cutout_Label = QLabel("%Cutout")

        self.PVSystem_PVdata_Multi_Button_Label = QLabel("Marque para inserir multiplos PVSystems com a mesma configuração")
        self.PVSystem_PVdata_Multi_Number_Label = QLabel("Informe a qtd de copias")

        # LineEdits
        self.PVSystem_PVdata_Name = QLineEdit()
        self.PVSystem_PVdata_Voltage = QLineEdit()
        self.PVSystem_PVdata_Irrad = QLineEdit()
        self.PVSystem_PVdata_Ppmp = QLineEdit()
        self.PVSystem_PVdata_Temp = QLineEdit()
        self.PVSystem_PVdata_PF = QLineEdit()
        self.PVSystem_PVdata_Cutin = QLineEdit()
        self.PVSystem_PVdata_Cutout = QLineEdit()

        self.PVSystem_PVdata_Multi_Number = QLineEdit()
        self.PVSystem_PVdata_Multi_Number.setEnabled(False)

        # Comboboxs
        self.PVSystem_PVdata_PTCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_EffCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_IrradCurve_ComboBox = QComboBox()
        self.PVSystem_PVdata_TempCurve_ComboBox = QComboBox()
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
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutin_Label, 11, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutin, 11, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutout_Label, 12, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutout, 12, 1, 1, 1)

        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Multi_Button, 13, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Multi_Button_Label, 13, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Multi_Number_Label, 14, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Multi_Number, 14, 1, 1, 1)

        self.PVSystem_GroupBox_PVdata.setLayout(self.PVSystem_GroupBox_PVdata_Layout)
        self.Dialog_Layout.addWidget(self.PVSystem_GroupBox_PVdata)
        self.Dialog_Layout.addLayout(QVBoxLayout())
        self.setLayout(self.Dialog_Layout)

        # Buttons Ok, Cancel and Apply
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.Cancel)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout)

        self.setLayout(self.Dialog_Layout)

    def add_pvsystem(self):
        if not (self.effcurve.list_curve_names and self.irradcurve.list_curve_names and self.ptcurve.list_curve_names and self.tempcurve.list_curve_names):
            QMessageBox(QMessageBox.Warning, "Curvas", "Todas as curvas precisam ser carregadas",
                        QMessageBox.Ok).exec()
        else:
            self.update_dialog()
            self.PVSystem_GroupBox_PVdata.setVisible(True)
            self.centralize()

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

    def removePVSystem(self):
        pass

    def Accept(self):
        self.close()
        self.loadPVSystem()
        self.update_dialog()
        self.PVSystem_GroupBox_PVdata.setVisible(False)
        self.adjustSize()
        if not self.PVSystem_List:
            self.Main_Toolbar.OpenDSS_InsertPVSystem_Act.setEnabled(False)
        else:
            self.Main_Toolbar.OpenDSS_InsertPVSystem_Act.setEnabled(True)
        self.clearPVConfigParameters()

        
    def Cancel(self):
        self.close()
        self.clearPVConfigParameters()
        self.PVSystem_GroupBox_PVdata.setVisible(False)

    def MultiPVs(self):
        if self.PVSystem_PVdata_Multi_Button.isChecked():
            self.PVSystem_PVdata_Multi_Number.setEnabled(True)
        else:
            self.PVSystem_PVdata_Multi_Number.setEnabled(False)

    def update_dialog(self):
        self.PVSystem_PVdata_PTCurve_ComboBox.addItems(self.ptcurve.list_curve_names)
        self.PVSystem_PVdata_EffCurve_ComboBox.addItems(self.effcurve.list_curve_names)
        self.PVSystem_PVdata_IrradCurve_ComboBox.addItems(self.irradcurve.list_curve_names)
        self.PVSystem_PVdata_TempCurve_ComboBox.addItems(self.tempcurve.list_curve_names)
        if self.PVSystem_List:
            self.PVSystem_GroupBox_PVconfig_ComboBox.clear()
            lista_aux = []
            for index, pvs_dict in enumerate(self.PVSystem_List):
                for key, value in pvs_dict.items():
                    if key == 'name':
                        lista_aux.append(value)
            self.PVSystem_GroupBox_PVconfig_ComboBox.addItems(lista_aux)


    # Gets

    def get_PVSystem_Name(self):
        return self.PVSystem_PVdata_Name.text()

    def get_PTCurve(self):
        for index, pt_dict in enumerate(self.ptcurve.PTCurve_list):
            for key, value in pt_dict.items():
                if value == self.PVSystem_PVdata_PTCurve_ComboBox.currentText():
                    return self.ptcurve.PTCurve_list[index]

    def get_EffCurve(self):
        for index, eff_dict in enumerate(self.effcurve.EffCurve_list):
            for key, value in eff_dict.items():
                if value == self.PVSystem_PVdata_EffCurve_ComboBox.currentText():
                    return self.effcurve.EffCurve_list[index]

    def get_IrradCurve(self):
        for index, irrad_dict in enumerate(self.irradcurve.IrradCurve_list):
            for key, value in irrad_dict.items():
                if value == self.PVSystem_PVdata_IrradCurve_ComboBox.currentText():
                    return self.irradcurve.IrradCurve_list[index]

    def get_TempCurve(self):
        for index, temp_dict in enumerate(self.tempcurve.TempCurve_list):
            for key, value in temp_dict.items():
                if value == self.PVSystem_PVdata_TempCurve_ComboBox.currentText():
                    return self.tempcurve.TempCurve_list[index]

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

    def get_cutin(self):
        return self.PVSystem_PVdata_Cutin.text()

    def get_cutout(self):
        return self.PVSystem_PVdata_Cutout.text()

    def loadPVSystem(self):
        PVSystem_Data = {}
        PVSystem_Data["name"] = self.get_PVSystem_Name()
        PVSystem_Data["bus1"] = self.get_PVSystem_Name()
        PVSystem_Data["phases"] = self.get_Phases()
        PVSystem_Data["kv"] = self.get_Nominal_Voltage()
        PVSystem_Data["irrad"] = self.get_Nominal_Irradiance()
        PVSystem_Data["pmpp"] = self.get_Nominal_Power()
        PVSystem_Data["temperature"] = self.get_Nominal_Temp()
        PVSystem_Data["pf"] = self.get_Power_Factor()
        PVSystem_Data["%cutin"] = self.get_cutin()
        PVSystem_Data["%cutout"] = self.get_cutout()
        PVSystem_Data["effcurve"] = self.get_EffCurve()
        PVSystem_Data["p-tcurve"] = self.get_PTCurve()
        PVSystem_Data["daily"] = self.get_IrradCurve()
        PVSystem_Data["tdaily"] = self.get_TempCurve()

        if self.PVSystem_PVdata_Name.text() not in self.Exist_PV_Names and not self.PVSystem_PVdata_Name.text().isspace() and self.PVSystem_PVdata_Name.text() != '':
            if self.PVSystem_PVdata_Multi_Button.isChecked():
                num_copias = int(self.PVSystem_PVdata_Multi_Number.text())
                for i in range(1, num_copias+1):
                    PVSystem_Data["name"] = self.get_PVSystem_Name() + str(i)
                    PVSystem_Data["bus1"] = self.get_PVSystem_Name() + str(i)
                    self.PVSystem_List.append(PVSystem_Data.copy())
                    self.Exist_PV_Names.append(self.get_PVSystem_Name()+str(i))
            else:
                self.PVSystem_List.append(PVSystem_Data.copy())
                self.Exist_PV_Names.append(self.get_PVSystem_Name())

        else:
            msg = QMessageBox()
            msg.information(self, 'Valores inválidos',
                            "Preencha todos os campos!\n Os valores estão inválidos ou não foram preenchidos")


    def clearPVConfigParameters(self):
        self.PVSystem_PVdata_Name.clear()
        self.PVSystem_PVdata_Voltage.clear()
        self.PVSystem_PVdata_Irrad.clear()
        self.PVSystem_PVdata_Ppmp.clear()
        self.PVSystem_PVdata_Temp.clear()
        self.PVSystem_PVdata_PF.clear()
        self.PVSystem_PVdata_Cutin.clear()
        self.PVSystem_PVdata_Cutout.clear()
        self.PVSystem_PVdata_PTCurve_ComboBox.clear()
        self.PVSystem_PVdata_EffCurve_ComboBox.clear()
        self.PVSystem_PVdata_IrradCurve_ComboBox.clear()
        self.PVSystem_PVdata_TempCurve_ComboBox.clear()
        self.PVSystem_PVdata_Phases_ComboBox.setCurrentIndex(1)
        self.PVSystem_PVdata_Multi_Number.clear()
        self.PVSystem_PVdata_Multi_Button.setCheckState(False)

    def centralize(self):
        qr = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerpoint)
        self.move(qr.topLeft())


