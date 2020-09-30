import io
import folium
from PyQt5 import QtWebEngineWidgets

import database.class_coord
import database.class_conn

class C_Viewer():

    def __init__(self):

        #################################
        self._DataBaseCoord = database.class_coord.C_DBaseCoord()
        self._DataBaseConn = database.class_conn.C_DBaseConn()
        #################################

        self.mapFields = ''
        self._ListFieldsColors = [] #Lista com as cores dos alimentadores
        self._ListFields = [] # Lista com os alimentadores
        self._nameSEMT = ''
        self._ListFieldsID = []

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
    def nameSEMT(self):
        return self._nameSEMT

    @ListFieldsColors.setter
    def ListFieldsColors(self, value):
        self._ListFieldsColors = value

    @ListFields.setter
    def ListFields(self, value):
        self._ListFields = value

    @nameSEMT.setter
    def nameSEMT(self, value):
        tmp = []
        tmp.append(value)
        self._nameSEMT = tmp

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

    @property
    def ListFieldsID(self):
        return self._ListFieldsID

    @ListFieldsID.setter
    def ListFieldsID(self, value):
        self._ListFieldsID = value


    ##################################################################################

        
    def setWebView (self, nameQtWebEngineWidgets):

        self.webEngView = nameQtWebEngineWidgets

        
    def createMap(self):

        self.DataBaseCoord.DataBaseConn = self.DataBaseConn

        self.ListFieldsID = self.DataBaseCoord.getCods_AL_SE_MT_DB(self.ListFields)

        #Varendo todos os alimentadores
        self.mapFields = ''

        for contadorAL in range(0, len(self.ListFields) ):
            #Pegando as coordenadas do Alimentador

            coordAlimentMT = self.DataBaseCoord.getCoord_AL_SE_MT_DB( self.ListFields[contadorAL] ) # Pegando os códigos dos Alimentadores [NomAL CodAL x y]
            
            if not self.mapFields : #Melhorar essa criação aqui
               self.mapFields = folium.Map(coordAlimentMT [0][0] ,zoom_start=13, name = "Alimentadores")
            
            folium.PolyLine( coordAlimentMT , color = self.ListFieldsColors[contadorAL] , weight=3.0, opacity=1, smooth_factor=0, control = False).add_to(self.mapFields)

        self.execOptionsMap()
    
    def viewMap(self):

        folium.LayerControl(collapsed=False).add_to(self.mapFields)
        
        fileData = io.BytesIO()
        
        #Salvando Arquivo binário
        self.mapFields.save(fileData, close_file = False)

        #Mostando Map
       
        self.webEngView.setHtml(fileData.getvalue().decode())
        
        self.webEngView.show()

    def execOptionsMap(self):

        #Transformador
        fieldsOptions = {"TrafoDIST":"Transformador(es) de Distribuição",
                         }

        for ctdOption in fieldsOptions:

            if ctdOption == "TrafoDIST":

                fgTrafoDIST = folium.FeatureGroup(name=fieldsOptions[ctdOption], show=False)

                self.mapFields.add_child(fgTrafoDIST)

                dados_db = self.DataBaseCoord.getData_TrafoDIST(self.nameSEMT)

                for ctd in range(0, len(dados_db)):

                    if (dados_db[ctd].ctmt in self.ListFieldsID):

                        infoText  = '<b>Trafo de Distribuição</b>'
                        infoText += '<br> ID: ' + dados_db[ctd].cod_id
                        infoText += '<br> ' + str(dados_db[ctd].pot_nom)  + ' kVA'
                        folium.Marker(
                                location = [dados_db[ctd].y, dados_db[ctd].x],
                                popup = infoText,
                                icon=folium.Icon(color='red', icon='info-sign'),
                                control = True
                            ).add_to(fgTrafoDIST)

        
        
        
        
        
        
        
        
    




