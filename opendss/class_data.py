import database.class_data
import class_exception

import database.class_conn
import opendss.class_config_dialog
import opendss.class_trafo_data
import prodist.tten as tten  # Níveis de tensão do prodist
import prodist.tlig as tlig  # Tipos de Ligações
import prodist.tpotatr as tpotatr  # Potências dos transformadores
import prodist.tcapelofu as tcapelofu  # Elos fusíveis


class C_Data():  # classe OpenDSS

    def __init__(self):
        self.teste_Tratamento_trafo = opendss.class_trafo_data.trafo_data()
        self.DataBase = database.class_data.C_DBaseData()  # Acesso ao Banco de Dados
        self.Config_Dia = opendss.class_config_dialog.LoadFlow()
        self._DataBaseConn = database.class_conn.C_DBaseConn()  # Carregando o acesso aos Arquivos do BDGD
        self._nCircuitoAT_MT = ''
        self._nSE_MT_Selecionada = ''
        self._nFieldsMT = ''

        # Transformadores de Distribuição selecionados
        self._nFieldsTD = ''

        ##Lista com o nome das Barras
        # self.busList = []
        self.listaAlimentadores = []
        self.busListDict = {}
        self.elementList = []
        self.recloserList = []
        self.fuseList = []
        self.relayList = []
        self.swtcontrolList = []
        ##Curvas de Carga
        self.loadShapeUniCons = {}
        self.ajusteTrafos = {}
        self.trafo_ten_sec = {}
        self.identificadorTrafo = {}
        self.num_de_fases = {}
        self.ajuste_memoria = []
        self.uni_tr_s = []
        self.memoALIMENTADOR =[]
        self.trafosATMT_ideais ={}
        self.barra_infinita = str()
        self.basekv = str()
        self.initUI()

    @property
    def DataBaseConn(self):
        return self._DataBaseConn

    @DataBaseConn.setter
    def DataBaseConn(self, value):
        self._DataBaseConn = value

    @property
    def nCircuitoAT_MT(self):
        return self._nCircuitoAT_MT

    @nCircuitoAT_MT.setter
    def nCircuitoAT_MT(self, value):
        self._nCircuitoAT_MT = value

    @property
    def nSE_MT_Selecionada(self):
        return self._nSE_MT_Selecionada

    @nSE_MT_Selecionada.setter
    def nSE_MT_Selecionada(self, value):
        self._nSE_MT_Selecionada = value

    @property
    def nFieldsMT(self):
        return self._nFieldsMT

    @nFieldsMT.setter
    def nFieldsMT(self, value):
        self._nFieldsMT = value

    @property
    def nFieldsTD(self):
        return self._nFieldsTD

    @nFieldsTD.setter
    def nFieldsTD(self, value):
        self._nFieldsTD = value

    def initUI(self):

        # Criando variáveis do Redirect
        self.memoFileHeader = []  # Cabeçalho do arquivo
        self.memoFileFooter = []  # Rodapé do arquivo
        self.memoFileEqTh = []  # Arquivo Thevenin
        self.memoFileEqThMT = []  # Arquivo Thevenin Média
        self.memoFileSecAT_EqThAT = []  # Seccionadora entre o Equivalente e a Seccionadora de AT
        self.memoFileTrafoATMT = []  # Transformadores de AT MT
        self.memoFileCondMT = []  # Condutores de Média Tensão
        self.memoFileCondBT = []  # Condutores de Baixa Tensão
        self.memoFileCondRamal = []  # Condutores de Ramal
        self.memoFileSecAT = []  # Seccionadora de Alta Tensão
        self.memoFileSecAT_Control = []  # Controle da Secionadora de Alta Tensão
        self.memoFileSecOleoMT = []  # Seccionadora a Óleo de Média Tensão
        self.memoFileSecOleoMT_Control = []  # Controle Seccionadora a Óleo de Média Tensão
        self.memoFileSecFacaMT = []  # Seccionadora Facade Média Tensão
        self.memoFileSecFacaMT_Control = []  # Controle Seccionadora Faca de Média Tensão
        self.memoFileSecFacaTripolarMT = []  # Seccionadora Faca Tripolar de Média Tensão
        self.memoFileSecFacaTripolarMT_Control = []  # Controle Seccionadora Faca Tripolar de Média Tensão
        self.memoFileSecFusivelMT = []  # Seccionadora Fusível Média Tensão
        self.memoFileSecFusivelMT_Control = []  # Controle Seccionadora Fusível de Média Tensão
        self.memoFileSecDJReleMT = []  # Seccionadora DJ Média Tensão
        self.memoFileSecDJReleMT_Control = []  # Controle Seccionadora DJ de Média Tensão
        self.memoFileSecReligadorMT = []  # Seccionadora Religador de  Média Tensão
        self.memoFileSecReligadorMT_Control = []  # Controle Seccionadora Religador de de Média Tensão
        self.memoFileSecTripolarSEMT = []  # Seccionadora Tripolar SE de  Média Tensão
        self.memoFileSecTripolarSEMT_Control = []  # Controle Seccionadora Tripolar SE de Média Tensão
        self.memoFileSecUnipolarSEMT = []  # Seccionadora Unipolar SE de  Média Tensão
        self.memoFileSecUnipolarSEMT_Control = []  # Controle Seccionadora Unipolar SE de Média Tensão
        self.memoFileReguladorMT = []  # Regulador de  Média Tensão
        self.memoFileSegLinhasMT = []  # Segmentos de Linhas de  Média Tensão
        self.memoFileUniConsumidoraMT = []  # Unidade Consumidora de Média Tensão
        self.memoFileUniConsumidoraLoadShapesMT = []  # Unidade Consumidora de Média Tensão - Curvas de Carga
        self.memoFileTrafoDist = []  # Transformadores de Distribuição
        self.memoFileSegLinhasBT = []  # Segmentos de Linhas de Baixa Tensão
        self.memoFileUniConsumidoraBT = []  # Unidade Consumidora de Baixa Tensão
        self.memoFileUniConsumidoraBT_TD = []  # Unidade Consumidora de Baixa Tensão no Transformador de Distribuição
        self.memoFileUniConsumidoraLoadShapesBT = []  # Unidade Consumidora de Baixa Tensão - Curvas de Carga
        self.memoFileRamaisLigBT = []  # Ramais de Ligação
        self.memoFileUndCompReatMT = []  # Unidade de Compensação de Reativo de Baixa Tensão
        self.memoFileUndCompReatBT = []  # Unidade de Compensação de Reativo de Baixa Tensão

    def exec_HeaderFile(self):

        self.DataBase.DataBaseConn = self.DataBaseConn

        self.memoFileHeader = []

        self.memoFileHeader.insert(0, "Clear ")

        self.memoFileHeader.insert(1, "! VAMOS QUE VAMOS ")

    def exec_FooterFile(self):
        try:
            self.memoFileFooter.append("! codigo finalizado ")

        except:
            raise class_exception.ExecOpenDSS("Erro no FOOTER")

    def execTest(self):

        self.DataBase.DataBaseConn = self.DataBaseConn

        print("Iniciando o processamento de teste ...")

        print("Cabeçalho ...")
        self.exec_HeaderFile()
        print("Rodapé ...")
        self.exec_FooterFile()
        print("Equivalente de Thevenin ...")
        self.exec_EQUIVALENTE_DE_THEVENIN()
        print("Equivalente de Thevenin MT...")
        self.exec_EQUIVALENTE_DE_THEVENIN_MEDIA()
        print("Trafo AT - MT...")
        self.exec_TRANSFORMADORES_DE_ALTA_PARA_MEDIA()
        print("Condutores MT...")
        self.exec_CONDUTORES_DE_MEDIA_TENSAO()
        print("Condutores de BT...")
        self.exec_CONDUTORES_DE_BAIXA_TENSAO()
        print("Condutores de Ramais ...")
        self.exec_CONDUTORES_DE_RAMAL()
        print("Seccionadoras de AT...")
        self.exec_SEC_DE_ALTA_TENSAO()
        print("Controle Seccionadoras de AT...")
        self.exec_CONTROLE_SEC_DE_ALTA_TENSAO()
        print("Chave a óleo de MT ...")
        self.exec_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO()
        print("Controle Chave a óleo de MT...")
        self.exec_CONTROLE_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO()
        print("Chave Faca de MT ...")
        self.exec_SEC_CHAVE_FACA_DE_MEDIA_TENSAO()
        print("Controle Chave Faca de MT ...")
        self.exec_CONTROLE_SEC_CHAVE_FACA_DE_MEDIA_TENSAO()
        print("Chave Faca Tripolar de MT ...")
        self.exec_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO()
        print("Controle Chave Faca Tripolar de MT ...")
        self.exec_CONTROLE_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO()
        print("Chave Fusível de MT ...")
        self.exec_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO()
        print("Controle Chave Fusível de MT ...")
        self.exec_CONTROLE_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO()
        print("DJ de MT ...")
        self.exec_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO()
        print("Controle DJ de MT ...")
        self.exec_CONTROLE_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO()
        print("Religador de MT ...")
        self.exec_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO()
        print("Controle do Religador de MT ...")
        self.exec_CONTROLE_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO()
        print("Chave Tripolar da SE MT ...")
        self.exec_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO()
        print("Controle Chave Tripolar da SE MT ...")
        self.exec_CONTROLE_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO()
        print("Chave Unipolar da SE MT ...")
        self.exec_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO()
        print("Controle da Chave Unipolar da SE MT ...")
        self.exec_CONTROLE_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO()
        print("Regulador MT ...")
        self.exec_REGULADORES_DE_MEDIA_TENSAO()
        print("Segmentos de Linhas MT ...")
        self.exec_SEG_LINHAS_DE_MEDIA_TENSAO()
        print("Unidades Consumidoras MT ...")
        self.exec_UNID_CONSUMIDORAS_MT()
        print("Trafos de Distribuição ...")
        self.exec_TRANSFORMADORES_DE_DISTRIBUICAO()
        print("Segmentos de Linhas BT ...")
        self.exec_SEG_LINHAS_DE_BAIXA_TENSAO()
        print("Unidades Consumidoras BT ...")
        self.exec_UNID_CONSUMIDORAS_BT()
        # print("Ramais de Ligação  ...")
        # self.exec_RAMAL_DE_LIGACAO()
        print("Unidades Compensadoras de MT ...")
        self.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO()
        print("Unidades Compensadoras de BT ...")
        self.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO()

        print("Processamento Finalizado!")

    def getEQUIVALENTE_DE_THEVENIN(self):
        try:
            dados_eqth = self.DataBase.getData_TrafosAT_MT(self.nCircuitoAT_MT)
            #print(self.nCircuitoAT_MT)
            memoFileEqTh = []
            memoFileEqTh.append("!Barramento Infinito")

            #for ctd in range(0, len(dados_eqth)):
            tmp = ''

            self.basekv = tten.TTEN[dados_eqth[0].ten_pri]

            # self.insertBusList(dados_eqth[ctd].nome)
            self.insertBusListDict(dados_eqth[0].cod_id, ".1.2.3.0")

            self.insertElementList("Vsource.source")

            tmp = "New Circuit.{0}".format(dados_eqth[0].cod_id)
            tmp += "  basekv={0}".format(self.basekv) + "  pu=1" + "  phase=3" + "  bus1={0}".format(
                dados_eqth[0].cod_id)
            #tmp += "  MVAsc3=10000000000000000000000" + "  MVAsc1=1000000000000000000000"
            self.barra_infinita = dados_eqth[0].cod_id
            memoFileEqTh.append(tmp)

            return memoFileEqTh

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações do Equivalente de Thevenin")

    def exec_EQUIVALENTE_DE_THEVENIN(self):

        self.memoFileEqTh = self.getEQUIVALENTE_DE_THEVENIN()

        self.memoFileEqTh.insert(0, "! EQUIVALENTE DE THEVENIN ")

    def getEQUIVALENTE_DE_THEVENIN_MEDIA(self):
        try:
            dados_eqth = self.DataBase.getData_CTMT_EQTH(self.nSE_MT_Selecionada)

            #memoFileEqThMT = []

            #tmp = ''
            for ctd in range(0, len(dados_eqth)):
                if dados_eqth[ctd].nome in self.nFieldsMT:
                    self.listaAlimentadores[dados_eqth[ctd].uni_tr_s] = dados_eqth[ctd].nome

                    # self.insertBusList(dados_eqth[ctd].nome)

                    #self.insertBusListDict(dados_eqth[ctd].nome, ".1.2.3.0")

                    #self.insertElementList("Circuit.{0}".format(dados_eqth[ctd].nome))

                    #basekv = tten.TTEN[dados_eqth[ctd].ten_nom]
                    #tmp += "New Circuit.{0}".format(dados_eqth[ctd].nome)
                    #tmp += "  basekv={0}".format(basekv) + " pu=1 " + "  phase=3 " + "  bus1={0}".format(
                        #dados_eqth[ctd].nome)


                    #memoFileEqThMT.append(tmp)

                #return memoFileEqThMT

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações do Equivalente de Thevenin")

    def exec_EQUIVALENTE_DE_THEVENIN_MEDIA(self):

        self.memoFileEqThMT = self.getEQUIVALENTE_DE_THEVENIN_MEDIA()

        self.memoFileEqThMT.insert(0, "! EQUIVALENTE DE THEVENIN MEDIA")

    def getSECEQTH(self, nomeSE_ATMT):

        try:

            tmpTrafo = []
            dados_trafo = self.DataBase.getData_TrafosAT_MT(nomeSE_ATMT)
            for ctd in range(0, len(dados_trafo)):
                tmpTrafo.append(dados_trafo[ctd].pac_1)
                tmpTrafo.append(dados_trafo[ctd].pac_2)

            dados_sec = self.DataBase.getData_SecAT(nomeSE_ATMT)

            tmpPAC1 = []
            tmpPAC2 = []

            for ctd in range(0, len(dados_sec)):
                tmpPAC1.append(dados_sec[ctd].pac_1)
                tmpPAC2.append(dados_sec[ctd].pac_2)

            tmpPAC = [list(set(tmpPAC1) - set(tmpPAC2)), list(set(tmpPAC2) - set(tmpPAC1))]

            tmpPAC = list(set().union(tmpPAC[0], tmpPAC[1]))  # Lista de barras que não estão conectadas em si

            tmpPAC = list(set(tmpPAC) - set(tmpTrafo))  # remove as barras dos transformadores de alta

            memoFileSECEQTH = []

            ##Definindo o LINECODE3
            memoFileSECEQTH.append(
                "New linecode.CHAVE_3 nphases = 3 BaseFreq = 60 r1 = 1e-3 x1 = 0.000")

            for ctd in range(0, len(dados_sec)):

                if ((dados_sec[ctd].pac_1 in tmpPAC) or (dados_sec[ctd].pac_2 in tmpPAC)):
                    # and ((dados_sec[ctd].pac_1.find(self.nCircuitoAT_MT[0:3]) != -1 ) or (dados_sec[ctd].pac_2.find(self.nCircuitoAT_MT[0:3])) != -1):

                    [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_sec[ctd].fas_con, dados_sec[ctd].pac_1,
                                                                        dados_sec[ctd].pac_2)

                    for con in tmpPAC:
                        pac_1 = pac_1.replace(con, self.nCircuitoAT_MT)
                        #print("kkkkkk", self.nCircuitoAT_MT)
                        pac_2 = pac_2.replace(con, self.nCircuitoAT_MT)
                        #print(pac_1, pac_2)

                    if dados_sec[ctd].fas_con == "ABC":
                        Linecode = " length=0.0001" + " LineCode=CHAVE_3 "
                    else:
                        Linecode = " length=0.0001"

                    if dados_sec[ctd].p_n_ope == "F":
                        operacao_da_chave = "YES"
                    if dados_sec[ctd].p_n_ope == "A":
                        operacao_da_chave = "NO"
                    if dados_sec[ctd].sit_ativ == "AT":
                        situacao = "true"
                    if dados_sec[ctd].sit_ativ == "DS":
                        situacao = "false"

                    temp_memoFileSEC = "New Line.{0}".format(dados_sec[ctd].cod_id) + "EQTH" + " Phases={0}".format(
                        num_de_fases)
                    temp_memoFileSEC += " Switch={0}".format(operacao_da_chave) + " Bus1={0}".format(pac_1)
                    temp_memoFileSEC += " Bus2={0}".format(pac_2) + Linecode
                    temp_memoFileSEC += " units=km" + " enabled={0}".format(situacao)

                    memoFileSECEQTH.append(temp_memoFileSEC)

                    ###Buffer
                    # self.insertBusList(dados_sec[ctd].pac_1)
                    # self.insertBusList(dados_sec[ctd].pac_2)
                    #
                    self.insertBusListDict(dados_sec[ctd].pac_1, self.afterValue(pac_1, "."))
                    self.insertBusListDict(dados_sec[ctd].pac_2, self.afterValue(pac_2, "."))

                    self.insertElementList("Line.{0}".format(dados_sec[ctd].cod_id) + "EQTH")

            return memoFileSECEQTH

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Seccionadoras de Conexão:")

    def exec_SEC_EQTHAT_SECAT(self):

        self.memoFileSecAT_EqThAT = self.getSECEQTH(self.nSE_MT_Selecionada)

        self.memoFileSecAT_EqThAT.insert(0,
                                         "! CHAVES SECCIONADORAS DE ALTA TENSAO - CONEXAO COM O EQUIVALENTE DE THEVENIN ")

    def getTRANSFORMADORES_DE_ALTA_PARA_MEDIA(self):
        try:
            print(self.nFieldsMT)
            self.Definindo_media_tensao_do_circuito()
            dados_trafo = self.DataBase.getData_TrafosAT_MT(self.nSE_MT_Selecionada)
            self.teste_Tratamento_trafo.ajuste_tensao_cargas_MT(dados_trafo)
            memoFileTrafoATMT = []

            self.trafosATMT_ideais['trafo_42'] = ['2', '3', self.barra_infinita, 'ATMT_42', '[1000000,1000000]',
                                                  '[' + self.basekv + ', 11.900]', '[delta, wye]', 'tap=1']

            self.trafosATMT_ideais['trafo_49'] = ['2', '3', self.barra_infinita, 'ATMT_49', '[1000000,1000000]',
                                                  '[' + self.basekv + ', 13.800]', '[delta, wye]', 'tap=1']

            self.trafosATMT_ideais['trafo_72'] = ['2', '3', self.barra_infinita, 'ATMT_72', '[1000000,1000000]',
                                                  '[' + self.basekv + ', 34.500]', '[delta, wye]', 'tap=1']

            #print(self.trafosATMT_ideais['trafo_72'][2], self.trafosATMT_ideais['trafo_72'][3],self.trafosATMT_ideais['trafo_72'][6])

            for ctd in self.trafosATMT_ideais:
                tmp = ""
                tmp += "New Transformer.{0}".format(ctd) + " windings={0}".format(
                    "2") + " Phases={0}".format("3")
                tmp += " buses={0}".format("[" + self.trafosATMT_ideais[ctd][2] + "," + self.trafosATMT_ideais[ctd][3] +
                                           ".1.2.3.0" + "]")
                tmp += " kVAs={0}".format(self.trafosATMT_ideais[ctd][4])
                tmp += " kVs={0}".format(self.trafosATMT_ideais[ctd][5])
                tmp += " conns={0}".format(self.trafosATMT_ideais[ctd][6]) + " tap=1"


                memoFileTrafoATMT.append(tmp)

                ##Buffer
                self.insertElementList("Transformer.{0}".format(ctd))
                # self.insertBusList(dados_trafo[ctd].pac_1)
                # self.insertBusList(dados_trafo[ctd].pac_2)
                ##
                self.insertBusListDict(self.barra_infinita, ".1.2.3")
                self.insertBusListDict(self.trafosATMT_ideais['trafo_72'][3], ".1.2.3.0")

            # for ctd in range(0, len(dados_trafo)):
            #     tmp = ""
            #
            #     tensao_pri = tten.TTEN[dados_trafo[ctd].ten_pri]
            #     tensao_sec = tten.TTEN[dados_trafo[ctd].ten_sec]
            #
            #     ligacao = tlig.TLIG[dados_trafo[ctd].lig]
            #
            #     # Potência
            #     pot_nom = tpotatr.TPOTAPRT[dados_trafo[ctd].pot_nom]
            #
            #     tmp += "New Transformer.{0}".format(dados_trafo[ctd].cod_id) + " windings={0}".format(
            #         "2") + " Phases={0}".format("3")
            #     tmp += " buses={0}".format("[" + dados_trafo[ctd].pac_1 + "," + dados_trafo[
            #         ctd].pac_2 + ".1.2.3.0" + "]") + " kVAs={0}".format(pot_nom)
            #     tmp += " kVs={0}".format("[" + tensao_pri + "," + tensao_sec + "]")
            #     tmp += " conns={0}".format(ligacao) + " tap=1"
            #
            #     memoFileTrafoATMT.append(tmp)
            #
            #     ##Buffer
            #     self.insertElementList("Transformer.{0}".format(dados_trafo[ctd].cod_id))
            #     # self.insertBusList(dados_trafo[ctd].pac_1)
            #     # self.insertBusList(dados_trafo[ctd].pac_2)
            #     ##
            #     self.insertBusListDict(dados_trafo[ctd].pac_1, ".1.2.3")
            #     self.insertBusListDict(dados_trafo[ctd].pac_2, ".1.2.3.0")



            return memoFileTrafoATMT

        ##Colocar os de três ennrolamentos

        except:
            raise class_exception.ExecOpenDSS(
                "Erro ao carregar as informações dos Transformadores de Alta para Média Tensão")

    def exec_TRANSFORMADORES_DE_ALTA_PARA_MEDIA(self):

        self.memoFileTrafoATMT = self.getTRANSFORMADORES_DE_ALTA_PARA_MEDIA()

        self.memoFileTrafoATMT.insert(0, "! TRANSFORMADORES DE ALTA PARA MEDIA TENSAO ")

    def getCONDUTORES(self, tipoCondutor):
        try:
            dados_cond = self.DataBase.getData_Condutores(tipoCondutor)

            memoFileCond = []

            for ctd in range(0, len(dados_cond)):
                tmp = ''
                tmp += "New Linecode.{0}".format(dados_cond[ctd].cod_id)
                tmp += " R1={0}".format(dados_cond[ctd].r1)
                tmp += " X1={0}".format(dados_cond[ctd].x1) + " normamps={0}".format(
                    dados_cond[ctd].cnom) + " units=km "
                memoFileCond.append(tmp)

                # self.insertElementList("Linecode.{0}".format(dados_cond[ctd].cod_id)

            return memoFileCond

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Condutores:" + tipoCondutor)

    def exec_CONDUTORES_DE_MEDIA_TENSAO(self):

        self.memoFileCondMT = self.getCONDUTORES("M")

        self.memoFileCondMT.insert(0, "! CONDUTORES DE MEDIA TENSAO ")

    def exec_CONDUTORES_DE_BAIXA_TENSAO(self):

        self.memoFileCondBT = self.getCONDUTORES("B")

        self.memoFileCondBT.insert(0, "! CONDUTORES DE BAIXA TENSAO ")

    def exec_CONDUTORES_DE_RAMAL(self):

        self.memoFileCondRamal = self.getCONDUTORES("R")

        self.memoFileCondRamal.insert(0, "! CONDUTORES DE RAMAL ")

        ################ PORQUE ISSO AQUI?

        # self.memoFileCondRamal.append("! LINECODE CHAVES ")

        # self.memoFileCondRamal.append("New Linecode.CHAVE_3 nphases=3 R1=0.0001 X1=0.0001 R0=0.02 X0=0.02 C1=0.02 C0=0.02 NormAmps=300 units=km BaseFreq=60")

    def getID_Fields(self, nameFields, seccionadora=None):

        lista_de_identificadores_dos_alimentadores = []
        if seccionadora is not None:
            for ctdDB in range(0, len(nameFields)):
                if nameFields[ctdDB].nome[0:3] in self.nFieldsMT[0][0:3]:
                    lista_de_identificadores_dos_alimentadores.append(nameFields[ctdDB].cod_id)
                    lista_de_identificadores_dos_alimentadores = (sorted(set(lista_de_identificadores_dos_alimentadores)))
        else:
            for ctdDB in range(0, len(nameFields)):
                if nameFields[ctdDB].nome in self.nFieldsMT:
                    lista_de_identificadores_dos_alimentadores.append(nameFields[ctdDB].cod_id)
                    lista_de_identificadores_dos_alimentadores = (sorted(set(lista_de_identificadores_dos_alimentadores)))
        return lista_de_identificadores_dos_alimentadores


    def getSEC(self, nomeSE_ATMT, tipoSEC, testAL_MT=None):
        try:
            ###Teste Alimentador para Chaves de Média Tensão

            if testAL_MT is not None:  # MT
                dados_ctmt = self.DataBase.getData_CTMT(None)

                lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)
                # if testAL_MT is not None:  # MT PORQUE DOIS IGUAIS

                dados_sec = self.DataBase.getData_SecMT(nomeSE_ATMT, tipoSEC)



            else:  # AT
                dados_sec = self.DataBase.getData_SecAT(nomeSE_ATMT)

            memoFileSEC = []

            for ctd in range(0, len(dados_sec)):

                [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_sec[ctd].fas_con, dados_sec[ctd].pac_1,
                                                                    dados_sec[ctd].pac_2)


                # if dados_sec[ctd].fas_con == "ABC":
                Linecode = " length=0.0001" + " LineCode=CHAVE_3 "
                # else:
                # Linecode = " length=0.0001"

                if dados_sec[ctd].p_n_ope == "F":
                    operacao_da_chave = "YES"
                if dados_sec[ctd].p_n_ope == "A":
                    operacao_da_chave = "YES"
                if dados_sec[ctd].sit_ativ == "AT":
                    situacao = "true"
                if dados_sec[ctd].sit_ativ == "DS":
                    situacao = "false"
                if dados_sec[ctd].sit_ativ == "0":
                    situacao = "false"

                if dados_sec[ctd].pac_2 in self.nFieldsMT:
                    for ctd_2 in range(0, len(self.media_tensao_do_circuito)):
                        if dados_sec[ctd].pac_2 == self.media_tensao_do_circuito[ctd_2].nom:
                            dados_trafo_p = self.media_tensao_do_circuito[ctd_2].ten_nom
                            break
                    #and dados_sec[ctd].pac_2 not in self.memoALIMENTADOR:
                    #self.memoALIMENTADOR.append(dados_sec[ctd].pac_2)
                    #dados_trafo_p = self.DataBase.getData_CTMT_EQTH(dados_sec[ctd].pac_2)
                    #print(self.memoALIMENTADOR)
                    #print(dados_sec[ctd].pac_2)
                    #print(dados_trafo_p[0].ten_nom)
                    #print(pac_2)
                    if dados_trafo_p == "42":
                        pac_1 = 'ATMT_42.1.2.3'

                    elif dados_trafo_p == "49":
                        pac_1 = 'ATMT_49.1.2.3'
                        
                    else:
                        pac_1 = 'ATMT_72.1.2.3'
                    #print(pac_1)

                temp_memoFileSEC = "New Line.{0}".format(dados_sec[ctd].cod_id)
                temp_memoFileSEC += " Switch={0}".format(operacao_da_chave) + " Bus1={0}".format(pac_1)
                temp_memoFileSEC += " Bus2={0}".format(pac_2) + Linecode
                temp_memoFileSEC += " units=km" + " enabled={0}".format(situacao) + " Phases={0}".format(num_de_fases)

                # Chaves de Média
                if testAL_MT is not None:  # MT
                    #print("lista de identificadores: ", lista_de_identificadores_dos_alimentadores, type(lista_de_identificadores_dos_alimentadores))
                    if dados_sec[ctd].ctmt in lista_de_identificadores_dos_alimentadores: #or len(
                            #dados_sec[ctd].ctmt) == 1:
                        if dados_sec[ctd].tip_unid == tipoSEC:
                            memoFileSEC.append(temp_memoFileSEC)

                            ##Buffer
                            self.insertElementList("Line.{0}".format(dados_sec[ctd].cod_id))
                            # self.insertBusList(dados_sec[ctd].pac_1)
                            # self.insertBusList(dados_sec[ctd].pac_2)
                            ##
                            self.insertBusListDict(dados_sec[ctd].pac_1, self.afterValue(pac_1, "."))
                            self.insertBusListDict(dados_sec[ctd].pac_2, self.afterValue(pac_2, "."))
                else:  # AT
                    memoFileSEC.append(temp_memoFileSEC)
                    ##Buffer
                    self.insertElementList("Line.{0}".format(dados_sec[ctd].cod_id))
                    # self.insertBusList(dados_sec[ctd].pac_1)
                    # self.insertBusList(dados_sec[ctd].pac_2)
                    ##
                    self.insertBusListDict(dados_sec[ctd].pac_1, self.afterValue(pac_1, "."))
                    self.insertBusListDict(dados_sec[ctd].pac_2, self.afterValue(pac_2, "."))
            return memoFileSEC

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Seccionadoras:" + tipoSEC)

    def exec_SEC_DE_ALTA_TENSAO(self):

        self.memoFileSecAT = self.getSEC(self.nSE_MT_Selecionada, None, None)

        self.memoFileSecAT.insert(0, "! CHAVES SECCIONADORAS DE ALTA TENSAO ")

    def getSEC_CONTROL(self, nomeSE_ATMT, tipoSEC, testAL_MT=None):
        try:
            lista = []
            ###Teste Alimentador para Chaves de Média Tensão

            if testAL_MT is not None:  # MT
                dados_ctmt = self.DataBase.getData_CTMT(None)

                lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)
                lista = lista_de_identificadores_dos_alimentadores

            if testAL_MT is not None:  # MT
                dados_sec = self.DataBase.getData_SecMT(nomeSE_ATMT, tipoSEC)
            else:  # AT
                dados_sec = self.DataBase.getData_SecAT(nomeSE_ATMT)

            memoFileSEC_CONTROL = []

            for ctd in range(0, len(dados_sec)):
                if dados_sec[ctd].p_n_ope == "F":
                    operacao_da_chave = "Close"
                if dados_sec[ctd].p_n_ope == "A":
                    operacao_da_chave = "Open"

                if tipoSEC == "22":  # Chave Fusível

                    curva_do_fusivel = tcapelofu.TCAPELFU[dados_sec[ctd].cap_elo]
                    RatedCurrent = dados_sec[ctd].cor_nom

                    temp_memoFileSEC_CONTROL = "New Fuse.{0}".format(
                        dados_sec[ctd].cod_id) + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format(
                        "Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " FuseCurve={0}".format(curva_do_fusivel).replace(",", ".") + " RatedCurrent={0}".format(
                        RatedCurrent)
                    temp_memoFileSEC_CONTROL += " State={0}".format(operacao_da_chave)
                    if dados_sec[ctd].ctmt in lista:
                        self.insertFuseList(temp_memoFileSEC_CONTROL)
                    ##Originalmente o OpenDSS não retorna esse elemento
                    temp_Element = ""  # "Fuse.{0}".format(dados_sec[ctd].cod_id)

                elif tipoSEC == "29":  # Chave DJ Relé
                    temp_memoFileSEC_CONTROL = "New Relay.{0}".format(
                        dados_sec[ctd].cod_id) + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format(
                        "Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " type=current" + " State={0}".format(operacao_da_chave)

                    temp_Element = "Relay.{0}".format(dados_sec[ctd].cod_id)
                    # Carvalho
                    if dados_sec[ctd].ctmt in lista:
                        self.insertRelayList(temp_memoFileSEC_CONTROL)

                elif tipoSEC == "32":  # Religador
                    temp_memoFileSEC_CONTROL = "New Swtcontrol.{0}".format(
                        # Era New Recloser, troquei pra swt pq tava dando problema. Vou rever depois - Messala
                        dados_sec[ctd].cod_id)  # + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format(
                        "Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " State={0}".format(operacao_da_chave)

                    temp_Element = "Recloser.{0}".format(dados_sec[ctd].cod_id)
                    # Carvalho
                    if dados_sec[ctd].ctmt in lista:
                        self.insertRecloserList(temp_memoFileSEC_CONTROL)
                else:
                    temp_memoFileSEC_CONTROL = "New Swtcontrol.{0}".format(
                        dados_sec[ctd].cod_id) + " SwitchedObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedTerm={0}".format("1") + " Action={0}".format(
                        operacao_da_chave)
                    temp_memoFileSEC_CONTROL += " lock=yes" + " State={0}".format(operacao_da_chave)
                    try:
                        if dados_sec[ctd].ctmt in lista:
                            self.insertSwtControlList(temp_memoFileSEC_CONTROL)
                    except:
                        pass
                    temp_Element = "Swtcontrol.{0}".format(dados_sec[ctd].cod_id)

                # Chaves de Média
                if testAL_MT is not None:  # MT
                    if dados_sec[ctd].ctmt in lista: #or len(dados_sec[ctd].ctmt) == 1:
                        if dados_sec[ctd].tip_unid == tipoSEC:
                            memoFileSEC_CONTROL.append(temp_memoFileSEC_CONTROL)

                            # Buffer
                            self.insertElementList(temp_Element)
                else:  # AT
                    memoFileSEC_CONTROL.append(temp_memoFileSEC_CONTROL)

                    # Buffer
                    self.insertElementList(temp_Element)

            return memoFileSEC_CONTROL

        except:
            raise class_exception.ExecOpenDSS(
                "Erro ao carregar as informações dos Controles das Seccionadoras:" + tipoSEC)

    def exec_CONTROLE_SEC_DE_ALTA_TENSAO(self):

        self.memoFileSecAT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, None, None)

        self.memoFileSecAT_Control.insert(0, "! CONTROLE DAS CHAVES SECCIONADORAS DE ALTA TENSAO ")

    def exec_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO(self):

        self.memoFileSecOleoMT = self.getSEC(self.nSE_MT_Selecionada, "17", "SIM")

        self.memoFileSecOleoMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO A OLEO ")

    def exec_CONTROLE_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO(self):

        self.memoFileSecOleoMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "17", "SIM")

        self.memoFileSecOleoMT_Control.insert(0, "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO TIPO OLEO ")

    def exec_SEC_CHAVE_FACA_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaMT = self.getSEC(self.nSE_MT_Selecionada, "19", "SIM")

        self.memoFileSecFacaMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FACA ")

    def exec_CONTROLE_SEC_CHAVE_FACA_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "19", "SIM")

        self.memoFileSecFacaMT_Control.insert(0, "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FACA ")

    def exec_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaTripolarMT = self.getSEC(self.nSE_MT_Selecionada, "20", "SIM")

        self.memoFileSecFacaTripolarMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FACA TRIPOLAR ")

    def exec_CONTROLE_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaTripolarMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "20", "SIM")

        self.memoFileSecFacaTripolarMT_Control.insert(0,
                                                      "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FACA TRIPOLAR ")

    def exec_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO(self):

        self.memoFileSecFusivelMT = self.getSEC(self.nSE_MT_Selecionada, "22", "SIM")

        self.memoFileSecFusivelMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL ")

    def exec_CONTROLE_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO(self):

        self.memoFileSecFusivelMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "22", "SIM")

        self.memoFileSecFusivelMT_Control.insert(0,
                                                 "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL ")

    def exec_SEC_CHAVE_FUSIVEL_ATERRAMENTO(self):

        self.memoFileSecFusivel_ATERRADO = self.getSEC(self.nSE_MT_Selecionada, "23", "SIM")

        self.memoFileSecFusivel_ATERRADO.insert(0,
                                                "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVE COM ATERRAMENTOL ")

    def exec_CONTROLE_SEC_CHAVE_FUSIVEL_ATERRAMENTO(self):

        self.memoFileSecFusivel_ATERRADO_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "23", "SIM")

        self.memoFileSecFusivel_ATERRADO_Control.insert(0,
                                                        "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL COM ATERRAMENTO ")

    def exec_SEC_CHAVE_FUSIVEL_LAMINA(self):

        self.memoFileSecFusivel_LAMINA = self.getSEC(self.nSE_MT_Selecionada, "26", "SIM")

        self.memoFileSecFusivel_LAMINA.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL LAMINA ")

    def exec_CONTROLE_SEC_CHAVE_FUSIVEL_LAMINA(self):

        self.memoFileSecFusivel_LAMINA_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "26", "SIM")

        self.memoFileSecFusivel_LAMINA_Control.insert(0,
                                                      "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL LAMINA ")

    def exec_SEC_CHAVE_FUSIVEL_TRESOPERACOES(self):

        self.memoFileSecFusivel_TRESOPERACOES = self.getSEC(self.nSE_MT_Selecionada, "27", "SIM")

        self.memoFileSecFusivel_TRESOPERACOES.insert(0,
                                                     "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL TRESOPERACOES ")

    def exec_CONTROLE_SEC_CHAVE_FUSIVEL_TRESOPERACOES(self):

        self.memoFileSecFusivel_TRESOPERACOES_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "27", "SIM")

        self.memoFileSecFusivel_TRESOPERACOES_Control.insert(0,
                                                             "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL TRES OPERACOES ")

    def exec_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO(self):

        self.memoFileSecDJReleMT = self.getSEC(self.nSE_MT_Selecionada, "29", "SIM")

        self.memoFileSecDJReleMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO DISJUNTOR ")

    def exec_CONTROLE_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO(self):

        self.memoFileSecDJReleMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "29", "SIM")

        self.memoFileSecDJReleMT_Control.insert(0,
                                                "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO DISJUNTOR ")

    def exec_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO(self):

        self.memoFileSecReligadorMT = self.getSEC(self.nSE_MT_Selecionada, "32", "SIM")

        self.memoFileSecReligadorMT.insert(0, "! CHAVES SECCIONADORAS RELIGADORES DE MEDIA TENSAO ")

    def exec_CONTROLE_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO(self):

        self.memoFileSecReligadorMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "32", "SIM")

        self.memoFileSecReligadorMT_Control.insert(0, "! CHAVES SECCIONADORAS RELIGADORES DE MEDIA TENSAO  ")

    def exec_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecTripolarSEMT = self.getSEC(self.nSE_MT_Selecionada, "33", "SIM")

        self.memoFileSecTripolarSEMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO TRIPOLAR SUBESTACAO")

    def exec_CONTROLE_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecTripolarSEMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "33", "SIM")

        self.memoFileSecTripolarSEMT_Control.insert(0,
                                                    "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO TRIPOLAR SUBESTACAO ")

    def exec_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecUnipolarSEMT = self.getSEC(self.nSE_MT_Selecionada, "34", "SIM")

        self.memoFileSecUnipolarSEMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO UNIPOLAR SUBESTACAO")

    def exec_CONTROLE_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecUnipolarSEMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "34", "SIM")

        self.memoFileSecUnipolarSEMT_Control.insert(0,
                                                    "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO UNIPOLAR SUBESTACAO ")

    def exec_SEC_CHAVE_SECCIONALIZADOR(self):

        self.memoFileSecSECCIONALIZADOR = self.getSEC(self.nSE_MT_Selecionada, "35", "SIM")

        self.memoFileSecSECCIONALIZADOR.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO SECCIONALIZADOR ")

    def exec_CONTROLE_SEC_CHAVE_SECCIONALIZADOR(self):

        self.memoFileSecSECCIONALIZADOR_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "35", "SIM")

        self.memoFileSecSECCIONALIZADOR_Control.insert(0,
                                                       "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO SECCIONALIZADOR ")

    def exec_SEC_CHAVE_SECCIONALIZADOR_MONOFASICO(self):

        self.memoFileSecSECCIONALIZADOR_MONOFASICO = self.getSEC(self.nSE_MT_Selecionada, "36", "SIM")

        self.memoFileSecSECCIONALIZADOR_MONOFASICO.insert(0,
                                                          "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO SECCIONALIZADOR MONOFÁSICO ")

    def exec_CONTROLE_SEC_CHAVE_SECCIONALIZADOR_MONOFASICO(self):

        self.memoFileSecSECCIONALIZADOR_MONOFASICO_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "36", "SIM")

        self.memoFileSecSECCIONALIZADOR_MONOFASICO_Control.insert(0,
                                                                  "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO SECCIONALIZADOR MONOFÁSICO ")

    def getSEGLINHA_REGULADOR_MT(self, nomeSE_MT, tipoSEG_REG):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoSEG_REG == "SEG":  # Segmentos de Linhas
                dados_db = self.DataBase.getData_SegLinhasMT(nomeSE_MT)

            elif tipoSEG_REG == "REG":  # Regulador de Média
                dados_db = self.DataBase.getData_ReguladorMT(nomeSE_MT)

            else:
                raise class_exception.ExecOpenDSS(
                    "Erro ao carregar as informações dos Segmentos de Linha ou Regulador, pois o tipo não foi especificado! \n" + tipoSEG_REG)

            memoFileLinha = []

            for ctd in range(0, len(dados_db)):

                [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1,
                                                                    dados_db[ctd].pac_2)

                if tipoSEG_REG == "SEG":  # Segmentos de Linhas
                    if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores) and \
                            (dados_db[ctd].pac_1 != self.nFieldsMT):
                        tmp = "New Line.{0}".format(dados_db[ctd].cod_id)
                        tmp += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        tmp += " Linecode={0}".format(dados_db[ctd].tip_cnd) + " Phases={0}".format(num_de_fases)
                        tmp += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                        tmp += " units=km"

                        memoFileLinha.append(tmp)

                        ##Buffer
                        self.insertElementList("Line.{0}".format(dados_db[ctd].cod_id))
                        # self.insertBusList(dados_db[ctd].pac_1)
                        # self.insertBusList(dados_db[ctd].pac_2)
                        #
                        self.insertBusListDict(dados_db[ctd].pac_1, self.afterValue(pac_1, "."))
                        self.insertBusListDict(dados_db[ctd].pac_2, self.afterValue(pac_2, "."))

                elif tipoSEG_REG == "REG":  # Regulador de Média         MESSALA: EU VOU ESCREVER COMO UM SEGMENTO POR ENQUANTO PQ ELE TA DERRUBANDO A TENSÃO NO SISTEMA. AINDA VOU OLHAR O MOTIVO

                    if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores) or len(
                            dados_db[ctd].descr) > 1:
                        # tmp = "New Transformer.{0}".format(dados_db[ctd].cod_id) + " windings={0}".format('2')
                        # tmp += " Phases={0}".format(num_de_fases) + " buses={0}".format('[' + pac_1 + ',' + pac_2 + ']')
                        # tmp += " conns={0}".format('[wye, wye]') + " kVAs={0}".format('[2000,2000]')
                        # tmp += " XHL={0}".format(".01") + " %LoadLoss={0}".format('0.00001')
                        # tmp += " ppm={0}".format('0.0')
                        # memoFileLinha.append(tmp)

                        # tmp = "New RegControl.{0}".format('c' + dados_db[ctd].cod_id)
                        # tmp += " Transformer={0}".format(dados_db[ctd].cod_id) + " winding=2 "
                        # tmp += " vreg=125" + " ptratio=60 " + " band=2"
                        # memoFileLinha.append(tmp)

                        tmp = "New Line.{0}".format(dados_db[ctd].cod_id)
                        tmp += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        tmp += " Linecode={0}".format('CHAVE_3 ') + " Phases={0}".format(num_de_fases)
                        tmp += " Length={0}".format('0.0001')
                        tmp += " units=km"

                        memoFileLinha.append(tmp)

                        ##Buffer
                        self.insertElementList("Transformer.{0}".format(dados_db[ctd].cod_id))
                        self.insertElementList("RegControl.{0}".format('c' + dados_db[ctd].cod_id))
                        # self.insertBusList(dados_db[ctd].pac_1)
                        # self.insertBusList(dados_db[ctd].pac_2)
                        #
                        self.insertBusListDict(dados_db[ctd].pac_1, self.afterValue(pac_1, "."))
                        self.insertBusListDict(dados_db[ctd].pac_2, self.afterValue(pac_2, "."))
                else:
                    raise class_exception.ExecOpenDSS(
                        "Erro ao carregar as informações dos Segmentos de Linha ou Regulador, pois o tipo não foi especificado! \n" + tipoSEG_REG)

            return memoFileLinha

        except:
            raise class_exception.ExecOpenDSS(
                "Erro ao carregar as informações dos Segmentos de Linha ou Regulador: " + tipoSEG_REG)

    def exec_SEG_LINHAS_DE_MEDIA_TENSAO(self):

        self.memoFileSegLinhasMT = self.getSEGLINHA_REGULADOR_MT(self.nSE_MT_Selecionada, "SEG")

        self.memoFileSegLinhasMT.insert(0, "! SEGMENTOS DE LINHA DE MEDIA TENSAO ")

    def exec_REGULADORES_DE_MEDIA_TENSAO(self):
        self.memoFileReguladorMT = self.getSEGLINHA_REGULADOR_MT(self.nSE_MT_Selecionada, "REG")

        self.memoFileReguladorMT.insert(0,
                                        "! UNIDADES REGULADORAS DE  MEDIA TENSAO MODELADA COMO TARNSFORMADORES DE BAIXA IMPEDANCIA ")

    def getUNIDADE_CONSUMIDORA(self, nomeSE_MT, tipoUniCons, conBTTD=None):
        loadshape = self.exec_Optimization(self.LoadShapes)
        vetor_carga_otimizada = []
        vetor_carga_NAO_otimizada = []

        try:
            mes = self.Config_Dia.get_Mes()

            # Curvas de Carga para se for Daily não precisar fazer nova consulta

            self.loadShapeUniCons[tipoUniCons] = []

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)
            if (tipoUniCons == "MT") or (tipoUniCons == "BT"):  #
                print("BUUUUG",nomeSE_MT)
                dados_db = self.DataBase.getData_UniConsumidora(nomeSE_MT, tipoUniCons)
            else:
                raise class_exception.ExecOpenDSS(
                    "Erro ao carregar as informações das Unidades Consumidoras, pois o tipo não foi especificado! \n" + tipoUniCons)

            memoFileUC = []
            #self.teste_Tratamento_trafo.tratamento_dados_TrafosDist(tipoUniCons, dados_db,
             #                                                       lista_de_identificadores_dos_alimentadores,
             #                                                       self.identificadorTrafo)

            #self.teste_Tratamento_trafo.get_trafo_sec(self.identificadorTrafo)
            self.tratamento_dados_TrafosDist(tipoUniCons, dados_db, lista_de_identificadores_dos_alimentadores)
            #for ctd in range(0, len(self.ajuste_memoria)):
                #if self.ajuste_memoria == self.teste_Tratamento_trafo.ajuste_memoria:
                    #print("DEU BOM")
                    #pass
                #else:
                    #print('DEU RUIM', dados_db[ctd].uni_tr)
            if tipoUniCons == "BT":
                self.teste_Tratamento_trafo.ajuste_tensao_cargas(dados_db)
            else:
                self.teste_Tratamento_trafo.ajuste_media_tensao(dados_db, 'UCMT', self.media_tensao_do_circuito)

            for ctd in range(0, len(dados_db)):

                tipo_curva = dados_db[ctd].tip_cc.replace(' ', "")

                if tipo_curva[0:3] == "RE-":
                    tipo_curva = "RES-" + tipo_curva[3:]

                elif tipo_curva[0:3] == "SER":
                    tipo_curva = "RES" + tipo_curva[3:]

                elif tipo_curva[0:2] == "PP":
                    tipo_curva = "SP" + tipo_curva[2:]

                curva_loadshape = loadshape[tipo_curva]
                #print('entrando', dados_db[ctd].ctmt, lista_de_identificadores_dos_alimentadores, dados_db[ctd].sit_ativ)
                if dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores and dados_db[ctd].sit_ativ == 'AT':
                    #print('entrou')
                    if mes == 'Janeiro':
                        max_carga = dados_db[ctd].ene_01
                    elif mes == 'Fevereiro':
                        max_carga = dados_db[ctd].ene_02
                    elif mes == 'Março':
                        max_carga = dados_db[ctd].ene_03
                    elif mes == 'Abril':
                        max_carga = dados_db[ctd].ene_04
                    elif mes == 'Maio':
                        max_carga = dados_db[ctd].ene_05
                    elif mes == 'Junho':
                        max_carga = dados_db[ctd].ene_06
                    elif mes == 'Julho':
                        max_carga = dados_db[ctd].ene_07
                    elif mes == 'Agosto':
                        max_carga = dados_db[ctd].ene_08
                    elif mes == 'Setembro':
                        max_carga = dados_db[ctd].ene_09
                    elif mes == 'Outubro':
                        max_carga = dados_db[ctd].ene_10
                    elif mes == 'Novembro':
                        max_carga = dados_db[ctd].ene_11
                    elif mes == 'Dezembro':
                        max_carga = dados_db[ctd].ene_12

                    carga_otimizada = (max_carga * 2) / ((sum(curva_loadshape) / max(curva_loadshape)) * 15)
                    if carga_otimizada > 0.6*(dados_db[ctd].car_inst):
                        carga_otimizada = 0.6*(dados_db[ctd].car_inst)

                    vetor_carga_otimizada.append(carga_otimizada)
                    vetor_carga_NAO_otimizada.append(dados_db[ctd].car_inst)

                    #if tipoUniCons == "BT":
                    #nivel_de_tensao = tten.TTEN[
                            #self.ajuste_memoria[ctd]]  # Pra coreção mudar mas vai ter que mudar
                    #else:
                        #nivel_de_tensao = tten.TTEN[dados_db[ctd].ten_forn]  # isso aqui vai ter que mudar

                    ######
                    ## Testando para verificar se o transformador foi listado na seleção, se foi ele vai ser considerado mesmo se concentrado as cargas
                    if (conBTTD == True) and (tipoUniCons == "BT"):

                        memoFileUC.append("! Tranformador de Distribuicao: " + dados_db[ctd].uni_tr)

                        if (dados_db[ctd].uni_tr not in self.nFieldsTD):

                            auxpac_1 = self.trafoDistUniCons[dados_db[ctd].uni_tr][-2]
                        else:
                            auxpac_1 = dados_db[ctd].pac
                    else:
                        auxpac_1 = dados_db[ctd].pac
                    ######

                    [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, auxpac_1, None)

                    #if tipoUniCons == "BT":
                        #conexao = "wye"
                    #if tipoUniCons == "MT":
                        #conexao = "wye"

                    if carga_otimizada != 0:

                        if num_de_fases != "2":
                            tmp = "New Load.{0}".format(dados_db[ctd].objectid) + " Bus1={0}".format(
                                pac_1) + " Phases={0}".format(num_de_fases)
                            tmp += " model=8 ZIPV=[0.5 0 0.5 1 0 0 0]" + " Kv={0}".format(dados_db[ctd].ten_forn)
                            tmp += " kW={0}".format(carga_otimizada) + " PF=0.92"
                            tmp += " conn={0}".format("wye")
                        else:
                            tmp = "New Load.{0}".format(dados_db[ctd].objectid) + " Bus1={0}".format(
                                pac_1.replace(".0", "")) + " Phases={0}".format("1")
                            tmp += " model=8 ZIPV=[0.5 0 0.5 1 0 0 0]" + " Kv={0}".format(dados_db[ctd].ten_forn)
                            tmp += " kW={0}".format(carga_otimizada) + " PF=0.92"
                            tmp += " conn={0}".format("delta")
                        #else:
                            #tmp = "New Load.{0}".format(dados_db[ctd].objectid) + " Bus1={0}".format(
                                #pac_1) + " Phases={0}".format(num_de_fases)
                            #tmp += " model=8 ZIPV=[0.5 0 0.5 1 0 0 0]" + " Kv={0}".format(nivel_de_tensao)
                            #tmp += " kW={0}".format(carga_otimizada) + " PF=0.92"
                            #tmp += " conn={0}".format(conexao)

                        memoFileUC.append(tmp)

                        self.loadShapeUniCons[tipoUniCons].append(
                            [dados_db[ctd].objectid, str(tipo_curva)])
                        ##Buffer
                        # self.insertBusList(dados_db[ctd].pac)
                        #
                        self.insertBusListDict(dados_db[ctd].pac, self.afterValue(pac_1, "."))

                        self.insertElementList("Load.{0}".format(dados_db[ctd].objectid))

            ####### TESTE DE CARGA
            ####### Sumário das Cargas
            #print("Relação de otimização: ", (sum(vetor_carga_otimizada) / sum(vetor_carga_NAO_otimizada)) * 100, "%")
            tmpUniTr = {}

            for ctd in range(0, len(dados_db)):
                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    if conBTTD == True:
                        if dados_db[ctd].uni_tr in tmpUniTr:
                            tmpUniTr[dados_db[ctd].uni_tr][-1] = tmpUniTr[dados_db[ctd].uni_tr][-1] + float(
                                dados_db[ctd].car_inst)
                        else:
                            tmpUniTr[dados_db[ctd].uni_tr] = [self.trafoDistUniCons[dados_db[ctd].uni_tr][-1],
                                                              float(dados_db[ctd].car_inst)]

            memoFileUC.append("! Sumário Rápido das Cargas")
            memoFileUC.append("! Somatório das potências das cargas sem curva de carga")
            for ctd in tmpUniTr:
                memoFileUC.append("! Transformador de Distribuição: " + ctd)
                memoFileUC.append("!    kVA: " + str(tmpUniTr[ctd][-2]))
                memoFileUC.append("!    Carga Total [kW]: {:03.2f}".format(tmpUniTr[ctd][-1]))
                memoFileUC.append("!    Carregamento [%]: {:03.2f}".format(tmpUniTr[ctd][-1] * 100 / tmpUniTr[ctd][-2]))

            #########################
            return memoFileUC

        except:
            raise class_exception.ExecOpenDSS(
                "Erro ao carregar as informações das Unidades Consumidoras: " + tipoUniCons)

    def exec_UNID_CONSUMIDORAS_MT(self):

        self.memoFileUniConsumidoraMT = self.getUNIDADE_CONSUMIDORA(self.nSE_MT_Selecionada, "MT", None)

        self.memoFileUniConsumidoraMT.insert(0, "! UNIDADES CONSUMIDORAS DE MEDIA TENSAO ")

    def exec_UNID_CONSUMIDORAS_BT(self):
        self.memoFileUniConsumidoraBT = self.getUNIDADE_CONSUMIDORA(self.nSE_MT_Selecionada, "BT", None)

        self.memoFileUniConsumidoraBT.insert(0, "! UNIDADES CONSUMIDORAS DE BAIXA TENSAO ")

    def exec_UNID_CONSUMIDORAS_BT_TD(self):
        self.memoFileUniConsumidoraBT_TD = self.getUNIDADE_CONSUMIDORA(self.nSE_MT_Selecionada, "BT", True)

        self.memoFileUniConsumidoraBT_TD.insert(0,
                                                "! UNIDADES CONSUMIDORAS DE BAIXA TENSAO NO TRANSFORMADOR DE DISTRIBUICAO")

    def exec_Optimization(self, LoadShapes):
        self.LoadShapes = LoadShapes
        return self.LoadShapes

    def getUNIDADE_CONSUMIDORA_LOADSHAPES(self, tipoUniCons):

        memoFileUCLS = []

        data = self.loadShapeUniCons[tipoUniCons]

        for ctd in data:
            # Filtro das erros de digitação das loadshapes
            if ctd[1][0:3] == "SER" or ctd[1][0:3] == "RE-":
                memoFileUCLS.append("Edit Load.{0}".format(ctd[0]) + " daily={0}".format("RES-" + ctd[1][3:]))

            elif ctd[1][0:2] == "PP":
                memoFileUCLS.append("Edit Load.{0}".format(ctd[0]) + " daily={0}".format("SP" + ctd[1][2:]))
            else:
                memoFileUCLS.append("Edit Load.{0}".format(ctd[0]) + " daily={0}".format(ctd[1]))
        return memoFileUCLS

    def exec_UNID_CONSUMIDORAS_LOADSHAPES_MT(self):

        self.memoFileUniConsumidoraLoadShapesMT = self.getUNIDADE_CONSUMIDORA_LOADSHAPES("MT")

        self.memoFileUniConsumidoraLoadShapesMT.insert(0, "! UNIDADES CONSUMIDORAS DE MEDIA TENSAO  - CURVAS DE CARGA")

    def exec_UNID_CONSUMIDORAS_LOADSHAPES_BT(self):

        self.memoFileUniConsumidoraLoadShapesBT = self.getUNIDADE_CONSUMIDORA_LOADSHAPES("BT")

        self.memoFileUniConsumidoraLoadShapesBT.insert(0, "! UNIDADES CONSUMIDORAS DE BAIXA TENSAO - CURVAS DE CARGA ")

    def getTRANSFORMADORES_DE_DISTRIBUICAO(self, nomeSE_MT):
        try:
            # Transformadores
            self.trafoDistUniCons = {}  ## Transformadores para as Cargas

            self.Get_EQTRD_By_CTMT()

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)
            print(lista_de_identificadores_dos_alimentadores)
            dados_db = self.DataBase.getData_TrafoDIST(self.lista_CTMT)

            #for ctd in range(0, len(dados_db)):
                #self.uni_tr_s.append(dados_db[ctd].uni_tr_s)

            #self.uni_tr_s = list(set(self.uni_tr_s))
            #variavel = str(self.uni_tr_s[0])

            #for ctd in range(1, len(self.uni_tr_s)):
                #variavel = variavel + "'" + " OR cod_id='" + str(self.uni_tr_s[ctd])

            #dados_trafo = self.DataBase.getData_TRAFO_UNTRS(variavel)
            # self.teste_Tratamento_trafo.ajuste_tensao_UNTRS(dados_trafo)

            self.teste_Tratamento_trafo.ajuste_tensao_trafos(dados_db)
            self.teste_Tratamento_trafo.ajuste_media_tensao(dados_db, 'alta_trafo_dist', self.media_tensao_do_circuito)
            memoFileTD = []
            for ctd in range(0, len(dados_db)):
                #self.identificadorTrafo.append(dados_db[ctd].cod_id)
                self.identificadorTrafo[dados_db[ctd].cod_id] = [dados_db[ctd].ten_lin_se, dados_db[ctd].fas_con_s]
                if dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores:
                    [num_de_fases, pac_1, pac_2_1, pac_2_2, windings] = self.getFasesConexao_trafodist(
                        dados_db[ctd].fas_con_s, dados_db[ctd].pac_1,
                        dados_db[ctd].pac_2)
                    self.num_de_fases[dados_db[ctd].cod_id] = num_de_fases

                    tensao_primario = str(dados_db[ctd].ten_pri)
                    tensao_secundario = str(dados_db[ctd].ten_lin_se)
                    tensao_sec_1 = str(dados_db[ctd].ten_lin_se)
                    tensao_sec_2 = tensao_sec_1
                    pot_nominal = tpotatr.TPOTAPRT[dados_db[ctd].pot_nom_eqtrd]
                    pot_nominal_bifase = tpotatr.TPOTAPRT_bifase[dados_db[ctd].pot_nom_eqtrd]
                    ligacao = tlig.TLIG[dados_db[ctd].lig]
                    ligacao_bifase = tlig.TLIG_BIFASICO[dados_db[ctd].lig]
                    if num_de_fases == '1' and windings == 3:
                        memoFileTD.append("! ALIMENTADOR: " + dados_db[ctd].ctmt)
                        # UNTRD
                        tmp = "New Transformer.{0}".format(dados_db[ctd].cod_id) + " windings={0}".format(windings)
                        tmp += " Phases={0}".format(num_de_fases)
                        tmp += " buses={0}".format('[' + pac_1 + ',' + pac_2_1 + ',' + pac_2_2 + ']')
                        tmp += " kVAs={0}".format(pot_nominal_bifase)
                        # EQRTD
                        tmp += " kVs={0}".format('[' + tensao_primario + ',' + tensao_sec_1 + ',' + tensao_sec_2 + ' ]')
                        tmp += " conns={0}".format(ligacao_bifase) + " %Rs={0}".format(
                            '[' + str(dados_db[ctd].r) + ',' + str(dados_db[ctd].r) + ',' + str(dados_db[ctd].r) + ']')
                        tmp += " XHL={0}".format(dados_db[ctd].xhl) + " XHT={0}".format(
                            dados_db[ctd].xhl) + " XLT={0}".format(dados_db[ctd].xhl)

                        memoFileTD.append(tmp)

                        ### trafo paras as cargas
                        self.trafoDistUniCons[str(dados_db[ctd].cod_id)] = [dados_db[ctd].pac_2, dados_db[ctd].pot_nom]

                        ##Buffer
                        # self.insertBusList(dados_db[ctd].pac_1)
                        # self.insertBusList(dados_db[ctd].pac_2)
                        ###
                        self.insertBusListDict(dados_db[ctd].pac_1, self.afterValue(pac_1, "."))
                        self.insertBusListDict(dados_db[ctd].pac_2, self.afterValue(pac_2_1, "."))
                        self.insertBusListDict(dados_db[ctd].pac_2, self.afterValue(pac_2_2, "."))
                        self.insertElementList("Transformer.{0}".format(dados_db[ctd].cod_id))

                    else:  # num_de_fases == '3':
                        memoFileTD.append("! ALIMENTADOR: " + dados_db[ctd].ctmt)
                        # UNTRD
                        tmp = "New Transformer.{0}".format(dados_db[ctd].cod_id) + " windings={0}".format(windings)
                        tmp += " Phases={0}".format(num_de_fases)
                        tmp += " buses={0}".format('[' + pac_1 + ',' + pac_2_1 + ']')
                        tmp += " kVAs={0}".format(pot_nominal)
                        # EQRTD
                        tmp += " kVs={0}".format('[' + tensao_primario + ',' + tensao_secundario + ' ]')
                        tmp += " conns={0}".format(ligacao) + " %Rs={0}".format(str(dados_db[ctd].r))
                        tmp += " XHL={0}".format(dados_db[ctd].xhl)
                        memoFileTD.append(tmp)

                        ### trafo paras as cargas
                        self.trafoDistUniCons[str(dados_db[ctd].cod_id)] = [dados_db[ctd].pac_2, dados_db[ctd].pot_nom]
                        ##Buffer
                        # self.insertBusList(dados_db[ctd].pac_1)
                        # self.insertBusList(dados_db[ctd].pac_2)
                        ###
                        self.insertBusListDict(dados_db[ctd].pac_1, self.afterValue(pac_1, "."))
                        self.insertBusListDict(dados_db[ctd].pac_2, self.afterValue(pac_2_1, "."))
                        self.insertElementList("Transformer.{0}".format(dados_db[ctd].cod_id))

            return memoFileTD

        except:
            raise class_exception.ExecOpenDSS(
                "Erro ao carregar as informações dos Transformadores de Distribuição MT ")

    def exec_TRANSFORMADORES_DE_DISTRIBUICAO(self):

        self.memoFileTrafoDist = self.getTRANSFORMADORES_DE_DISTRIBUICAO(self.nSE_MT_Selecionada)

        self.memoFileTrafoDist.insert(0, "! TRANSFORMADORES DE DISTRIBUICAO ")

    def getSEG_LINHAS_RAMAL_LIGACAO(self, nomeSE_MT, tipoLinha, conBTTD=None):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoLinha == "SEGBT":  # Segmentos de Linhas de Baixa Tensão
                dados_db = self.DataBase.getData_SegLinhasRamLigBT(nomeSE_MT, "SEGBT")
            elif tipoLinha == "RLIG":  # Ramal de Ligação
                dados_db = self.DataBase.getData_SegLinhasRamLigBT(nomeSE_MT, "RLIG")
            else:
                raise class_exception.ExecOpenDSS(
                    "Erro ao carregar as informações das Linhas BT, pois o tipo não foi especificado! \n" + tipoLinha)

            memoFileLinha = []

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    checkOK = False

                    if conBTTD:
                        if dados_db[ctd].uni_tr in self.nFieldsTD:
                            checkOK = True
                    else:
                        checkOK = True

                    if checkOK:
                        [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1,
                                                                            dados_db[ctd].pac_2)

                        tmp = "New Line.{0}".format(dados_db[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                        tmp += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        tmp += " Linecode={0}".format(dados_db[ctd].tip_cnd)
                        tmp += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                        tmp += " units=km"

                        memoFileLinha.append(tmp)

                        ##Buffer
                        self.insertElementList("Line.{0}".format(dados_db[ctd].cod_id))
                        # self.insertBusList(dados_db[ctd].pac_1)
                        # self.insertBusList(dados_db[ctd].pac_2)
                        #
                        self.insertBusListDict(dados_db[ctd].pac_1, self.afterValue(pac_1, "."))
                        self.insertBusListDict(dados_db[ctd].pac_2, self.afterValue(pac_2, "."))

            return memoFileLinha

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoLinha)

    def exec_SEG_LINHAS_DE_BAIXA_TENSAO(self):

        self.memoFileSegLinhasBT = self.getSEG_LINHAS_RAMAL_LIGACAO(self.nSE_MT_Selecionada, "SEGBT", False)

        self.memoFileSegLinhasBT.insert(0, "! SEGMENTOS DE LINHA DE BAIXA TENSAO ")

    def exec_SEG_LINHAS_DE_BAIXA_TENSAO_TD(self):

        self.memoFileSegLinhasBT = self.getSEG_LINHAS_RAMAL_LIGACAO(self.nSE_MT_Selecionada, "SEGBT", True)

        self.memoFileSegLinhasBT.insert(0, "! SEGMENTOS DE LINHA DE BAIXA TENSAO ")

    def exec_RAMAL_DE_LIGACAO(self):

        self.memoFileRamaisLigBT = self.getSEG_LINHAS_RAMAL_LIGACAO(self.nSE_MT_Selecionada, "RLIG", False)

        self.memoFileRamaisLigBT.insert(0, "! RAMAL_DE_LIGACAO ")

    def getUNID_COMPENSADORAS_DE_REATIVO(self, nomeSE_MT, tipoCAP):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoCAP == "MT":  # Segmentos de Linhas de Baixa Tensão
                dados_db = self.DataBase.getData_UniCompReativo(nomeSE_MT, "MT")
            elif tipoCAP == "BT":  # Ramal de Ligação
                dados_db = self.DataBase.getData_UniCompReativo(nomeSE_MT, "BT")
            else:
                raise class_exception.ExecOpenDSS(
                    "Erro ao carregar as informações das Linhas BT, pois o tipo não foi especificado! \n" + tipoCAP)

            memoFileComp = []

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):
                    [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1,
                                                                        None)

                    tmp = "New Capacitor.{0}".format(dados_db[ctd].cod_id) + " Bus1={0}".format(pac_1)
                    tmp += " Phases={0}".format(num_de_fases)
                    tmp += " kVAR={0}".format(str(dados_db[ctd].pot_nom))

                    memoFileComp.append(tmp)

                    ##Buffer
                    self.insertElementList("Capacitor.{0}".format(dados_db[ctd].cod_id))
                    # self.insertBusList(dados_db[ctd].pac_1)
                    #
                    self.insertBusListDict(dados_db[ctd].pac_1, self.afterValue(pac_1, "."))

            return memoFileComp

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoCAP)

    def exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO(self):

        self.memoFileUndCompReatMT = self.getUNID_COMPENSADORAS_DE_REATIVO(self.nSE_MT_Selecionada, "MT")

        self.memoFileUndCompReatMT.insert(0, "! UNIDADES COMPENSADORAS DE REATIVO DE MEDIA TENSAO")

    def exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO(self):

        self.memoFileUndCompReatBT = self.getUNID_COMPENSADORAS_DE_REATIVO(self.nSE_MT_Selecionada, "BT")

        self.memoFileUndCompReatBT.insert(0, "! UNIDADES COMPENSADORAS DE REATIVO DE BAIXA TENSAO ")

    ############### Otimizações Adicionais

    def getFasesConexao(self, fas_con, pac_1, pac_2=None):

        resultfase = ''

        if pac_2 is None:
            pac_2 = ""

        if fas_con == "ABC":
            num_de_fases = "3"
            pac_1 = pac_1.replace('-', "") + ".1.2.3"
            pac_2 = pac_2.replace('-', "") + ".1.2.3"
        if fas_con == ("AB"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".1.2"
            pac_2 = pac_2.replace('-', "") + ".1.2"
        if fas_con == ("BC"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".2.3"
            pac_2 = pac_2.replace('-', "") + ".2.3"
        if fas_con == ("CA"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".3.1"
            pac_2 = pac_2.replace('-', "") + ".3.1"
        if fas_con == "ABCN":
            num_de_fases = "3"
            pac_1 = pac_1.replace('-', "") + ".1.2.3.0"
            pac_2 = pac_2.replace('-', "") + ".1.2.3.0"
        if fas_con == ("ABN"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".1.2.0"
            pac_2 = pac_2.replace('-', "") + ".1.2.0"
        if fas_con == ("BCN"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".2.3.0"
            pac_2 = pac_2.replace('-', "") + ".2.3.0"
        if fas_con == ("CAN"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".3.1.0"
            pac_2 = pac_2.replace('-', "") + ".3.1.0"
        if fas_con == ("AN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".1.0"
            pac_2 = pac_2.replace('-', "") + ".1.0"
        if fas_con == ("BN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".2.0"
            pac_2 = pac_2.replace('-', "") + ".2.0"
        if fas_con == ("CN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".3.0"
            pac_2 = pac_2.replace('-', "") + ".3.0"
        if fas_con == ("A"):
            num_de_fases = "1"
            pac_1 = pac_1.replace("-", "") + ".1"
            pac_2 = pac_2.replace("-", "") + ".1"
        if fas_con == ("B"):
            num_de_fases = "1"
            pac_1 = pac_1.replace("-", "") + ".2"
            pac_2 = pac_2.replace("-", "") + ".2"
        if fas_con == ("C"):
            num_de_fases = "1"
            pac_1 = pac_1.replace("-", "") + ".3"
            pac_2 = pac_2.replace("-", "") + ".3"

        resultfase = [num_de_fases, pac_1, pac_2]

        return resultfase

    def getFasesConexao_trafodist(self, fas_con_s, pac_1, pac_2=None):

        resultfase = ''

        if pac_2 is None:
            pac_2 = ""

        if fas_con_s == "ABCN":
            num_de_fases = "3"
            pac_1 = pac_1.replace('-', "") + ".1.2.3"
            pac_2_1 = pac_2.replace('-', "") + ".1.2.3.0"
            pac_2_2 = pac_2_1
            windings = 2
        elif fas_con_s == ("ABN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".1.2"
            pac_2_1 = pac_2.replace('-', "") + ".1.0"
            pac_2_2 = pac_2.replace('-', "") + ".0.2"
            windings = 3
        elif fas_con_s == ("BCN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".2.3"
            pac_2_1 = pac_2.replace('-', "") + ".2.0"
            pac_2_2 = pac_2.replace('-', "") + ".0.3"
            windings = 3
        elif fas_con_s == ("CAN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".3.1"
            pac_2_1 = pac_2.replace('-', "") + ".3.0"
            pac_2_2 = pac_2.replace('-', "") + ".0.1"
            windings = 3
        elif fas_con_s == ("AN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".1.0"
            pac_2_1 = pac_2.replace('-', "") + ".1.0"
            pac_2_2 = pac_2_1
            windings = 2
        elif fas_con_s == ("BN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".2.0"
            pac_2_1 = pac_2.replace('-', "") + ".2.0"
            pac_2_2 = pac_2_1
            windings = 2
        elif fas_con_s == ("CN"):
            num_de_fases = "1"
            pac_1 = pac_1.replace('-', "") + ".3.0"
            pac_2_1 = pac_2.replace('-', "") + ".3.0"
            pac_2_2 = pac_2_1
            windings = 2

        resultfase = [num_de_fases, pac_1, pac_2_1, pac_2_2, windings]

        return resultfase

    def tratamento_dados_TrafosDist(self, tipoUniCons, dados_db, lista_de_identificadores_dos_alimentadores): #ESSA lista de identificadores tem que ser otimizada.

        if tipoUniCons == 'BT':
            self.ajusteTrafos.clear()
            self.ajuste_memoria.clear()
            UniCons_filter = self.identificadorTrafo.keys()
            for ctd in range(0, len(dados_db)):
                if dados_db[ctd].uni_tr not in self.ajusteTrafos.keys():
                    self.ajusteTrafos[dados_db[ctd].uni_tr] = {"1": []}
                    self.ajusteTrafos[dados_db[ctd].uni_tr].update({"2": []})
                    self.ajusteTrafos[dados_db[ctd].uni_tr].update({"3": []})

                if len(dados_db[ctd].fas_con) == 2:
                    self.ajusteTrafos[dados_db[ctd].uni_tr]["1"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].uni_tr + '1')

                elif len(dados_db[ctd].fas_con) == 3:
                    self.ajusteTrafos[dados_db[ctd].uni_tr]["2"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].uni_tr + '2')

                elif len(dados_db[ctd].fas_con) == 4:
                    self.ajusteTrafos[dados_db[ctd].uni_tr]["3"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].uni_tr + '3')

        else:
            UniCons_filter = lista_de_identificadores_dos_alimentadores
            for ctd in range(0, len(dados_db)):
                if dados_db[ctd].ctmt not in self.ajusteTrafos.keys():
                    self.ajusteTrafos[dados_db[ctd].ctmt] = {"1": []}
                    self.ajusteTrafos[dados_db[ctd].ctmt].update({"2": []})
                    self.ajusteTrafos[dados_db[ctd].ctmt].update({"3": []})

                if len(dados_db[ctd].fas_con) == 2:
                    self.ajusteTrafos[dados_db[ctd].ctmt]["1"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].ctmt + '1')

                elif len(dados_db[ctd].fas_con) == 3:
                    self.ajusteTrafos[dados_db[ctd].ctmt]["2"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].ctmt + '2')

                elif len(dados_db[ctd].fas_con) == 4:
                    self.ajusteTrafos[dados_db[ctd].ctmt]["3"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].ctmt + '3')

        for ctd in UniCons_filter:
            if ctd in self.ajusteTrafos.keys():
                for ctd_2 in range(1, 4):
                    if self.ajusteTrafos[ctd][str(ctd_2)]:
                        self.ajusteTrafos[ctd][str(ctd_2)] = max(set(self.ajusteTrafos[ctd][str(ctd_2)]),
                                                                 key=self.ajusteTrafos[ctd][
                                                                  str(ctd_2)].count)
                        for count in range(0, len(self.ajuste_memoria)):
                            ctmt_lenght = len(ctd)
                            if self.ajuste_memoria[count][0:ctmt_lenght] == ctd and self.ajuste_memoria[count][
                                ctmt_lenght] == str(
                                    ctd_2):
                                self.ajuste_memoria[count] = self.ajusteTrafos[ctd][str(ctd_2)]
                                #self.ajusteTrafos[ctd][str(ctd_2)] = self.ajuste_memoria[count]


        #print('padrao', len(self.ajuste_memoria))
        #print('padrao', len(self.ajusteTrafos))
        #print(('padrao', self.ajuste_memoria))
        #print(('padrao', self.ajusteTrafos))

    def Definindo_media_tensao_do_circuito(self):

        for ctd in range(0, len(self.nFieldsMT)):
            print(ctd)
            if ctd == 0:
                self.listaAlimentadores = self.nFieldsMT[ctd] + "'"
            else:
                self.listaAlimentadores = self.listaAlimentadores + " OR pac = '" + self.nFieldsMT[ctd] + "'"
        print(self.listaAlimentadores)
        self.media_tensao_do_circuito = self.DataBase.getData_CTMT_EQTH(self.listaAlimentadores)

    def Get_EQTRD_By_CTMT(self):
        for ctd in range(0, len(self.media_tensao_do_circuito)):
            if ctd == 0:
                self.lista_CTMT = self.media_tensao_do_circuito[ctd].cod_id + "'"
            else:
                self.lista_CTMT = self.lista_CTMT + " OR pac_1 LIKE '%" + self.media_tensao_do_circuito[ctd].cod_id + "'"




    def Ajuste_cargas_bifasicas(self, trafo_dist, ten_forn):
        #print(trafo_dist, ten_forn, self.num_de_fases[trafo_dist], type(ten_forn), type(trafo_dist))

        if self.num_de_fases[trafo_dist] == "1":
            if ten_forn == 0.44:
                ten_forn_ajustada = 0.38

            #elif ten_forn == 0.254:
            #    ten_forn_ajustada = 0.127

        else:
            #if ten_forn == 0.22:
            #    ten_forn_ajustada = 0.127

            #elif ten_forn == 0.38:
            #    ten_forn_ajustada = 0.22

            #elif ten_forn == 0.44:
            #    ten_forn_ajustada = 0.254
            ten_forn_ajustada = ten_forn
        return ten_forn_ajustada


    def afterValue(self, value, a):
        # Find and validate first part.
        pos_a = value.find(a)
        if pos_a == -1: return ""
        # Returns chars after the found string.
        adjusted_pos_a = pos_a + len(a) - 1
        if adjusted_pos_a >= len(value): return ""
        return value[adjusted_pos_a:]

    #def insertBusList(self, pac):
    #    if pac.replace('-', "") not in self.busList:
    #        self.busList.append(pac.replace('-', ""))

    def insertBusListDict(self, pac, pac_fases):
        if pac.replace('-', "") not in self.busListDict:
            self.busListDict[pac.replace('-', "")] = pac_fases

    def insertElementList(self, name):
        if str(name) not in self.elementList:
            self.elementList.append(str(name))

    def insertRecloserList(self, name):
        if str(name) not in self.recloserList:
            self.recloserList.append(str(name))

    def insertFuseList(self, name):
        if str(name) not in self.fuseList:
            self.fuseList.append(str(name))

    def insertRelayList(self, name):
        if str(name) not in self.relayList:
            self.relayList.append(str(name))

    def insertSwtControlList(self, name):
        if str(name) not in self.swtcontrolList:
            self.swtcontrolList.append(str(name))
