from PyQt5.QtWidgets import QStatusBar

###
import database.class_conn
import opendss.class_opendss
import opendss.class_config_dialog
import opendss.class_insert_dialog
import database.class_base
import class_exception
import maps.class_view
import main_panels_dock
import configparser

class C_MainActions():
    def __init__(self):

        ################ Pegando instancias definidas no Main

        self.MainWindowStatusBar = QStatusBar()
        self.MainNetPanel = main_panels_dock.C_NetPanel(self)
        self.MainResultsPanel = main_panels_dock.C_ResultsPanel(self)
        self.MainMapView = maps.class_view.C_Viewer()

        #############################################

        self.initUI()

    def initUI(self): ### Instanciando os objetos
        self.DataBaseConn = database.class_conn.C_DBaseConn()  # Carregando o acesso aos Arquivos do BDGD
        self.DataBase = database.class_base.C_DBase()
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        # Contribuição Sandy
        self.OpenDSS_DialogSettings = opendss.class_config_dialog.C_ConfigDialog()  # Instânciando a classe dialog Settings
        self.OpenDSS_DialogInsert = opendss.class_insert_dialog.C_Insert_Dialog() # Instânciando a classe dialog Insert
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

    def showDockResultsPanel(self):
        if self.MainResultsPanel.isHidden():
            self.MainResultsPanel.show()
        else:
            self.MainResultsPanel.hide()

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

        self.OpenDSS_DialogSettings.show()

    def execOpenDSS(self):

        self.execCreateDSS() ## Cria o arquivo que será utilizado pelo OpenDSS

        self.OpenDSS.exec_OpenDSS()

        self.MainWindowStatusBar.setStatusBar_Fluxo_Text("Fluxo: " + self.OpenDSS_DialogSettings.dataInfo["Mode"])
        self.MainWindowStatusBar.setStatusBar_Fluxo_status_Text("Solved")


    def execInsertDSS(self):
        self.OpenDSS_DialogInsert.show()
        self.OpenDSS_DialogInsert.TabEnergyMeter.get_EnergyMeter_AllBusNames_()


    def execCreateDSS(self):

        self.OpenDSS.definedSettings(self.OpenDSS_DialogSettings.dataInfo)

        self.OpenDSS.DataBaseConn = self.DataBaseConn
        self.OpenDSS.nCircuitoAT_MT = self.MainNetPanel.get_CirATMT_Selected()
        self.OpenDSS.nSE_MT_Selecionada = self.MainNetPanel.getSelectedSEMT()
        self.OpenDSS.nFieldsMT = self.MainNetPanel.getSelectedFieldsNames()
        self.OpenDSS.tableVoltageResults = self.MainResultsPanel.TableVoltage

        self.OpenDSS.loadData()




    def saveOpenDSS(self):

        self.execCreateDSS()
        self.OpenDSS.exec_SaveFileDialogDSS()


    #################################################################################








