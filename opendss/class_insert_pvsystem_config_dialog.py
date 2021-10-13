from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QRadioButton, QDialog, QGridLayout, QGroupBox, \
    QVBoxLayout, QCheckBox, QTabWidget, QDoubleSpinBox, QLabel, QComboBox, QDesktopWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt

import random
import unidecode
import opendss.class_opendss
import config as cfg
import main_toolbar

import opendss.PVSystem.class_pvsystem_effcurve_dialog
import opendss.PVSystem.class_pvsystem_irradcurve_dialog
import opendss.PVSystem.class_pvsystem_ptcurve_dialog
import opendss.PVSystem.class_pvsystem_tempcurve_dialog
import opendss.PVSystem.class_pvsystem_substation_dialog

class C_Config_PVSystem_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.titleWindow = "PVSystem Config"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.adjustSize()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Main_Toolbar = main_toolbar.C_MenuToolBar()

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

        # PVSystem Data
        self.PVsystem_GroupBox = QGroupBox("PVSystem")  # Criando a GroupBox invcontrol
        self.PVsystem_GroupBox.setMinimumWidth(400)
        self.PVsystem_GroupBox_Layout = QGridLayout()  # Layout da GroupBox é em Grid

        # GroupBox PVSystem Config
        # Tree Widget
        self.PVsystem_GroupBox_TreeWidget = QTreeWidget()
        self.PVsystem_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Potência', 'Barra'])
        self.PVsystem_GroupBox_TreeWidget.setColumnWidth(0, 130)
        self.PVsystem_GroupBox_TreeWidget.setColumnWidth(1, 80)
        self.PVsystem_GroupBox_Layout.addWidget(self.PVsystem_GroupBox_TreeWidget, 0, 1, 1, 3)

        # Botao Adicionar
        self.PVsystem_GroupBox_Add_Btn = QPushButton("Adicionar")  # Botão de Adicionar dentro do GroupBox
        self.PVsystem_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.PVsystem_GroupBox_Add_Btn.clicked.connect(self.addPVsystem)
        self.PVsystem_GroupBox_Layout.addWidget(self.PVsystem_GroupBox_Add_Btn, 1, 1, 1, 1)
        # Botao Excluir
        self.PVsystem_GroupBox_Delete_Btn = QPushButton("Excluir")  # Botão de Excluir dentro do GroupBox
        self.PVsystem_GroupBox_Delete_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.PVsystem_GroupBox_Delete_Btn.clicked.connect(self.removePVsystem)
        self.PVsystem_GroupBox_Layout.addWidget(self.PVsystem_GroupBox_Delete_Btn, 1, 2, 1, 1)
        # Botão Editar
        self.PVsystem_GroupBox_Edit_Btn = QPushButton("Editar")  # Botão de editar dentro do GroupBox
        self.PVsystem_GroupBox_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.PVsystem_GroupBox_Edit_Btn.clicked.connect(self.editPVsystem)
        self.PVsystem_GroupBox_Layout.addWidget(self.PVsystem_GroupBox_Edit_Btn, 1, 3, 1, 1)
        # Botao OK
        self.PVsystem_GroupBox_OK_Btn = QPushButton("OK")  # Botão OK dentro do GroupBox
        self.PVsystem_GroupBox_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.PVsystem_GroupBox_OK_Btn.clicked.connect(self.acceptInsertPVsystem)
        self.PVsystem_GroupBox_Layout.addWidget(self.PVsystem_GroupBox_OK_Btn, 2, 1, 1, 2)
        # Botao Cancelar
        self.PVsystem_GroupBox_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.PVsystem_GroupBox_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.PVsystem_GroupBox_Cancel_Btn.clicked.connect(self.cancelInsertPVsystem)
        self.PVsystem_GroupBox_Layout.addWidget(self.PVsystem_GroupBox_Cancel_Btn, 2, 3, 1, 1)

        self.PVsystem_GroupBox.setLayout(self.PVsystem_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.PVsystem_GroupBox)  # adiciona a GroupBox ao Dialog
        self.setLayout(self.Dialog_Layout)

        ##################################### Tabs #####################################################################
        self.TabWidget = QTabWidget()
        self.TabConfig = PVSystem()  # Tab das configurações
        self.TabWidget.addTab(self.TabConfig, "Configurações")

        self.PVConfig_GroupBox = QGroupBox()  # GroupBox que engloba as Tabs
        self.PVConfig_GroupBox_Layout = QGridLayout()
        self.PVConfig_GroupBox.setVisible(False)

        ### Botões das Configurações
        self.Config_Btns_Layout = QHBoxLayout()
        self.Config_Btns_Layout.setAlignment(Qt.AlignRight)
        # Botao Restaurar Default
        self.Config_Btns_Default_Btn = QPushButton("Restaurar Default")  # Botão Default dentro do GroupBox
        self.Config_Btns_Default_Btn.setFixedHeight(30)
        self.Config_Btns_Default_Btn.setFixedWidth(200)
        self.Config_Btns_Default_Btn.clicked.connect(self.restauradefault)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Default_Btn)
        # Botão OK
        self.Config_Btns_OK_Btn = QPushButton("OK")  # Botão Ok dentro do GroupBox
        self.Config_Btns_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Config_Btns_OK_Btn.setFixedHeight(30)
        self.Config_Btns_OK_Btn.clicked.connect(self.AcceptAddEditPVsystem)
        self.Config_Btns_OK_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_OK_Btn)
        # Botao Cancelar
        self.Config_Btns_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Config_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Config_Btns_Cancel_Btn.setFixedHeight(30)
        self.Config_Btns_Cancel_Btn.clicked.connect(self.CancelAddEditPVsystem)
        self.Config_Btns_Cancel_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Cancel_Btn)

        self.PVConfig_GroupBox_Layout.addWidget(self.TabWidget)

        self.PVConfig_GroupBox_Layout.addItem(self.Config_Btns_Layout)

        self.PVConfig_GroupBox.setLayout(self.PVConfig_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.PVConfig_GroupBox)
        self.Dialog_Layout.addLayout(QVBoxLayout())
        self.setLayout(self.Dialog_Layout)

    def addPVsystem(self):
        self.update_dialog()
        self.TabConfig.PVSystem_PVdata_Name.setEnabled(True)
        self.EnableDisableParameters(True)
        self.adjustSize()
        self.centralize()
        self.DefaultConfigParameters()

    def removePVsystem(self):
        for ctd in range(self.PVsystem_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
            Item = self.PVsystem_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                self.PVsystem_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                for i in self.PVSystem_List:
                    if i["name"] == Item.text(0):
                        self.PVSystem_List.remove(i)

    def editPVsystem(self):
        self.update_dialog()
        checkCont = 0
        for ctd in range(self.PVsystem_GroupBox_TreeWidget.topLevelItemCount() - 1, - 1, - 1):
            if self.PVsystem_GroupBox_TreeWidget.topLevelItem(ctd).checkState(0) == Qt.Checked:
                checkCont += 1
                Item = self.PVsystem_GroupBox_TreeWidget.topLevelItem(ctd)
                
        if checkCont == 1:
            self.clearPVConfigParameters()
            self.DefaultConfigParameters()
            for i in self.PVSystem_List:
                if i["name"] == Item.text(0):
                    self.TabConfig.PVSystem_PVdata_Name.setText(i["name"])
                    self.TabConfig.PVSystem_PVdata_Voltage.setValue(float(i["kv"]))
                    self.TabConfig.PVSystem_PVdata_Irrad.setValue(float(i["irrad"]))
                    self.TabConfig.PVSystem_PVdata_Ppmp.setValue(float(i["pmpp"]))
                    self.TabConfig.PVSystem_PVdata_KVA.setValue(float(i["kva"]))
                    self.TabConfig.PVSystem_PVdata_Temp.setValue(float(i["temperature"]))
                    self.TabConfig.PVSystem_PVdata_PF.setValue(float(i["pf"]))
                    self.TabConfig.PVSystem_PVdata_Cutin.setValue(float(i["cutin"]))
                    self.TabConfig.PVSystem_PVdata_Cutout.setValue(float(i["cutout"]))
                    self.TabConfig.PVSystem_PVdata_Phases_ComboBox.setCurrentText(i["phases"])
                    self.TabConfig.PVSystem_PVdata_Forma_ComboBox.setCurrentText(i["forma"])
                    self.TabConfig.eff.Config_EffCurve_GroupBox_TreeWidget_Item(
                        self.TabConfig.effcurve.EffCurve_GroupBox_TreeWidget,
                        i["EffCurve"]["EffCurveName"],
                        str(i["EffCurve"]["Xarray"]).strip('[]').replace("'", ""),
                        str(i["EffCurve"]["Yarray"]).strip('[]').replace("'", ""),
                        cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    self.TabConfig.pt.Config_PTCurve_GroupBox_TreeWidget_Item(
                        self.TabConfig.ptcurve.PTCurve_GroupBox_TreeWidget,
                        i["PTCurve"]["PTCurveName"],
                        str(i["PTCurve"]["Xarray"]).strip('[]').replace("'", ""),
                        str(i["PTCurve"]["Yarray"]).strip('[]').replace("'", ""),
                        cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    self.TabConfig.temp.Config_TempCurve_GroupBox_TreeWidget_Item(
                        self.TabConfig.tempcurve.TempCurve_GroupBox_TreeWidget,
                        i["TempCurve"]["TempCurveName"],
                        str(i["TempCurve"]["Xarray"]).strip('[]').replace("'", ""),
                        str(i["TempCurve"]["Yarray"]).strip('[]').replace("'", ""),
                        cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    self.TabConfig.irrad.Config_IrradCurve_GroupBox_TreeWidget_Item(
                        self.TabConfig.irradcurve.IrradCurve_GroupBox_TreeWidget,
                        i["IrradCurve"]["IrradCurveName"],
                        str(i["IrradCurve"]["Xarray"]).strip('[]').replace("'", ""),
                        str(i["IrradCurve"]["Yarray"]).strip('[]').replace("'", ""),
                        cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    if self.TabConfig.PVSystem_PVdata_Forma_ComboBox.currentText() == "Subestação":
                        self.TabConfig.subestacao.Subestacao_Name.setText(i["Subestacao"]["subsname"])
                        self.TabConfig.subestacao.Subestacao_XHL.setValue(float(i["Subestacao"]["xhl"]))
                        self.TabConfig.subestacao.Subestacao_Bus1_LineEdit.setText(i["Subestacao"]["bus1"])
                        self.TabConfig.subestacao.Subestacao_VPrimary.setValue(float(i["Subestacao"]["kv1"]))
                        self.TabConfig.subestacao.Subestacao_KVAPrimary.setValue(float(i["Subestacao"]["kva1"]))
                        self.TabConfig.subestacao.Subestacao_ConnPrimary_ComboBox.setCurrentText(i["Subestacao"]["conn1"])
                        self.TabConfig.subestacao.Subestacao_Bus2_ComboBox.setCurrentText(i["Subestacao"]["bus2"])
                        self.TabConfig.subestacao.Subestacao_VSecond.setValue(float(i["Subestacao"]["kv2"]))
                        self.TabConfig.subestacao.Subestacao_KVASecond.setValue(float(i["Subestacao"]["kva2"]))
                        self.TabConfig.subestacao.Subestacao_ConnSecond_ComboBox.setCurrentText(i["Subestacao"]["conn2"])
                    else:
                        self.TabConfig.Barra_GroupBox_ComboBox.setCurrentText(i["barra"])

            self.TabConfig.PVSystem_PVdata_Name.setEnabled(False)
            self.EnableDisableParameters(True)
            self.adjustSize()

        elif checkCont > 1:
            msg = QMessageBox()
            msg.information(self, "Editar PVSystem", "Selecione somente um PVSystem para editar!")

        else:
            msg = QMessageBox()
            msg.information(self, "Editar PVSystem", "Selecione pelo menos um PVsystem para editar!")


    def acceptInsertPVsystem(self):
        self.OpenDSS.PVSystem_Data = self.PVSystem_List
        self.clearPVConfigParameters()
        self.DefaultConfigParameters()
        self.close()

    def cancelInsertPVsystem(self):
        self.clearPVConfigParameters()
        self.DefaultConfigParameters()
        self.close()

    def restauradefault(self):
        self.clearPVConfigParameters()
        self.DefaultConfigParameters()

    def AcceptAddEditPVsystem(self):
        self.TabConfig.defaultcurves()
        if self.SelectPTcurve():
            if self.SelectEffcurve():
                if self.SelectTempcurve():
                    if self.SelectIrrad():
                        if self.CheckForma():
                            if self.TabConfig.get_PVSystem_Name() == '':
                                msg = QMessageBox()
                                msg.information(self, "Inserir PVSystem", "Adicione um nome ao PVSystem")

                            else:
                                countName = 0
                                PV = {}
                                PVlist = []
                                PV['name'] = self.TabConfig.get_PVSystem_Name()
                                PV['phases'] = self.TabConfig.get_Phases()
                                PV['kv'] = self.TabConfig.get_Nominal_Voltage()
                                PV['irrad'] = self.TabConfig.get_Nominal_Irradiance()
                                PV['pmpp'] = self.TabConfig.get_Nominal_Power()
                                PV['kva'] = self.TabConfig.get_Nominal_KVA()
                                PV['temperature'] = self.TabConfig.get_Nominal_Temp()
                                PV['pf'] = self.TabConfig.get_Power_Factor()
                                PV['cutin'] = self.TabConfig.get_cutin()
                                PV['cutout'] = self.TabConfig.get_cutout()
                                PV['forma'] = self.TabConfig.get_forma_conexao()
                                eff = self.TabConfig.effcurve.dataEffCurve
                                pt = self.TabConfig.ptcurve.dataPTCurve
                                temp = self.TabConfig.tempcurve.dataTempCurve
                                irrad = self.TabConfig.irradcurve.dataIrradCurve
                                PV.update({"EffCurve": eff})
                                PV.update({"PTCurve": pt})
                                PV.update({"TempCurve": temp})
                                PV.update({"IrradCurve": irrad})
                                if self.TabConfig.PVSystem_PVdata_Forma_ComboBox.currentText() == "Subestação":
                                    Subs = self.TabConfig.subestacao.dataSubestacao.copy()
                                    PV.update({"Subestacao": Subs})
                                else:
                                    PV['barra'] = self.TabConfig.get_direto_na_barra()

                                if self.TabConfig.PVSystem_PVdata_Name.isEnabled():  # Se estiver adicionando um PVSystem
                                    for ctd in range(0, self.PVsystem_GroupBox_TreeWidget.topLevelItemCount()):
                                        Item = self.PVsystem_GroupBox_TreeWidget.topLevelItem(ctd)

                                        if Item.text(0) == self.TabConfig.get_PVSystem_Name():
                                            countName += 1

                                    if countName == 0:
                                        if self.TabConfig.PVSystem_PVdata_Forma_ComboBox.currentText() == "Subestação":
                                            PVSystem_TreeWidget_Item(self.PVsystem_GroupBox_TreeWidget,
                                                                     self.TabConfig.get_PVSystem_Name(),
                                                                     self.TabConfig.get_Nominal_Power().replace(".", ","),
                                                                     self.TabConfig.subestacao.Subestacao_Bus2_ComboBox.currentText())

                                        else:
                                            PVSystem_TreeWidget_Item(self.PVsystem_GroupBox_TreeWidget,
                                                                     self.TabConfig.get_PVSystem_Name(),
                                                                     self.TabConfig.get_Nominal_Power().replace(".", ","),
                                                                     self.TabConfig.Barra_GroupBox_ComboBox.currentText())

                                        self.PVSystem_List.append(PV)

                                    else:
                                        msg = QMessageBox()
                                        msg.information(self, "Inserir PVSystem", "Não foi possível adicionar, já existe um PVsystem com esse nome")

                                else:  # Se estiver editando um PVSystem
                                    for ctd in self.PVSystem_List:
                                        if ctd["name"] == PV["name"]:
                                            ctd["phases"] = PV["phases"]
                                            ctd["kv"] = PV["kv"]
                                            ctd["irrad"] = PV["irrad"]
                                            ctd["pmpp"] = PV["pmpp"]
                                            ctd["kva"] = PV["kva"]
                                            ctd["temperature"] = PV["temperature"]
                                            ctd["pf"] = PV["pf"]
                                            ctd["cutin"] = PV["cutin"]
                                            ctd["cutout"] = PV["cutout"]
                                            ctd["EffCurve"] = PV["EffCurve"]
                                            ctd["PTCurve"] = PV["PTCurve"]
                                            ctd["TempCurve"] = PV["TempCurve"]
                                            ctd["IrradCurve"] = PV["IrradCurve"]
                                            ctd["forma"] = PV["forma"]
                                            if ctd["forma"] == "Subestação":
                                                ctd["Subestacao"] = PV["Subestacao"]
                                            else:
                                                ctd["barra"] = PV["barra"]

                                            for ctd in range(self.PVsystem_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
                                                Item = self.PVsystem_GroupBox_TreeWidget.topLevelItem(ctd)

                                                if Item.text(0) == self.TabConfig.get_PVSystem_Name():
                                                    self.PVsystem_GroupBox_TreeWidget.takeTopLevelItem(ctd)

                                                    if self.TabConfig.PVSystem_PVdata_Forma_ComboBox.currentText() == "Subestação":
                                                        PVSystem_TreeWidget_Item(self.PVsystem_GroupBox_TreeWidget,
                                                                                 self.TabConfig.get_PVSystem_Name(),
                                                                                 self.TabConfig.get_Nominal_Power().replace(".", ","),
                                                                                 self.TabConfig.subestacao.Subestacao_Bus2_ComboBox.currentText())

                                                    else:
                                                        PVSystem_TreeWidget_Item(self.PVsystem_GroupBox_TreeWidget,
                                                                                 self.TabConfig.get_PVSystem_Name(),
                                                                                 self.TabConfig.get_Nominal_Power().replace(".", ","),
                                                                                 self.TabConfig.Barra_GroupBox_ComboBox.currentText())

                                self.clearPVConfigParameters()
                                self.DefaultConfigParameters()
                                self.EnableDisableParameters(False)
                                self.adjustSize()

    def CancelAddEditPVsystem(self):
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):
        if bool:
            self.PVConfig_GroupBox.setVisible(True)
            self.PVsystem_GroupBox.setVisible(False)
        else:
            self.PVConfig_GroupBox.setVisible(False)
            self.PVsystem_GroupBox.setVisible(True)

    def clearPVConfigParameters(self):
        self.TabConfig.PVSystem_PVdata_Name.clear()
        self.TabConfig.ptcurve.PTCurve_GroupBox_TreeWidget.clear()
        self.TabConfig.ptcurve.graphWidget.clear()
        self.TabConfig.ptcurve.dataPTCurve = {}
        self.TabConfig.effcurve.EffCurve_GroupBox_TreeWidget.clear()
        self.TabConfig.effcurve.graphWidget.clear()
        self.TabConfig.effcurve.dataEffCurve = {}
        self.TabConfig.tempcurve.TempCurve_GroupBox_TreeWidget.clear()
        self.TabConfig.tempcurve.graphWidget.clear()
        self.TabConfig.tempcurve.dataTempCurve = {}
        self.TabConfig.irradcurve.IrradCurve_GroupBox_TreeWidget.clear()
        self.TabConfig.irradcurve.graphWidget.clear()
        self.TabConfig.irradcurve.dataIrradCurve = {}
        self.TabConfig.PVSystem_PVdata_Voltage.clear()
        self.TabConfig.PVSystem_PVdata_Irrad.clear()
        self.TabConfig.PVSystem_PVdata_Ppmp.clear()
        self.TabConfig.PVSystem_PVdata_KVA.clear()
        self.TabConfig.PVSystem_PVdata_Temp.clear()
        self.TabConfig.PVSystem_PVdata_PF.clear()
        self.TabConfig.PVSystem_PVdata_Cutin.clear()
        self.TabConfig.PVSystem_PVdata_Cutout.clear()
        self.TabConfig.PVSystem_PVdata_Phases_ComboBox.setCurrentIndex(1)
        self.TabConfig.subestacao.clearSubstationParameters()

    def DefaultConfigParameters(self):
        self.TabConfig.PVSystem_PVdata_Name.setText("")
        self.TabConfig.PVSystem_PVdata_Voltage.setValue(0.48)
        self.TabConfig.PVSystem_PVdata_Irrad.setValue(1.00)
        self.TabConfig.PVSystem_PVdata_Ppmp.setValue(500.00)
        self.TabConfig.PVSystem_PVdata_KVA.setValue(500.00)
        self.TabConfig.PVSystem_PVdata_Temp.setValue(25.00)
        self.TabConfig.PVSystem_PVdata_PF.setValue(1.00)
        self.TabConfig.PVSystem_PVdata_Cutin.setValue(0.10)
        self.TabConfig.PVSystem_PVdata_Cutout.setValue(0.10)
        self.TabConfig.PVSystem_PVdata_Phases_ComboBox.setCurrentIndex(1)
        self.TabConfig.subestacao.defaultSubstationParameters()

    def update_dialog(self):
        self.allbus = self.OpenDSS.getBusList()
        self.TabConfig.subestacao.Subestacao_Bus2_ComboBox.addItems(self.allbus)
        self.TabConfig.Barra_GroupBox_ComboBox.addItems(self.allbus)

    def SelectPTcurve(self):
        if self.TabConfig.ptcurve.dataPTCurve == {}:
            msg = QMessageBox()
            msg.information(self, "Inserir PVSystem", "Selecione uma PT curve para o PVSystem")
            return False
        else:
            return True

    def SelectEffcurve(self):
        if self.TabConfig.effcurve.dataEffCurve == {}:
            msg = QMessageBox()
            msg.information(self, "Inserir PVSystem", "Selecione uma Eff curve para o PVSystem")
            return False
        else:
            return True

    def SelectTempcurve(self):
        if self.TabConfig.tempcurve.dataTempCurve == {}:
            msg = QMessageBox()
            msg.information(self, "Inserir PVSystem", "Selecione uma Temp curve para o PVSystem")
            return False
        else:
            return True

    def SelectIrrad(self):
        if self.TabConfig.irradcurve.dataIrradCurve == {}:
            msg = QMessageBox()
            msg.information(self, "Inserir PVSystem", "Selecione uma Irrad curve para o PVSystem")
            return False
        else:
            return True

    def CheckForma(self):
        if self.TabConfig.PVSystem_PVdata_Forma_ComboBox.currentText() == "Subestação":
            if self.TabConfig.subestacao.get_Substation_Name() == "":
                msg = QMessageBox()
                msg.information(self, "Inserir PVSystem", "Adicione uma Subestação ou conecte direto na barra")
                return False
            else:
                return True
        else:
            return True

    def centralize(self):
        qr = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerpoint)
        self.move(qr.topLeft())

class PVSystem(QDialog):
    def __init__(self):
        super().__init__()

        self.effcurve = opendss.PVSystem.class_pvsystem_effcurve_dialog.C_Config_EffCurve_Dialog()
        self.irradcurve = opendss.PVSystem.class_pvsystem_irradcurve_dialog.C_Config_IrradCurve_Dialog()
        self.ptcurve = opendss.PVSystem.class_pvsystem_ptcurve_dialog.C_Config_PTCurve_Dialog()
        self.tempcurve = opendss.PVSystem.class_pvsystem_tempcurve_dialog.C_Config_TempCurve_Dialog()
        self.subestacao = opendss.PVSystem.class_pvsystem_substation_dialog.Subestacao()

        self.eff = opendss.PVSystem.class_pvsystem_effcurve_dialog
        self.irrad = opendss.PVSystem.class_pvsystem_irradcurve_dialog
        self.pt = opendss.PVSystem.class_pvsystem_ptcurve_dialog
        self.temp = opendss.PVSystem.class_pvsystem_tempcurve_dialog

        self.InitUI()

    def InitUI(self):

        ##Layout principal
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        ################################### GroupBox das Configurações #################################################
        # PVSystem Data
        self.PVSystem_GroupBox_PVdata = QGroupBox()
        self.PVSystem_GroupBox_PVdata_Layout = QGridLayout()

        # GroupBox Subestação
        self.Subestacao_GroupBox = QGroupBox("Subestação")
        self.Subestacao_GroupBox_Layout = QGridLayout()

        self.Subestacao_GroupBox_Label = QLabel("Adicionar Subestação")
        self.Subestacao_GroupBox_Btn = QPushButton("Subestação")

        self.Subestacao_GroupBox_Layout.addWidget(self.Subestacao_GroupBox_Label, 0, 0, 1, 1)
        self.Subestacao_GroupBox_Layout.addWidget(self.Subestacao_GroupBox_Btn, 0, 1, 1, 1)

        # GroupBox Direto na barra
        self.Barra_GroupBox = QGroupBox("Direto na Barra")
        self.Barra_GroupBox_Layout = QGridLayout()
        self.Barra_GroupBox.setVisible(False)

        self.Barra_GroupBox_Label = QLabel("Barra de Conexão")
        self.Barra_GroupBox_ComboBox = QComboBox()

        self.Barra_GroupBox_Layout.addWidget(self.Barra_GroupBox_Label, 0, 0, 1, 1)
        self.Barra_GroupBox_Layout.addWidget(self.Barra_GroupBox_ComboBox, 0, 1, 1, 1)

        #  GroupBox PVSystem Data
        #  Labels
        self.PVSystem_PVdata_Name_Label = QLabel("Nome:")
        self.PVSystem_Import_PTCurve_Label = QLabel("Carregar Curva Potencia x Tempo")
        self.PVSystem_Import_EffCurve_Label = QLabel("Carregar Curva Eficiência x Potencia")
        self.PVSystem_Import_TempCurve_Label = QLabel("Carregar Curva Temperatura")
        self.PVSystem_Import_IrradCurve_Label = QLabel("Carregar Curva de Irradiação")
        self.PVSystem_PVdata_Phases_Label = QLabel("Nº Fases:")
        self.PVSystem_PVdata_Voltage_Label = QLabel("Tensão do Painel (kV):")
        self.PVSystem_PVdata_Irrad_Label = QLabel("Irradiação Nominal (normalizada):")
        self.PVSystem_PVdata_Ppmp_Label = QLabel("Potência MPPT (W):")
        self.PVSystem_PVdata_KVA_Label = QLabel("Potência do Inversor (KVA):")
        self.PVSystem_PVdata_Temp_Label = QLabel("Temperatura de Operação:")
        self.PVSystem_PVdata_PF_Label = QLabel("Fator de Potência:")
        self.PVSystem_PVdata_Cutin_Label = QLabel("%Cutin")
        self.PVSystem_PVdata_Cutout_Label = QLabel("%Cutout")
        self.PVSystem_PVdata_Forma_Label = QLabel("Forma de Conexão")

        # LineEdits
        self.PVSystem_PVdata_Name = QLineEdit()
        self.PVSystem_PVdata_Voltage = QDoubleSpinBox()
        self.PVSystem_PVdata_Voltage.setDecimals(2)
        self.PVSystem_PVdata_Voltage.setRange(0.01, 1000)
        self.PVSystem_PVdata_Voltage.setToolTip("Aceita valores entre 0,01 e 1000")
        self.PVSystem_PVdata_Voltage.setButtonSymbols(2)
        self.PVSystem_PVdata_Voltage.setValue(4.6)
        self.PVSystem_PVdata_Irrad = QDoubleSpinBox()
        self.PVSystem_PVdata_Irrad.setDecimals(2)
        self.PVSystem_PVdata_Irrad.setRange(0, 1)
        self.PVSystem_PVdata_Irrad.setToolTip("Aceita valores entre 0 e 1")
        self.PVSystem_PVdata_Irrad.setButtonSymbols(2)
        self.PVSystem_PVdata_Irrad.setValue(1)
        self.PVSystem_PVdata_Ppmp = QDoubleSpinBox()
        self.PVSystem_PVdata_Ppmp.setDecimals(2)
        self.PVSystem_PVdata_Ppmp.setRange(0.01, 1000)
        self.PVSystem_PVdata_Ppmp.setToolTip("Aceita valores entre 0,01 e 1000")
        self.PVSystem_PVdata_Ppmp.setButtonSymbols(2)
        self.PVSystem_PVdata_Ppmp.setValue(500)
        self.PVSystem_PVdata_KVA = QDoubleSpinBox()
        self.PVSystem_PVdata_KVA.setDecimals(2)
        self.PVSystem_PVdata_KVA.setRange(0.01, 1000)
        self.PVSystem_PVdata_KVA.setToolTip("Aceita valores entre 0,01 e 1000")
        self.PVSystem_PVdata_KVA.setButtonSymbols(2)
        self.PVSystem_PVdata_KVA.setValue(500)
        self.PVSystem_PVdata_Temp = QDoubleSpinBox()
        self.PVSystem_PVdata_Temp.setDecimals(2)
        self.PVSystem_PVdata_Temp.setRange(0, 100)
        self.PVSystem_PVdata_Temp.setToolTip("Aceita valores entre 0 e 100")
        self.PVSystem_PVdata_Temp.setButtonSymbols(2)
        self.PVSystem_PVdata_Temp.setValue(25)
        self.PVSystem_PVdata_PF = QDoubleSpinBox()
        self.PVSystem_PVdata_PF.setDecimals(2)
        self.PVSystem_PVdata_PF.setRange(-1, 1)
        self.PVSystem_PVdata_PF.setToolTip("Aceita valores entre -1 e 1")
        self.PVSystem_PVdata_PF.setButtonSymbols(2)
        self.PVSystem_PVdata_PF.setValue(1)
        self.PVSystem_PVdata_Cutin = QDoubleSpinBox()
        self.PVSystem_PVdata_Cutin.setDecimals(2)
        self.PVSystem_PVdata_Cutin.setRange(0, 100)
        self.PVSystem_PVdata_Cutin.setToolTip("Aceita valores entre 0 e 100")
        self.PVSystem_PVdata_Cutin.setButtonSymbols(2)
        self.PVSystem_PVdata_Cutin.setValue(0.1)
        self.PVSystem_PVdata_Cutout = QDoubleSpinBox()
        self.PVSystem_PVdata_Cutout.setDecimals(2)
        self.PVSystem_PVdata_Cutout.setRange(0, 100)
        self.PVSystem_PVdata_Cutout.setToolTip("Aceita valores entre 0 e 100")
        self.PVSystem_PVdata_Cutout.setButtonSymbols(2)
        self.PVSystem_PVdata_Cutout.setValue(0.1)

        # Comboboxs
        self.PVSystem_PVdata_Phases_ComboBox = QComboBox()
        self.PVSystem_PVdata_Phases_ComboBox.addItems(["1", "3"])
        self.PVSystem_PVdata_Forma_ComboBox = QComboBox()
        self.PVSystem_PVdata_Forma_ComboBox.addItems(["Subestação", "Direto na Barra"])
        self.PVSystem_PVdata_Forma_ComboBox.currentIndexChanged.connect(self.setDisabled_Forma_GroupBox)

        # Buttons
        self.PVSystem_Import_PTCurve_Btn = QPushButton("PT Curve")
        self.PVSystem_Import_EffCurve_Btn = QPushButton("Eff Curve")
        self.PVSystem_Import_TempCurve_Btn = QPushButton("Temp Curve")
        self.PVSystem_Import_IrradCurve_Btn = QPushButton("Irrad Curve")

        # CheckBox
        self.Default_CheckBox = QCheckBox("Adicionar curvas default")

        # Add Widgets and Layouts
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Name_Label, 0, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Name, 0, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_PTCurve_Label, 1, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_PTCurve_Btn, 1, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_EffCurve_Label, 2, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_EffCurve_Btn, 2, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_TempCurve_Label, 3, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_TempCurve_Btn, 3, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_IrradCurve_Label, 4, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_Import_IrradCurve_Btn, 4, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.Default_CheckBox, 5, 0, 1, 2)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Phases_Label, 6, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Phases_ComboBox, 6, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Voltage_Label, 7, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Voltage, 7, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Irrad_Label, 8, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Irrad, 8, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Ppmp_Label, 9, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Ppmp, 9, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_KVA_Label, 10, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_KVA, 10, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Temp_Label, 11, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Temp, 11, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_PF_Label, 12, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_PF, 12, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutin_Label, 13, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutin, 13, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutout_Label, 14, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Cutout, 14, 1, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Forma_Label, 15, 0, 1, 1)
        self.PVSystem_GroupBox_PVdata_Layout.addWidget(self.PVSystem_PVdata_Forma_ComboBox, 15, 1, 1, 1)

        # GroupBox Curves Config Buttons - Actions
        self.PVSystem_Import_EffCurve_Btn.clicked.connect(self.add_eff_curve)
        self.PVSystem_Import_IrradCurve_Btn.clicked.connect(self.add_irrad_curve)
        self.PVSystem_Import_PTCurve_Btn.clicked.connect(self.add_pt_curve)
        self.PVSystem_Import_TempCurve_Btn.clicked.connect(self.add_temp_curve)
        self.Subestacao_GroupBox_Btn.clicked.connect(self.add_subestacao)

        self.Tab_layout = QGridLayout()

        self.PVSystem_GroupBox_PVdata.setLayout(self.PVSystem_GroupBox_PVdata_Layout)
        self.Barra_GroupBox.setLayout(self.Barra_GroupBox_Layout)
        self.Subestacao_GroupBox.setLayout(self.Subestacao_GroupBox_Layout)
        self.Tab_layout.addWidget(self.PVSystem_GroupBox_PVdata, 0, 1, 1, 1)
        self.Tab_layout.addWidget(self.Barra_GroupBox, 1, 1, 1, 1)
        self.Tab_layout.addWidget(self.Subestacao_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Tab_layout)

    def get_PVSystem_Name(self):
        return unidecode.unidecode(self.PVSystem_PVdata_Name.text().strip().replace(" ", "_"))

    def get_PTCurve(self):
        return self.ptcurve.dataPTCurve

    def get_EffCurve(self):
        return self.effcurve.dataEffCurve

    def get_IrradCurve(self):
        return self.irradcurve.dataIrradCurve

    def get_TempCurve(self):
        return self.tempcurve.dataTempCurve

    def get_Phases(self):
        return self.PVSystem_PVdata_Phases_ComboBox.currentText()

    def get_Nominal_Voltage(self):
        return self.PVSystem_PVdata_Voltage.text().replace(",", ".")

    def get_Nominal_Irradiance(self):
        return self.PVSystem_PVdata_Irrad.text().replace(",", ".")

    def get_Nominal_Power(self):
        return self.PVSystem_PVdata_Ppmp.text().replace(",", ".")

    def get_Nominal_KVA(self):
        return self.PVSystem_PVdata_KVA.text().replace(",", ".")

    def get_Nominal_Temp(self):
        return self.PVSystem_PVdata_Temp.text().replace(",", ".")

    def get_Power_Factor(self):
        return self.PVSystem_PVdata_PF.text().replace(",", ".")

    def get_cutin(self):
        return self.PVSystem_PVdata_Cutin.text().replace(",", ".")

    def get_cutout(self):
        return self.PVSystem_PVdata_Cutout.text().replace(",", ".")

    def get_forma_conexao(self):
        return self.PVSystem_PVdata_Forma_ComboBox.currentText()

    def get_direto_na_barra(self):
        return self.Barra_GroupBox_ComboBox.currentText()

    def add_eff_curve(self):
        self.effcurve.show()

    def add_irrad_curve(self):
        self.irradcurve.show()

    def add_pt_curve(self):
        self.ptcurve.show()

    def add_temp_curve(self):
        self.tempcurve.show()

    def add_subestacao(self):
        self.subestacao.show()

    def defaultcurves(self):
        if self.Default_CheckBox.isChecked():
            self.effcurve.default_entries()
            self.irradcurve.default_entries()
            self.ptcurve.default_entries()
            self.tempcurve.default_entries()

    def setDisabled_Forma_GroupBox(self):
        if self.PVSystem_PVdata_Forma_ComboBox.currentText() == "Subestação":
            self.Subestacao_GroupBox.setVisible(True)
            self.Barra_GroupBox.setVisible(False)
        else:
            self.Subestacao_GroupBox.setVisible(False)
            self.Barra_GroupBox.setVisible(True)

class PVSystem_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, pot, bus):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(PVSystem_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Unchecked)
        ## Column 1 - Potência:
        self.setText(1, pot)
        ## Column 2 - Barra:
        self.setText(2, bus)