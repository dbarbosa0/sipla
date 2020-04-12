from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QPlainTextEdit, QWidget, QLineEdit, QPushButton




class C_Insert_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS Insert"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(500, 200)

        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ###### Tabs
        self.TabWidget = QTabWidget()
        self.TabEnergyMeter = EnergyMeter()  # QWidget
        self.TabMonitor = Monitor()  # QWidget
        self.TabWidget.addTab(self.TabEnergyMeter, QIcon('img/icon_opendss_energymeter.png'), "Medidor")
        self.TabWidget.addTab(self.TabMonitor, QIcon('img/icon_opendss_monitor.png'), "Monitor")
        self.Dialog_Layout.addWidget(self.TabWidget)

        self.setLayout(self.Dialog_Layout)

class EnergyMeter(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIEnergyMeter()

    def InitUIEnergyMeter(self):

        ## GroupBox Inserir Medidores
        self.EnergyMeter_GroupBox = QGroupBox("Medidores de Energia ")
        self.EnergyMeter_GroupBox_Label = QLabel("Medidores instalados")
        self.EnergyMeter_GroupBox_ComboBox = QComboBox()
        self.EnergyMeter_GroupBox_Novo_Pushbutton = QPushButton("Novo")
        self.EnergyMeter_GroupBox_Novo_Pushbutton.clicked.connect(self.exec_Meters_OpenDSS)

        # Layout do GroupoBox
        self.EnergyMeter_GroupBox_Layout = QGridLayout()
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_Label, 0, 0, 1, 1)
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_ComboBox, 0, 1, 1, 1)
        self.EnergyMeter_GroupBox_Layout.addWidget(self.EnergyMeter_GroupBox_Novo_Pushbutton, 0, 2, 1, 1)

        # Layout do GroupoBox
        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.EnergyMeter_GroupBox)


        self.EnergyMeter_GroupBox.setLayout(self.EnergyMeter_GroupBox_Layout)


        self.setLayout(self.Tab_layout)


    def exec_Meters_OpenDSS(self):
        self.NewEnergyMetr_Dialog = NewEnergyMeter_Dialog()
        self.NewEnergyMetr_Dialog.show()

class NewEnergyMeter_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.titleWindow = "New EnergyMeter"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"
        self.InitUI()
    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(500, 500)

        self.NewEnergyMeter_Layout = QVBoxLayout() #Layout da Dialog

        ###### Tabs
        self.NewMeterTabWidget = QTabWidget()
        self.TabEnergyMeter = NewEnergyMeter()
        self.NewMeterTabWidget.addTab(self.TabEnergyMeter, QIcon('img/icon_opendss_energymeter.png'), "Novo Medidor")
        self.NewEnergyMeter_Layout.addWidget(self.NewMeterTabWidget)
        self.setLayout(self.NewEnergyMeter_Layout)

class NewEnergyMeter(QWidget):
    def __init__(self):
        super().__init__()


        self.InitUINewEnergyMeter()

    def InitUINewEnergyMeter(self):
        self.Insert_EnergyMeter_GroupBox = QGroupBox(" Novo Medidor")
        self.Insert_EnergyMeter_GroupBox_Name_Label = QLabel("Nome:")
        self.Insert_EnergyMeter_GroupBox_Element_Label = QLabel("Elemento:")
        self.Insert_EnergyMeter_GroupBox_Terminal_Label = QLabel("Terminal:")

        self.Insert_EnergyMeter_GroupBox_Name_LineEdit = QLineEdit()
        self.Insert_EnergyMeter_GroupBox_Element_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox = QComboBox()
        self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox.addItems(["1","2"])

        self.Insert_EnergyMeter_GroupBox_Layout = QGridLayout()
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Name_Label, 0, 0, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Element_Label, 1, 0, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Terminal_Label, 2, 0, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Name_LineEdit, 0, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Element_ComboBox, 1, 1, 1, 1)
        self.Insert_EnergyMeter_GroupBox_Layout.addWidget(self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox, 2, 1, 1, 1)


        self.Tab_layout = QVBoxLayout()
        self.Tab_layout.addWidget(self.Insert_EnergyMeter_GroupBox)
        self.Insert_EnergyMeter_GroupBox.setLayout(self.Insert_EnergyMeter_GroupBox_Layout)

        self.setLayout(self.Tab_layout)



    # Métodos Set Variáveis

    def get_NameEnergyMeter(self):
        self.NameEnergyMeter = self.Insert_EnergyMeter_GroupBox_Name_LineEdit.text()
        return self.NameEnergyMeter

    def get_ElementEnergyMeter(self):
        self.ElementEnergyMeter = self.Insert_EnergyMeter_GroupBox_Element_ComboBox.currentText()
        return self.ElementEnergyMeter

    def get_TerminalEnergyMeter(self):
        self.TerminalEnergyMeter = self.Insert_EnergyMeter_GroupBox_Terminal_ComboBox.currentText()
        return self.TerminalEnergyMeter






class Monitor(QWidget):
    def __init__(self):
        super().__init__()

        self.InitUIMonitor()

    def InitUIMonitor(self):

        ## GroupBox Inserir Monitores
        self.Monitor_GroupBox = QGroupBox("Monitores")