from PyQt5.QtWidgets import QStatusBar
from PyQt5 import QtCore

###
import class_database_coord
import class_exception
import class_dialog_opendss
import class_maps_view
import  main_panels_dock

class C_MainActions():
    def __init__(self):
        self.DataBase = class_database_coord.C_DBase  # Carregando o acesso ao BDGD
        self.MainWindowStatusBar = QStatusBar
        self.MainNetPanel = main_panels_dock.C_NetPanel
        self.MainMapView = class_maps_view.C_MapsViewer
        self.mainDialogOpenDSS = class_dialog_opendss.C_Dialog_OpenDSS()

    def acessDataBase(self):
        try:
            if self.DataBase.setBDGD():
                self.MainWindowStatusBar.setStatusBar_Status_Text("On-Line")
                self.getSE_AT_DB()
            else:
                raise class_exception.ConnDataBaseError("Erro de conexão com o Banco de Dados")

        except class_exception.ConnDataBaseError:
            pass

    def getSE_AT_DB(self): ## Carregando as subestações de Alta tensão
        self.MainNetPanel.set_SEAT(self.DataBase.getSE_AT_DB())
        self.MainNetPanel.show()

    def getCirAT_MT_DB(self, nomeSE_AT): #metodo_INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA
        return self.MainNetPanel.set_CirATMT(self.DataBase.getCirAT_MT_DB(nomeSE_AT))

    def getSE_MT_AL_DB(self, nomeSEMT): # Pega os alimentadores de média tensão associados a SE MT
        return self.MainNetPanel.set_SEMT_Fields(self.DataBase.getSE_MT_AL_DB( [nomeSEMT] ))

    def showDockNetPanel(self):
        if self.MainNetPanel.isHidden():
            self.MainNetPanel.show()
        else:
            self.MainNetPanel.hide()

    ##### Visualizando no Mapa
    def execMapView(self, viewMap, fieldsOptions = None):

        fieldsSelected = self.MainNetPanel.getSelectedFieldsNames()
        fieldsColors = self.MainNetPanel.getSelectedFieldsColors()


        if  viewMap.isChecked():

            self.MainMapView.setDataBase(self.DataBase)
            self.MainMapView.setFieldColors(fieldsColors) # Cores dos Alimentadores
            self.MainMapView.setFields(fieldsSelected) ## Alimentadores
            self.MainMapView.setSE_MT(self.MainNetPanel.get_SEMT_Selected())

            self.MainMapView.createMap()

            self.MainMapView.viewMap()

        else:
            print("funcionou sem visualizar")
            #self.btn_confirma_rede_de_alimentadores_selecionados_PushButton.setEnabled(False)
            
    #################################################################################
    ##### VAI SER SUBSTITUIDO PELA INTERFACE DE SANDY
    #################################################################################
    
    def execOpenDSS(self):
        self.mainDialogOpenDSS .setDirDataBase(self.DataBase.getBDGD())
        self.mainDialogOpenDSS .setCircuitoAT_MT( self.MainNetPanel.get_CirATMT())
        self.mainDialogOpenDSS .setSE_MT_Selecionada(self.MainNetPanel.get_SEMT_Selected())
        self.mainDialogOpenDSS .setFields_SE_MT_Selecionada(self.MainNetPanel.getSelectedFieldsNames())
        self.mainDialogOpenDSS .createFile()

    def saveOpenDSS(self):
        self.opendssDiag.exec_CRIAR_ARQUIVO_NO_FORMATO_OPENDSS()
    #################################################################################








