from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QFormLayout, QGroupBox, \
    QPushButton, QVBoxLayout, QTabWidget, QLabel, QComboBox, QLineEdit, \
    QDialogButtonBox


class C_OpenDSS_ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(C_OpenDSS_ConfigDialog, self).__init__(parent)

        self.titleWindow = "OpenDSS Settings"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"

    #        self.InitUI()

    def InitUI(self):
        self.WindowOpenDSS = QDialog()
        self.WindowOpenDSS.setWindowTitle(self.titleWindow)
        self.WindowOpenDSS.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.WindowOpenDSS.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.WindowOpenDSS.resize(500, 500)

        self.TabLoadFlow = LoadFlow()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.TabLoadFlow.Accept)
        self.buttonBox.rejected.connect(self.WindowOpenDSS.reject)

        self.Tabwidget = QTabWidget()
        self.Tabwidget.addTab(self.TabLoadFlow, "Simulação")

        self.Tabwidget_VboxLayout = QVBoxLayout()
        self.Tabwidget_VboxLayout.addWidget(self.Tabwidget)
        self.Tabwidget_VboxLayout.addWidget(self.buttonBox)

        self.WindowOpenDSS.setLayout(self.Tabwidget_VboxLayout)

        self.WindowOpenDSS.exec_()


class LoadFlow(C_OpenDSS_ConfigDialog):
    def __init__(self):
        super(LoadFlow, self).__init__()

        self.listmode = ["Snapshot", "Daily"]  # lista de modos disponíveis
        self.InitUI_LoadFlow()

    def InitUI_LoadFlow(self):
        ## GroupBox Fluxo de Carga
        self.LoadFlow_simulation_GroupBox_fluxo = QGroupBox("Fluxo de Carga")
        self.LoadFlow_simulation_GroupBox_fluxo_Label = QLabel("Set VoltageBases")
        self.LoadFlow_simulation_GroupBox_fluxo_LineEdit = QLineEdit()

        # Layout do GroupoBox Fluxo de Carga
        self.LoadFlow_simulation_GroupBox_fluxo_Layout = QGridLayout()
        self.LoadFlow_simulation_GroupBox_fluxo_Layout.addWidget(self.LoadFlow_simulation_GroupBox_fluxo_Label, 0, 0, 1,
                                                                 1)
        self.LoadFlow_simulation_GroupBox_fluxo_Layout.addWidget(self.LoadFlow_simulation_GroupBox_fluxo_LineEdit, 0, 1,
                                                                 1, 1)

        ## GroupBox Modo
        self.LoadFlow_simulation_GroupBox_mode = QGroupBox("Modo")

        self.LoadFlow_simulation_GroupBox_mode_Label = QLabel("Set Mode")
        self.LoadFlow_simulation_GroupBox_mode_ComboBox = QComboBox()
        self.LoadFlow_simulation_GroupBox_mode_ComboBox.addItems(self.listmode)
        self.LoadFlow_simulation_GroupBox_mode_ComboBox.currentIndexChanged.connect(
            self.setDisabled_LoadFlow_simulation_GroupBox_Complementos)
        self.LoadFlow_simulation_GroupBox_mode_QPushButton = QPushButton("Ok")
        self.LoadFlow_simulation_GroupBox_mode_QPushButton.setFixedWidth(30)
        self.LoadFlow_simulation_GroupBox_mode_QPushButton.clicked.connect(
            self.setDisabled_LoadFlow_simulation_GroupBox_Complementos)

        # Layout do GroupoBox modo
        self.LoadFlow_simulation_GroupBox_mode_Layout = QGridLayout()
        self.LoadFlow_simulation_GroupBox_mode_Layout.addWidget(self.LoadFlow_simulation_GroupBox_mode_Label, 1, 1, 1,
                                                                1)
        self.LoadFlow_simulation_GroupBox_mode_Layout.addWidget(self.LoadFlow_simulation_GroupBox_mode_ComboBox, 1, 2,
                                                                1, 1)
        self.LoadFlow_simulation_GroupBox_mode_Layout.addWidget(self.LoadFlow_simulation_GroupBox_mode_QPushButton, 1,
                                                                3, 1, 1)

        ## GroupBox complementos
        self.LoadFlow_simulation_GroupBox_Complementos = QGroupBox("Complementos")
        self.LoadFlow_simulation_GroupBox_Complementos_stepsize_Label = QLabel("Set Stepsize:")
        self.LoadFlow_simulation_GroupBox_Complementos_number_Label = QLabel("Set Number:")
        self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_Label = QLabel("Set Maxiterations:")
        self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_Label = QLabel("Set Maxcontroliter:")

        ## LineEdit complementos

        self.LoadFlow_simulation_GroupBox_Complementos_stepsize_LineEdit = QLineEdit()
        self.LoadFlow_simulation_GroupBox_Complementos_number_LineEdit = QLineEdit()
        self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_LineEdit = QLineEdit()
        self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_LineEdit = QLineEdit()

        self.LoadFlow_simulation_GroupBox_Complementos_stepsize_LineEdit.setEnabled(False)
        self.LoadFlow_simulation_GroupBox_Complementos_number_LineEdit.setEnabled(False)
        self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_LineEdit.setEnabled(False)
        self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_LineEdit.setEnabled(False)

        # Layout do GroupoBox complementos
        self.LoadFlow_simulation_GroupBox_Complementos_Layout = QGridLayout()
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_stepsize_Label, 0, 0, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_number_Label, 1, 0, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_stepsize_LineEdit, 0, 1, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_number_LineEdit, 1, 1, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_Label, 2, 0, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_Label, 3, 0, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_LineEdit, 2, 1, 1, 1)
        self.LoadFlow_simulation_GroupBox_Complementos_Layout.addWidget(
            self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_LineEdit, 3, 1, 1, 1)

        # Seta layouts

        self.LoadFlow_simulation_GroupBox_fluxo.setLayout(self.LoadFlow_simulation_GroupBox_fluxo_Layout)
        self.LoadFlow_simulation_GroupBox_mode.setLayout(self.LoadFlow_simulation_GroupBox_mode_Layout)
        self.LoadFlow_simulation_GroupBox_Complementos.setLayout(self.LoadFlow_simulation_GroupBox_Complementos_Layout)

        ## Layout da TAB1
        self.LoadFlow_first_layout = QFormLayout()
        self.LoadFlow_first_layout.addWidget(self.LoadFlow_simulation_GroupBox_fluxo)
        self.LoadFlow_first_layout.addWidget(self.LoadFlow_simulation_GroupBox_mode)
        self.LoadFlow_first_layout.addWidget(self.LoadFlow_simulation_GroupBox_Complementos)

        self.setLayout(self.LoadFlow_first_layout)

    def setDisabled_LoadFlow_simulation_GroupBox_Complementos(self):

        if self.LoadFlow_simulation_GroupBox_mode_ComboBox.currentText() == "Daily":

            self.LoadFlow_simulation_GroupBox_Complementos_stepsize_LineEdit.setEnabled(True)
            self.LoadFlow_simulation_GroupBox_Complementos_number_LineEdit.setEnabled(True)
            self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_LineEdit.setEnabled(True)
            self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_LineEdit.setEnabled(True)
        else:
            self.LoadFlow_simulation_GroupBox_Complementos_stepsize_LineEdit.setEnabled(False)
            self.LoadFlow_simulation_GroupBox_Complementos_number_LineEdit.setEnabled(False)
            self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_LineEdit.setEnabled(False)

            self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_LineEdit.setEnabled(False)

    # Métodos Set Variáveis

    def get_VoltageBases(self):
        self.VoltageBases = self.LoadFlow_simulation_GroupBox_fluxo_LineEdit.text()
        return self.VoltageBases

    def get_Mode(self):
        self.mode = self.LoadFlow_simulation_GroupBox_mode_ComboBox.currentText()
        return self.mode

    def get_Stepsize(self):
        self.stepsize = self.LoadFlow_simulation_GroupBox_Complementos_stepsize_LineEdit.text()
        return self.stepsize

    def get_Number(self):
        self.Number = self.LoadFlow_simulation_GroupBox_Complementos_number_LineEdit.text()
        return self.Number

    def get_Maxiterations(self):
        self.Maxiterations = self.LoadFlow_simulation_GroupBox_Complementos_maxiterations_LineEdit.text()
        return self.Maxiterations

    def get_Maxcontroliter(self):
        self.Maxcontroliter = self.LoadFlow_simulation_GroupBox_Complementos_Maxcontroliter_LineEdit.text()
        return self.Maxcontroliter

    def Accept(self):
        print("Gets Ativados")
        self.get_VoltageBases()
        self.get_Mode()
        self.get_Stepsize()
        self.get_Number()
        self.get_Maxiterations()
        self.get_Maxcontroliter()



