import platform
import io
import sys
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets

import class_database_conn

class C_MapsViewer():

    def __init__(self):
        
        self.dataBase = class_database_conn.C_ConnDBase()
        
        self.mapFields = ''
        
        self.fieldsColors = [] #Lista com as cores dos alimentadores
        self.listFields = [] # Lista com os alimentadores
        
        self.nameSE_MT = ''
    
        self.webEngView = QtWebEngineWidgets.QWebEngineView()
        
        self.initUI()

    def initUI(self):
        pass
    
    def setDataBase(self, nameDataBase):
        self.dataBase = nameDataBase

        
    def setNameFileViewer(self, nameFile):
        self.nameFileView = nameFile
        
    def setFieldColors(self, listColors):
        self.fieldsColors = listColors
        
    def setFields(self, listFields):
        self.listFields = listFields
    
    def setSE_MT(self, nameSE_MT):
        self.nameSE_MT = nameSE_MT
        #grupoCoordAlimentMT = self.dataBase.getCoord_AL_SE_MT_DB(self.listFields[0])
        
    def setWebView (self, nameQtWebEngineWidgets):
        self.webEngView = nameQtWebEngineWidgets
        
        
    def createMap(self):
        #Varendo todos os alimentadores
        for contadorAL in range(0, len(self.listFields) ):
            #Pegando as coordenadas do Alimentador
            coordAlimentMT = self.dataBase.getCoord_AL_SE_MT_DB(self.listFields[contadorAL]) # Pegando os códigos dos Alimentadores [NomAL CodAL x y]
            
            if not self.mapFields : #Melhorar essa criação aqui
               self.mapFields = folium.Map(coordAlimentMT [0][0] ,zoom_start=13) 
            
            folium.PolyLine( coordAlimentMT , color = self.fieldsColors[contadorAL] , weight=3.0, opacity=1, smooth_factor=0).add_to(self.mapFields )
            
    
    def viewMap(self):
        
        fileData = io.BytesIO()
        
        #Salvando Arquivo binário
        self.mapFields.save(fileData, close_file = False)
        
        #Mostando Map
       
        self.webEngView.setHtml(fileData.getvalue().decode())
        
        self.webEngView.show()


        
        
        
        
        
        
        
        
        
    




