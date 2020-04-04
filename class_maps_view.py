import io
import folium
from PyQt5 import QtWebEngineWidgets

import class_database_coord
import class_database_conn

class C_MapsViewer():

    def __init__(self):

        #################################
        self._DataBaseCoord = class_database_coord.C_DBaseCoord()
        self._DataBaseConn = class_database_conn.C_DBaseConn()
        #################################

        self.mapFields = ''
        self._ListFieldsColors = [] #Lista com as cores dos alimentadores
        self._ListFields = [] # Lista com os alimentadores
        self._NameSE_MT = ''

        self.webEngView = QtWebEngineWidgets.QWebEngineView()
        
        self.initUI()

    def initUI(self):
        self.DataBaseCoord.DataBaseConn = self.DataBaseConn



    @property
    def ListFieldsColors(self):
        return self._ListFieldsColors

    @property
    def ListFields(self):
        return self._ListFields

    @property
    def NameSE_MT(self):
        return self._NameSE_MT

    @ListFieldsColors.setter
    def ListFieldsColors(self, value):
        self._ListFieldsColors = value

    @ListFields.setter
    def ListFields(self, value):
        self._ListFields = value

    @NameSE_MT.setter
    def NameSE_MT(self, value):
        self._NameSE_MT = value

    @property
    def DataBaseCoord(self):
        return self._DataBaseCoord

    @DataBaseCoord.setter
    def DataBaseCoord(self, value):
        self._DataBaseCoord = value

    @property
    def DataBaseConn(self):
        return self._DataBaseConn

    @DataBaseConn.setter
    def DataBaseConn(self, value):
        self._DataBaseConn = value


    ##################################################################################

        
    def setWebView (self, nameQtWebEngineWidgets):

        self.webEngView = nameQtWebEngineWidgets
        
        
    def createMap(self):

        #Varendo todos os alimentadores

        for contadorAL in range(0, len(self.ListFields) ):
            #Pegando as coordenadas do Alimentador

            coordAlimentMT = self.DataBaseCoord.getCoord_AL_SE_MT_DB( self.ListFields[contadorAL] ) # Pegando os códigos dos Alimentadores [NomAL CodAL x y]
            
            if not self.mapFields : #Melhorar essa criação aqui
               self.mapFields = folium.Map(coordAlimentMT [0][0] ,zoom_start=13) 
            
            folium.PolyLine( coordAlimentMT , color = self.ListFieldsColors[contadorAL] , weight=3.0, opacity=1, smooth_factor=0).add_to(self.mapFields )
            
    
    def viewMap(self):
        
        fileData = io.BytesIO()
        
        #Salvando Arquivo binário
        self.mapFields.save(fileData, close_file = False)
        
        #Mostando Map
       
        self.webEngView.setHtml(fileData.getvalue().decode())
        
        self.webEngView.show()


        
        
        
        
        
        
        
        
        
    




