from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, \
    QPushButton, QMessageBox, QLabel, QLineEdit, QComboBox, QHBoxLayout, QDoubleSpinBox
from PyQt5.QtCore import Qt

import opendss.class_opendss
import opendss.storage.class_select_dispatch_curve
import opendss.storage.class_select_price_curve
import opendss.storage.class_config_storagecontroller
import config as cfg
import unidecode

class C_ActPow_LoadShape_DispMode_Dialog(QDialog): ## Classe Dialog Despacho LoadShape da Potencia Ativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho LoadShape da Potência Ativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.Select_DispCurve = opendss.storage.class_select_dispatch_curve.C_Config_DispCurve_Dialog()

        self.StorageControllersTemporario = []

        self._NumComboBox = 0
        self._StorageConfig_GroupBox_Nome_LineEdit = 0
        self._StorageConfig_GroupBox_PercentageReserve_LineEdit = 0
        self._StorageVersion_GroupBox_Storage1_RadioBtn = 0

        self.InitUI()

    @property
    def NumComboBox(self):
        return self._NumComboBox

    @NumComboBox.setter
    def NumComboBox(self, value):
        self._NumComboBox = value

    @property
    def StorageConfig_GroupBox_Nome_LineEdit(self):
        return self._StorageConfig_GroupBox_Nome_LineEdit

    @StorageConfig_GroupBox_Nome_LineEdit.setter
    def StorageConfig_GroupBox_Nome_LineEdit(self, value):
        self._StorageConfig_GroupBox_Nome_LineEdit = value

    @property
    def StorageConfig_GroupBox_PercentageReserve_LineEdit(self):
        return self._StorageConfig_GroupBox_PercentageReserve_LineEdit

    @StorageConfig_GroupBox_PercentageReserve_LineEdit.setter
    def StorageConfig_GroupBox_PercentageReserve_LineEdit(self, value):
        self._StorageConfig_GroupBox_PercentageReserve_LineEdit = value

    @property
    def StorageVersion_GroupBox_Storage1_RadioBtn(self):
        return self._StorageVersion_GroupBox_Storage1_RadioBtn

    @StorageVersion_GroupBox_Storage1_RadioBtn.setter
    def StorageVersion_GroupBox_Storage1_RadioBtn(self, value):
        self._StorageVersion_GroupBox_Storage1_RadioBtn = value

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)  # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()
        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog


        ## GroupBox Seleção do Storage Controller
        self.StorControl_GroupBox_Selection = QGroupBox("Storage Controllers")
        self.StorControl_GroupBox_Selection_Label = QLabel("Selecione um dos Storage Controllers Existentes")
        self.StorControl_GroupBox_Selection_ComboBox = QComboBox()

        # Layout do GroupBox Seleção do Storage Controller
        self.StorControl_GroupBox_Selection_Layout = QGridLayout()
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Label, 0, 0, 1, 3)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_ComboBox, 1, 0, 1, 3)
        self.StorControl_GroupBox_Selection.setLayout(self.StorControl_GroupBox_Selection_Layout)

        self.Dialog_Layout.addWidget(self.StorControl_GroupBox_Selection)

        ##### Btns
        self.StorControl_GroupBox_Selection_Remover_Btn = QPushButton("Remover")
        self.StorControl_GroupBox_Selection_Remover_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.StorControl_GroupBox_Selection_Remover_Btn.clicked.connect(self.removeStorControl)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Remover_Btn, 2, 0, 1, 1)

        self.StorControl_GroupBox_Selection_Edit_Btn = QPushButton("Editar")
        self.StorControl_GroupBox_Selection_Edit_Btn.setIcon(QIcon('img/icon_edit.png'))
        self.StorControl_GroupBox_Selection_Edit_Btn.clicked.connect(self.editStorControl)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Edit_Btn, 2, 1, 1, 1)

        self.StorControl_GroupBox_Selection_Adicionar_Btn = QPushButton("Adicionar")
        self.StorControl_GroupBox_Selection_Adicionar_Btn.setIcon(QIcon('img/icon_add.png'))
        self.StorControl_GroupBox_Selection_Adicionar_Btn.clicked.connect(self.addStorControl)
        self.StorControl_GroupBox_Selection_Layout.addWidget(self.StorControl_GroupBox_Selection_Adicionar_Btn, 2, 2, 1, 1)

        self.StorControl_GroupBox = QGroupBox("Configurações Gerais do Storage Controller")
        self.StorControl_GroupBox.setVisible(False)
        ## GroupBox opções
        ### Labels
        self.StorControl_Name_Label = QLabel("Nome:")
        self.StorControl_Element_Label = QLabel("Elemento:")
        self.StorControl_Terminal_Label = QLabel("Terminal:")
        self.StorControl_Reserve_Label = QLabel("Energia reserva:")
        self.StorControl_DispFactor_Label = QLabel("Dispatch Factor")

        ### LineEdits
        self.StorControl_Name = QLineEdit()
        self.StorControl_Reserve = QLineEdit()

        ### Comboboxs
        self.StorControl_Element_ComboBox = QComboBox()
        self.StorControl_Element_ComboBox.clear()
        self.StorControl_Terminal_ComboBox = QComboBox()
        self.StorControl_Terminal_ComboBox.addItems(["1", "2"])

        ### SpinBox
        self.StorControl_DispFactor_SpinBox = QDoubleSpinBox()
        self.StorControl_DispFactor_SpinBox.setValue(1.0)
        self.StorControl_DispFactor_SpinBox.setRange(0.0, 1.0)
        self.StorControl_DispFactor_SpinBox.setDecimals(1)
        self.StorControl_DispFactor_SpinBox.setSingleStep(0.1)

        ### Layout
        self.StorControl_Layout = QGridLayout()
        self.StorControl_Layout.addWidget(self.StorControl_Name_Label, 0, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Element_Label, 1, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Terminal_Label, 2, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Reserve_Label, 3, 0, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_DispFactor_Label, 4, 0, 1, 1)

        self.StorControl_Layout.addWidget(self.StorControl_Name, 0, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Element_ComboBox, 1, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Terminal_ComboBox, 2, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_Reserve, 3, 1, 1, 1)
        self.StorControl_Layout.addWidget(self.StorControl_DispFactor_SpinBox, 4, 1, 1, 1)

        ###### Botões dos Parâmetros
        self.StorControl_Btns_Layout = QHBoxLayout()
        self.StorControl_Btns_Layout.setAlignment(Qt.AlignRight)

        self.StorControl_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.StorControl_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.StorControl_Btns_Cancel_Btn.clicked.connect(self.CancelAddEdit)
        self.StorControl_Btns_Layout.addWidget(self.StorControl_Btns_Cancel_Btn)

        self.StorControl_Btns_Ok_Btn = QPushButton("OK")
        self.StorControl_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.StorControl_Btns_Ok_Btn.clicked.connect(self.AcceptAddEditStorControl)
        self.StorControl_Btns_Layout.addWidget(self.StorControl_Btns_Ok_Btn)
        self.StorControl_Layout.addItem(self.StorControl_Btns_Layout, 5, 0, 1, 2)
        ####

        self.StorControl_GroupBox.setLayout(self.StorControl_Layout)

        self.Dialog_Layout.addWidget(self.StorControl_GroupBox)

        ##############################################################################################

        ###### Botão Dialog para configurar a curva de despacho
        self.DispCurve_Btn_Layout = QHBoxLayout()
        self.DispCurve_Btn = QPushButton("Configurar curva de despacho")
        self.DispCurve_Btn.clicked.connect(self.selectDispCurve)
        self.DispCurve_Btn_Layout.addWidget(self.DispCurve_Btn)

        self.Dialog_Layout.addLayout(self.DispCurve_Btn_Layout)

        ###### Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dialog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dialog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dialog_Btns_Cancel_Btn.clicked.connect(self.cancelStorageControlSelection)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Cancel_Btn)

        self.Dialog_Btns_Ok_Btn = QPushButton("OK")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.acceptStorageControlSelection)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout)

        self.setLayout(self.Dialog_Layout)

    def getStorage_Name(self):
        return unidecode.unidecode(self.StorageConfig_GroupBox_Nome_LineEdit.text().replace(" ", "_"))

    def get_StorControl_Version(self):
        if self.StorageVersion_GroupBox_Storage1_RadioBtn.isChecked():
            return 1
        else:
            return 2

    def getStorage_PercentageReserve(self):
        return self.StorageConfig_GroupBox_PercentageReserve_LineEdit.text()

    def get_StorControl_Name(self):
        return unidecode.unidecode(self.StorControl_Name.text().replace(" ", "_"))

    def get_ElementStorControl(self):
        return self.StorControl_Element_ComboBox.currentText()

    def get_TerminalStorControl(self):
        return self.StorControl_Terminal_ComboBox.currentText()

    def get_ReserveStorControl(self):
        return self.StorControl_Reserve.text()

    def get_DispFactor(self):
        return self.StorControl_DispFactor_SpinBox.value()

    def clearStorControlParameters(self):
        self.StorControl_Name.setText("")
        self.StorControl_Element_ComboBox.setCurrentIndex(0)
        self.StorControl_Terminal_ComboBox.setCurrentIndex(0)
        self.StorControl_Reserve.setText(self.getStorage_PercentageReserve())
        self.StorControl_DispFactor_SpinBox.setValue(1.0)

    def addStorControl(self):
        if self.StorControl_GroupBox_Selection_ComboBox.count() + 1 - self.NumComboBox <= 1: # Para garantir que só adicione um controlador por Storage
            self.clearStorControlParameters()
            self.StorControl_Name.setEnabled(True)
            self.EnableDisableParameters(True)
        else:
            QMessageBox(QMessageBox.Warning, "Storage Controller",
                        "Só é possível adicionar um Storage Controller por Storage.\nEdite ou remova algum dos existentes!",
                        QMessageBox.Ok).exec()

    def editStorControl(self):
        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            self.clearStorControlParameters()
            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                    self.StorControl_Name.setText(ctd["StorageControllerName"])
                    self.StorControl_Element_ComboBox.setCurrentText(ctd["Element"])
                    self.StorControl_Terminal_ComboBox.setCurrentText(ctd["Terminal"])
                    self.StorControl_Reserve.setText(ctd["Reserve"])
                    self.StorControl_DispFactor_SpinBox.setValue(ctd["DispFactor"])
            self.StorControl_Name.setEnabled(False)
            self.EnableDisableParameters(True)

    def CancelAddEdit(self):
        self.clearStorControlParameters()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def EnableDisableParameters(self, bool):
        if bool:
            self.StorControl_GroupBox.setVisible(True)
            self.StorControl_GroupBox_Selection.setEnabled(False)
            self.Dialog_Btns_Ok_Btn.setEnabled(False)
            self.Dialog_Btns_Cancel_Btn.setEnabled(False)
            self.DispCurve_Btn.setEnabled(False)
        else:
            self.StorControl_GroupBox.setVisible(False)
            self.StorControl_GroupBox_Selection.setEnabled(True)
            self.Dialog_Btns_Ok_Btn.setEnabled(True)
            self.Dialog_Btns_Cancel_Btn.setEnabled(True)
            self.DispCurve_Btn.setEnabled(True)

    def removeStorControl(self):
        for ctd in self.StorageControllersTemporario:
            if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                self.StorageControllersTemporario.remove(ctd)
                QMessageBox(QMessageBox.Warning, "Storage Controller",
                            "Storage Controller " + ctd["StorageControllerName"] + " removido com sucesso!",
                            QMessageBox.Ok).exec()
        self.updateDialog()

    def AcceptAddEditStorControl(self):
        StorageController = {}
        StorageController["StorageControllerName"] = self.get_StorControl_Name()
        StorageController["StorageControllerVersion"] = self.get_StorControl_Version()
        StorageController["ElementList"] = []
        StorageController["Element"] = self.get_ElementStorControl()
        StorageController["Terminal"] = self.get_TerminalStorControl()
        StorageController["Reserve"] = self.get_ReserveStorControl()
        StorageController["DispFactor"] = self.get_DispFactor()
        StorageController["DispatchMode"] = "LoadShape"

        if self.StorControl_Name.isEnabled():
            ctdExist = False
            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == StorageController["StorageControllerName"]:
                    ctdExist = True
            if not ctdExist:
                self.StorageControllersTemporario.append(StorageController)
                QMessageBox(QMessageBox.Information, "Storage Controller",
                            "Storage Controller " + StorageController["StorageControllerName"] + " inserido com sucesso!",
                            QMessageBox.Ok).exec()
            else:
                QMessageBox(QMessageBox.Warning, "Storage Controller",
                            "Storage Controller" + StorageController["StorageControllerName"] + " já existe! \nFavor verificar!",
                            QMessageBox.Ok).exec()
        else:
            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == StorageController["StorageControllerName"]:
                    ctd["Element"] = StorageController["Element"]
                    ctd["Terminal"] = StorageController["Terminal"]
                    ctd["Reserve"] = StorageController["Reserve"]
                    ctd["DispFactor"] = StorageController["DispFactor"]
                    QMessageBox(QMessageBox.Information, "Storage Controller",
                                "Storage Controller" + ctd["StorageControllerName"] + " atualizado com sucesso!",
                                QMessageBox.Ok).exec()

        self.updateDialog()
        self.EnableDisableParameters(False)
        self.adjustSize()

    def acceptStorageControlSelection(self):
        DispatchCurveOK = False

        if self.StorControl_GroupBox_Selection_ComboBox.currentText() == "":
            QMessageBox(QMessageBox.Warning, "Storage Controller", "Pelo menos um Storage Controller deve ser selecionado!",
                        QMessageBox.Ok).exec()
        else:
            if self.Select_DispCurve.dataDispCurve == {}:
                QMessageBox(QMessageBox.Warning, "Storage Controller", "Selecione uma curva de despacho!", QMessageBox.Ok).exec()
            else:
                DispatchCurveOK = True
                for ctd in self.StorageControllersTemporario:
                    if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                        ctd.update(self.Select_DispCurve.dataDispCurve)

        if DispatchCurveOK:
            for ctd in self.StorageControllersTemporario: # Garante que dois StorageController não controlem um mesmo Storage
                if self.getStorage_Name() in ctd["ElementList"] and (not ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText()):
                    self.StorageControllersTemporario.remove(ctd)

            for ctd in self.StorageControllersTemporario:
                if ctd["StorageControllerName"] == self.StorControl_GroupBox_Selection_ComboBox.currentText():
                    ctd["ElementList"].append(self.getStorage_Name())

            for ctd in self.StorageControllersTemporario: # Garante que nao haja StorController que não controle nenhum Storage
                if not ctd["ElementList"]:
                    self.StorageControllersTemporario.remove(ctd)

            self.close()

    def cancelStorageControlSelection(self):
        self.close()

    def updateDialog(self):
        self.StorControl_GroupBox_Selection_ComboBox.clear()
        if not self.StorageControllersTemporario == []:
            for ctd in self.StorageControllersTemporario:
                if "DispatchMode" in ctd and ctd["StorageControllerVersion"] == self.get_StorControl_Version():
                    self.StorControl_GroupBox_Selection_ComboBox.addItem(ctd["StorageControllerName"])

        self.StorControl_Element_ComboBox.clear()
        self.StorControl_Element_ComboBox.addItems(self.OpenDSS.getElementList())

    def selectDispCurve(self):
        self.Select_DispCurve.show()
