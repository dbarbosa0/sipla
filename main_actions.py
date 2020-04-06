from PyQt5.QtWidgets import QStatusBar
from PyQt5 import QtCore

###
import class_database_conn
import class_dialog_opendss
import class_opendss_config_dialog
import class_database
import class_exception
import class_dialog_opendss
import class_maps_view
import  main_panels_dock

class C_MainActions():
    def __init__(self):

        ################ Pegando instancias definidas no Main

        self.MainWindowStatusBar = QStatusBar()
        self.MainNetPanel = main_panels_dock.C_NetPanel(self)
        self.MainMapView = class_maps_view.C_MapsViewer()

        #############################################

        self.initUI()

    def initUI(self): ### Instanciando os objetos
        self.DataBaseConn = class_database_conn.C_DBaseConn()  # Carregando o acesso aos Arquivos do BDGD
        self.DataBase = class_database.C_DBase()
        #self.DialogOpenDSS = class_dialog_opendss.C_Dialog_OpenDSS()
        # Contribuição Sandy
        self.OpenDSS_DialogSettings = class_opendss_config_dialog.C_OpenDSS_ConfigDialog()  # Instânciando a classe dialog Settings


        ######### Passando os objetos
        self.DataBase.DataBaseConn = self.DataBaseConn
        self.MainMapView.DataBaseConn = self.DataBaseConn


        #############################################

    def acessDataBase(self):
        try:
            self.DataBaseConn.setDirDataBase()
            self.MainWindowStatusBar.setStatusBar_Status_Text("On-Line")
            self.getSE_AT_DB()

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

        self.MainMapView.DataBaseConn = self.DataBaseConn

        if viewMap.isChecked():

            ##### Definindo variáveis

            self.MainMapView.ListFields = self.MainNetPanel.getSelectedFieldsNames()
            self.MainMapView.ListFieldsColors = self.MainNetPanel.getSelectedFieldsColors()
            self.MainMapView.nameSEMT = self.MainNetPanel.getSelectedSEMT()

            ##### Métodos
            self.MainMapView.createMap(fieldsOptions)

            self.MainMapView.viewMap()

        else:
            print("funcionou sem visualizar")
            #self.btn_confirma_rede_de_alimentadores_selecionados_PushButton.setEnabled(False)
            
    #################################################################################
    ##### VAI SER SUBSTITUIDO PELA INTERFACE DE SANDY
    #################################################################################

    # Contribuição Sandy
    def exec_configOpenDSS_Settings(self):
        self.OpenDSS_DialogSettings.InitUI()

    def execOpenDSS(self):

        self.DialogOpenDSS.DataBaseConn = self.DataBaseConn

        self.DialogOpenDSS.nCircuitoAT_MT = self.MainNetPanel.getSelectedSEMT_CirATMT()
        self.DialogOpenDSS.nSE_MT_Selecionada = self.MainNetPanel.getSelectedSEMT()
        self.DialogOpenDSS.nFieldsMT = self.MainNetPanel.getSelectedFieldsNames()


        self.DialogOpenDSS.createFile()

    def saveOpenDSS(self):
        self.opendssDiag.exec_CRIAR_ARQUIVO_NO_FORMATO_OPENDSS()
    #################################################################################








