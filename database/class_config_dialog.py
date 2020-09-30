from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QFileDialog, QGroupBox, QHBoxLayout,\
    QPushButton, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QMessageBox
from PyQt5.QtCore import Qt

import configparser
import class_exception
import config as cfg
import os
import platform

class C_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Database Settings"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.databaseInfo = {}

        self.DBPRODIST = ["CTAT", "EQTRM", "SSDMT", "UNREMT", "UNTRS", "CTMT", "EQTRS", "UCBT", "UNSEAT", "EQSE", \
                          "RAMLIG", "UCMT", "UNSEMT", "EQTRD", "SEGCON", "UNCRMT", "UNCRBT", "UNTRD"]


        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()


        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ##### Option DataBase
        self.Conn_GroupBox = QGroupBox("Método de Conexão com o BDGD")
        self.Conn_GroupBox_Layout = QHBoxLayout()

        self.Conn_GroupBox_Radio_Sqlite = QRadioButton("Local - SQLite")
        self.Conn_GroupBox_Radio_Sqlite.setChecked(True)
        self.Conn_GroupBox_Layout.addWidget(self.Conn_GroupBox_Radio_Sqlite)

        self.Conn_GroupBox_Radio_Mysql = QRadioButton("MySQL")
        self.Conn_GroupBox_Radio_Mysql.setChecked(False)
        self.Conn_GroupBox_Radio_Mysql.setEnabled(False)
        self.Conn_GroupBox_Layout.addWidget(self.Conn_GroupBox_Radio_Mysql)

        self.Conn_GroupBox.setLayout(self.Conn_GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.Conn_GroupBox)


        #### Grupo do Sqlite
        self.Conn_GroupBox_Sqlite = QGroupBox("Conexão Local")
        self.Conn_GroupBox_Sqlite_Layout = QHBoxLayout()

        self.Conn_GroupBox_Sqlite_Label = QLabel("Diretório:")
        self.Conn_GroupBox_Sqlite_Layout.addWidget(self.Conn_GroupBox_Sqlite_Label)
        self.Conn_GroupBox_Sqlite_Edit = QLineEdit()
        self.Conn_GroupBox_Sqlite_Edit.setMinimumWidth(300)
        self.Conn_GroupBox_Sqlite_Edit.setEnabled(False)
        self.Conn_GroupBox_Sqlite_Layout.addWidget(self.Conn_GroupBox_Sqlite_Edit)

        self.Conn_GroupBox_Sqlite_Btn = QPushButton()
        self.Conn_GroupBox_Sqlite_Btn.setIcon(QIcon('img/icon_opendatabase.png'))
        self.Conn_GroupBox_Sqlite_Btn.setFixedWidth(30)
        self.Conn_GroupBox_Sqlite_Btn.clicked.connect(self.OpenDataBase)
        self.Conn_GroupBox_Sqlite_Layout.addWidget(self.Conn_GroupBox_Sqlite_Btn)

        self.Conn_GroupBox_Sqlite.setLayout(self.Conn_GroupBox_Sqlite_Layout)
        self.Dialog_Layout.addWidget(self.Conn_GroupBox_Sqlite)

        ###### Botões
        self.Dilalog_Btns_Layout = QHBoxLayout()
        self.Dilalog_Btns_Layout.setAlignment(Qt.AlignRight)

        self.Dilalog_Btns_Save_Btn = QPushButton("Salvar Parâmetros")
        self.Dilalog_Btns_Save_Btn.setIcon(QIcon('img/icon_save.png'))
        self.Dilalog_Btns_Save_Btn.setFixedWidth(170)
        self.Dilalog_Btns_Save_Btn.clicked.connect(self.saveDefaultParameters)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Save_Btn)

        self.Dilalog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dilalog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dilalog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Cancel_Btn)

        self.Dilalog_Btns_Ok_Btn = QPushButton("OK")
        self.Dilalog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dilalog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dilalog_Btns_Layout, 0)
        self.setLayout(self.Dialog_Layout)

        ####
        self.loadDefaultParameters()

    def Accept(self):
        self.loadParameters()
        self.close()

    def getConn_GroupBox_Radio_Btn(self):
        if self.Conn_GroupBox_Radio_Sqlite.isChecked():
            return "sqlite"
        elif self.Conn_GroupBox_Radio_Mysql.isChecked():
            return "mysql"

    def loadParameters(self):

        ## Geral
        self.databaseInfo["Conn"] = self.getConn_GroupBox_Radio_Btn()
        self.databaseInfo["DirDataBase"] = self.get_DirDataBaseSqlite()

    def get_DirDataBaseSqlite(self):
        dirDataBase = self.Conn_GroupBox_Sqlite_Edit.text()

        if (dirDataBase != "") and (self.checkDirDataBaseSqlite(dirDataBase)):
            return dirDataBase
        else:
            return ""

    def loadDefaultParameters(self):  # Só carrega quando abre a janela pela primeira vez
        try:
            config = configparser.ConfigParser()
            config.read('siplaconfigdatabase.ini')

            ## Default
            if config['BDGD']['Conn'] == "sqlite":
                self.Conn_GroupBox_Radio_Sqlite.setChecked(True)
            elif config['BDGD']['Conn'] == "mysql":
                self.Conn_GroupBox_Radio_Mysql.setChecked(False)

            if os.path.isdir(config['BDGD']['dir']):
                if self.checkDirDataBaseSqlite(config['BDGD']['dir']):
                    self.Conn_GroupBox_Sqlite_Edit.setText(config['BDGD']['dir'])
            else:
                self.Conn_GroupBox_Sqlite_Edit.clear()

            ##### Carregando parâmetros
            self.loadParameters()

        except:
            raise class_exception.FileDataBaseError("Configuração do Banco de Dados", "Erro ao carregar os parâmetros do Banco de Dados!")

    def saveDefaultParameters(self):
        try:
            config = configparser.ConfigParser()

            ## Load Flow
            config['BDGD']= { }
            config['BDGD']['Conn'] = self.getConn_GroupBox_Radio_Btn()
            config['BDGD']['dir'] = self.get_DirDataBaseSqlite()

            with open('siplaconfigdatabase.ini', 'w') as configfile:
                config.write(configfile)

            QMessageBox(QMessageBox.Information, "DataBase Configuration", "Configurações Salvas com Sucesso!", QMessageBox.Ok).exec()

        except:
            raise class_exception.FileDataBaseError("Configuração do Banco de Dados", "Erro ao salvar os parâmetros do Banco de Dados!")

    def OpenDataBase(self):
        # este código é executado sempre que alguém fizer
        # self.nome = value
        nameDirDataBase = str(
            QFileDialog.getExistingDirectory(None, "Selecione o Diretório com o Danco de Dados", "Banco/",
                                             QFileDialog.ShowDirsOnly))

        nameDirDataBase += "/"

        if platform.system() == "Windows":
            nameDirDataBase = nameDirDataBase.replace('/', '\\')

        if self.checkDirDataBaseSqlite(nameDirDataBase):
            self.Conn_GroupBox_Sqlite_Edit.setText(nameDirDataBase)
        else:
            self.Conn_GroupBox_Sqlite_Edit.setText("")

    def checkDirDataBaseSqlite(self, nameDirDataBase):

        msg = ''

        for ctd in self.DBPRODIST:
            if not os.path.isfile(nameDirDataBase + ctd + ".sqlite"):
                msg += ctd + ".sqlite\n"

        if msg != '':
            QMessageBox(QMessageBox.Warning, "DataBase Configuration", "Diretório não apresenta os arquivos necessários! \n" + msg,
                        QMessageBox.Ok).exec()
            return False
        else:
            return True



