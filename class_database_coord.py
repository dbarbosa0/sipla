import class_database_conn
import class_exception 

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

            ct_mt = self.DataBaseConn.getSQLDB("CTMT","SELECT cod_id, nom FROM ctmt;")

            for linha in ct_mt.fetchall():
                for i in range(0, len(listaNomesAL_MT) ):
                    if linha[1] == listaNomesAL_MT[i]:
                        lista_de_identificadores_dos_alimentadores.append(linha[0])

            lista_de_identificadores_dos_alimentadores_filtrados = (sorted(set(lista_de_identificadores_dos_alimentadores)))

            return lista_de_identificadores_dos_alimentadores_filtrados
        except:
            raise class_exception.ExecDataBaseError("Erro ao pegar os Códigos dos Alimentadores de Média Tensão!")

    def getCoord_AL_SE_MT_DB(self, nomeAL_MT): #Pega as coordenadas de um alimentador de uma SE MT

        try:
            nomeAL_MTS = []
            nomeAL_MTS.append(str(nomeAL_MT))

            codAlimentador = self.getCods_AL_SE_MT_DB(nomeAL_MTS)

            lista_de_coordenadas_do_alimentador = []

            #ct_mt = self.DataBaseConn.getSQLDB("CTMT","SELECT * FROM ctmt;")

            sqlStr = "SELECT ctmt,x,y,vertex_index,objectid FROM ssdmt WHERE ctmt ='" + str(codAlimentador[0]) + "' ORDER BY objectid"

            cod_al = self.DataBaseConn.getSQLDB("SSDMT",sqlStr)

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
