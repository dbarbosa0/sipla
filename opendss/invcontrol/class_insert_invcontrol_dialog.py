from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QDoubleSpinBox, QSpinBox, QDesktopWidget
from PyQt5.QtCore import Qt

import random
import opendss.invcontrol.class_config_voltvar_xycurve
import opendss.invcontrol.class_config_voltwatt_xycurve
import opendss.invcontrol.class_config_voltvar_elementlist
import opendss.invcontrol.class_config_voltwatt_elementlist
import opendss.class_opendss
import config as cfg
import unidecode


class C_Insert_InvControl_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Inserir Controle do Inversor"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InvControlList = []

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.VV_XYCurveFile = opendss.invcontrol.class_config_voltvar_xycurve
        self.VW_XYCurveFile = opendss.invcontrol.class_config_voltwatt_xycurve

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)       # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        ##Layout principal
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        ####################### GroupBox invcontrol ############################################################
        self.InvControl_GroupBox = QGroupBox("InvControl")  # Criando a GroupBox invcontrol
        self.InvControl_GroupBox.setMinimumWidth(400)
        self.InvControl_GroupBox_Layout = QGridLayout()  # Layout da GroupBox é em Grid

        # Tree Widget
        self.InvControl_GroupBox_TreeWidget = QTreeWidget()
        self.InvControl_GroupBox_TreeWidget.setHeaderLabels(['Nome', 'Modo', 'Elementos PC'])
        self.InvControl_GroupBox_TreeWidget.setColumnWidth(0, 130)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_TreeWidget, 0, 1, 1, 3)
        # Botao Adicionar
        self.InvControl_GroupBox_Add_Btn = QPushButton("Adicionar")  # Botão de Adicionar dentro do GroupBox
        self.InvControl_GroupBox_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.InvControl_GroupBox_Add_Btn.clicked.connect(self.addInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Add_Btn, 1, 1, 1, 1)
        # Botao Excluir
        self.InvControl_GroupBox_Delete_Btn = QPushButton("Excluir")  # Botão de Excluir dentro do GroupBox
        self.InvControl_GroupBox_Delete_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.InvControl_GroupBox_Delete_Btn.clicked.connect(self.removeInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Delete_Btn, 1, 2, 1, 1)
        # Botão Editar
        self.InvControl_GroupBox_Edit_Btn = QPushButton("Editar")  # Botão de editar dentro do GroupBox
        self.InvControl_GroupBox_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.InvControl_GroupBox_Edit_Btn.clicked.connect(self.editInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Edit_Btn, 1, 3, 1, 1)
        # Botao OK
        self.InvControl_GroupBox_OK_Btn = QPushButton("OK")  # Botão OK dentro do GroupBox
        self.InvControl_GroupBox_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.InvControl_GroupBox_OK_Btn.clicked.connect(self.acceptInsertInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_OK_Btn, 2, 1, 1, 2)
        # Botao Cancelar
        self.InvControl_GroupBox_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.InvControl_GroupBox_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.InvControl_GroupBox_Cancel_Btn.clicked.connect(self.cancelInsertInvControl)
        self.InvControl_GroupBox_Layout.addWidget(self.InvControl_GroupBox_Cancel_Btn, 2, 3, 1, 1)

        self.InvControl_GroupBox.setLayout(self.InvControl_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.InvControl_GroupBox)  # adiciona a GroupBox ao Dialog
        self.setLayout(self.Dialog_Layout)

        ##################################### Tabs #####################################################################
        self.TabWidget = QTabWidget()
        self.TabConfig = InvConfig()  # Tab das configurações
        self.TabWidget.addTab(self.TabConfig, "Configurações")

        ################################### GroupBox das Configurações #################################################
        self.InvEConfig_GroupBox = QGroupBox()  # GroupBox que engloba as Tabs
        self.InvEConfig_GroupBox_Layout = QGridLayout()
        self.InvEConfig_GroupBox.setVisible(False)

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
        self.Config_Btns_OK_Btn = QPushButton("OK")              # Botão Ok dentro do GroupBox
        self.Config_Btns_OK_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Config_Btns_OK_Btn.setFixedHeight(30)
        self.Config_Btns_OK_Btn.clicked.connect(self.AcceptAddEditInvControl)
        self.Config_Btns_OK_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_OK_Btn)
        # Botao Cancelar
        self.Config_Btns_Cancel_Btn = QPushButton("Cancelar")  # Botão Cancelar dentro do GroupBox
        self.Config_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Config_Btns_Cancel_Btn.setFixedHeight(30)
        self.Config_Btns_Cancel_Btn.clicked.connect(self.CancelAddEditInvControl)
        self.Config_Btns_Cancel_Btn.setFixedWidth(125)
        self.Config_Btns_Layout.addWidget(self.Config_Btns_Cancel_Btn)

        self.InvEConfig_GroupBox_Layout.addWidget(self.TabWidget)
        self.InvEConfig_GroupBox_Layout.addItem(self.Config_Btns_Layout)

        self.InvEConfig_GroupBox.setLayout(self.InvEConfig_GroupBox_Layout)

        self.Dialog_Layout.addWidget(self.InvEConfig_GroupBox)  # adiciona a GroupBox das Configurações ao Dialog

        self.setLayout(self.Dialog_Layout)

    def get_InvControlName(self):
        return unidecode.unidecode(self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.text().strip().replace(" ", "_"))

    def addInvControl(self):
        self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setEnabled(True)
        self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setEnabled(True)
        self.EnableDisableParameters(True)
        self.DefaultConfigParameters()
        self.adjustSize()
        self.centralize()

    def removeInvControl(self):
        for ctd in range(self.InvControl_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
            Item = self.InvControl_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                self.InvControl_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                for i in self.InvControlList:
                    if i["InvControlName"] == Item.text(0):
                        self.InvControlList.remove(i)

    def editInvControl(self):
        checkCont = 0
        for ctd in range(self.InvControl_GroupBox_TreeWidget.topLevelItemCount() - 1, - 1, - 1):
            if self.InvControl_GroupBox_TreeWidget.topLevelItem(ctd).checkState(0) == Qt.Checked:
                checkCont += 1
                Item = self.InvControl_GroupBox_TreeWidget.topLevelItem(ctd)

        if checkCont == 1:
            self.clearInvControlParameters()
            for i in self.InvControlList:
                if i["InvControlName"] == Item.text(0):
                    self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setText(i["InvControlName"])
                    self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setCurrentText(i["Mode"])

                    if self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR": #VOLTVAR
                        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText(i["VV_EventLog"])
                        self.TabConfig.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setValue(float(i["VV_DeltaQFactor"]))
                        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setValue(
                            float(i["VV_VarChangeTolerance"]))
                        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setValue(
                            float(i["VV_VoltageChangeTolerance"]))
                        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setValue(
                            float(i["VV_HysteresisOffSet"]))
                        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText(
                            i["VV_VoltageCurvexRef"])
                        if self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                            self.TabConfig.VoltVar_GroupBox_AvgWindowLen_SpinBox.setValue(
                                int(i["VV_AvgWindowLen"]))
                            self.TabConfig.VoltVar_GroupBox_AvgWindowLen_ComboBox.setCurrentText(i["VV_Unit"])
                        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText(
                            i["VV_RateofChangeMode"])
                        if self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                            self.TabConfig.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setValue(float(i["VV_LPFtau"]))
                        if self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                            self.TabConfig.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setValue(
                                float(i["VV_RiseFallLimit"]))
                        self.TabConfig.VoltVar_GroupBox_RefReactivePower_ComboBox.setCurrentText(
                            i["VV_RefReactivePower"])
                        ptsX = str(i["VV_XYCurve"]["Xarray"]).strip('[]').replace("'", "")
                        ptsY = str(i["VV_XYCurve"]["Yarray"]).strip('[]').replace("'", "")
                        self.VV_XYCurveFile.Config_XYCurve_GroupBox_TreeWidget_Item(
                                    self.TabConfig.VV_XYCurve.XYCurve_GroupBox_TreeWidget,
                                    i["VV_XYCurve"]["XYCurveName"],
                                    ptsX,
                                    ptsY,
                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])
                    else:    ###VOLTWATT
                        self.TabConfig.VoltWatt_GroupBox_EventLog_ComboBox.setCurrentText(i["VW_EventLog"])
                        self.TabConfig.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setValue(
                            float(i["VW_DeltaPFactor"]))
                        self.TabConfig.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setValue(
                            float(i["VW_ActivePChangeTolerance"]))
                        self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText(
                            i["VW_VoltageCurvexRef"])
                        if self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                            self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setValue(
                                int(i["VW_AvgWindowLen"]))
                            self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setCurrentText(i["VW_Unit"])
                        self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.setCurrentText(
                            i["VW_RateofChangeMode"])
                        if self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                            self.TabConfig.VoltWatt_GroupBox_LPFtau_LineEdit.setValue(float(i["VW_LPFtau"]))
                        if self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                            self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setValue(
                                float(i["VW_RiseFallLimit"]))
                        self.TabConfig.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.setCurrentText(
                            i["VW_VoltWattYAxis"])
                        ptsX = str(i["VW_XYCurve"]["Xarray"]).strip('[]').replace("'", "")
                        ptsY = str(i["VW_XYCurve"]["Yarray"]).strip('[]').replace("'", "")
                        self.VW_XYCurveFile.Config_XYCurve_GroupBox_TreeWidget_Item(
                                    self.TabConfig.VW_XYCurve.XYCurve_GroupBox_TreeWidget,
                                    i["VW_XYCurve"]["XYCurveName"],
                                    ptsX,
                                    ptsY,
                                    cfg.colorsList[random.randint(0, len(cfg.colorsList) - 1)])

            self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setEnabled(False)
            self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setEnabled(False)
            self.EnableDisableParameters(True)
            self.adjustSize()

        elif checkCont > 1:
            msg = QMessageBox()
            msg.information(self, "Editar Controle do Inversor", "Selecione somente um InvControl para editar!")

        else:
            msg = QMessageBox()
            msg.information(self, "Editar Controle do Inversor", "Selecione pelo menos um InvControl para editar!")

    def restauradefault(self):
        self.clearInvControlParameters()
        self.DefaultConfigParameters()

    def acceptInsertInvControl(self):
        self.OpenDSS.InvControl = self.InvControlList
        self.clearInvControlParameters()
        self.DefaultConfigParameters()
        self.close()

    def cancelInsertInvControl(self):
        self.clearInvControlParameters()
        self.DefaultConfigParameters()
        self.close()

    def AcceptAddEditInvControl(self):

        if self.SelectXYCurve():
            if self.SelectElementList():
                if self.get_InvControlName() == "":
                    msg = QMessageBox()
                    msg.information(self, "Inserir Controle do Inversor", "Adicione um nome ao InvControl")

                else:
                    countName = 0
                    InvControl = {}

                    ######################## seta data das configurações gerais ############################################
                    InvControl["InvControlName"] = self.get_InvControlName()
                    InvControl["Mode"] = self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText()

                    ####################### seta data das configurações VoltVar ###########################################
                    if self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
                        InvControl["VV_DerList"] = self.TabConfig.VV_ElementList.Derlist
                        InvControl.update({"VV_XYCurve": self.TabConfig.VV_XYCurve.dataVV_XYCurve})
                        InvControl["VV_EventLog"] = self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.currentText()
                        InvControl["VV_DeltaQFactor"] = unidecode.unidecode(
                            self.TabConfig.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.text().replace(",", "."))
                        InvControl["VV_VarChangeTolerance"] = unidecode.unidecode(
                            self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.text().replace(",", "."))
                        InvControl["VV_VoltageChangeTolerance"] = unidecode.unidecode(
                            self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.text().replace(",","."))
                        InvControl["VV_HysteresisOffSet"] = unidecode.unidecode(
                            self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.text().replace(",", "."))
                        InvControl[
                            "VV_VoltageCurvexRef"] = self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentText()
                        if self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                            InvControl["VV_AvgWindowLen"] = self.TabConfig.VoltVar_GroupBox_AvgWindowLen_SpinBox.text()
                            InvControl["VV_Unit"] = self.TabConfig.VoltVar_GroupBox_AvgWindowLen_ComboBox.currentText()
                        InvControl[
                            "VV_RateofChangeMode"] = self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText()
                        if self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                            InvControl["VV_LPFtau"] = unidecode.unidecode(
                                self.TabConfig.VoltVar_GroupBox_LPFtau_DoubleSpinBox.text().replace(",", "."))
                        if self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                            InvControl["VV_RiseFallLimit"] = unidecode.unidecode(
                                self.TabConfig.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.text().replace(",", "."))
                        InvControl[
                            "VV_RefReactivePower"] = self.TabConfig.VoltVar_GroupBox_RefReactivePower_ComboBox.currentText()

                    ####################### seta data das configurações VoltWatt ###################################################
                    else:
                        InvControl["VW_DerList"] = self.TabConfig.VW_ElementList.Derlist
                        InvControl.update({"VW_XYCurve": self.TabConfig.VW_XYCurve.dataVW_XYCurve})
                        InvControl["VW_EventLog"] = self.TabConfig.VoltWatt_GroupBox_EventLog_ComboBox.currentText()
                        InvControl["VW_DeltaPFactor"] = unidecode.unidecode(
                            self.TabConfig.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.text().replace(",", "."))
                        InvControl["VW_ActivePChangeTolerance"] = unidecode.unidecode(
                            self.TabConfig.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.text().replace(",",
                                                                                                                 "."))
                        InvControl[
                            "VW_VoltageCurvexRef"] = self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentText()
                        if self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                            InvControl["VW_AvgWindowLen"] = self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_SpinBox.text()
                            InvControl["VW_Unit"] = self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_ComboBox.currentText()
                        InvControl[
                            "VW_RateofChangeMode"] = self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText()
                        if self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                            InvControl["VW_LPFtau"] = unidecode.unidecode(
                                self.TabConfig.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.text().replace(",", "."))
                        if self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                            InvControl["VW_RiseFallLimit"] = unidecode.unidecode(
                                self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.text().replace(",", "."))
                        InvControl[
                            "VW_VoltWattYAxis"] = self.TabConfig.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.currentText()

                    if self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.isEnabled():  # Se estiver adicionando um InvControl
                        for ctd in range(0, self.InvControl_GroupBox_TreeWidget.topLevelItemCount()):
                            Item = self.InvControl_GroupBox_TreeWidget.topLevelItem(ctd)

                            if Item.text(0) == self.get_InvControlName():
                                countName += 1

                        if countName == 0:

                            InvControl_TreeWidget_Item(self.InvControl_GroupBox_TreeWidget,
                                                       self.get_InvControlName(),
                                                       self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText(),
                                                       self.PCElement())

                            self.InvControlList.append(InvControl)

                        else:
                            msg = QMessageBox()
                            msg.information(self, "Inserir Controle do Inversor", "Não foi possível adicionar, já existe um InvControl com esse nome")

                    else:  # Se estiver editando um InvControl
                        for ctd in self.InvControlList:
                            if ctd["InvControlName"] == InvControl["InvControlName"]:

                                ctd["Mode"] = InvControl["Mode"]
                                if InvControl["Mode"] == "VOLTVAR":
                                    ctd["VV_DerList"] = InvControl["VV_DerList"]
                                    ctd["VV_EventLog"] = InvControl["VV_EventLog"]
                                    ctd["VV_DeltaQFactor"] = InvControl["VV_DeltaQFactor"]
                                    ctd["VV_VarChangeTolerance"] = InvControl["VV_VarChangeTolerance"]
                                    ctd["VV_VoltageChangeTolerance"] = InvControl["VV_VoltageChangeTolerance"]
                                    ctd["VV_HysteresisOffSet"] = InvControl["VV_HysteresisOffSet"]
                                    ctd["VV_VoltageCurvexRef"] = InvControl["VV_VoltageCurvexRef"]
                                    if InvControl["VV_VoltageCurvexRef"] == "avg":
                                        ctd["VV_AvgWindowLen"] = InvControl["VV_AvgWindowLen"]
                                        ctd["VV_Unit"] = InvControl["VV_Unit"]
                                    ctd["VV_RateofChangeMode"] = InvControl["VV_RateofChangeMode"]
                                    if InvControl["VV_RateofChangeMode"] == "LPF":
                                        ctd["VV_LPFtau"] = InvControl["VV_LPFtau"]
                                    if InvControl["VV_RateofChangeMode"] == "RISEFALL":
                                        ctd["VV_RiseFallLimit"] = InvControl["VV_RiseFallLimit"]
                                    ctd["VV_RefReactivePower"] = InvControl["VV_RefReactivePower"]
                                else:
                                    ctd["VW_DerList"] = InvControl["VW_DerList"]
                                    ctd["VW_EventLog"] = InvControl["VW_EventLog"]
                                    ctd["VW_DeltaPFactor"] = InvControl["VW_DeltaPFactor"]
                                    ctd["VW_ActivePChangeTolerance"] = InvControl["VW_ActivePChangeTolerance"]
                                    ctd["VW_VoltageCurvexRef"] = InvControl["VW_VoltageCurvexRef"]
                                    if InvControl["VW_VoltageCurvexRef"] == "avg":
                                        ctd["VW_AvgWindowLen"] = InvControl["VW_AvgWindowLen"]
                                        ctd["VW_Unit"] = InvControl["VW_Unit"]
                                    ctd["VW_RateofChangeMode"] = InvControl["VW_RateofChangeMode"]
                                    if InvControl["VW_RateofChangeMode"] == "LPF":
                                        ctd["VW_LPFtau"] = InvControl["VW_LPFtau"]
                                    if InvControl["VW_RateofChangeMode"] == "RISEFALL":
                                        ctd["VW_RiseFallLimit"] = InvControl["VW_RiseFallLimit"]
                                    ctd["VW_VoltWattYAxis"] = InvControl["VW_VoltWattYAxis"]
                                for ctd in range(self.InvControl_GroupBox_TreeWidget.topLevelItemCount() - 1, -1, -1):
                                    Item = self.InvControl_GroupBox_TreeWidget.topLevelItem(ctd)
                                    if Item.text(0) == self.get_InvControlName():
                                        self.InvControl_GroupBox_TreeWidget.takeTopLevelItem(ctd)
                                        InvControl_TreeWidget_Item(self.InvControl_GroupBox_TreeWidget,
                                                                   self.get_InvControlName(),
                                                                   self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText(),
                                                                   self.PCElement())

                    self.clearInvControlParameters()
                    self.DefaultConfigParameters()
                    self.EnableDisableParameters(False)
                    self.adjustSize()
        self.vv_list = ''
        self.vw_list = ''

    def CancelAddEditInvControl(self):
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):
        if bool:
            self.InvEConfig_GroupBox.setVisible(True)
            self.InvControl_GroupBox.setVisible(False)
        else:
            self.InvEConfig_GroupBox.setVisible(False)
            self.InvControl_GroupBox.setVisible(True)

    def SelectXYCurve(self):
        if self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            if self.TabConfig.VV_XYCurve.dataVV_XYCurve == {}:
                msg = QMessageBox()
                msg.information(self, "Inserir Controle do Inversor", "Selecione uma Curva XY para o InvControl")

                return False
            else:
                return True

        else:
            if self.TabConfig.VW_XYCurve.dataVW_XYCurve == {}:
                msg = QMessageBox()
                msg.information(self, "Inserir Controle do Inversor", "Selecione uma Curva XY para o InvControl")

                return False
            else:
                return True

    def PCElement(self):
        self.vv_list = ''
        for ctd in self.TabConfig.VV_ElementList.namelist:
            self.vv_list += str(ctd) + ", "

        self.vw_list = ''
        for ctd in self.TabConfig.VW_ElementList.namelist:
            self.vw_list += str(ctd) + ", "

        if self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            return self.vv_list[:-2]
        else:
            return self.vw_list[:-2]

    def SelectElementList(self):
        if self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            if self.TabConfig.VV_ElementList.Derlist == []:
                msg = QMessageBox()
                msg.information(self, "Inserir Controle do Inversor",
                                "Selecione pelo menos um elemento para o InvControl se conectar")

                return False
            else:
                return True
        else:
            if self.TabConfig.VW_ElementList.Derlist == []:
                msg = QMessageBox()
                msg.information(self, "Inserir Controle do Inversor",
                                "Selecione pelo menos um elemento para o InvControl se conectar")

                return False
            else:
                return True


    def DefaultConfigParameters(self):
        if self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.isEnabled():
            self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setText("")
        if self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.isEnabled():
            self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setCurrentText("VOLTVAR")

        ###VOLTVAR
        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText("Yes")
        self.TabConfig.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setValue(-1.0)
        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setValue(0.025)
        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setValue(0.0001)
        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setValue(0.0)
        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("rated")
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_SpinBox.setValue(0.0)
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_ComboBox.setCurrentText("s")
        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText("INACTIVE")
        self.TabConfig.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setValue(0.0)
        self.TabConfig.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setValue(-1.0)
        self.TabConfig.VoltVar_GroupBox_RefReactivePower_ComboBox.setCurrentText("VARAVAL")

        ###VOLTWATT
        self.TabConfig.VoltWatt_GroupBox_EventLog_ComboBox.setCurrentText("Yes")
        self.TabConfig.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setValue(-1.0)
        self.TabConfig.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setValue(0.01)
        self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("rated")
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setValue(0.0)
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setCurrentText("s")
        self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.setCurrentText("INACTIVE")
        self.TabConfig.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setValue(0.0)
        self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setValue(-1.0)
        self.TabConfig.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.setCurrentText("PMPPPU")

        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setEnabled(False)
        self.TabConfig.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)
        self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setEnabled(False)

    def clearInvControlParameters(self):
        self.TabConfig.NameEMode_GroupBox_Nome_LineEdit.setText("")
        self.TabConfig.NameEMode_GroupBox_Mode_ComboBox.setCurrentText("")

        self.TabConfig.VV_ElementList.clear()
        self.TabConfig.VW_ElementList.clear()

        ###VOLTVAR
        self.TabConfig.VV_XYCurve.XYCurve_GroupBox_TreeWidget.clear()
        self.TabConfig.VV_XYCurve.graphWidget.clear()
        self.TabConfig.VV_XYCurve.dataVV_XYCurve = {}

        self.TabConfig.VoltVar_GroupBox_EventLog_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_SpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_AvgWindowLen_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_RateofChangeMode_ComboBox.setCurrentText("")
        self.TabConfig.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltVar_GroupBox_RefReactivePower_ComboBox.setCurrentText("")

        ###VOLTWATT
        self.TabConfig.VW_XYCurve.XYCurve_GroupBox_TreeWidget.clear()
        self.TabConfig.VW_XYCurve.graphWidget.clear()
        self.TabConfig.VW_XYCurve.dataVW_XYCurve = {}

        self.TabConfig.VoltWatt_GroupBox_EventLog_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setValue(0)
        self.TabConfig.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_RateofChangeMode_ComboBox.setCurrentText("")
        self.TabConfig.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setValue(0)
        self.TabConfig.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.setCurrentText("")

    def centralize(self):
        qr = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerpoint)
        self.move(qr.topLeft())

class InvConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIInversorConfig()

        self.VV_XYCurve = opendss.invcontrol.class_config_voltvar_xycurve.C_Config_VoltVar_XYCurve_Dialog()
        self.VW_XYCurve = opendss.invcontrol.class_config_voltwatt_xycurve.C_Config_VoltWatt_XYCurve_Dialog()
        self.VV_ElementList = opendss.invcontrol.class_config_voltvar_elementlist.C_Config_ElementList_Dialog()
        self.VW_ElementList = opendss.invcontrol.class_config_voltwatt_elementlist.C_Config_ElementList_Dialog()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

    def InitUIInversorConfig(self):

        self.listmode = ["VOLTVAR", "VOLTWATT"]  # lista de modos disponíveis

        ###################### GroupBox NameEMode #######################################################
        self.NameEMode_GroupBox = QGroupBox()  # Criando a GroupBox InvConfig
        self.NameEMode_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        # Configurar nome do elemento
        self.NameEMode_GroupBox_Nome_Label = QLabel("Nome")
        self.NameEMode_GroupBox_Nome_LineEdit = QLineEdit()
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Nome_Label, 0, 0, 1, 1)
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Nome_LineEdit, 0, 1, 1, 1)
        # Configurar modo de controle
        self.NameEMode_GroupBox_Mode_Label = QLabel("Modo de Controle")
        self.NameEMode_GroupBox_Mode_ComboBox = QComboBox()
        self.NameEMode_GroupBox_Mode_ComboBox.addItems(self.listmode)
        self.NameEMode_GroupBox_Mode_ComboBox.currentIndexChanged.connect(self.setDisabled_Mode_GroupBox)
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Mode_Label, 1, 0, 1, 1)
        self.NameEMode_GroupBox_Layout.addWidget(self.NameEMode_GroupBox_Mode_ComboBox, 1, 1, 1, 1)

        ###################### GroupBox VOLTVAR #######################################################
        self.VoltVar_GroupBox = QGroupBox("VOLTVAR")  # Criando a GroupBox InvConfig
        self.VoltVar_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        # Configurar DERList
        self.VoltVar_GroupBox_DERList_Label = QLabel("DERList")
        self.VoltVar_GroupBox_DERList_Btn = QPushButton("Selecionar Elementos")
        self.VoltVar_GroupBox_DERList_Btn.clicked.connect(self.VV_ElementListConfig)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DERList_Label, 0, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DERList_Btn, 0, 1, 1, 2)
        # Configurar vvc_curve1
        self.VoltVar_GroupBox_VVCCurvex1_Label = QLabel("vvc_curve1")
        self.VoltVar_GroupBox_VVCCurvex1_Btn = QPushButton("Adicionar Curva XY")
        self.VoltVar_GroupBox_VVCCurvex1_Btn.clicked.connect(self.VV_XYCurveConfig)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VVCCurvex1_Label, 1, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VVCCurvex1_Btn, 1, 1, 1, 2)
        # Configurar EventLog
        self.VoltVar_GroupBox_EventLog_Label = QLabel("EventLog")
        self.VoltVar_GroupBox_EventLog_ComboBox = QComboBox()
        self.VoltVar_GroupBox_EventLog_ComboBox.addItems(["Yes", "No"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_EventLog_Label, 2, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_EventLog_ComboBox, 2, 1, 1, 2)
        # Configurar deltaQ_Factor
        self.VoltVar_GroupBox_DeltaQFactor_Label = QLabel("deltaQ_Factor (p.u.)")
        self.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox = QDoubleSpinBox()
        self.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setDecimals(2)
        self.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setRange(-1, 1)
        self.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setToolTip("Aceita valores entre -1,00 e 1,00")
        self.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DeltaQFactor_Label, 3, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_DeltaQFactor_DoubleSpinBox, 3, 1, 1, 2)
        # Configurar VarChangeTolerance (p.u.)
        self.VoltVar_GroupBox_VarChangeTolerance_Label = QLabel("VarChangeTolerance (p.u.)")
        self.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox = QDoubleSpinBox()
        self.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setDecimals(3)
        self.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setRange(-100, 100)
        self.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setToolTip("Aceita valores entre -100,000 e 100,000")
        self.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VarChangeTolerance_Label, 4, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VarChangeTolerance_DoubleSpinBox, 4, 1, 1, 2)
        # Configurar VoltageChangeTolerance (p.u.)
        self.VoltVar_GroupBox_VoltageChangeTolerance_Label = QLabel("VoltageChangeTolerance (p.u.)")
        self.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox = QDoubleSpinBox()
        self.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setDecimals(4)
        self.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setRange(-100, 100)
        self.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setToolTip("Aceita valores entre -100,0000 e 100,0000")
        self.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageChangeTolerance_Label, 5, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageChangeTolerance_DoubleSpinBox, 5, 1, 1, 2)
        # Configurar hysteresis_offset
        self.VoltVar_GroupBox_HysteresisOffSet_Label = QLabel("hysteresis_offset (p.u.)")
        self.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox = QDoubleSpinBox()
        self.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setDecimals(2)
        self.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setRange(-100, 100)
        self.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setToolTip("Aceita valores entre -100,00 e 100,00")
        self.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_HysteresisOffSet_Label, 6, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_HysteresisOffSet_DoubleSpinBox, 6, 1, 1, 2)
        # Configurar voltage_curvex_ref
        self.VoltVar_GroupBox_VoltageCurvexRef_Label = QLabel("voltage_curvex_ref")
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.addItems(["rated", "avg"])
        self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentIndexChanged.connect(
                                                        self.Enable_VoltageCurvexRef_SpinBox)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageCurvexRef_Label, 7, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox, 7, 1, 1, 2)
        # Configurar avgwindowlen
        self.VoltVar_GroupBox_AvgWindowLen_Label = QLabel("avgwindowlen")
        self.VoltVar_GroupBox_AvgWindowLen_SpinBox = QSpinBox()
        self.VoltVar_GroupBox_AvgWindowLen_SpinBox.setRange(0, 100)
        self.VoltVar_GroupBox_AvgWindowLen_SpinBox.setToolTip("Aceita valores entre 0 e 100")
        self.VoltVar_GroupBox_AvgWindowLen_SpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_AvgWindowLen_SpinBox.setEnabled(False)
        self.VoltVar_GroupBox_AvgWindowLen_ComboBox = QComboBox()
        self.VoltVar_GroupBox_AvgWindowLen_ComboBox.addItems(["s", "m", "h"])
        self.VoltVar_GroupBox_AvgWindowLen_ComboBox.setEnabled(False)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_Label, 8, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_SpinBox, 8, 1, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_AvgWindowLen_ComboBox, 8, 2, 1, 1)
        # Configurar RateofChangeMode
        self.VoltVar_GroupBox_RateofChangeMode_Label = QLabel("RateofChangeMode")
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox = QComboBox()
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox.addItems(["INACTIVE", "LPF", "RISEFALL"])
        self.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentIndexChanged.connect(
                                                        self.Enable_RateofChageMode_DoubleSpinBox)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RateofChangeMode_Label, 9, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RateofChangeMode_ComboBox, 9, 1, 1, 2)
        # Configurar LPFtau
        self.VoltVar_GroupBox_LPFtau_Label = QLabel("LPFtau (s)")
        self.VoltVar_GroupBox_LPFtau_DoubleSpinBox = QDoubleSpinBox()
        self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setDecimals(3)
        self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setRange(-100, 100)
        self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setToolTip("Aceita valores entre -100,000 e 100,000")
        self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_LPFtau_Label, 10, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_LPFtau_DoubleSpinBox, 10, 1, 1, 2)
        # Configurar RiseFallLimit
        self.VoltVar_GroupBox_RiseFallLimit_Label = QLabel("RiseFallLimit (p.u./s)")
        self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox = QDoubleSpinBox()
        self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setDecimals(3)
        self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setRange(-1, 100)
        self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setToolTip("Aceita valores entre -1,000 e 100,000")
        self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setButtonSymbols(2)
        self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RiseFallLimit_Label, 11, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox, 11, 1, 1, 2)
        # Configurar RefReactivePower
        self.VoltVar_GroupBox_RefReactivePower_Label = QLabel("RefReactivePower")
        self.VoltVar_GroupBox_RefReactivePower_ComboBox = QComboBox()
        self.VoltVar_GroupBox_RefReactivePower_ComboBox.addItems(["VARAVAL", "VARMAX"])
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RefReactivePower_Label, 12, 0, 1, 1)
        self.VoltVar_GroupBox_Layout.addWidget(self.VoltVar_GroupBox_RefReactivePower_ComboBox, 12, 1, 1, 2)

        ###################### GroupBox VOLTWATT #######################################################
        self.VoltWatt_GroupBox = QGroupBox("VOLTWATT")  # Criando a GroupBox InvConfig
        self.VoltWatt_GroupBox_Layout = QGridLayout()  # Layout da GroupBox do InvConfig é em Grid
        self.VoltWatt_GroupBox.setVisible(False)
        # Configurar DERList
        self.VoltWatt_GroupBox_DERList_Label = QLabel("DERList")
        self.VoltWatt_GroupBox_DERList_Btn = QPushButton("Selecionar Elementos")
        self.VoltWatt_GroupBox_DERList_Btn.clicked.connect(self.VW_ElementListConfig)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DERList_Label, 0, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DERList_Btn, 0, 1, 1, 2)
        # Configurar voltwatt_curve
        self.VoltWatt_GroupBox_VoltWattCurve_Label = QLabel("voltwatt_curve")
        self.VoltWatt_GroupBox_VoltWattCurve_Btn = QPushButton("Adicionar Curva XY")
        self.VoltWatt_GroupBox_VoltWattCurve_Btn.clicked.connect(self.VW_XYCurveConfig)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattCurve_Label, 1, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattCurve_Btn, 1, 1, 1, 2)
        # Configurar EventLog
        self.VoltWatt_GroupBox_EventLog_Label = QLabel("EventLog")
        self.VoltWatt_GroupBox_EventLog_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_EventLog_ComboBox.addItems(["Yes", "No"])
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_EventLog_Label, 2, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_EventLog_ComboBox, 2, 1, 1, 2)
        # Configurar deltaP_Factor
        self.VoltWatt_GroupBox_DeltaPFactor_Label = QLabel("deltaP_Factor (p.u.)")
        self.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox = QDoubleSpinBox()
        self.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setDecimals(2)
        self.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setRange(-1, 1)
        self.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setToolTip("Aceita valores entre -1,00 e 1,00")
        self.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox.setButtonSymbols(2)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DeltaPFactor_Label, 3, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_DeltaPFactor_DoubleSpinBox, 3, 1, 1, 2)
        # Configurar ActivePChangeTolerance
        self.VoltWatt_GroupBox_ActivePChangeTolerance_Label = QLabel("ActivePChangeTolerance (p.u.)")
        self.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox = QDoubleSpinBox()
        self.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setDecimals(2)
        self.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setRange(-100, 100)
        self.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setToolTip("Aceita valores entre -100,00 e 100,00")
        self.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox.setButtonSymbols(2)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_ActivePChangeTolerance_Label, 4, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_ActivePChangeTolerance_DoubleSpinBox, 4, 1, 1, 2)
        # Configurar voltage_curvex_ref
        self.VoltWatt_GroupBox_VoltageCurvexRef_Label = QLabel("voltage_curvex_ref")
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.addItems(["rated", "avg"])
        self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentIndexChanged.connect(
                                                                 self.Enable_VoltageCurvexRef_SpinBox)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltageCurvexRef_Label, 5, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox, 5, 1, 1, 2)
        # Configurar avgwindowlen
        self.VoltWatt_GroupBox_AvgWindowLen_Label = QLabel("avgwindowlen")
        self.VoltWatt_GroupBox_AvgWindowLen_SpinBox = QSpinBox()
        self.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setRange(0, 100)
        self.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setToolTip("Aceita valores entre 0 e 100")
        self.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setButtonSymbols(2)
        self.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setEnabled(False)
        self.VoltWatt_GroupBox_AvgWindowLen_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_AvgWindowLen_ComboBox.addItems(["s", "m", "h"])
        self.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setEnabled(False)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_AvgWindowLen_Label, 6, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_AvgWindowLen_SpinBox, 6, 1, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_AvgWindowLen_ComboBox, 6, 2, 1, 1)
        # Configurar RateofChangeMode
        self.VoltWatt_GroupBox_RateofChangeMode_Label = QLabel("RateofChangeMode")
        self.VoltWatt_GroupBox_RateofChangeMode_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.addItems(["INACTIVE", "LPF", "RISEFALL"])
        self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentIndexChanged.connect(
                                                            self.Enable_RateofChageMode_DoubleSpinBox)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RateofChangeMode_Label, 7, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RateofChangeMode_ComboBox, 7, 1, 1, 2)
        # Configurar LPFtau
        self.VoltWatt_GroupBox_LPFtau_Label = QLabel("LPFtau (s)")
        self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox = QDoubleSpinBox()
        self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setDecimals(3)
        self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setRange(-100, 100)
        self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setToolTip("Aceita valores entre -100,000 e 100,000")
        self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setButtonSymbols(2)
        self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_LPFtau_Label,8, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox, 8, 1, 1, 2)
        # Configurar RiseFallLimit
        self.VoltWatt_GroupBox_RiseFallLimit_Label = QLabel("RiseFallLimit (p.u./s)")
        self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox = QDoubleSpinBox()
        self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setDecimals(3)
        self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setRange(-1, 100)
        self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setToolTip("Aceita valores entre -1,000 e 100,000")
        self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setButtonSymbols(2)
        self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RiseFallLimit_Label, 9, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox, 9, 1, 1, 2)
        # Configurar VoltwattYAxis
        self.VoltWatt_GroupBox_VoltWattYAxis_Label = QLabel("VoltwattYAxis")
        self.VoltWatt_GroupBox_VoltWattYAxis_ComboBox = QComboBox()
        self.VoltWatt_GroupBox_VoltWattYAxis_ComboBox.addItems(["PMPPPU", "PAVAILABLEPU", "PCTPMPPPU", "KVARATINGPU"])
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattYAxis_Label, 10, 0, 1, 1)
        self.VoltWatt_GroupBox_Layout.addWidget(self.VoltWatt_GroupBox_VoltWattYAxis_ComboBox, 10, 1, 1, 2)

        ##################################################################################################

        self.Tab_layout = QGridLayout()

        self.NameEMode_GroupBox.setLayout(self.NameEMode_GroupBox_Layout)
        self.Tab_layout.addWidget(self.NameEMode_GroupBox, 0, 1, 1, 1)

        self.VoltVar_GroupBox.setLayout(self.VoltVar_GroupBox_Layout)
        self.Tab_layout.addWidget(self.VoltVar_GroupBox, 1, 1, 1, 1)

        self.VoltWatt_GroupBox.setLayout(self.VoltWatt_GroupBox_Layout)
        self.Tab_layout.addWidget(self.VoltWatt_GroupBox, 1, 1, 1, 1)

        self.setLayout(self.Tab_layout)

    def setDisabled_Mode_GroupBox(self):

        if self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            self.VoltVar_GroupBox.setVisible(True)
            self.VoltWatt_GroupBox.setVisible(False)
        else:
            self.VoltVar_GroupBox.setVisible(False)
            self.VoltWatt_GroupBox.setVisible(True)

    def Enable_VoltageCurvexRef_SpinBox(self):
        if self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            if self.VoltVar_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                self.VoltVar_GroupBox_AvgWindowLen_SpinBox.setEnabled(True)
                self.VoltVar_GroupBox_AvgWindowLen_ComboBox.setEnabled(True)
            else:
                self.VoltVar_GroupBox_AvgWindowLen_SpinBox.setEnabled(False)
                self.VoltVar_GroupBox_AvgWindowLen_ComboBox.setEnabled(False)
        else:
            if self.VoltWatt_GroupBox_VoltageCurvexRef_ComboBox.currentText() == "avg":
                self.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setEnabled(True)
                self.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setEnabled(True)
            else:
                self.VoltWatt_GroupBox_AvgWindowLen_SpinBox.setEnabled(False)
                self.VoltWatt_GroupBox_AvgWindowLen_ComboBox.setEnabled(False)

    def Enable_RateofChageMode_DoubleSpinBox(self):
        if self.NameEMode_GroupBox_Mode_ComboBox.currentText() == "VOLTVAR":
            if self.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setEnabled(True)
                self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
            elif self.VoltVar_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(True)
                self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)
            else:
                self.VoltVar_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
                self.VoltVar_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)
        else:
            if self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "LPF":
                self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setEnabled(True)
                self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
            elif self.VoltWatt_GroupBox_RateofChangeMode_ComboBox.currentText() == "RISEFALL":
                self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(True)
                self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)
            else:
                self.VoltWatt_GroupBox_RiseFallLimit_DoubleSpinBox.setEnabled(False)
                self.VoltWatt_GroupBox_LPFtau_DoubleSpinBox.setEnabled(False)

    def VV_XYCurveConfig(self):
        self.VV_XYCurve.show()

    def VW_XYCurveConfig(self):
        self.VW_XYCurve.show()

    def VV_ElementListConfig(self):
        self.VV_ElementList.clear()
        self.VV_ElementList.update()
        self.VV_ElementList.show()

    def VW_ElementListConfig(self):
        self.VW_ElementList.clear()
        self.VW_ElementList.update()
        self.VW_ElementList.show()

class InvControl_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, mode, element):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(InvControl_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Unchecked)
        ## Column 1 - Modo:
        self.setText(1, mode)
        ## Column 2 - Elementos PC:
        self.setText(2, element)