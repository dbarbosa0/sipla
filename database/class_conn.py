import class_exception

import sqlite3

class C_DBaseConn(): #Classe de banco de dados

    def __init__(self):
        #Variáveis das Classes

        #Informações do Diretório
        self._DataBaseInfo = {}

    @property
    def DataBaseInfo(self):
        # Este código é executado quando alguém for
        # ler o valor de self.nome
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo

    def getSQLDB(self,nomeBancoDados,strSQL):

        try:
            #Conectando em apenas leitura!
            if self.DataBaseInfo["Conn"] == "sqlite":

                connDB = sqlite3.connect('file:' + self.DataBaseInfo["DirDataBase"] + nomeBancoDados + '.sqlite?mode=ro', uri=True)

                cbanco = connDB.execute(strSQL)

            elif self.DataBaseInfo["Conn"] == "mysql":
                pass

            return cbanco

        except:
            raise class_exception.ConnDataBaseError("Erro de conexão no Banco de Dados:" + nomeBancoDados)

                
                

            
            

        
        
        
            
                

    
