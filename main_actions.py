from PyQt5.QtWidgets import QStatusBar, QMessageBox

###
import database.class_conn
import opendss.class_opendss
import opendss.class_config_dialog
import opendss.class_insert_energymeter_dialog
import opendss.class_insert_monitor_dialog
import opendss.storage.class_insert_storage_dialog
import opendss.invcontrol.class_insert_invcontrol_dialog
import opendss.invcontrol.class_config_voltvar_elementlist
import opendss.storage.class_config_storagecontroller
import opendss.class_insert_pvsystem_config_dialog
import opendss.class_insert_pvsystem_substation_dialog
import opendss.class_energymeter_results_dialog
import opendss.class_config_plot_monitor_dialog
import opendss.class_scan_config_dialog
import protect.class_devices
import protect.class_tcc_curves
import database.class_base
import database.class_config_dialog
# import class_exception
import maps.class_view
import main_panels_dock
import main_toolbar
import class_about_dialog
import datetime

class C_MainActions():
    def __init__(self):

        ################ Pegando instancias definidas no Main

        self.MainWindowStatusBar = QStatusBar()
        self.MainWindowToolBar = main_toolbar.C_MenuToolBar()
        self.MainNetPanel = main_panels_dock.C_NetPanel(self)
        self.MainResultsPanel = main_panels_dock.C_ResultsPanel(self)
        self.MainMapView = maps.class_view.C_Viewer()
        self.About = class_about_dialog.C_AboutDialog()

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
        self.OpenDSS_DialogResultsEnergyMeter = opendss.class_energymeter_results_dialog.C_ResultsEnergyMeter_Dialog()
        self.OpenDSS_DialogResultsEnergyMeter.OpenDSS = self.OpenDSS
        # Contribuição Carvalho
        self.SCAnalyze_DialogSettings = opendss.class_scan_config_dialog.C_SCAnalyze_ConfigDialog()
        self.SCAnalyze_DialogSettings.OpenDSS = self.OpenDSS #Apontando o ponteiro de OpenDSS C_MainActions
        self.Devices_DialogSettings = protect.class_devices.C_Devices_ConfigDialog()
        self.Devices_DialogSettings.OpenDSS = self.OpenDSS #Apontando o ponteiro de OpenDSS C_MainActions
        self.Devices_DialogSettings.TabRecloser.OpenDSS = self.OpenDSS
        self.Devices_DialogSettings.TabFuse.OpenDSS = self.OpenDSS
        self.Devices_DialogSettings.TabRelay.OpenDSS = self.OpenDSS
        self.Devices_DialogSettings.TabSwtControl.OpenDSS = self.OpenDSS
        self.Curves_DialogSettings = protect.class_tcc_curves.C_Config_Curves_Dialog()

        # Contribuição Felipe
        self.OpenDSS_PVSystem_DialogSettings = opendss.class_insert_pvsystem_config_dialog.C_Config_PVSystem_Dialog()
        self.OpenDSS_PVSystem_DialogInsert = opendss.class_insert_pvsystem_substation_dialog.C_Insert_PVSystem_Substation_Dialog(self.OpenDSS_PVSystem_DialogSettings)
        self.OpenDSS_PVSystem_DialogSettings.OpenDSS = self.OpenDSS
        self.OpenDSS_PVSystem_DialogInsert.OpenDSS = self.OpenDSS

        # Contribuição Jonas
        self.OpenDSS_DialogInsertStorage = opendss.storage.class_insert_storage_dialog.C_Insert_Storage_Dialog()
        self.OpenDSS_DialogInsertStorage.OpenDSS = self.OpenDSS
        self.OpenDSS_DialogInsertStorage.DispModeActPowDialog.ConfigStorageController.OpenDSS = self.OpenDSS
        self.OpenDSS_DialogInsertStorage.DispModeActPowDialog.DialogActPowLoadShape.OpenDSS = self.OpenDSS
        # Contribuição Lenon
        self.OpenDSS_DialogInsertInvControl = opendss.invcontrol.class_insert_invcontrol_dialog.C_Insert_InvControl_Dialog()
        self.OpenDSS_DialogInsertInvControl.OpenDSS = self.OpenDSS
        self.OpenDSS_DialogInsertInvControl.TabConfig.VV_ElementList.OpenDSS = self.OpenDSS
        self.OpenDSS_DialogInsertInvControl.TabConfig.VW_ElementList.OpenDSS = self.OpenDSS

    #############################################

    def updateStatusBar(self):

        ##Verifica Conexão
        if self.OpenDSS.DataBaseConn.testConn():
            self.MainWindowStatusBar.StatusBar_Status.setText("On-Line")
        else:
            self.MainWindowStatusBar.StatusBar_Status.setText("Off-Line")

        ##Tipo de Fluxo
        self.MainWindowStatusBar.StatusBar_Fluxo.setText("Fluxo: " + self.OpenDSS_DialogSettings.dataInfo["Mode"])
        if self.OpenDSS.StatusSolutionProcessTime > 0:
            self.MainWindowStatusBar.StatusBar_Fluxo_Status.setText("Solved: "\
                                + str(datetime.timedelta(seconds=self.OpenDSS.StatusSolutionProcessTime)))

        ##Dados Carregados
        if self.OpenDSS.loadDataFlag:
            self.MainWindowStatusBar.StatusBar_LoadData.setText("Data Loaded")
        else:
            self.MainWindowStatusBar.StatusBar_LoadData.setText("Data Not Loaded")

    def updateToobarMenu(self):
        ##Funções que precisam do Fluxo

        if self.OpenDSS.StatusSolutionProcessTime > 0:
            self.MainWindowToolBar.Plot_Monitor_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Results_EnergyMeter_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(True)
        else:
            self.MainWindowToolBar.Plot_Monitor_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Results_EnergyMeter_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(False)

        ## Habilitar o Solve Apenas se puder visualizar, o que significa que está tudo certo
        if self.MainNetPanel.Deck_GroupBox_MapView_Btn.isEnabled():
            self.MainWindowToolBar.OpenDSS_Run_Act.setEnabled(True)
        else:
            self.MainWindowToolBar.OpenDSS_Run_Act.setEnabled(False)

        ##Funções que precisam do Load Data inpedentemente do Fluxo
        if self.OpenDSS.loadDataFlag:
            self.MainWindowToolBar.OpenDSS_InsertEnergyMeter_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_InsertMonitor_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_InsertStorage_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_InsertInvControl_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(True)
            self.MainWindowToolBar.OpenDSS_View_Act.setEnabled(True)
            #Jonas
            self.MainWindowToolBar.OpenDSS_InsertStorage_Act.setEnabled(True)
            #Carvalho
            self.MainWindowToolBar.SCAnalyze_Config_Act.setEnabled(True)
            self.MainWindowToolBar.SCAnalyze_Run_Act.setEnabled(True)
            self.MainWindowToolBar.Protect_Devices_Act.setEnabled(True)
            #self.MainWindowToolBar.Protect_Curves_Act.setEnabled(True)

            #Felipe
            self.MainWindowToolBar.OpenDSSMenuSubInsert_SubPVSystem.setEnabled(True)
            #self.MainWindowToolBar.OpenDSS_ConfigPVSystem_Act.setEnabled(True)
        else:
            self.MainWindowToolBar.OpenDSS_InsertEnergyMeter_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_InsertMonitor_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_InsertStorage_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_InsertInvControl_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Save_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_Create_Act.setEnabled(False)
            self.MainWindowToolBar.OpenDSS_View_Act.setEnabled(False)
            self.MainWindowToolBar.SCAnalyze_Config_Act.setEnabled(False)
            self.MainWindowToolBar.SCAnalyze_Run_Act.setEnabled(False)
            #Jonas
            self.MainWindowToolBar.OpenDSS_InsertStorage_Act.setEnabled(False)
            #Carvalho
            self.MainWindowToolBar.SCAnalyze_Config_Act.setEnabled(False)
            self.MainWindowToolBar.SCAnalyze_Run_Act.setEnabled(False)
            self.MainWindowToolBar.Protect_Devices_Act.setEnabled(False)
            #self.MainWindowToolBar.Protect_Curves_Act.setEnabled(False)

            # Felipe
            self.MainWindowToolBar.OpenDSSMenuSubInsert_SubPVSystem.setEnabled(False)


    #############################################

    def connectDataBase(self):
        self.DataBaseConn.DataBaseInfo = self.DataBase_DialogSettings.databaseInfo

        if self.OpenDSS.DataBaseConn.testConn():
            self.getSE_AT_DB()
            self.updateStatusBar()
        else:
            QMessageBox(QMessageBox.Warning, "DataBase Configuration", \
                        "A Conexão com o Banco de Dados deve ser configurada!", QMessageBox.Ok).exec()

    def configDataBase(self):
        self.DataBase_DialogSettings.exec()
        self.updateStatusBar()
        self.MainNetPanel.setDisabled_NetPanel_Config_GroupBox_SEAT()

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

    def execAbout(self):
        self.About.show()


    ##### Visualizando no Mapa
    def execMapView(self):

        ##### Definindo variáveis
        self.MainMapView.DataBaseConn = self.DataBaseConn

        self.MainMapView.ListFields = self.MainNetPanel.getSelectedFieldsNames()
        self.MainMapView.ListFieldsColors = self.MainNetPanel.getSelectedFieldsColors()
        self.MainMapView.nameSEMT = self.MainNetPanel.getSelectedSEMT()

        ##### Métodos
        self.MainMapView.createMap()
        self.MainMapView.viewMap()



    #################################################################################
    ##### VAI SER SUBSTITUIDO PELA INTERFACE DE SANDY
    #################################################################################

    # Contribuição Sandy
    def exec_configOpenDSS_Settings(self):
        self.updateToobarMenu()
        self.OpenDSS_DialogSettings.exec()

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

    def execResultsEnergyMeter(self):
        self.OpenDSS_DialogResultsEnergyMeter.updateDialog()
        self.OpenDSS_DialogResultsEnergyMeter.show()

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

    ##Executa o Load Data
    def execLoadDataDSS(self):
        self.execCreateDSS()
        self.OpenDSS.loadData()
        self.updateToobarMenu()
        self.updateStatusBar()

    def saveOpenDSS(self):
        #self.execCreateDSS()
        self.OpenDSS.exec_SaveFileDialogDSS()

    # Contribuição Carvalho
    def exec_configSCAnalyze_Settings(self):
        self.SCAnalyze_DialogSettings.updateDialog()
        self.SCAnalyze_DialogSettings.show()

    def exec_SCAnalyze(self):
        self.OpenDSS.exec_DynamicFlt()

    # Contribuição Felipe
    def exec_PVSystem_Settings(self):
        self.OpenDSS_PVSystem_DialogSettings.show()

    def exec_PVSystem_Substation(self):
        self.OpenDSS_PVSystem_DialogInsert.show()

    def exec_Device_Settings(self):
        self.Devices_DialogSettings.updateMainProtectDialog()
        self.Devices_DialogSettings.show()

    def exec_Curves_Settings(self):
        self.Curves_DialogSettings.show()

    #################################################################################

    def fieldsChangedDSS(self): # A alteração dos alimentadores implica em rodar o LoadData novamente
        self.OpenDSS.loadDataFlag = False
        self.updateToobarMenu()
        self.updateStatusBar()

        ##Limpando os Monitores
        self.OpenDSS.Monitors.clear()
        self.OpenDSS_DialogInsertMonitor.Monitors.clear()

        ##Limpando os Medidores
        self.OpenDSS.EnergyMeters.clear()
        self.OpenDSS_DialogInsertEnergyMeter.EnergyMeters.clear()


    #Contribuição Jonas
    def execInsertStorage(self):
        self.OpenDSS_DialogInsertStorage.updateDialog()
        self.OpenDSS_DialogInsertStorage.show()
        #self.OpenDSS_DialogInsertStorage.DispModeActPowDialog.ConfigStorageController.updateDialog()

    #Contribuição Lenon
    def execInsertInvControl(self):
        self.OpenDSS_DialogInsertInvControl.move(500, 90)
        self.OpenDSS_DialogInsertInvControl.show()








