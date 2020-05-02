import database.class_conn
import class_exception


class C_DBaseCoord():
    def __init__(self):
        self._DataBaseConn = ""
        self.DataBaseConn = database.class_conn.C_DBaseConn()

    @property
    def DataBaseConn(self):
        return self._DataBaseConn

    @DataBaseConn.setter
    def DataBaseConn(self, value):
        self._DataBaseConn = value

    ######################## Visualização

    def getCods_AL_SE_MT_DB(self, listaNomesAL_MT): #Pega os códigos dos alimenatadores de uma SE MT

        try:

            lista_de_identificadores_dos_alimentadores = []

            ct_mt = self.DataBaseConn.getSQLDB("CTMT","SELECT DISTINCT cod_id, nom FROM ctmt ORDER BY nom")

            for linha in ct_mt.fetchall():
                if linha[1] in listaNomesAL_MT:
                        lista_de_identificadores_dos_alimentadores.append(linha[0])

            return lista_de_identificadores_dos_alimentadores
        except:
            raise class_exception.ExecDataBaseError("Erro ao pegar os Códigos dos Alimentadores de Média Tensão!")

    def getCoord_AL_SE_MT_DB(self, nomeAL_MT): #Pega as coordenadas de um alimentador de uma SE MT

        try:
            nomeAL_MTS = []
            nomeAL_MTS.append(str(nomeAL_MT))

            codAlimentador = self.getCods_AL_SE_MT_DB(nomeAL_MTS)

            lista_de_coordenadas_do_alimentador = []

            sqlStr = "SELECT DISTINCT ctmt,x,y,vertex_index,objectid FROM ssdmt WHERE ctmt ='" + str(codAlimentador[0]) + "' ORDER BY objectid"

            cod_al = self.DataBaseConn.getSQLDB("SSDMT", sqlStr)

            dadosCoord =[]
            dadosCoordInicio = []
            dadosCoordFim = []

            for linha in cod_al.fetchall():
                    if linha[3] == 0:
                        dadosCoordInicio = [linha[2], linha[1]]
                    if linha[3] == 1:
                        dadosCoordFim = [linha[2], linha[1]]

                        dadosCoord = [dadosCoordInicio, dadosCoordFim]

                        lista_de_coordenadas_do_alimentador.append(dadosCoord)

            return lista_de_coordenadas_do_alimentador

        except:
            raise class_exception.ExecDataBaseError("Erro ao pegar as Coordenadas dos Alimentadores de Média Tensão!")

    def getData_TrafoDIST(self, nomeSE_MT, codField):  # Pega os reguladores de MT

        try:

            sqlStrUNTRD = "SELECT cod_id, pot_nom, ctmt, x, y " \
                          " FROM  untrd WHERE sub = '" + nomeSE_MT[0] + "' AND ctmt = '" + codField + "'"

            lista_dados = []

            dadosUNTRD = self.DataBaseConn.getSQLDB("UNTRD", sqlStrUNTRD)


            for lnhUNTRD in dadosUNTRD.fetchall():  # Pegando o Transformador

                ##Verificar a questão do X e do Y

                tmp_dados = [lnhUNTRD[4],lnhUNTRD[3],lnhUNTRD[0],lnhUNTRD[1]]

                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecData(
                "Erro no processamento do Banco de Dados para os Transformadores de Distribuição! ")
