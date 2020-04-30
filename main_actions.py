from PyQt5.QtWidgets import QStatusBar, QMessageBox

###
import database.class_conn
import opendss.class_opendss
import opendss.class_config_dialog
import opendss.class_insert_energymeter_dialog
import opendss.class_insert_monitor_dialog
import opendss.class_config_plot_monitor_dialog
import opendss.class_scan_config_dialog
import database.class_base
import database.class_config_dialog
import class_exception
import maps.class_view
import main_panels_dock
import main_toolbar
import datetime

class C_MainActions():
    def __init__(self):

        ################ Pegando instancias definidas no Main

        self.MainWindowStatusBar = QStatusBar()
        self.MainWindowToolBar = main_toolbar.C_MenuToolBar()
        self.MainNetPanel = main_panels_dock.C_NetPanel(self)
        self.MainResultsPanel = main_panels_dock.C_ResultsPanel(self)
        self.MainMapView = maps.class_view.C_Viewer()

        ###

        #############################################

        self.initUI()

    def initUI(self): ### Instanciando os objetos
        self.DataBaseConn = database.class_conn.C_DBaseConn()  # Carregando o acesso aos Arquivos do BDGD
        self.DataBase = database.class_base.C_DBase()
        self.DataBase_DialogSettings = database.class_config_dialog.C_ConfigDialog() # Instânciando a classe dialog Settings
        self.OpenDSS = opendss.class_opendss.C_OpenDSS()
        self.OpenDSS.DataBaseConn = self.DataBaseConn

        # Contribuição Sandy
        self.OpenDSS_DialogSettings = opendss.class_config_dialog.C_ConfigDialog()  # Instânciando a classe dialog Settings

        self.OpenDSS.OpenDSSConfig = self.OpenDSS_DialogSettings.dataInfo
        self.DataBase.DataBaseConn = self.DataBaseConn

        ###
        self.OpenDSS_DialogInsertEnergyMeter = opendss.class_insert_energymeter_dialog.C_Insert_EnergyMeter_Dialog() # Instânciando a classe dialog Insert
        self.OpenDSS_DialogInsertEnergyMeter.OpenDSS = self.OpenDSS
        self.OpenDSS_DialogInsertMonitor = opendss.class_insert_monitor_dialog.C_Insert_Monitor_Dialog()  # Instânciando a classe dialog Insert
        self.OpenDSS_DialogInsertMonitor.OpenDSS = self.OpenDSS
        self.OpenDSS_DialogPlotMonitor = opendss.class_config_plot_monitor_dialog.C_Config_Plot_Dialog()
        self.OpenDSS_DialogPlotMonitor.OpenDSS = self.OpenDSS
        # Contribuição Carvalho
        self.SCAnalyze_DialogSettings = opendss.class_scan_config_dialog.C_SCAnalyze_ConfigDialog()
        self.SCAnalyze_DialogSettings.OpenDSS = self.OpenDSS #Apontando o ponteiro de OpenDSS C_MainActions


    #############################################

    def updateStatusBar(self):

        ##Verifica Conexão
        if (self.DataBase_DialogSettings.databaseInfo["Conn"] == "sqlite") and (
                self.DataBase_DialogSettings.databaseInfo["DirDataBase"]):
            self.MainWindowStatusBar.StatusBar_Status.setText("On-Line")

        ##Tipo de Fluxo
        self.MainWindowStatusBar.StatusBar_Fluxo.setText("Fluxo: " + self.OpenDSS_DialogSettings.dataInfo["Mode"])
        if self.OpenDSS.StatusSolutionProcessTime > 0:
            self.MainWindowStatusBar.StatusBar_Fluxo_Status.setText("Solved: "\
                                + str(datetime.timedelta(minutes=self.OpenDSS.StatusSolutionProcessTime)))

    def updateToobarMenu(self):
        ##Funções que precisam do Fluxo

        if self.OpenDSS.StatusSolutionProcessTime > 0:
            self.MainWindowToolBar.OpenDSS_InsertEnergyMeter_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_InsertMonitor_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_View_Act.setEnabled(True)
            self.MainWindowToolBar.SCAnalyze_Config_Act.setEnabled(True)
            self.MainWindowToolBar.SCAnalyze_Run_Act.setEnabled(True)
            self.MainWindowToolBar.Plot_Monitor_Act.setEnabled(True)
        else:
            self.MainWindowToolBar.OpenDSS_InsertEnergyMeter_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_InsertMonitor_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_View_Act.setEnabled(False)
            self.MainWindowToolBar.SCAnalyze_Config_Act.setEnabled(False)
            self.MainWindowToolBar.SCAnalyze_Run_Act.setEnabled(False)
            self.MainWindowToolBar.Plot_Monitor_Act.setEnabled(False)

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
            self.updateStatusBar()
        else:
            QMessageBox(QMessageBox.Warning, "DataBase Configuration", \
                        "A Conexão com o Banco de Dados deve ser configurada!", QMessageBox.Ok).exec()


    def configDataBase(self):
        self.DataBase_DialogSettings.show()

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

        ##### Definindo variáveis
        self.MainMapView.DataBaseConn = self.DataBaseConn

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
            ##Atualizando o ToolBar
            self.updateToobarMenu()
            self.updateStatusBar()


    def execInsertEnergyMeter(self):
        self.OpenDSS_DialogInsertEnergyMeter.updateDialog()
        self.OpenDSS_DialogInsertEnergyMeter.show()

    def execInsertMonitor(self):
        self.OpenDSS_DialogInsertMonitor.updateDialog()
        self.OpenDSS_DialogInsertMonitor.show()

    def execPlotMonitor(self):
        self.OpenDSS_DialogPlotMonitor.StepSizeTime = self.OpenDSS_DialogSettings.dataInfo["StepSizeTime"]
        self.OpenDSS_DialogPlotMonitor.StepSize = self.OpenDSS_DialogSettings.dataInfo["StepSize"]
        self.OpenDSS_DialogPlotMonitor.updateDialog()
        self.OpenDSS_DialogPlotMonitor.show()

    def execCreateDSS(self):
        ## Zerando os resultados anteriores
        #self.MainResultsPanel.reloadTabs()

        ## Passando Parâmetros
        self.OpenDSS.nCircuitoAT_MT = self.MainNetPanel.get_CirATMT_Selected()
        self.OpenDSS.nSE_MT_Selecionada = self.MainNetPanel.getSelectedSEMT()
        self.OpenDSS.nFieldsMT = self.MainNetPanel.getSelectedFieldsNames()
        self.OpenDSS.tableVoltageResults = self.MainResultsPanel.TableVoltage

        self.OpenDSS.loadData()


    def saveOpenDSS(self):
        #self.execCreateDSS()
        self.OpenDSS.exec_SaveFileDialogDSS()

    # Contribuição Carvalho
    def exec_configSCAnalyze_Settings(self):
        self.SCAnalyze_DialogSettings.updateDialog()
        self.SCAnalyze_DialogSettings.show()

    def exec_SCAnalyze(self):
        self.OpenDSS.exec_DynamicFlt()



    #################################################################################








