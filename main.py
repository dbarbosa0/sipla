from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWebEngineWidgets import*

from class_database import C_DBase
from class_maps_view import C_MapsViewer
from class_exception import C_Error, ConnDataBaseError
from class_dialog_opendss import C_Dialog_OpenDSS

import sys
import platform
import sip


__version__ = "0.0.1"



class Janela_principal(QMainWindow):
    
    def __init__(self):

        super(Janela_principal, self).__init__()

        self.nome_da_janela  = "SIPLA - Version: " + __version__
        self.icone_da_janela = "Imagens/logo.png"
        self.stylesheet = "fusion"

        self.initUI()

    def initUI(self):
        
        ### Variáveis Importantes
        self.acessDataBase = C_DBase() #Acesso ao Banco de Dados
        self.mapsViewer = C_MapsViewer() #Visualização do Mapa
        self.opendssDiag = C_Dialog_OpenDSS() #Carrengando o OpenDSS
        

        self.setWindowTitle(self.nome_da_janela)
        self.setWindowIcon(QIcon(self.icone_da_janela))
        geometria =  QApplication.desktop().availableGeometry()
#        self.setGeometry(0, 0, int(geometria.width()), int(geometria.height()))
        qtRectangle = self.frameGeometry()
        #centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qtRectangle.topLeft())

        #self.resize(QDesktopWidget().availableGeometry().width()* 0.7, QDesktopWidget().availableGeometry().height()* 0.7 )

        self.resize(1366, 768)

        #self.showMaximized()

        self.status_1 = QLabel("Status: Off-Line")
        self.status_1.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.statusBar().addPermanentWidget(QFrame())
        self.statusBar().addPermanentWidget(self.status_1)

        self.status_2 = QLabel("Fluxo: ")
        self.status_2.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.statusBar().addPermanentWidget(QFrame())
        self.statusBar().addPermanentWidget(self.status_2)

        self.status_3 = QLabel(platform.system())
        self.status_3.setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.statusBar().addPermanentWidget(QFrame())
        self.statusBar().addPermanentWidget(self.status_3)

        self.statusBar().setStyleSheet('border: 0; background-color: #DCDCDC;')
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}")

        self.statusBar().addPermanentWidget(self.statusBar().showMessage("SIPLA  " + __version__))

        self.metodo_ACAO()
        self.metodo_MENU()
        self.metodo_BARRA_DE_FERRAMENTAS()

        self.metodo_VISUALIZADOR()

        widget = QWidget()
        self.setCentralWidget(widget)
        layout_principal = QGridLayout()
        layout_principal.setContentsMargins(1,1,1,1)
        layout_principal.addWidget(self.Visual_GroupBox ,0,0,1,1)
        widget.setLayout(layout_principal)


    def metodo_ACAO(self):
        self.acao_carregamento_de_rede = QAction(QIcon("Imagens/openrede.png"), "&Carregamento de rede", self,
            shortcut=(""), statusTip="Carregamento de rede",
            triggered = self.metodo_CARREGAMENTO_DE_REDE)
        self.acao_visualizar_rede = QAction(QIcon("Imagens/insertequipe.png"), "&Visualizar rede carregada", self,
            shortcut=(""), statusTip="Visualizar rede carregada",
            triggered = self.metodo_VISUALIZADOR_DE_REDE_CARREGADA)
        self.acao_resultados_por_tabela = QAction(QIcon("Imagens/resultados.png"), "&Visualizar resultados em tabela", self,
            shortcut=(""), statusTip="Visualizar resultados",
            triggered = self.metodo_VISUALIZAR_RESULTADOS_POR_TABELA)

        ###############################
        self.acao_executar_opendss = QAction(QIcon("Imagens/resultados.png"), "&Gerar .dss", self,
                                             shortcut=(""), statusTip="Gerar Arquivo para OpenDSS",
                                             triggered=self.metodo_EXECUTAR_OPENDSS)
        self.acao_salvar_opendss = QAction(QIcon("Imagens/resultados.png"), "&Salvar .dss", self,
                                             shortcut=(""), statusTip="Salvar Arquivo para OpenDSS",
                                             triggered=self.metodo_SALVAR_OPENDSS)

    def metodo_MENU(self):
        menu = self.menuBar()
        rede_de_alta = menu.addMenu('&Rede')
        rede_de_alta.addAction(self.acao_carregamento_de_rede)
        resultados = menu.addMenu('&Resultados')
        resultados.addAction(self.acao_resultados_por_tabela)

        ################################
        menu_item_opendss = menu.addMenu('&OpenDSS')
        menu_item_opendss.addAction(self.acao_executar_opendss)
        menu_item_opendss.addAction(self.acao_salvar_opendss)




    def metodo_BARRA_DE_FERRAMENTAS(self):
        barra_de_ferramentas_rede = self.addToolBar("Rede")
        barra_de_ferramentas_rede.addAction(self.acao_carregamento_de_rede)
        barra_de_ferramentas_rede.addAction(self.acao_visualizar_rede)
        barra_de_ferramentas_resultados_por_tabela = self.addToolBar("Resultados")
        barra_de_ferramentas_resultados_por_tabela.addAction(self.acao_resultados_por_tabela)

    def metodo_CARREGAMENTO_DE_REDE(self):

        #Verificando se já existe, permitindo apenas uma vez

        if not hasattr(self, 'carregamento_de_rede_GroupBox'):
            #Definindo o Banco de Dados
            try:
                if self.acessDataBase.setBDGD():
                    self.status_1.setText("Status: On-Line")
                else:
                    raise ConnDataBaseError("Erro de conexão com o Banco de Dados")

                ##Grupo
                self.carregamento_de_rede_QDockWidget = QDockWidget("Dados da Rede", self)
                self.carregamento_de_rede_GroupBox = QGroupBox()
                self.layout_do_carregamento_de_rede_QDockWidget = QFormLayout()
                self.carregamento_de_rede_QDockWidget.setWidget(self.carregamento_de_rede_GroupBox)
                self.addDockWidget(Qt.LeftDockWidgetArea, self.carregamento_de_rede_QDockWidget)
                self.CONFIGURACAO_GroupBox = QGroupBox("&Configuração")
                self.layout_CONFIGURACAO_GroupBox = QGridLayout()

                ## Carregando as subestações de Alta tensão
                self.tmp_QComboBox = QComboBox(self)
                self.tmp_QComboBox.clear()
                self.tmp_QComboBox.addItems(self.getSE_AT())

                ######

                self.lista_de_nomes_das_subestacoes_de_alta_tensao_disponiveis_ComboBox = self.tmp_QComboBox
                self.btn_confirma_subestacao_de_alta_PushButton=QPushButton("Ok")
                self.btn_confirma_subestacao_de_alta_PushButton.setFixedWidth(30)
                self.btn_confirma_subestacao_de_alta_PushButton.clicked.connect(self.metodo_INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA)
                self.layout_CONFIGURACAO_GroupBox.addWidget(QLabel("SE - Alta Tensão"), 1, 0, 1, 1)
                self.layout_CONFIGURACAO_GroupBox.addWidget(self.lista_de_nomes_das_subestacoes_de_alta_tensao_disponiveis_ComboBox, 1, 1, 1, 1)
                self.layout_CONFIGURACAO_GroupBox.addWidget(self.btn_confirma_subestacao_de_alta_PushButton, 1, 2, 1, 1)

                self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox = QComboBox(self)
                self.btn_confirma_subestacao_de_alta_PushButton=QPushButton("Ok")
                self.btn_confirma_subestacao_de_alta_PushButton.setFixedWidth(30)
                self.btn_confirma_subestacao_de_alta_PushButton.clicked.connect(self.metodo_INFORMA_SUBESTACAO_DE_MEDIA)
                self.layout_CONFIGURACAO_GroupBox.addWidget(QLabel("Circuito"), 2, 0, 1, 1)
                self.layout_CONFIGURACAO_GroupBox.addWidget(self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox, 2, 1, 1, 1)
                self.layout_CONFIGURACAO_GroupBox.addWidget(self.btn_confirma_subestacao_de_alta_PushButton, 2, 2, 1, 1)

                ##################

                self.lista_de_nomes_das_subestacoes_de_media_tensao_disponiveis_ComboBox = QComboBox(self)
                self.btn_confirma_subestacao_de_media_PushButton=QPushButton("Ok")
                self.btn_confirma_subestacao_de_media_PushButton.setFixedWidth(30)
                self.btn_confirma_subestacao_de_media_PushButton.clicked.connect(self.metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO)
                self.btn_confirma_subestacao_de_media_PushButton.setEnabled(False)
                self.layout_CONFIGURACAO_GroupBox.addWidget(QLabel("SE - média tensão"), 3, 0, 1, 1)
                self.layout_CONFIGURACAO_GroupBox.addWidget(self.lista_de_nomes_das_subestacoes_de_media_tensao_disponiveis_ComboBox, 3, 1, 1, 1)
                self.layout_CONFIGURACAO_GroupBox.addWidget(self.btn_confirma_subestacao_de_media_PushButton, 3, 2, 1, 1)


                self.CONFIGURACAO_GroupBox.setLayout(self.layout_CONFIGURACAO_GroupBox)

                self.ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox = QGroupBox("&Alimentadores")
                self.layout_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox = QVBoxLayout()
                self.btn_limpar_layout_PushButton = QPushButton("Redefinir")
                self.btn_limpar_layout_PushButton.setFixedWidth(80)
                self.btn_limpar_layout_PushButton.clicked.connect(self.metodo_LIMPAR_LAYOUT_ALIMENTADORES)
                self.layout_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox.addWidget(self.btn_limpar_layout_PushButton)
                self.ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox.setLayout(self.layout_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox)

                self.layout_do_carregamento_de_rede_QDockWidget.addRow(self.CONFIGURACAO_GroupBox)
                self.layout_do_carregamento_de_rede_QDockWidget.addRow(self.ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox)

                self.carregamento_de_rede_GroupBox.setLayout(self.layout_do_carregamento_de_rede_QDockWidget)

            except ConnDataBaseError:
                pass
        else:
            self.carregamento_de_rede_QDockWidget.show()
            
        
        
    ################### Acesso ao Banco de Dados ################################    
    def getSE_AT(self):
         return self.acessDataBase.getSE_AT_DB()
     
    def getSE_MT(self,nomeSE_AT):
        return self.acessDataBase.getSE_MT_DB(nomeSE_AT)
    
    def getSE_MT_AL(self,nomeSE_MT):
        return self.acessDataBase.getSE_MT_AL_DB(nomeSE_MT)
    
    ################### Get Seleção do ComboBox ################################    
    
    def metodo_PASSA_O_NOME_DO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO(self):
        if self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox.currentText():
            nome_do_circuito_alta_para_media = self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox.currentText()
            return nome_do_circuito_alta_para_media
        
    def metodo_PASSA_O_NOME_DO_CIRCUITO_DE_ALTA_SELECIONADO(self):
        if self.lista_de_nomes_das_subestacoes_de_alta_tensao_disponiveis_ComboBox.currentText():
            circuito_de_alta_para_media_selecionado = self.lista_de_nomes_das_subestacoes_de_alta_tensao_disponiveis_ComboBox.currentText()
            return circuito_de_alta_para_media_selecionado
        
    def metodo_INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA(self):
        
        circuito_de_alta_para_media_selecionado = self.metodo_PASSA_O_NOME_DO_CIRCUITO_DE_ALTA_SELECIONADO()
        
        self.acesso_a_circuitos_de_alta_para_media = self.getSE_MT(circuito_de_alta_para_media_selecionado)
        
        self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox.clear()
        
        self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox.addItems(self.acesso_a_circuitos_de_alta_para_media)

    def metodo_PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO(self):
        
        if self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox.currentText():
            
            subestacao_de_media_tensao_associada_ao_circuito_alta_para_media = [self.lista_de_nomes_dos_circuitos_de_alta_para_media_disponiveis_ComboBox.currentText()[-3:]]
            
            subestacao_de_media_tensao_selecionada = subestacao_de_media_tensao_associada_ao_circuito_alta_para_media
            
            return subestacao_de_media_tensao_selecionada
        
    def metodo_INFORMA_SUBESTACAO_DE_MEDIA(self):
        
        self.lista_de_nomes_das_subestacoes_de_media_tensao_disponiveis_ComboBox.clear()
        
        self.btn_confirma_subestacao_de_media_PushButton.setEnabled(True)
        
        try:
            self.lista_de_nomes_das_subestacoes_de_media_tensao_disponiveis_ComboBox.addItems(self.metodo_PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO())
        except TypeError:
                pass

    def metodo_INFORMA_ALIMENTADORES_DE_MEDIA(self):
        
        subestacao_de_media_tensao_selecionada = self.metodo_PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO()
        
        return self.getSE_MT_AL(subestacao_de_media_tensao_selecionada)
        

    def metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO(self):

        if not hasattr(self, 'ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox'):
        
            self.btn_confirma_subestacao_de_media_PushButton.setEnabled(False)
            self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox = QGroupBox("Escolha alimentadores disponíveis:")

            self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO = QFormLayout()

            ####

            self.label_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO  = QLabel("Alimentadores Selecionados: ")
            self.btn_confirma_alimentadores_selecionados_PushButton=QPushButton("Selecionar")
            self.btn_confirma_alimentadores_selecionados_PushButton.clicked.connect(self.metodo_ATIVA_CONFIGURAR_VISUALIZACAO_DE_ALIMENTADORES)
            self.btn_confirma_alimentadores_selecionados_PushButton.setFixedWidth(100)
            layoutV_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO = QVBoxLayout(self)
            layoutV_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.addLayout(self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO)
            layoutV_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.addWidget(self.btn_confirma_alimentadores_selecionados_PushButton)
            self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox.setLayout(layoutV_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO)

            self.layout_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_GroupBox.addWidget(self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox)

        else:

            self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox.show()

        item_alimentador = self.metodo_INFORMA_ALIMENTADORES_DE_MEDIA()

        nAlimentadores = len(item_alimentador)
        #pegando os já existentes
        alimQComboBox = (self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.itemAt(u).widget()
                   for u in range(self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.count()))

        alimExist = []
        for wCheckBox in alimQComboBox:
            alimExist.append(wCheckBox.text())

        for ctdAlim in range(0, nAlimentadores):
            if not item_alimentador[ctdAlim] in alimExist:
                self.checkbox = QCheckBox(format(str(item_alimentador[ctdAlim])))
                self.checkbox.setCheckState(Qt.Unchecked)
                self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.addWidget(self.checkbox)
                self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.setAlignment(Qt.AlignLeft)

    def metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS(self):
        lista_de_alimentadores_selecionados_check_list = []
        for i in range(self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.count()):
            chBox = self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.itemAt(i).widget()
            if chBox.isChecked():
                lista_de_alimentadores_selecionados_check_list.append(chBox.text())
        return lista_de_alimentadores_selecionados_check_list

    def metodo_CONFIGURAR_VISUALIZACAO_DE_ALIMENTADORES(self):

        self.configuracao_de_visualizacao_QDockWidget = QDockWidget("&Configuração de visualização de rede", self)
        self.configuracao_de_visualizacao_GroupBox=QGroupBox("Circuitos selecionados")
        self.Widget_principal = QTreeWidget()
        self.layout_configuracao_de_visualizacao_QDockWidget = QFormLayout()
        self.configuracao_de_visualizacao_QDockWidget.setWidget(self.configuracao_de_visualizacao_GroupBox)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.configuracao_de_visualizacao_QDockWidget)
        self.layout_configuracao_de_visualizacao_QDockWidget.addRow(self.Widget_principal)
        self.Widget_principal.setHeaderLabels(['Alimentador', 'Cor'])
        self.configuracao_de_visualizacao_GroupBox.setLayout(self.layout_configuracao_de_visualizacao_QDockWidget)
        self.btn_confirma_rede_de_alimentadores_selecionados_PushButton=QPushButton("Carregar rede")
        self.btn_confirma_rede_de_alimentadores_selecionados_PushButton.clicked.connect(self.plotMapsViewer)
        self.btn_confirma_rede_de_alimentadores_selecionados_PushButton.setFixedWidth(100)

        self.btn_confirma_visualizacao_de_alimentadores_selecionados_QCheckBox=QCheckBox("Visualizar rede")
        self.btn_confirma_visualizacao_de_alimentadores_selecionados_QCheckBox.setChecked(True)
        self.layout_configuracao_de_visualizacao_QDockWidget.addRow(self.btn_confirma_visualizacao_de_alimentadores_selecionados_QCheckBox)
        self.layout_configuracao_de_visualizacao_QDockWidget.addRow(self.btn_confirma_rede_de_alimentadores_selecionados_PushButton)

        self.Widget_principal.setLayout(QGridLayout())

    def metodo_ATIVA_CONFIGURAR_VISUALIZACAO_DE_ALIMENTADORES(self):
        
        self.carregamento_de_rede_QDockWidget.close()
        self.metodo_CONFIGURAR_VISUALIZACAO_DE_ALIMENTADORES()
        
        try:
            self.metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS()
            alim_selecionados = self.metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS()
            cont=len(alim_selecionados)
            lista_de_cores_selecionadas =[]
            if cont > 0:
                lista=self.metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS()
                lista_de_cores_disponiveis = ["Preto", "Azul","Marron","Laranja", "Azul Escuro", "Cyan ", "Lílas", "Cinza","Rosa","Verde Escuro"]
                for i in range(0,len(lista)):
                     self.conjunto_alimentador_cor = QTreeWidgetItem(self.Widget_principal, [lista[i], lista_de_cores_disponiveis[i]])

#            self.metodo_LIMPAR_LAYOUT_ALIMENTADORES()
            return lista_de_cores_selecionadas
        except:
             pass

    def metodo_INFORMA_ALIMENTADORES(self):
        alimentadores = self.metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS()
        return alimentadores

    def metodo_INFORMA_COR_ALIMENTADORES(self):
        lista_de_cores_selecionadas = []
        alimentadores = self.metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS()
        lista_de_cores_disponiveis = ["Black", "Blue","Goldenrod", "OrangeRede", "DarkBlue", "Cyan ", "DarkMagenta", "grey31","DeepPink","DarkGreen"]
        for i in range(0,len(alimentadores)):
            lista_de_cores_selecionadas.append(lista_de_cores_disponiveis[i])
        return lista_de_cores_selecionadas 


    def metodo_LIMPAR_LAYOUT_ALIMENTADORES(self):
        try:
            for i in range(len( self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO), 0, -1):
                self.layoutH_do_metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO.removeRow(i-1)

            #sip.delete(self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox)
            #self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox = None
            self.ESCOLHA_DE_ALIMENTADORES_DE_MEDIA_TENSAO_GroupBox.close()
            self.btn_confirma_subestacao_de_media_PushButton.setEnabled(True)
        except RuntimeError:
            print("Layout já se encontra limpo !")


    def metodo_VISUALIZADOR(self):

        self.Visual_GroupBox = QGroupBox("Visualizador")
        self.visualWebView = QWebEngineView()
        self.layout_Visual_GroupBox = QGridLayout()
        self.layout_Visual_GroupBox.addWidget(self.visualWebView, 0, 0)
        self.Visual_GroupBox.setLayout(self.layout_Visual_GroupBox)

    def metodo_VISUALIZADOR_DE_REDE_CARREGADA(self):
        
        self.mapsViewer.viewMap()
        
    def metodo_fechar(self):
        self.visualWebView.setVisible(False) 


    def metodo_VISUALIZAR_RESULTADOS_POR_TABELA(self):

        #Verificando se já existe, permitindo apenas uma vez

        if not hasattr(self, 'tabela_de_grandezas_QDockWidget'):

            self.tabela_de_grandezas_QDockWidget = QDockWidget("Resultados", self)
            self.tabela_de_grandezas_GroupBox=QGroupBox("Grandezas Elétricas")

            self.layout_tabela_de_grandezas_QDockWidget = QFormLayout()
            self.tabela_de_grandezas_QDockWidget.setWidget(self.tabela_de_grandezas_GroupBox)
            self.addDockWidget(Qt.BottomDockWidgetArea, self.tabela_de_grandezas_QDockWidget)

            self.TabWidget_principal = QTabWidget()
    #        self.TabWidget_principal.setSizePolicy(QSizePolicy.Preferred,
    #                QSizePolicy.Ignored)

            tab1 = QWidget()

            self.tableWidget = QTableWidget(15, 15)

            tab1hbox = QHBoxLayout()
            tab1hbox.setContentsMargins(5, 5, 5, 5)
            tab1hbox.addWidget(self.tableWidget)
            tab1.setLayout(tab1hbox)

            tab11 = QWidget()
            self.tableWidget1 = QTableWidget(15, 15)

            tab11hbox = QHBoxLayout()
            tab11hbox.setContentsMargins(5, 5, 5, 5)
            tab11hbox.addWidget(self.tableWidget1)
            tab11.setLayout(tab11hbox)


            tab111 = QWidget()
            self.tableWidget11 = QTableWidget(15, 15)

            tab111hbox = QHBoxLayout()
            tab111hbox.setContentsMargins(5, 5, 5, 5)
            tab111hbox.addWidget(self.tableWidget11)
            tab111.setLayout(tab111hbox)

            tab1111 = QWidget()
            self.tableWidget111 = QTableWidget(15, 15)

            tab1111hbox = QHBoxLayout()
            tab1111hbox.setContentsMargins(5, 5, 5, 5)
            tab1111hbox.addWidget(self.tableWidget111)
            tab1111.setLayout(tab1111hbox)

            tab11111 = QWidget()
            self.tableWidget1111 = QTableWidget(15, 15)

            tab11111hbox = QHBoxLayout()
            tab11111hbox.setContentsMargins(5, 5, 5, 5)
            tab11111hbox.addWidget(self.tableWidget1111)
            tab11111.setLayout(tab11111hbox)

            self.TabWidget_principal.addTab(tab1, " &Tensão de Fase Nodal")
            self.TabWidget_principal.addTab(tab11, " &Tensão de Sequência")
            self.TabWidget_principal.addTab(tab111, " &Potencia por Elemento")
            self.TabWidget_principal.addTab(tab1111, " &Potência por Fase")
            self.TabWidget_principal.addTab(tab11111, " &Potência por Sequência de Fase")

            self.layout_tabela_de_grandezas_QDockWidget.addRow(self.TabWidget_principal)

            self.tabela_de_grandezas_GroupBox.setLayout(self.layout_tabela_de_grandezas_QDockWidget)
        else:
            self.tabela_de_grandezas_QDockWidget.show()

    def plotMapsViewer(self):
        if self.btn_confirma_visualizacao_de_alimentadores_selecionados_QCheckBox.isChecked():
       
            self.mapsViewer.setDataBase(self.acessDataBase)
            self.mapsViewer.setFieldColors(self.metodo_INFORMA_COR_ALIMENTADORES())
            self.mapsViewer.setFields(self.metodo_INFORMA_ALIMENTADORES())
            self.mapsViewer.setSE_MT(self.metodo_PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO())
            self.mapsViewer.setWebView (self.visualWebView)
            self.mapsViewer.createMap()  
            
            self.metodo_VISUALIZADOR_DE_REDE_CARREGADA()        
        else:
            print("funcionou sem visualizar")
            self.btn_confirma_rede_de_alimentadores_selecionados_PushButton.setEnabled(False)
        
    def metodo_EXECUTAR_OPENDSS(self):
        print(self.acessDataBase.getBDGD())
        self.opendssDiag.setDirDataBase(self.acessDataBase.getBDGD())
        self.opendssDiag.setCircuitoAT_MT(self.metodo_PASSA_O_NOME_DO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO())
        self.opendssDiag.setSE_MT_Selecionada(self.metodo_PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO())
        self.opendssDiag.setFields_SE_MT_Selecionada(self.metodo_LISTA_DE_ALIMENTADORES_SELECIONADOS())
        self.opendssDiag.createFile()

    def metodo_SALVAR_OPENDSS(self):
        self.opendssDiag.exec_CRIAR_ARQUIVO_NO_FORMATO_OPENDSS()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    janela = Janela_principal()
    janela.show()
    sys.exit(app.exec_())






#a = Janela_principal()
