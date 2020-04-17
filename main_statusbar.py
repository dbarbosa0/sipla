from PyQt5.QtWidgets import QStatusBar, QLabel, QDockWidget,QFrame
import platform


import configparser

class C_StatusBar(QStatusBar):
    def __init__(self, MainWin):

        QDockWidget.__init__(self)

        config = configparser.ConfigParser()
        config.read('siplaconfig.ini')

        self.MainWin = MainWin
        self.MainStatusBar = MainWin.statusBar()
        self.MainStatusBar.setObjectName("StatusBarApp")
        
        # ******* Create the Status Bar Itens *******
        self.StatusBar_Status = QLabel("Off-Line")
        self.StatusBar_Status.setObjectName("StatusBar_Status")
        #self.StatusBar_Status.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.MainStatusBar.addPermanentWidget(QFrame())
        self.MainStatusBar.addPermanentWidget(self.StatusBar_Status)

        self.StatusBar_Fluxo = QLabel("Fluxo: " + config['LoadFlow']['mode'])
        self.StatusBar_Fluxo.setObjectName("StatusBarApp_Fluxo")
        #self.StatusBar_Fluxo.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.MainStatusBar.addPermanentWidget(QFrame())
        self.MainStatusBar.addPermanentWidget(self.StatusBar_Fluxo)


        self.StatusBar_Fluxo_status = QLabel("Not Solved")
        self.StatusBar_Fluxo_status.setObjectName("StatusBarApp_Fluxo_status")
        #self.StatusBar_Fluxo.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.MainStatusBar.addPermanentWidget(QFrame())
        self.MainStatusBar.addPermanentWidget(self.StatusBar_Fluxo_status)


        self.StatusBar_Plataform = QLabel(platform.system())
        self.StatusBar_Plataform.setObjectName("StatusBarApp_Plataform")
        #self.StatusBar_Plataform.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.MainStatusBar.addPermanentWidget(QFrame())
        self.MainStatusBar.addPermanentWidget(self.StatusBar_Plataform)

        self.StatusBar_Version = QLabel("SIPLA BETA")
        self.StatusBar_Version.setObjectName("StatusBarApp_Version")
        self.MainStatusBar.setStyleSheet('border: 0; background-color: #DCDCDC;')
        #self.MainStatusBar.setStyleSheet("QStatusBar::item {border: none;}")
        self.MainStatusBar.addPermanentWidget(self.StatusBar_Version)

    def setStatusBar_Status_Text(self, msgText):
        self.StatusBar_Status.setText(msgText)

    def setStatusBar_Fluxo_Text(self, msgText):
        self.StatusBar_Fluxo.setText(msgText)

    def setStatusBar_Fluxo_status_Text(self, msgText):
        self.StatusBar_Fluxo_status.setText(msgText)
