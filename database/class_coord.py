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

    def getCoord_AL_SE_MT_BT_DB(self, nomeAL_MT): #Pega as coordenadas dos circuitos de baixa de um alimentador

        try:
            nomeAL_MTS = []
            nomeAL_MTS.append(str(nomeAL_MT))

            codAlimentador = self.getCods_AL_SE_MT_DB(nomeAL_MTS)

            lista_de_coordenadas_do_alimentador = []

            sqlStr = "SELECT DISTINCT ctmt,x,y,vertex_index,objectid FROM ssdbt WHERE ctmt ='" + str(codAlimentador[0]) + "' ORDER BY objectid"

            cod_al = self.DataBaseConn.getSQLDB("SSDBT", sqlStr)

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
            raise class_exception.ExecDataBaseError("Erro ao pegar as Coordenadas dos Alimentadores de Baixa Tensão!")


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


    def getData_UniConsumidoraMT(self, nomeSE_MT, codField):

        try:
            lista_dados  = []

            sqlStrSSDMT = "SELECT pn_con_1, pn_con_2, x, y" \
                        " FROM  ssdmt WHERE sub = '" + nomeSE_MT[0] + "' AND ctmt = '" + codField + "'"

            tmp_ssdmt = []

            dadosSSDMT = self.DataBaseConn.getSQLDB("SSDMT", sqlStrSSDMT)

            for lnhSSDMT in dadosSSDMT.fetchall():  # Pegando o Transformador

                tmp_dados = [lnhSSDMT[0],lnhSSDMT[1],lnhSSDMT[2],lnhSSDMT[3]]

                tmp_ssdmt.append(tmp_dados)


            ######### Dados do Consumidor
            sqlStrUCMT = "SELECT pn_con, brr, sit_ativ, car_inst, dat_con, ctmt" \
                          " FROM  ucmt WHERE sub = '" + nomeSE_MT[0] + "' AND ctmt = '" + codField + "'"

            dadosUCMT = self.DataBaseConn.getSQLDB("UCMT", sqlStrUCMT)


            for lnhUCMT in dadosUCMT.fetchall():  # Pegando o Transformador

                ##Verificar a questão do X e do Y

                tmp_dados = []

                for lnhSSDMT in tmp_ssdmt:

                    if (lnhSSDMT[0] == lnhUCMT[0]) or (lnhSSDMT[1] == lnhUCMT[0]):

                        tmp_dados = [lnhSSDMT[3], lnhSSDMT[2], lnhUCMT[1],lnhUCMT[2],lnhUCMT[3],lnhUCMT[4]]

                        break

                lista_dados.append(tmp_dados)


            return lista_dados

        except:
            raise class_exception.ExecData(
                "Erro no processamento do Banco de Dados para as Unidades Consumidoras de Média Tensão! ")