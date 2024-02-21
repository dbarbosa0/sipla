import class_exception
import sqlite3
import MySQLdb


class C_DBaseConn:  # Classe de banco de dados

    def __init__(self):
        # Variáveis das Classes

        # Informações do Diretório
        self._DataBaseInfo = {}

    @property
    def DataBaseInfo(self):
        # Este código é executado quando alguém for
        # ler o valor de self.nome
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo

    def getSQLDB(self, nomeBancoDados, strSQL):

        try:
            # Conectando em apenas leitura!

            connDB = sqlite3.connect(
                'file:' + self.DataBaseInfo["Sqlite_DirDataBase"] + nomeBancoDados + '.sqlite?mode=ro', uri=True)

            cbanco = connDB.execute(strSQL)

            return cbanco

        except:
            raise class_exception.ConnDataBaseError("Erro de conexão no Banco de Dados:" + nomeBancoDados)

    def testConn(self):

        try:
            # Conectando em apenas leitura!

            connDB = sqlite3.connect('file:' + self.DataBaseInfo["Sqlite_DirDataBase"] + 'CTAT.sqlite?mode=ro',
                                     uri=True)
            cbanco = connDB.execute('select sqlite_version();')

            return True

        except:
            return False
