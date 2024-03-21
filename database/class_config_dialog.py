from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QFileDialog, QGroupBox, QHBoxLayout,\
    QPushButton, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QMessageBox,\
    QGridLayout, QCheckBox
from PyQt5.QtCore import Qt

import configparser
import class_exception
import config as cfg
import os
import platform
import zipfile

class C_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Configuração da Base de Dados Geográfica da Distribuidora"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.databaseInfo = {}

        self.DBPRODIST2017 = ["CTAT", "EQTRM", "SSDMT", "UNREMT", "UNTRS", "CTMT", "EQTRS", "UCBT", "UNSEAT",
                              "EQSE", "RAMLIG", "UCMT", "UNSEMT", "EQTRD", "SEGCON", "UNCRMT", "UNCRBT", "UNTRD"]
        self.DBPRODIST2021 = ["CTAT", "EQTRM", "SSDMT", "UNREMT", "UNTRAT", "CTMT", "EQTRAT", "UCBT", "UNSEAT",
                              "EQSE", "RAMLIG", "UCMT", "UNSEMT", "EQTRMT", "SEGCON", "UNCRMT", "UNCRBT", "UNTRMT"]

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()


        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ##### Option DataBase
        self.GroupBox = QGroupBox("Modelo da BDGD (manual de instruções da BDGD 2021/revisão 1):")
        self.GroupBox_Layout = QGridLayout()

        self.GroupBox_Radio_Modelo_Versao_1_0 = QRadioButton("Modelo Versão 1.0 (2021)")
        self.GroupBox_Radio_Modelo_Versao_1_0.setChecked(True)
        self.GroupBox_Layout.addWidget(self.GroupBox_Radio_Modelo_Versao_1_0, 0, 0)

        self.GroupBox_Radio_Modelo_Novo = QRadioButton("Modelo Novo (2017)")
        self.GroupBox_Radio_Modelo_Novo.setChecked(False)
        self.GroupBox_Layout.addWidget(self.GroupBox_Radio_Modelo_Novo, 0, 1)

        self.GroupBox_Radio_Modelo_Antigo = QRadioButton("Modelo Antigo (2016)")
        self.GroupBox_Radio_Modelo_Antigo.setChecked(False)
        self.GroupBox_Layout.addWidget(self.GroupBox_Radio_Modelo_Antigo, 0, 2)


        self.GroupBox_Radio_check_identificar = QCheckBox("Identificar automaticamente")
        self.GroupBox_Radio_check_identificar.setChecked(True)
        self.GroupBox_Layout.addWidget(self.GroupBox_Radio_check_identificar, 1, 0)


        self.GroupBox.setLayout(self.GroupBox_Layout)
        self.Dialog_Layout.addWidget(self.GroupBox)


        #### Grupo do Sqlite
        self.GroupBox_Sqlite = QGroupBox("Conexão Local")
        self.GroupBox_Sqlite_Layout = QHBoxLayout()

        self.GroupBox_Sqlite_Label = QLabel("Diretório:")
        self.GroupBox_Sqlite_Layout.addWidget(self.GroupBox_Sqlite_Label)
        self.GroupBox_Sqlite_Edit = QLineEdit()
        self.GroupBox_Sqlite_Edit.setMinimumWidth(300)
        self.GroupBox_Sqlite_Edit.setEnabled(False)
        self.GroupBox_Sqlite_Layout.addWidget(self.GroupBox_Sqlite_Edit)

        self.GroupBox_Sqlite_Btn = QPushButton()
        self.GroupBox_Sqlite_Btn.setIcon(QIcon('img/icon_opendatabase.png'))
        self.GroupBox_Sqlite_Btn.setFixedWidth(30)
        self.GroupBox_Sqlite_Btn.clicked.connect(self.OpenDataBase)
        self.GroupBox_Sqlite_Layout.addWidget(self.GroupBox_Sqlite_Btn)

        self.GroupBox_Sqlite.setLayout(self.GroupBox_Sqlite_Layout)
        self.Dialog_Layout.addWidget(self.GroupBox_Sqlite)


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
        self.updateDialog()


        self.GroupBox_Radio_check_identificar.toggled.connect(self.updateDialog)

    def Accept(self):
        if zipfile.is_zipfile(self.get_versaoDataBaseSqlite()): #is zip file?
            window = Window_confirmacao_zip_file(self.get_DirDataBaseSqlite())
            window.show()
            window.exec_()

            self.GroupBox_Sqlite_Edit.setText(window.dir_path)
            self.Accept()
        else:
            self.loadParameters()
            self.close()


    def getGroupBox_Radio_Btn(self):
        if self.GroupBox_Radio_Modelo_Versao_1_0.isChecked():
            return "Modelo Versao 1.0"
        elif self.GroupBox_Radio_Modelo_Novo.isChecked():
            return "Modelo Novo"
        elif self.GroupBox_Radio_Modelo_Antigo.isChecked():
            return "Modelo Antigo"

    def loadParameters(self):

        ## Geral
        self.databaseInfo["Modelo"] = self.getGroupBox_Radio_Btn()
        self.databaseInfo["versao"] = self.get_versaoDataBaseSqlite()
        self.databaseInfo["Sqlite_DirDataBase"] = self.get_DirDataBaseSqlite()


    def get_DirDataBaseSqlite(self):
        dirDataBase = self.GroupBox_Sqlite_Edit.text()

        if (dirDataBase != "") and (self.checkDirDataBaseSqlite(dirDataBase, self.databaseInfo["versao"])):
            return dirDataBase
        else:
            return ""

    def get_versaoDataBaseSqlite(self):
        """
        Identifica a versão da database com base no banco de transformadores de média tensão
        """
        dirDataBase = self.GroupBox_Sqlite_Edit.text()

        if os.path.isfile(dirDataBase + "UNTRD" + ".sqlite"):
            return "2017"
        elif os.path.isfile(dirDataBase + "UNTRMT" + ".sqlite"):
            return "2021"
        else:
            return ""

    def loadDefaultParameters(self):  # Só carrega quando abre a janela pela primeira vez
        try:
            config = configparser.ConfigParser()
            config.read('siplaconfigdatabase.ini')

            ## Default
            match config['BDGD']['Modelo']:
                case "Modelo Versao 1.0":
                    self.GroupBox_Radio_Modelo_Versao_1_0.setChecked(True)
                case "Modelo Novo":
                    self.GroupBox_Radio_Modelo_Novo.setChecked(True)
                case "Modelo Antigo":
                    self.GroupBox_Radio_Modelo_Antigo.setChecked(True)

            if os.path.isdir(config['Sqlite']['dir']):
                if self.checkDirDataBaseSqlite(config['Sqlite']['dir'], config['Sqlite']['versao']):
                    self.GroupBox_Sqlite_Edit.setText(config['Sqlite']['dir'])
            else:
                self.GroupBox_Sqlite_Edit.clear()

            ##### Carregando parâmetros
            self.loadParameters()
        except:
            raise class_exception.FileDataBaseError("Configuração do Banco de Dados",
                                                    "Erro ao carregar os parâmetros do Banco de Dados!")

    def saveDefaultParameters(self):
        try:
            self.loadParameters()

            config = configparser.ConfigParser()

            ## Load Flow
            config['BDGD']= { }
            config['BDGD']['Modelo'] = self.databaseInfo["Modelo"]

            config['Sqlite'] = {}
            config['Sqlite']['dir'] = self.databaseInfo["Sqlite_DirDataBase"]
            config['Sqlite']['versao'] = self.databaseInfo["versao"]


            with open('siplaconfigdatabase.ini', 'w') as configfile:
                config.write(configfile)

            QMessageBox(QMessageBox.Information, "DataBase Configuration", "Configurações Salvas com Sucesso!",
                        QMessageBox.Ok).exec()

        except:
            raise class_exception.FileDataBaseError("Configuração do Banco de Dados", "Erro ao salvar os parâmetros\
                                                    do Banco de Dados!")

    def OpenDataBase(self):
        nameDirDataBase = str(
            QFileDialog.getExistingDirectory(None, "Selecione o Diretório com o Danco de Dados", "Banco/",
                                             QFileDialog.ShowDirsOnly))

        self.GroupBox_Sqlite_Edit.setText(nameDirDataBase)
        versaodatabase = self.get_versaoDataBaseSqlite()

        if self.checkDirDataBaseSqlite(nameDirDataBase, versaodatabase):
            self.GroupBox_Sqlite_Edit.setText(nameDirDataBase)
        else:
            self.GroupBox_Sqlite_Edit.setText("")

    def checkDirDataBaseSqlite(self, nameDirDataBase, versaodatabase):
        """
        Identifica a versão da database com base no banco de transformadores de média tensão, verifica e lista se todos
        os bancos necessário estão presentes no diretório de acordo com a respectiva versão.
        :param nameDirDataBase:
        :return True or False:
        """
        msg = ''

        match versaodatabase:
            case "2017":
                for ctd2017 in self.DBPRODIST2017:
                    if not os.path.isfile(nameDirDataBase + ctd2017 + ".sqlite"):
                        msg += ctd2017 + ".sqlite\n"
            case "2021":
                for ctd2021 in self.DBPRODIST2021:
                    if not os.path.isfile(nameDirDataBase + ctd2021 + ".sqlite"):
                        msg += ctd2021 + ".sqlite\n"
            case _:
                for ctd2017, ctd2021 in zip(self.DBPRODIST2017, self.DBPRODIST2021):
                    if ctd2017 == ctd2021 and not os.path.isfile(nameDirDataBase + ctd2017 + ".sqlite"):
                        msg += ctd2017 + ".sqlite\n"
                    elif not os.path.isfile(nameDirDataBase + ctd2017 + ".sqlite"):
                        msg += ctd2017 + ".sqlite (Para bases de 2017 até 2020)\n"
                    elif not os.path.isfile(nameDirDataBase + ctd2021 + ".sqlite"):
                        msg += ctd2021 + ".sqlite (Para bases a partir de 2021)\n"
                msg += "Não foi possível identificar o ano da base devido a falta dos arquivos listados"

        if msg != '':
            QMessageBox(QMessageBox.Warning, "DataBase Configuration",
                        "Diretório não apresenta os arquivos necessários! \n" + msg, QMessageBox.Ok).exec()
            return False
        else:
            return True

    def updateDialog(self):

        if self.GroupBox_Radio_check_identificar.isChecked():
            self.GroupBox_Radio_Modelo_Versao_1_0.setHidden(True)
            self.GroupBox_Radio_Modelo_Novo.setHidden(True)
            self.GroupBox_Radio_Modelo_Antigo.setHidden(True)
        elif not self.GroupBox_Radio_check_identificar.isChecked():
            self.GroupBox_Radio_Modelo_Versao_1_0.setHidden(False)
            self.GroupBox_Radio_Modelo_Novo.setHidden(False)
            self.GroupBox_Radio_Modelo_Antigo.setHidden(False)
        self.adjustSize()

class Window_confirmacao_zip_file(QMessageBox):

    def __init__(self, dir_path):
        super().__init__()

        self.dir_path = dir_path

        # Construção da janela
        self.titleWindow = "Arquivo da BDGD em formato zip"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))
        self.adjustSize()

        self.setIcon(QMessageBox.Information)
        self.setText("O arquivo da BDGD está compactado no formato zip. É\nnecessário que descompactemos o arquivo para"
                     " leitura\npelo SIPLA.\nConfirmar a descompactação do arquivo na pasta original?\n"
                     "(O arquivo em formato zip pode ser excluído após esse processo)")

        self.buttonClicked.connect(self.decompact_zip)

    def decompact_zip(self):
        with zipfile.ZipFile(self.dir_path, mode='r') as container:
            for file in container.namelist():
                print(file)
