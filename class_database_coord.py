from typing import NamedTuple

import class_database_conn
import class_exception


##Classes de Dados
class dadosTrafoDist(NamedTuple):
    cod_id: str
    pot_nom:str
    ctmt: str
    x: str
    y:str

class C_DBaseCoord():
    def __init__(self):
        self._DataBaseConn = class_database_conn.C_DBaseConn()

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

            ct_mt = self.DataBaseConn.getSQLDB("CTMT","SELECT DISTINCT cod_id, nom FROM ctmt;")

            for linha in ct_mt.fetchall():
                for i in range(0, len(listaNomesAL_MT) ):
                    if linha[1] == listaNomesAL_MT[i]:
                        lista_de_identificadores_dos_alimentadores.append(linha[0])

            lista_de_identificadores_dos_alimentadores_filtrados = (sorted(lista_de_identificadores_dos_alimentadores))

            return lista_de_identificadores_dos_alimentadores_filtrados
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

    def getData_TrafoDIST(self, nomeSE_MT):  # Pega os reguladores de MT

        try:

            sqlStrUNTRD = "SELECT cod_id, pot_nom, ctmt, x, y " \
                          " FROM  untrd WHERE sub = '" + nomeSE_MT[0] + "'"

            lista_dados = []

            dadosUNTRD = self.DataBaseConn.getSQLDB("UNTRD", sqlStrUNTRD)


            for lnhUNTRD in dadosUNTRD.fetchall():  # Pegando o Transformador
                tmp_dados = dadosTrafoDist(
                    lnhUNTRD[0],  # cod_id
                    lnhUNTRD[1],  # pot_nom
                    lnhUNTRD[2], #ctmt
                    lnhUNTRD[3],  # x
                    lnhUNTRD[4],  # y
                )

                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecData(
                "Erro no processamento do Banco de Dados para os Transformadores de Distribuição! ")
