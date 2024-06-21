import sys, time

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory, QSplashScreen


#import opendss.class_insert_dialog
###
import config
import maps.class_view
###################################
# Classes de Construção da Interface Inicial
import main_statusbar
import main_toolbar
import main_actions
import main_panels
import main_panels_dock

import platform
import multiprocessing


class mainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)

        self.titleWindow = config.__name__ + " - Version: " + config.__version__
        self.iconWindow = config.sipla_icon
        self.stylesheet = "fusion"

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.resize(1366, 768)
        #self.showMaximized()
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

        self.initUI()

    def initUI(self):
        # Instanciando os Objetos da Interface
        ########################################################
        self.mainStatusBar = main_statusbar.C_StatusBar(self)  # Barra de Status
        self.mainToolBar = main_toolbar.C_MenuToolBar(self)  # Menu e ToolBar
        self.mainPainelCentral = main_panels.C_MainPanel(self)  # Painel Central
        self.mainDockNet = main_panels_dock.C_NetPanel(self)  # Dock com configurações da rede
        self.mainDockResults = main_panels_dock.C_ResultsPanel(self)  # Dock com configurações da rede
        self.mainActions = main_actions.C_MainActions()  # Carregando os métodos da interface principal
        #####
        #self.OpenDSS_Insert_dialog = opendss.class_insert_dialog.C_Insert_Dialog()

        #Instaciando os Demais Objetos
        self.mainMapView = maps.class_view.C_Viewer() ##Carregando Mapa

        ### Vinculando o Motor do Mapa ao Painel Central
        self.mainMapView.setWebView(self.mainPainelCentral.MapPainel_WebView)

        ## Painel Central
        self.setCentralWidget(self.mainPainelCentral)

        ## Dock
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.mainDockNet)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.mainDockResults)
        self.setDockOptions(QMainWindow.DockOption.AnimatedDocks)
        self.mainDockNet.mainActions = self.mainActions


        ### Passando os Dados para o Actions
        self.mainActions.MainWindowStatusBar = self.mainStatusBar
        self.mainActions.MainWindowToolBar = self.mainToolBar
        self.mainActions.updateToobarMenu()
        self.mainActions.MainNetPanel = self.mainDockNet
        self.mainActions.MainResultsPanel = self.mainDockResults
        self.mainActions.MainMapView = self.mainMapView

        ### Passando os Dados para o ToolBar

        self.mainToolBar.Actions = self.mainActions


if __name__ == '__main__':
    siplaApp = QApplication(sys.argv)

    if platform.system() == 'Linux':
        # Define the method to create all multiprocessed processes in Linux
        multiprocessing.set_start_method('fork')
    elif platform.system() == 'Windows':
        # Devido a limitação da versão 6.5 do PyQt, em que não há controle sobre o tema da janela no windown, isto é o
        # tema padrão no os é seguido, definimos uma paleta para os elementos que segue o tema do os.
        siplaApp.setStyle('fusion')

        paleta = siplaApp.palette()
        paleta.setColor(QPalette.ColorRole.Window, paleta.color(QPalette.ColorRole.Base))
        paleta.setColor(QPalette.ColorRole.WindowText, paleta.color(QPalette.ColorRole.ButtonText))
        paleta.setColor(QPalette.ColorRole.Base, paleta.color(QPalette.ColorRole.Base))
        paleta.setColor(QPalette.ColorRole.AlternateBase, paleta.color(QPalette.ColorRole.AlternateBase))
        paleta.setColor(QPalette.ColorRole.ToolTipBase, paleta.color(QPalette.ColorRole.ToolTipBase))
        paleta.setColor(QPalette.ColorRole.ToolTipText, paleta.color(QPalette.ColorRole.ToolTipText))
        paleta.setColor(QPalette.ColorRole.Text, paleta.color(QPalette.ColorRole.ButtonText))
        paleta.setColor(QPalette.ColorRole.Button, paleta.color(QPalette.ColorRole.Button))
        paleta.setColor(QPalette.ColorRole.ButtonText, paleta.color(QPalette.ColorRole.ButtonText))
        paleta.setColor(QPalette.ColorRole.BrightText, paleta.color(QPalette.ColorRole.BrightText))
        paleta.setColor(QPalette.ColorRole.Highlight, paleta.color(QPalette.ColorRole.Highlight))
        paleta.setColor(QPalette.ColorRole.HighlightedText, paleta.color(QPalette.ColorRole.HighlightedText))

        siplaApp.setPalette(paleta)

    # Create and display the splash screen
    splash_pix = QPixmap('img/Logo_SIPLA.png')
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    siplaApp.processEvents()

    GUI = mainWindow()
    GUI.show()
    splash.close()
    sys.exit(siplaApp.exec())
