# Carvalho Tag
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog,QHBoxLayout, QPushButton, QVBoxLayout, QTabWidget
from PyQt5.QtCore import Qt

import protect.class_recloser
import protect.class_fuse
import protect.class_relay
import protect.class_swtcontrol
import config as cfg


class C_Devices_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Dispositivos de proteção"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.editedDevices = []
        self.addedDevices = []
        self.ImportedCurvesMain = []
        # self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.resize(300, 200)

        self.Dialog_Layout = QVBoxLayout()  # Layout da Dialog

        self.TabWidget = QTabWidget()
        self.TabRecloser = protect.class_recloser.Recloser()
        self.TabFuse = protect.class_fuse.Fuse()
        self.TabRelay = protect.class_relay.Relay()
        self.TabSwtControl = protect.class_swtcontrol.SwtControl()

        self.TabWidget.addTab(self.TabRecloser, "Religador")
        self.TabWidget.addTab(self.TabFuse, "Fusível")
        self.TabWidget.addTab(self.TabRelay, "Relé")
        self.TabWidget.addTab(self.TabSwtControl, "Switch Control")
        self.Dialog_Layout.addWidget(self.TabWidget)

        #  Botões
        self.Dialog_Btns_Layout = QHBoxLayout()
        self.Dialog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dialog_Btns_Ok_Btn = QPushButton("Ok")
        self.Dialog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dialog_Btns_Ok_Btn.setMinimumWidth(80)
        self.Dialog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dialog_Btns_Layout.addWidget(self.Dialog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dialog_Btns_Layout, 0)

        self.setLayout(self.Dialog_Layout)

    def Accept(self):
        self.gen_devices()
        self.exec_Devices()
        self.close()

        self.updateImportedCurves()

    def updateMainProtectDialog(self):
        self.TabFuse.updateProtectDialog()
        self.TabRecloser.updateProtectDialog()
        self.TabRelay.updateProtectDialog()
        self.TabSwtControl.updateProtectDialog()

    def updateImportedCurves(self):
        for curvestring in self.TabRecloser.Edit_Recloser.ImportedCurves:
            if curvestring not in self.ImportedCurvesMain:
                self.ImportedCurvesMain.append(curvestring)

        for curvestring in self.TabFuse.Edit_Fuse.ImportedCurves:
            if curvestring not in self.ImportedCurvesMain:
                self.ImportedCurvesMain.append(curvestring)

        for curvestring in self.TabRelay.Edit_Relay.ImportedCurves:
            if curvestring not in self.ImportedCurvesMain:
                self.ImportedCurvesMain.append(curvestring)

        print(self.ImportedCurvesMain)

    def gen_devices(self):
        self.addedDevices = []
        self.editedDevices = []
        for item in self.TabRecloser.RecloserDataInfo:
            if item in self.TabRecloser.AddRecloserDataInfo:
                self.addedDevices.append(item)
            else:
                self.editedDevices.append(item)
        
        for item in self.TabFuse.FuseDataInfo:
            if item in self.TabFuse.AddFuseDataInfo:
                self.addedDevices.append(item)
            else:
                self.editedDevices.append(item)
        
        for item in self.TabRelay.RelayDataInfo:
            if item in self.TabRelay.AddRelayDataInfo:
                self.addedDevices.append(item)
            else:
                self.editedDevices.append(item)
        
        for item in self.TabSwtControl.SwtControlDataInfo:
            if item in self.TabSwtControl.AddSwtControlDataInfo:
                self.addedDevices.append(item)
            else:
                self.editedDevices.append(item)

    # SERÁ MOVIDA PARA A "class_opendss"
    def exec_Devices(self):

        self.memoFileDevices = []

        for ctd in self.addedDevices:
            tmp = "New " + ctd["Device"] + "." + ctd["Name"] + " "
            for key, value in ctd.items():
                if value != '' and value != 'None'and value is not None and key != 'Device' and key != 'Name':
                    tmp += key + "=" + value + " "
            # print(tmp)

            self.memoFileDevices.append(tmp)

        for ctd in self.editedDevices:
            tmp = "Edit " + ctd["Device"] + "." + ctd["Name"] + " "
            for key, value in ctd.items():
                if value != '' and value != 'None'and value is not None and key != 'Device' and key != 'Name':
                    tmp += key + "=" + value + " "
            print(tmp)

            self.memoFileDevices.append(tmp)

        #print(self.memoFileDevices)