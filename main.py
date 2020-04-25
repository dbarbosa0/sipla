import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyleFactory


###
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


class mainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)

        self.titleWindow = config.__name__ + " - Version: " + config.__version__
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.resize(1366, 768)
        self.showMaximized()
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
        self.addDockWidget(Qt.LeftDockWidgetArea, self.mainDockNet)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.mainDockResults)
        self.setDockOptions(QMainWindow.AnimatedDocks)


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

    GUI = mainWindow()
    GUI.show()

    sys.exit(siplaApp.exec())
