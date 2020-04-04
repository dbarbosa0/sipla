from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView



class C_MainPanel(QWidget):
    def __init__(self, MainWidget):
        QWidget.__init__(self)
        self.MainWidget = MainWidget

        self.MapPainel_mainLayout = QGridLayout()

        self.MapPainel_hLayout = QHBoxLayout()

        self.MapPainel_GroupBox = QGroupBox("Visualizador")
        self.MapPainel_WebView = QWebEngineView()
        self.MapPainel_hLayout.addWidget(self.MapPainel_WebView)
        self.MapPainel_GroupBox.setLayout(self.MapPainel_hLayout)

        self.MapPainel_mainLayout.addWidget(self.MapPainel_GroupBox)

        self.setLayout(self.MapPainel_mainLayout.layout())


    @property
    def MainWidget(self):
        return self.__parent

    @MainWidget.setter
    def MainWidget(self, value):
        self.__parent = value
