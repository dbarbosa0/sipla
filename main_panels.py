from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
import folium
import io, config

from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"pt-BR,pt;q=0.9,es;q=0.8,de;q=0.7")

class C_MainPanel(QWidget):
    def __init__(self, MainWidget):
        QWidget.__init__(self)



        self.MainWidget = MainWidget

        self.MapPainel_mainLayout = QGridLayout()
        self.MapPainel_hLayout = QHBoxLayout()

        self.MapPainel_GroupBox = QGroupBox("Visualizador")
        self.MapPainel_WebView = QWebEngineView()
        interceptor = Interceptor()
        self.MapPainel_WebView.page().profile().setUrlRequestInterceptor(interceptor)

        self.MapPainel_WebView.setContextMenuPolicy(Qt.NoContextMenu)

        self.MapPainel_hLayout.addWidget(self.MapPainel_WebView)
        self.MapPainel_GroupBox.setLayout(self.MapPainel_hLayout)

        self.MapPainel_mainLayout.addWidget(self.MapPainel_GroupBox)

        self.setLayout(self.MapPainel_mainLayout.layout())

        fileData = io.BytesIO()
        map = folium.Map(location=[-13.518 , -41.248], zoom_start=7)

        # Carvalho
        #tiles='https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoid2h5c29mYXN0IiwiYSI6ImNrZzdmbHN2eTA0M3ozMG84dmp2dzkzeHMifQ.UzHSwsJDEiS9--bQvg9Jig',attr='Mapbox')

        config.basemaps['Google Maps'].add_to(map)

        map.save(fileData, close_file=False)

        self.MapPainel_WebView.setHtml(fileData.getvalue().decode())
       #self.MapPainel_WebView.load(QUrl.fromLocalFile(fileData.getvalue().decode()))
        self.MapPainel_WebView.show()

    @property
    def MainWidget(self):
        return self.__parent

    @MainWidget.setter
    def MainWidget(self, value):
        self.__parent = value

