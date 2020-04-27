from PyQt5.QtWidgets import QStatusBar, QMessageBox

###
import database.class_conn
import opendss.class_opendss
import opendss.class_config_dialog
import opendss.class_insert_energymeter_dialog
import database.class_base
import database.class_config_dialog
import class_exception
import maps.class_view
import main_panels_dock
import configparser
import main_toolbar

class C_MainActions():
    def __init__(self):

        ################ Pegando instancias definidas no Main

        self.MainWindowStatusBar = QStatusBar()
        self.MainWindowToolBar = main_toolbar.C_MenuToolBar()
        self.MainNetPanel = main_panels_dock.C_NetPanel(self)
        self.MainResultsPanel = main_panels_dock.C_ResultsPanel(self)
        self.MainMapView = maps.class_view.C_Viewer()


        #############################################

        self.initUI()

    def initUI(self): ### Instanciando os objetos
        self.DataBaseConn = database.class_conn.C_DBaseConn()  # Carregando o acesso aos Arquivos do BDGD
        self.DataBase = database.class_base.C_DBase()
        self.DataBase_DialogSettings = database.class_config_dialog.C_ConfigDialog() # Instânciando a classe dialog Settings
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        # Contribuição Sandy
        self.OpenDSS_DialogSettings = opendss.class_config_dialog.C_ConfigDialog()  # Instânciando a classe dialog Settings
        self.OpenDSS_DialogInsert = opendss.class_insert_energymeter_dialog.C_Insert_Dialog() # Instânciando a classe dialog Insert
        self.OpenDSS_DialogInsert.OpenDSS = self.OpenDSS
        self.DataBase.DataBaseConn = self.DataBaseConn
        self.MainMapView.DataBaseConn = self.DataBaseConn

    #############################################


    def setStatusBar(self, type, msg):

        if type == "Status":
            self.MainWindowStatusBar.setStatusBar_Status_Text(msg)
        elif type == "Flow":
            self.MainWindowStatusBar.setStatusBar_Fluxo_Text(msg)
        elif type == "FlowStatus":
            self.MainWindowStatusBar.setStatusBar_Fluxo_Status_Text(msg)

    def getStatusBar(self, type):

        if type == "Status":
            return self.MainWindowStatusBar.getStatusBar_Status_Text()
        elif type == "Flow":
            return self.MainWindowStatusBar.getStatusBar_Fluxo_Text()
        elif type == "FlowStatus":
           return self.MainWindowStatusBar.getStatusBar_Fluxo_Status_Text()

    def updateToobarMenu(self):

        ##Funções que precisam do Fluxo

        if self.getStatusBar("FlowStatus") == "Solved":
            self.MainWindowToolBar.OpenDSS_InsertEnergyMeter_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_View_Act.setEnabled(True)
        else:
            self.MainWindowToolBar.OpenDSS_InsertEnergyMeter_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_View_Act.setEnabled(False)

        ## Habilitar o Solve Apenas se puder visualizar, o que significa que está tudo certo
        if self.MainNetPanel.Deck_GroupBox_MapView_Btn.isEnabled():
            self.MainWindowToolBar.OpenDSS_Run_Act.setEnabled(True)

        else:
            self.MainWindowToolBar.OpenDSS_Run_Act.setEnabled(False)


    #############################################

    def connectDataBase(self):
        if (self.DataBase_DialogSettings.databaseInfo["Conn"] == "sqlite") and (
        self.DataBase_DialogSettings.databaseInfo["DirDataBase"]):
            self.DataBaseConn.DataBaseInfo = self.DataBase_DialogSettings.databaseInfo
            self.getSE_AT_DB()
            self.setStatusBar("Status", "On-Line")

    def configDataBase(self):
        self.DataBase_DialogSettings.show()
        self.connectDataBase()

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
    def execMapView(self, fieldsOptions = None):

        self.MainMapView.DataBaseConn = self.DataBaseConn

        ##### Definindo variáveis

        self.MainMapView.ListFields = self.MainNetPanel.getSelectedFieldsNames()
        self.MainMapView.ListFieldsColors = self.MainNetPanel.getSelectedFieldsColors()
        self.MainMapView.nameSEMT = self.MainNetPanel.getSelectedSEMT()

        ##### Métodos
        self.MainMapView.createMap(fieldsOptions)

        self.MainMapView.viewMap()

            
    #################################################################################
    ##### VAI SER SUBSTITUIDO PELA INTERFACE DE SANDY
    #################################################################################

    # Contribuição Sandy
    def exec_configOpenDSS_Settings(self):
        self.updateToobarMenu()
        self.OpenDSS_DialogSettings.show()

    def execOpenDSS(self):

        ## testando o Daily
        if (self.OpenDSS_DialogSettings.dataInfo["Mode"] == "Daily") and (not self.OpenDSS_DialogSettings.dataInfo["LoadShapes"]):
            QMessageBox(QMessageBox.Information, "OpenDSS Configuration", \
                        "A(s) Curva(s) de Carga deve(m) ser carregada(s) no modo Daily!", QMessageBox.Ok).exec()
        else:
            self.execCreateDSS() ## Cria o arquivo que será utilizado pelo OpenDSS
            self.OpenDSS.exec_OpenDSS()
            self.setStatusBar("Flow", self.OpenDSS_DialogSettings.dataInfo["Mode"])
            self.setStatusBar("FlowStatus", "Solved")
            ##Atualizando o ToolBar
            self.updateToobarMenu()

    def execInsertEnergyMeter(self):
        self.OpenDSS_DialogInsert.updateDialog()
        self.OpenDSS_DialogInsert.show()


    def execCreateDSS(self):
        ## Zerando os resultados anteriores
        #self.MainResultsPanel.reloadTabs()

        ## Passando Parâmetros
        self.OpenDSS.definedSettings(self.OpenDSS_DialogSettings.dataInfo)

        self.OpenDSS.DataBaseConn = self.DataBaseConn
        self.OpenDSS.nCircuitoAT_MT = self.MainNetPanel.get_CirATMT_Selected()
        self.OpenDSS.nSE_MT_Selecionada = self.MainNetPanel.getSelectedSEMT()
        self.OpenDSS.nFieldsMT = self.MainNetPanel.getSelectedFieldsNames()
        self.OpenDSS.tableVoltageResults = self.MainResultsPanel.TableVoltage

        self.OpenDSS.loadData()


    def saveOpenDSS(self):

        #self.execCreateDSS()
        self.OpenDSS.exec_SaveFileDialogDSS()


    #################################################################################








