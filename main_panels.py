from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QEvent, Qt
import folium, io

class C_MainPanel(QWidget):
    def __init__(self, MainWidget):
        QWidget.__init__(self)
        self.MainWidget = MainWidget

        self.MapPainel_mainLayout = QGridLayout()
        self.MapPainel_hLayout = QHBoxLayout()

        self.MapPainel_GroupBox = QGroupBox("Visualizador")
        self.MapPainel_WebView = QWebEngineView()
        self.MapPainel_WebView.setContextMenuPolicy(Qt.NoContextMenu)

        self.MapPainel_hLayout.addWidget(self.MapPainel_WebView)
        self.MapPainel_GroupBox.setLayout(self.MapPainel_hLayout)

        self.MapPainel_mainLayout.addWidget(self.MapPainel_GroupBox)

        self.setLayout(self.MapPainel_mainLayout.layout())

        fileData = io.BytesIO()
        folium.Map([-13.518 , -41.248],
                   zoom_start=7,
                   tiles="https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoid2h5c29mYXN0IiwiYSI6ImNrZzdmbHN2eTA0M3ozMG84dmp2dzkzeHMifQ.UzHSwsJDEiS9--bQvg9Jig",
                   attr='Mapbox').save(fileData, close_file=False)
        self.MapPainel_WebView.setHtml(fileData.getvalue().decode())
        self.MapPainel_WebView.show()


    @property
    def MainWidget(self):
        return self.__parent

    @MainWidget.setter
    def MainWidget(self, value):
        self.__parent = value



