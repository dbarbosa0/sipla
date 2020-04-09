from PyQt5.QtWidgets import QFileDialog
import class_exception

from os import path
import platform
import sqlite3

class C_DBaseConn(): #Classe de banco de dados

    def __init__(self):
        #Variáveis das Classes

        #Nome do Diretório
        self._DirDataBase = ""
        self._defDirDataBase = False ## determina se o diretório já foi definido

        self.nameDataBase = ''
        #Todos dos Banco de Dados que serão necessários
        self.DBPRODIST = ["CTAT", "EQTRM", "SSDMT", "UNREMT", "UNTRS", "CTMT", "EQTRS", "UCBT", "UNSEAT", "EQSE", "RAMLIG", "UCMT", "UNSEMT", "EQTRD", "SEGCON", "UNCRMT", "UNCRBT", "UNTRD"]

    @property
    def DirDataBase(self):
        # Este código é executado quando alguém for
        # ler o valor de self.nome
        return self._DirDataBase

    @DirDataBase.setter
    def DirDataBase(self, nameDirDataBase):
        try:
            for ctd in self.DBPRODIST:
                if not path.isfile(nameDirDataBase + ctd + ".sqlite"):
                    raise class_exception.FileDataBaseError("Arquivo " + ctd + ".sqlite ausente!")

            self._defDirDataBase = True
            self._DirDataBase = nameDirDataBase

        except:
            pass

    @property
    def defDirDataBase(self):
        return self._defDirDataBase


    def setDirDataBase(self):
        # este código é executado sempre que alguém fizer
        # self.nome = value
        try:
            if not self.defDirDataBase:
                nameDirDataBase = str(QFileDialog.getExistingDirectory(None, "Selecione o Diretório com o Danco de Dados", "Banco/",
                                                                       QFileDialog.ShowDirsOnly))

                nameDirDataBase += "/"

                if platform.system() == "Windows":
                    nameDirDataBase = nameDirDataBase.replace('/', '\\')

                self.DirDataBase = nameDirDataBase

            else:
                raise class_exception.FileDataBaseError("Diretório do DataBase já foi definido!")

            return True
        except:
            pass


    def getSQLDB(self,nomeBancoDados,strSQL):

        try:
            #Conectando em apenas leitura!
            connDB =  sqlite3.connect('file:' + self.DirDataBase + nomeBancoDados + '.sqlite?mode=ro', uri=True)

            cbanco = connDB.execute(strSQL)

            return cbanco

        except:
            raise class_exception.ConnDataBaseError("Erro de conexão no Banco de Dados:" + nomeBancoDados)

                
                

            
            

        
        
        
            
                

    
