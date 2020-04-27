from PyQt5.QtWidgets import QDockWidget, QAction, QMenuBar, QToolBar
from PyQt5.QtGui import QIcon

class C_MenuToolBar(QDockWidget):
    def __init__(self, MainWin = None):

        QDockWidget.__init__(self)

        self.MainMenu = QMenuBar()

        if MainWin != None:
            self.MainWin = MainWin
            self.MainMenu = self.MainWin.menuBar()

        self.MainMenu.setObjectName("MenuApp")

        ########################################################################################################

        # ******* Actions the Power System Network Menu  *******
        self.NetActRef = {'Net_Select_Act': 0
                           #'OpnFileAct': 0,
                           #'SavFileAct': 0
                           }

        # ******* Create the Power System Network Menu *******
        self.NetMenu = self.MainMenu.addMenu('&Rede')

        self.Net_Select_Act = QAction(QIcon('img/icon_opennet.png'), 'Seleciona a Rede', self)
        self.Net_Select_Act.setShortcut("Ctrl+N")
        self.Net_Select_Act.setStatusTip('Seleciona a Rede')
        self.Net_Select_Act.triggered.connect(self.exec_selectNet)
        self.Net_Select_Act.setObjectName('Net_Select_Act')
        self.NetActRef['Net_Select_Act'] = self.Net_Select_Act

        # ******* Create File Menu Items *******
        #self.OpnFileAct = QAction(QIcon('img/open.png'), 'Open File', self)
        #self.OpnFileAct.setShortcut("Ctrl+O")
        #self.OpnFileAct.setStatusTip('Open an Existing Project File')
        #self.OpnFileAct.triggered.connect(self.OpenProjFile)
        #self.Net_select_ActRef['OpnFileAct'] = self.OpnFileAct

        #self.SavFileAct = QAction(QIcon('img/save.png'), 'Save File', self)
        #self.SavFileAct.setShortcut("Ctrl+S")
        #self.SavFileAct.setStatusTip('Save Current Project File')
        #self.SavFileAct.triggered.connect(self.SaveProjFile)
        #self.Net_select_MenuActRef['SavFileAct'] = self.SavFileAct
        
        # ******* Setup the Configuration Menu *******
        self.NetMenu.addAction(self.Net_Select_Act)

        ########################################################################################################
        
        # ******* Actions the OpenDSS Menu  *******
        self.OpenDSSActRef = {'OpenDSS_Config_Act': 0, # Configurar o OpenDSS
                              'OpenDSS_Run_Act': 0,  # Configurar o OpenDSS
                              'OpenDSS_InsertEnergyMeter_Act': 0, # Inserir o Energy Meter
                              'OpenDSS_InsertEnergyMonitor_Act': 0,  # Inserir o Energy Meter
                              'OpenDSS_Create_Act': 0, # Criar Arquivo .DSS
                              'OpenDSS_Save_Act': 0,
                              'OpenDSS_View_Act': 0,} # Salvar Arquivo .DSS

        # ******* Create the OpenDSSuration Menu *******
        self.OpenDSSMenu = self.MainMenu.addMenu('&OpenDSS')

        # ******* Create OpenDSSMenu Items *******
        self.OpenDSS_Config_Act = QAction(QIcon('img/icon_opendss_config.png'), '&Configurar', self)
        self.OpenDSS_Config_Act.setShortcut("F2")
        self.OpenDSS_Config_Act.setStatusTip('Configurar o OpenDSS')
        self.OpenDSS_Config_Act.triggered.connect(self.exec_configDSS)
        self.OpenDSS_Config_Act.setObjectName('OpenDSS_Config_Act')
        self.OpenDSSActRef['OpenDSS_Config_Act'] = self.OpenDSS_Config_Act

        self.OpenDSS_Run_Act = QAction(QIcon('img/icon_opendss_run.png'), '&Executar (Solve)', self)
        self.OpenDSS_Run_Act.setShortcut("F3")
        self.OpenDSS_Run_Act.setStatusTip('Executar o OpenDSS')
        self.OpenDSS_Run_Act.triggered.connect(self.exec_OpenDSS)
        self.OpenDSS_Run_Act.setObjectName('OpenDSS_Run_Act')
        self.OpenDSSActRef['OpenDSS_Run_Act'] = self.OpenDSS_Run_Act

        self.OpenDSS_InsertEnergyMeter_Act = QAction(QIcon('img/icon_opendss_energymeter.png'), 'Energy &Meter', self)
        self.OpenDSS_InsertEnergyMeter_Act.setShortcut("")
        self.OpenDSS_InsertEnergyMeter_Act.setStatusTip('Inserir Energy Meter na Rede')
        self.OpenDSS_InsertEnergyMeter_Act.triggered.connect(self.exec_InsertEnergyMeter)
        self.OpenDSS_InsertEnergyMeter_Act.setObjectName('OpenDSS_InsertEnergyMeter_Act')
        self.OpenDSSActRef['OpenDSS_InsertEnergyMeter_Act'] = self.OpenDSS_InsertEnergyMeter_Act
        
        self.OpenDSS_InsertEnergyMonitor_Act = QAction(QIcon('img/icon_opendss_energymeter.png'), 'Energy &Monitor', self)
        self.OpenDSS_InsertEnergyMonitor_Act.setShortcut("")
        self.OpenDSS_InsertEnergyMonitor_Act.setStatusTip('Inserir Energy Meter na Rede')
        self.OpenDSS_InsertEnergyMonitor_Act.triggered.connect(self.exec_InsertEnergyMonitor)
        self.OpenDSS_InsertEnergyMonitor_Act.setObjectName('OpenDSS_InsertEnergyMonitor_Act')
        self.OpenDSSActRef['OpenDSS_InsertEnergyMonitor_Act'] = self.OpenDSS_InsertEnergyMonitor_Act


        self.OpenDSS_Create_Act = QAction(QIcon('img/icon_opendss.png'), '&Gerar Arquivo .DSS', self)
        self.OpenDSS_Create_Act.setShortcut("Ctrl+Shift+G")
        self.OpenDSS_Create_Act.setStatusTip('Gerar Arquivo .DSS para o OpenDSS')
        self.OpenDSS_Create_Act.triggered.connect(self.exec_createFileDSS)
        self.OpenDSS_Create_Act.setObjectName('OpenDSS_Create_Act')
        self.OpenDSSActRef['OpenDSS_Create_Act'] = self.OpenDSS_Create_Act

        self.OpenDSS_Save_Act = QAction(QIcon('img/icon_save.png'), '&Salvar Arquivo .DSS', self)
        self.OpenDSS_Save_Act.setShortcut("Ctrl+Shift+S")
        self.OpenDSS_Save_Act.setStatusTip('Salvar Arquivo .DSS para o OpenDSS')
        self.OpenDSS_Save_Act.triggered.connect(self.exec_saveFileDSS)
        self.OpenDSS_Save_Act.setObjectName('OpenDSS_Save_Act')
        self.OpenDSSActRef['OpenDSS_Save_Act'] = self.OpenDSS_Save_Act

        self.OpenDSS_View_Act = QAction(QIcon('img/icon_opendss_view.png'), '&Visualizar Arquivo .DSS', self)
        self.OpenDSS_View_Act.setShortcut("Ctrl+Shift+V")
        self.OpenDSS_View_Act.setStatusTip('Visualizar o Arquivo .DSS para o OpenDSS')
        self.OpenDSS_View_Act.triggered.connect(self.exec_viewFileDSS)
        self.OpenDSS_View_Act.setObjectName('OpenDSS_View_Act')
        self.OpenDSSActRef['OpenDSS_View_Act'] = self.OpenDSS_View_Act

        # ******* Setup the OpenDSS Menu *******
        self.OpenDSSMenu.addAction(self.OpenDSS_Config_Act)
        self.OpenDSSMenu.addAction(self.OpenDSS_Run_Act)
        self.OpenDSSMenu.addSeparator()
        self.OpenDSSMenuSubInsert = self.OpenDSSMenu.addMenu(QIcon('img/icon_opendss_insert_equip.png'),
                                                              'Insert ')
        self.OpenDSSMenuSubInsert.addAction(self.OpenDSS_InsertEnergyMeter_Act)
        self.OpenDSSMenuSubInsert.addAction(self.OpenDSS_InsertEnergyMonitor_Act)
        self.OpenDSSMenuSubProcess = self.OpenDSSMenu.addMenu(QIcon('img/icon_opendss_subprocess.png'),
                                                              'Sub-processos ')
        self.OpenDSSMenuSubProcess.addAction(self.OpenDSS_Create_Act)
        self.OpenDSSMenuSubProcess.addAction(self.OpenDSS_Save_Act)
        self.OpenDSSMenu.addSeparator()
        self.OpenDSSMenu.addAction(self.OpenDSS_View_Act)

        ########################################################################################################

        # ******* Actions the Window Menu  *******
        self.WindowActRef = {'Window_show_table_Act': 0,
                             'Window_show_map_Act': 0}

        # ******* Create the Windowuration Menu *******
        self.WindowMenu = self.MainMenu.addMenu('&Janela')

        self.Window_show_table_Act = QAction(QIcon('img/icon_results.png'), '&Visualizar Resultados em Tabela', self)
        self.Window_show_table_Act.setShortcut("Ctrl+Alt+J")
        self.Window_show_table_Act.setStatusTip('Visualizar Resultados em Tabela')
        self.Window_show_table_Act.triggered.connect(self.exec_showTableResults)
        self.Window_show_table_Act.setObjectName('Window_show_table_Act')
        self.WindowActRef['Window_show_table_Act'] = self.Window_show_table_Act

        # ******* Create WindowMenu Items *******
        
        self.Window_show_map_Act = QAction(QIcon('img/icon_map.png'), '&Visualizar Mapa', self)
        self.Window_show_map_Act.setShortcut("Ctrl+Alt+F")
        self.Window_show_map_Act.setStatusTip('Visualizar Mapa')
        self.Window_show_map_Act.triggered.connect(self.exec_showNetMap)
        self.Window_show_map_Act.setObjectName('Window_show_map_Act')
        self.WindowActRef['Window_show_map_Act'] = self.Window_show_map_Act


        # ******* Setup the Window Menu *******
        self.WindowMenu.addAction(self.Window_show_table_Act)
        self.WindowMenu.addAction(self.Window_show_map_Act)

        ########################################################################################################

        # ******* Actions the Configuration Menu  *******
        self.ConfigActRef = {'Config_BDGD_Act': 0,
                             'Connect_BDGD_Act': 0}

        # ******* Create the Configuration Menu *******
        self.ConfigMenu = self.MainMenu.addMenu('&Configuração')
        self.Config_BDGD_Act = QAction(QIcon('img/icon_opendatabase.png'), 'Configurar o BDGD', self)
        self.Config_BDGD_Act.setShortcut("Ctrl+Alt+D")
        self.Config_BDGD_Act.setStatusTip('Configura a Conexão com o Banco de Dados BDGD')
        self.Config_BDGD_Act.triggered.connect(self.exec_configBDGD)
        self.Config_BDGD_Act.setObjectName('Config_BDGD_Act')
        self.ConfigActRef['Config_BDGD_Act'] = self.Config_BDGD_Act

        self.Connect_BDGD_Act = QAction(QIcon('img/icon_database_connect.png'), 'Conectar ao BDGD', self)
        self.Connect_BDGD_Act.setShortcut("Ctrl+Alt+C")
        self.Connect_BDGD_Act.setStatusTip('Conecta ao BDGD')
        self.Connect_BDGD_Act.triggered.connect(self.exec_connBDGD)
        self.Connect_BDGD_Act.setObjectName('Connect_BDGD_Act')
        self.ConfigActRef['Connect_BDGD_Act'] = self.Connect_BDGD_Act



        # ******* Create Configuration Menu Items *******

        # ******* Setup the Configuration Menu *******
        self.ConfigMenu.addAction(self.Connect_BDGD_Act)
        self.ConfigMenu.addAction(self.Config_BDGD_Act)


        ########################################################################################################

        # ******* Actions the Help Menu  *******
        self.HelpActRef = {'Help_About_Act': 0}

        # ******* Create the Help Menu *******
        self.HelpMenu = self.MainMenu.addMenu('&Ajuda')
        self.Help_About_Act = QAction(QIcon('img/logo.png'), 'So&bre', self)
        self.Help_About_Act.setShortcut("Ctrl+H")
        self.Help_About_Act.setStatusTip('Sobre o SIPLA')
        self.Help_About_Act.triggered.connect(self.exec_aboutSIPLA)
        self.Help_About_Act.setObjectName('Help_About_Act')
        self.HelpActRef['Help_About_Act'] = self.Help_About_Act

        # ******* Create Help  Menu Items *******

        # ******* Setup the Help Menu *******
        self.HelpMenu.addAction(self.Help_About_Act)

        if MainWin != None:
            self.InitToolBar(MainWin)

    def InitToolBar(self, MainWin = None):

            # Dynamically Add Items to the Toolbar

            self.mainToolBar = MainWin.addToolBar("Acesso Rápido")

            self.mainToolBar.setObjectName("ToolBarApp")

            # This represents reading these values in via a Query
            toolBarNetworkLayout =  {0: 'Net_Select_Act',
                                     1: 'Spacer'}

            for idx in toolBarNetworkLayout:
                item = toolBarNetworkLayout[idx]

                if item == 'Spacer':
                    self.mainToolBar.addSeparator()
                else:
                    self.mainToolBar.addAction(self.NetActRef[item])


            # Dynamically Add Items to the Toolbar

            # This represents reading these values in via a Query
            toolBarOpenDSSLayout =  {0: 'OpenDSS_Create_Act',
                                     1: 'Spacer',
                                     2: 'OpenDSS_Save_Act'}

            for idx in toolBarOpenDSSLayout:
                item = toolBarOpenDSSLayout[idx]

                if item == 'Spacer':
                    self.mainToolBar.addSeparator()
                else:
                    self.mainToolBar.addAction(self.OpenDSSActRef[item])

            # Dynamically Add Items to the Toolbar

            # This represents reading these values in via a Query
            #toolBarInsertEquipamentLayout =  {0: 'OpenDSS_Create_Act',
            #                         1: 'Spacer',
            #                         }

            #for idx in toolBarInsertEquipamentLayout :
            #    item = toolBarInsertEquipamentLayout [idx]

            #    if item == 'Spacer':
            #        self.mainToolBar.addSeparator()
            #    else:
            #        self.mainToolBar.addAction(self.OpenDSSActRef[item])



    def exec_selectNet(self): #self.metodo_CARREGAMENTO_DE_REDE
        self.Actions.showDockNetPanel()

    def exec_configBDGD(self):
        self.Actions.configDataBase()

    def exec_connBDGD(self):
        self.Actions.connectDataBase()

    def exec_showTableResults(self): #self.metodo_VISUALIZAR_RESULTADOS_POR_TABELA)
        self.Actions.showDockResultsPanel()

    def exec_showNetMap(self):  #  self.metodo_VISUALIZADOR_DE_REDE_CARREGADA
        print("Visualizar a Rede")

    ###################################################################
    ### OpenDSS
    ###################################################################

    def exec_configDSS(self):
        self.Actions.exec_configOpenDSS_Settings()

    def exec_OpenDSS(self):
        self.Actions.execOpenDSS()

    def exec_InsertEnergyMeter(self):
        self.Actions.execInsertEnergyMeter()

    def exec_InsertEnergyMonitor(self):
        self.Actions.execInsertEnergyMonitor()

    def exec_createFileDSS(self):
        self.Actions.execCreateDSS()
        
    def exec_saveFileDSS(self):
        self.Actions.saveOpenDSS()

    def exec_viewFileDSS(self):
        print("Visualizar o Arquivo do OpenDSS")


    ####################################################################

    def exec_aboutSIPLA(self):
        print("Sobre o SIPLA")




