from typing import NamedTuple
import database.class_conn
import class_exception


##Classes de Dados
class dadosTrafoDist(NamedTuple):
    cod_id: str 
    pac_1: str 
    pac_2: str 
    pac_3: str 
    fas_con_p:str 
    fas_con_s:str 
    fas_con_t:str 
    sit_ativ:str 
    tip_unid:str 
    cap_elo:str 
    cap_cha:str 
    tap:str 
    pot_nom:str 
    per_fer:str 
    per_tot:str 
    ctmt:str 
    tip_trafo:str 
    cod_id_eqtrd:str 
    pac_1_eqtrd:str 
    pac_2_eqtrd:str 
    pac_3_eqtrd:str 
    fas_con:str 
    pot_nom_eqtrd:str 
    lig:str 
    ten_pri:str 
    ten_sec:str 
    ten_ter:str 
    lig_fas_p:str 
    lig_fas_s:str 
    lig_fas_t:str 
    per_fer_eqtrd:str 
    per_tot_eqtrd:str 
    r:str 
    xhl:str 
    xht:str 
    xlt:str

class dadosUnidCompReat(NamedTuple):
    cod_id:str
    fas_con:str
    pot_nom:str
    pac_1:str
    ctmt:str

class dadosSegLinhas(NamedTuple):
    cod_id: str
    ctmt: str
    pac_1: str
    pac_2: str
    fas_con: str
    comp: str
    tip_cnd: str

class dadosUNREMT(NamedTuple):
    cod_id: str
    ctmt: str
    pac_1: str
    pac_2: str
    fas_con: str
    sit_ativ: str

class dadosUnidCons(NamedTuple):
    objectid: str
    pac: str
    ctmt: str
    fas_con: str
    ten_forn: str
    sit_ativ: str
    tip_cc: str
    car_inst: str
    uni_tr: str

class dadosCondutores(NamedTuple):
    cod_id: str
    r1: str
    x1: str
    cnom: str
    cmax: str

class dadosCTATMT(NamedTuple):
    nome: str
    ten_nom: str
    cod_id: str

class dadosTransformador(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    pot_nom: str
    lig: str
    ten_pri: str
    ten_sec: str
    ten_ter: str

class dadosSECAT(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    fas_con: str
    tip_unid: str
    p_n_ope: str
    cap_elo: str
    cor_nom: str
    sit_ativ: str

class dadosSECMT(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    fas_con: str
    tip_unid: str
    ctmt: str
    uni_tr_s: str
    p_n_ope: str
    cap_elo: str
    cor_nom: str
    sit_ativ: str


class C_DBaseData():

    def __init__(self):
        super(C_DBaseData, self).__init__()
##########################

        self._DataBaseConn = database.class_conn.C_DBaseConn() #Criando a instância do Banco de Dados

    @property
    def DataBaseConn(self):
        return self._DataBaseConn

    @DataBaseConn.setter
    def DataBaseConn(self, value):
        self._DataBaseConn = value

######################################## Data

    def getData_EqThevenin(self, nomeCircuitoAlta):  # Pega as coordenadas de um alimentador de uma SE MT

        try:
            lista_dados = []

            sqlStr = "SELECT nom, ten_nom, cod_id FROM ctat WHERE nom ='" + nomeCircuitoAlta +"'"

            dadosSE = self.DataBaseConn.getSQLDB("CTAT", sqlStr)

            for linha in dadosSE.fetchall():
                tmp_dados = dadosCTATMT(
                    linha[0], #nome: str
                    linha[1], #ten_nom: str
                    linha[2], # cod_id: str
                )

                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para o Equivalente de Thevenin!")

    def getData_CTMT(self, nomeSE_MT = None):  # Pega as coordenadas de um alimentador de uma SE MT


        try:

            sqlStr = "SELECT nom, ten_nom, cod_id  FROM ctmt ORDER BY cod_id"

            if nomeSE_MT is not None:
                sqlStr += " WHERE sub ='" + nomeSE_MT + "'"

            lista_dados = []

            dadosSE = self.DataBaseConn.getSQLDB("CTMT", sqlStr)

            for linha in dadosSE.fetchall():
                tmp_dados = dadosCTATMT (
                    linha[0], #nome: str
                    linha[1], #ten_nom: str
                    linha[2]  # cod_id: str
                )

                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para o Equivalente de Thevenin de Média Tensão!")

    def getData_TrafosAT_MT(self, nomeSE_MT):  # Pega os transformadores de AT para MT

        try:

            sqlStr = "SELECT  cod_id, pac_1, pac_2, pot_nom, lig, ten_pri, ten_sec, ten_ter FROM eqtrs WHERE odi ='" + "1" + nomeSE_MT + "0001" + "'"

            lista_dados = []

            dadosSE = self.DataBaseConn.getSQLDB("EQTRS", sqlStr)

            for linha in dadosSE.fetchall():
                tmp_dados = dadosTransformador(
                    linha[0], # cod_id
                    linha[1], # pac_1
                    linha[2], # pac_2
                    linha[3], # pot_nom
                    linha[4], # lig
                    linha[5], # ten_pri
                    linha[6], # ten_sec
                    linha[7], # ten_ter
                )
                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para os Transformadores de Média Tensão!")

    def getData_Condutores(self, tipoCondutor):  # Pega os condutores de MT

            try:
                sqlStr = "SELECT cod_id, r1, x1, cnom, cmax FROM segcon WHERE cod_id LIKE '%" + tipoCondutor + "%' ORDER BY cod_id"

                lista_dados = []

                dadosSE = self.DataBaseConn.getSQLDB("SEGCON", sqlStr)

                for linha in dadosSE.fetchall():
                    tmp_dados = dadosCondutores(
                        linha[0],  # cod_id: str
                        linha[1],  # r1: str
                        linha[2],  #x1: str
                        linha[3],  #cnom: str
                        linha[4],  #cmax: str
                    )
                    lista_dados.append(tmp_dados)

                return lista_dados

            except:
                raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para os Condutores: " + tipoCondutor)

    def getData_SecAT(self, nomeSE_MT):  # Pega as seccionadoras de AT

        try:
            sqlStr = "SELECT cod_id, pac_1, pac_2, fas_con, tip_unid, p_n_ope, cap_elo, cor_nom, sit_ativ  FROM unseat WHERE sub = '" + nomeSE_MT + "'"

            lista_dados = []


            dadosSECDB = self.DataBaseConn.getSQLDB("UNSEAT", sqlStr)

            for linha in dadosSECDB.fetchall():
                tmp_dados = dadosSECAT(
                    linha[0],  #cod_id
                    linha[1],  # pac_1
                    linha[2],  # pac_2
                    linha[3],  #fas_con
                    linha[4],  #tip_unid
                    linha[5],  #p_n_ope
                    linha[6],  #cap_elo
                    linha[7],  #cor_nom
                    linha[8], #sit_ativ
                )
                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para as Seccionadoras de AT")

    def getData_SecMT(self, nomeSE_MT, tipoSEC):  # Pega as seccionadoras de MT

        try:

            sqlStr = "SELECT cod_id, pac_1, pac_2, fas_con, tip_unid, ctmt, uni_tr_s, p_n_ope, cap_elo, cor_nom, sit_ativ  FROM unsemt WHERE sub = '" + \
                         nomeSE_MT + "' AND tip_unid = '" + tipoSEC + "' ORDER BY tip_unid"
            lista_dados = []


            dadosSECDB = self.DataBaseConn.getSQLDB("UNSEMT", sqlStr)

            for linha in dadosSECDB.fetchall():
                tmp_dados = dadosSECMT(
                    linha[0],  # cod_id
                    linha[1],  # pac_1
                    linha[2],  # pac_2
                    linha[3],  # fas_con
                    linha[4],  # tip_unid
                    linha[5],  # ctmt
                    linha[6],  # uni_tr_s
                    linha[7],  # p_n_ope
                    linha[8],  # cap_elo
                    linha[9],  # cor_nom
                    linha[10],  # sit_ativ
                )
                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para as Seccionadoras MT: " + str(tipoSEC))

    def getData_SegLinhasMT(self, nomeSE_MT):  # Pega os segmentos de linhas de MT

        try:

            sqlStr = "SELECT DISTINCT cod_id, ctmt, pac_1, pac_2, fas_con, comp, tip_cnd FROM ssdmt WHERE sub = '" + \
                         nomeSE_MT + "' ORDER BY ctmt"

            lista_dados = []

            dadosSECDB = self.DataBaseConn.getSQLDB("SSDMT", sqlStr)

            for linha in dadosSECDB.fetchall():
                tmp_dados = dadosSegLinhas(
                    linha[0],  # cod_id
                    linha[1],  # ctmt
                    linha[2],  # pac_1
                    linha[3],  # pac_2
                    linha[4],  # fas_con
                    linha[5],  # comp
                    linha[6],  # tip_cnd
                )
                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para os Segmentos de Linha! ")

    def getData_ReguladorMT(self, nomeSE_MT):  # Pega os reguladores de MT

        try:

            sqlStr = "SELECT cod_id, ctmt, pac_1, pac_2, fas_con, sit_ativ FROM unremt WHERE sub = '" + \
                         nomeSE_MT + "'"

            lista_dados = []

            dadosSECDB = self.DataBaseConn.getSQLDB("UNREMT", sqlStr)

            for linha in dadosSECDB.fetchall():
                tmp_dados = dadosUNREMT(
                    linha[0],  # cod_id
                    linha[1],  # ctmt
                    linha[2],  # pac_1
                    linha[3],  # pac_2
                    linha[4],  # fas_con
                    linha[5],  # sit_ativ
                )
                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para os Reguladores de MT! ")


    def getData_UniConsumidora(self, nomeSE_MT, tipoUniCons):  # Pega os reguladores

        try:
            if tipoUniCons == "MT":

                dbase = "UCMT"
                uni_tr = "uni_tr_s"

            elif tipoUniCons == "BT":

                dbase = "UCBT"
                uni_tr = "uni_tr_d"

            else:
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras!\nTipo não foi especificado! \n" + tipoUniCons)

            lista_dados = []

            sqlStr = "SELECT objectid, pac, ctmt, fas_con, ten_forn, sit_ativ, tip_cc, car_inst, " + uni_tr + " FROM " + dbase + " WHERE sub = '" + \
                     nomeSE_MT + "' ORDER BY " + uni_tr

            dadosUniConsDB = self.DataBaseConn.getSQLDB(dbase, sqlStr)

            for linha in dadosUniConsDB.fetchall():
                tmp_dados = dadosUnidCons(
                    linha[0],  # objectid
                    linha[1],  # pac
                    linha[2],  # ctmt
                    linha[3],  # fas_con
                    linha[4],  # ten_forn
                    linha[5],  # sit_ativ
                    linha[6],  # tip_cc
                    linha[7],  # car_inst
                    linha[8]   # uni_tr
                )
                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para as Unidades Consumidoras! ")


    def getData_TrafoDIST(self, nomeSE_MT):  # Pega os reguladores de MT

        try:

            sqlStrUNTRD = "SELECT cod_id, pac_1, pac_2, pac_3, fas_con_p, fas_con_s, fas_con_t, sit_ativ, tip_unid, " \
                     " cap_elo, cap_cha, tap, pot_nom, per_fer, per_tot, ctmt, tip_trafo " \
                     " FROM  untrd WHERE sub = '" + nomeSE_MT + "' ORDER BY cod_id"

            sqlStrEQTRD = "SELECT cod_id, pac_1, pac_2, pac_3, fas_con, pot_nom, lig, ten_pri, ten_sec, ten_ter, " \
                         " lig_fas_p, lig_fas_s, lig_fas_t, per_fer, per_tot, r, xhl, xht, xlt " \
                         " FROM  eqtrd"

            lista_dados = []

            dadosUNTRD = self.DataBaseConn.getSQLDB("UNTRD", sqlStrUNTRD)
            dadosEQTRD = self.DataBaseConn.getSQLDB("EQTRD", sqlStrEQTRD)

            lista_dados_UNTRD = []

            for lnhUNTRD in dadosUNTRD.fetchall(): # Pegando o Transformador
                lista_dados_UNTRD.append(lnhUNTRD)

            for lnhEQTRD in dadosEQTRD.fetchall():  # Pegando o Transformador

                for lnhUNTRD in lista_dados_UNTRD:

                    if lnhUNTRD[ 1] == lnhEQTRD[ 1]: #Transformadores com o mesmo pac_1
                        tmp_dados = dadosTrafoDist (
                            lnhUNTRD[ 0], # cod_id
                            lnhUNTRD[ 1], # pac_1
                            lnhUNTRD[ 2], # pac_2
                            lnhUNTRD[ 3], # pac_3
                            lnhUNTRD[ 4], # fas_con_p
                            lnhUNTRD[ 5], # fas_con_s
                            lnhUNTRD[ 6], # fas_con_t
                            lnhUNTRD[ 7], # sit_ativ
                            lnhUNTRD[ 8], # tip_unid
                            lnhUNTRD[ 9], # cap_elo
                            lnhUNTRD[10], # cap_cha
                            lnhUNTRD[11], # tap
                            lnhUNTRD[12], # pot_nom
                            lnhUNTRD[13], # per_fer
                            lnhUNTRD[14], # per_tot
                            lnhUNTRD[15], # ctmt
                            lnhUNTRD[16], # tip_trafo
                            lnhEQTRD[ 0], # cod_id_eqtrd
                            lnhEQTRD[ 1], # pac_1_eqtrd
                            lnhEQTRD[ 2], # pac_2_eqtrd
                            lnhEQTRD[ 3], # pac_3_eqtrd
                            lnhEQTRD[ 4], # fas_con
                            lnhEQTRD[ 5], # pot_nom_eqtrd
                            lnhEQTRD[ 6], # lig
                            lnhEQTRD[ 7], # ten_pri
                            lnhEQTRD[ 8], # ten_sec
                            lnhEQTRD[ 9], # ten_ter
                            lnhEQTRD[10], # lig_fas_p
                            lnhEQTRD[11], # lig_fas_s
                            lnhEQTRD[12], # lig_fas_t
                            lnhEQTRD[13], # per_fer_eqtrd
                            lnhEQTRD[14], # per_tot_eqtrd
                            lnhEQTRD[15], # r
                            lnhEQTRD[16], # xhl
                            lnhEQTRD[17], # xht
                            lnhEQTRD[18] # xlt
                        )

                        lista_dados.append(tmp_dados)



            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados para os Transformadores de Distribuição! ")


    def getData_SegLinhasRamLigBT(self, nomeSE_MT, tipoLinha):  # Pega os reguladores

        try:
            if tipoLinha == "SEGBT":  # Segmentos de Linhas de Baixa Tensão

                dbase = "SSDBT"

            elif tipoLinha == "RLIG":  # Ramal de Ligação

                dbase = "RAMLIG"

            else:
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações das linhas de BT!\nTipo não foi especificado! \n" + tipoLinha)

            sqlStr = "SELECT DISTINCT cod_id, ctmt, pac_1, pac_2, fas_con, comp, tip_cnd FROM " + dbase + " WHERE sub = '" + nomeSE_MT + "'"

            dadosLinhaDB = self.DataBaseConn.getSQLDB(dbase, sqlStr)

            lista_dados = []


            for linha in dadosLinhaDB.fetchall():
                tmp_dados = dadosSegLinhas(
                    linha[0],  # cod_id
                    linha[1],  # ctmt
                    linha[2],  # pac_1
                    linha[3],  # pac_2
                    linha[4],  # fas_con
                    linha[5],  # comp
                    linha[6],  # tip_cnd
                )

                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados das Linhas de BT e Ramais de Ligação!\n" + tipoLinha)


    def getData_UniCompReativo(self, nomeSE_MT, tipoCAP):  # Pega os reguladores

        try:
            if tipoCAP == "MT":  # Média Tensão
                dbase = "UNCRMT"

            elif tipoCAP == "BT":  # Ramal de Ligação
                dbase = "UNCRBT"

            else:
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos compensadores de reativo!\nTipo não foi especificado! \n" + tipoCAP)

            sqlStr = "SELECT cod_id, fas_con, pot_nom, pac_1, ctmt FROM " + dbase + " WHERE sub = '" + nomeSE_MT + "'"

            dadosCapDB = self.DataBaseConn.getSQLDB(dbase, sqlStr)

            lista_dados = []

            for linha in dadosCapDB.fetchall():
                tmp_dados = dadosUnidCompReat(
                    linha[0],  # cod_id
                    linha[1],  # fas_con
                    linha[2],  # pot_nom
                    linha[3],  # pac_1
                    linha[4],  # ctmt
                )

                lista_dados.append(tmp_dados)

            return lista_dados

        except:
            raise class_exception.ExecOpenDSS("Erro no processamento do Banco de Dados dos Compensadores de Reativo!\n" + tipoCAP)