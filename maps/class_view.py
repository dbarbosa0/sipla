import io
import folium
import folium.plugins
from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore, QtGui

import database.class_coord
import database.class_conn
import config

class C_Viewer():

    def __init__(self):

        #################################
        self._DataBaseCoord = database.class_coord.C_DBaseCoord()
        self._DataBaseConn = database.class_conn.C_DBaseConn()
        #################################

        self.mapFields = ''
        self._ListFields = [] # Lista com os alimentadores
        self._nameSEMT = ''
        self._ListFieldsID = []

        ######### Alteração da Visualização ##########


        self.dataFields_BTTrafos = {}

        ##############################################

        self.webEngView = QtWebEngineWidgets.QWebEngineView()
        
        self.initUI()

    def initUI(self):
        self.DataBaseCoord.DataBaseConn = self.DataBaseConn


    @property
    def ListFields(self):
        return self._ListFields

    @property
    def nameSEMT(self):
        return self._nameSEMT

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

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        self.DataBaseCoord.DataBaseConn = self.DataBaseConn

        self.getListFieldsID()

        # Varendo todos os alimentadores
        self.mapFields = ''

        ## Layer de MT
        self.createLayerMTMap()

        ## Layer de BT
        self.createLayerBTMap()

        # opções
        self.execOptionsFieldsTDMap()
        self.execOptionsFieldsUCMTMap()

        QtWidgets.QApplication.restoreOverrideCursor()

    def createLayerMTMap(self):
        paranaue = folium.FeatureGroup( name = 'paranaue', show=True)

        map = self.mapFields

        for contadorAL in range(0, len(self.ListFields)):
            # Pegando as coordenadas do Alimentador

            # Pegando os códigos dos Alimentadores [NomAL CodAL x y]
            coordAlimentMT, dados_linha = self.DataBaseCoord.getCoord_AL_SE_MT_DB(self.ListFields[contadorAL])
            print('self.ListFields')
            print(len(self.ListFields))
            print(contadorAL)
            print(dados_linha)
            print(coordAlimentMT)
            print(len(dados_linha))
            print(len(coordAlimentMT))
            #print('final')
            #print(self.mapFields)
            colorField = self.dataFields_BTTrafos[self.ListFields[contadorAL]][-3]
            cartodb='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png'
            # Melhorar essa criação aqui
            if not self.mapFields:
                self.mapFields = folium.Map(location=coordAlimentMT[0][0], zoom_start=13,
                                            tiles=None)
                                            #attr='copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="http://cartodb.com/a:ttributions">CartoDB</a>, CartoDB <a href ="http//cartodb.com/attributions">attributions</a>')
                #config.basemaps['Google Maps'].add_to(self.mapFields)
                #tiles = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png',
                #attr = 'copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="http://cartodb.com/a:ttributions">CartoDB</a>, CartoDB <a href ="http//cartodb.com/attributions">attributions</a>',
                #zoom_start = 13
                folium.TileLayer(cartodb, name='CartoDB',
                                 attr='Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>').add_to(self.mapFields)
            if coordAlimentMT:
                folium.PolyLine(coordAlimentMT, color=colorField, weight=5.0, opacity=1, smooth_factor=0, control=True).add_to(self.mapFields)

    def createLayerBTMap(self):

        for contadorAL in range(0, len(self.ListFields)):
            ####### Baixa Tensão por Transformador ##########

            #Pegando a lista de TDs e suas cores

            listTDField = self.dataFields_BTTrafos[self.ListFields[contadorAL]][-2]
            listColorTDField = self.dataFields_BTTrafos[self.ListFields[contadorAL]][-1]

            for ctdTD in range(0, len(listTDField)):

            # Pegando os códigos dos Alimentadores [NomAL CodAL x y]
                coordAlimentBT = self.DataBaseCoord.getCoord_AL_SE_MT_BT_DB(listTDField[ctdTD])
            # self.mapFields = folium.Map(coordAlimentBT[0][0], zoom_start=13, name="Alimentadores")
                if coordAlimentBT: # Existem transformadores que não possuem Rede de Baixa Tensão
                    folium.PolyLine( coordAlimentBT, color=listColorTDField[ctdTD],  weight=3.0, opacity=1, smooth_factor=0, control = True).add_to(self.mapFields)

    def getListFieldsID(self):
        self.ListFields = list(self.dataFields_BTTrafos.keys())
        self.ListFieldsID = self.DataBaseCoord.getCods_AL_SE_MT_DB(self.ListFields)
    
    def viewMap(self):

        folium.LayerControl(collapsed=False).add_to(self.mapFields)
        #folium.LayerControl(position='topright', collapsed=True).add_to(self.mapFields)

        fileData = io.BytesIO()

        #Salvando Arquivo binário
        self.mapFields.save(fileData, close_file = False)

        #Mostando Map

        self.webEngView.setHtml(fileData.getvalue().decode())

        self.webEngView.show()

    def execOptionsFieldsTDMap(self):

        for ctdOption in range(0, len(self.ListFields)):

            fgTrafoDIST = folium.FeatureGroup( name = 'TD: ' + self.ListFields[ctdOption], show=True)

            self.mapFields.add_child(fgTrafoDIST)

            dados_db = self.DataBaseCoord.getData_TrafoDIST(self.nameSEMT, self.ListFieldsID[ctdOption])

            infoTextTrafo = '<b>Trafo de Distribuição</b>'
            infoTextTrafo += '<br> ID: ${cod_id.text}'
            infoTextTrafo += '<br> ${pot_nom.text} kVA / ${tipo_trafo.text} '
            infoTextTrafo += '<br> ${posto_trafo.text} / ${pos_trafo.text}'
            infoTextTrafo += '<br> Barra 1: ${pac_1_trafo.text}'
            infoTextTrafo += '<br> Barra 2: ${pac_2_trafo.text}'
            infoTextTrafo += '<br> AL: ' + self.ListFields[ctdOption]
            callbackTrafo = ('function (row) {'
                             'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
                             'var icon = L.AwesomeMarkers.icon({'
                             "icon: 'play',"
                             "iconColor: 'white',"
                             "markerColor: 'red',"
                             "prefix: 'fa',"
                             "extraClasses: 'fa-rotate-270'"
                             '});'
                             'marker.setIcon(icon);'
                             "var popup = L.popup({maxWidth: '300'});"
                             "const cod_id = {text: row[2]};"
                             "const pot_nom = {text: row[3]};"
                             "const tipo_trafo = {text: row[4]};"
                             "const pos_trafo = {text: row[5]};"
                             "const posto_trafo = {text: row[6]};"
                             "const pac_1_trafo = {text: row[7]};"
                             "const pac_2_trafo = {text: row[8]};"
                             "var textpopup = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> " + infoTextTrafo + "</div>`)[0];"
                                                                                                                                                   "popup.setContent(textpopup);"
                                                                                                                                                   "marker.bindPopup(popup);"
                                                                                                                                                   'return marker};')
            folium.plugins.FastMarkerCluster(
                data=dados_db,
                callback=callbackTrafo
            ).add_to(fgTrafoDIST)

    def execOptionsFieldsUCMTMap(self):

        for ctdOption in range(0, len(self.ListFields)):

            fgUniConsMT = folium.FeatureGroup(name='UCMT: ' + self.ListFields[ctdOption], show=True)

            self.mapFields.add_child(fgUniConsMT)


            dados_db = self.DataBaseCoord.getData_UniConsumidoraMT(self.nameSEMT, self.ListFieldsID[ctdOption])

            infoTextUniConsMT = '<b>Unidade Consumidora de Média Tensão</b>'
            infoTextUniConsMT += '<br> AL: ' + self.ListFields[ctdOption]
            infoTextUniConsMT += '<br> Situação: ${sit_ativ.text}'
            infoTextUniConsMT += '<br> Data de Conexão: ${dat_con.text}'
            infoTextUniConsMT += '<br> ${car_inst.text} kVA'
            infoTextUniConsMT += '<br> ${brr.text}'

            callbackUniConsMT = ('function (row) {'
                                 'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
                                 'var icon = L.AwesomeMarkers.icon({'
                                 "icon: 'info-sign',"
                                 "iconColor: 'white',"
                                 "markerColor: 'green',"
                                 "prefix: 'glyphicon',"
                                 "extraClasses: 'fa-rotate-0'"
                                 '});'
                                 'marker.setIcon(icon);'
                                 "var popup = L.popup({maxWidth: '300'});"
                                 "const brr = {text: row[2]};"
                                 "const sit_ativ = {text: row[3]};"
                                 "const car_inst = {text: row[4]};"
                                 "const dat_con = {text: row[5]};"
                                 "var textpopup = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> " + infoTextUniConsMT + "</div>`)[0];"
                                                                                                                                                           "popup.setContent(textpopup);"
                                                                                                                                                           "marker.bindPopup(popup);"
                                                                                                                                                           'return marker};')

            folium.plugins.FastMarkerCluster(
                data=dados_db,
                callback=callbackUniConsMT
            ).add_to(fgUniConsMT)

        
        
    




