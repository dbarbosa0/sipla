import database.class_data
import class_exception

import database.class_conn

class C_Data(): # classe OpenDSS

    def __init__(self):

        self.DataBase = database.class_data.C_DBaseData() #Acesso ao Banco de Dados
        self._DataBaseConn = database.class_conn.C_DBaseConn()  # Carregando o acesso aos Arquivos do BDGD
        
        
        self._nCircuitoAT_MT = ''
        self._nSE_MT_Selecionada = ''
        self._nFieldsMT = ''

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
        

    def initUI(self):

        #Criando variáveis do Redirect
        self.memoFileHeader = [] #Cabeçalho do arquivo
        self.memoFileFooter = []  # Rodapé do arquivo
        self.memoFileEqTh = []  # Arquivo Thevenin
        self.memoFileEqThMT = []  # Arquivo Thevenin Média
        self.memoFileSecAT_EqThAT = [] # Seccionadora entre o Equivalente e a Seccionadora de AT
        self.memoFileTrafoATMT = [] #Transformadores de AT MT
        self.memoFileCondMT = [] #Condutores de Média Tensão
        self.memoFileCondBT = [] #Condutores de Baixa Tensão
        self.memoFileCondRamal = [] #Condutores de Ramal
        self.memoFileSecAT = [] #Seccionadora de Alta Tensão
        self.memoFileSecAT_Control = [] # Controle da Secionadora de Alta Tensão
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
        self.memoFileTrafoDist = []  #Transformadores de Distribuição
        self.memoFileSegLinhasBT = []  # Segmentos de Linhas de Baixa Tensão
        self.memoFileUniConsumidoraBT = []  # Unidade Consumidora de Baixa Tensão
        self.memoFileRamaisLigBT = [] # Ramais de Ligação
        self.memoFileUndCompReatMT = [] #Unidade de Compensação de Reativo de Baixa Tensão
        self.memoFileUndCompReatBT = [] #Unidade de Compensação de Reativo de Baixa Tensão


    def exec_HeaderFile(self):

        self.DataBase.DataBaseConn = self.DataBaseConn

        self.memoFileHeader = []

        self.memoFileHeader.insert(0, "Clear ")

        self.memoFileHeader.insert(1,"! VAMOS QUE VAMOS ")

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
        #print("Ramais de Ligação  ...")
        #self.exec_RAMAL_DE_LIGACAO()
        print("Unidades Compensadoras de MT ...")
        self.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO()
        print("Unidades Compensadoras de BT ...")
        self.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO()

        print("Processamento Finalizado!")


    def getEQUIVALENTE_DE_THEVENIN(self):
        try:
            dados_eqth = self.DataBase.getData_EqThevenin(self.nCircuitoAT_MT)

            memoFileEqTh = []

            for ctd in range(0,len(dados_eqth)):
                tmp = ''
                if dados_eqth[ctd].ten_nom == "82":
                    basekv = "69"
                if dados_eqth[ctd].ten_nom  == "94":
                    basekv = "138"
                if dados_eqth[ctd].ten_nom== "96":
                    basekv = "230"

                tmp = "New Circuit.{0}".format(dados_eqth[ctd].nome)
                tmp += "  basekv={0}".format(basekv)  + "  pu=1" + "  phase=3" + "  bus1={0}".format(dados_eqth[ctd].nome)
                tmp += "  MVAsc3=10000000000000000000000" + "  MVAsc1=1000000000000000000000"

                memoFileEqTh.append(tmp)

            return memoFileEqTh

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações do Equivalente de Thevenin")

    def exec_EQUIVALENTE_DE_THEVENIN(self):

        self.memoFileEqTh = self.getEQUIVALENTE_DE_THEVENIN()

        self.memoFileEqTh.insert(0, "! EQUIVALENTE DE THEVENIN ")

    def getEQUIVALENTE_DE_THEVENIN_MEDIA(self):
        try:

            dados_eqth = self.DataBase.getData_CTMT(self.nSE_MT_Selecionada)


            memoFileEqThMT = []

            tmp = ''

            for ctd in range(0,len(dados_eqth)):
                if dados_eqth[ctd].nome in self.nFieldsMT :
                    if dados_eqth[ctd].ten_nom  == "82":
                        basekv = "69"
                    if dados_eqth[ctd].ten_nom == "94":
                        basekv = "138"
                    if dados_eqth[ctd].ten_nom == "96":
                        basekv = "230"
                    if dados_eqth[ctd].ten_nom == "42":
                        basekv = "11.9"
                    if dados_eqth[ctd].ten_nom == "49":
                        basekv = "13.8"
                    if dados_eqth[ctd].ten_nom == "82":
                        basekv = "69"
                    if dados_eqth[ctd].ten_nom == "94":
                        basekv = "138"
                    if dados_eqth[ctd].ten_nom == "72":
                        basekv = "230"

                    tmp += "New Circuit.{0}".format(dados_eqth[ctd].nome)
                    tmp += "  basekv={0}".format(basekv)  + " pu=1 " + "  phase=3 " + "  bus1={0}".format(dados_eqth[ctd].nome)
                    tmp += "  MVAsc3=10000000000000000000000" + " MVAsc1=1000000000000000000000"

                    memoFileEqThMT.append(tmp)

                return memoFileEqThMT

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

            tmpPAC = [list(set(tmpPAC1) - set(tmpPAC2)) , list(set(tmpPAC2) - set(tmpPAC1)) ]

            tmpPAC = list(set().union(tmpPAC[0],tmpPAC[1])) # Lista de barras que não estão conectadas em si

            tmpPAC = list(set(tmpPAC) - set(tmpTrafo)) # remove as barras dos transformadores

            memoFileSECEQTH = []

            ##Definindo o LINECODE3
            memoFileSECEQTH.append("New linecode.CHAVE_3 nphases = 3 BaseFreq = 60 r1 = 1e-3 x1 = 0.000 r0 = 1e-3 x0 = 0.000 c1 = 0.000 c0 = 0.000")

            for ctd in range(0, len(dados_sec)):

                if ((dados_sec[ctd].pac_1 in tmpPAC) or (dados_sec[ctd].pac_2 in tmpPAC)):
                        #and ((dados_sec[ctd].pac_1.find(self.nCircuitoAT_MT[0:3]) != -1 ) or (dados_sec[ctd].pac_2.find(self.nCircuitoAT_MT[0:3])) != -1):

                    [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_sec[ctd].fas_con, dados_sec[ctd].pac_1, dados_sec[ctd].pac_2)

                    for con in tmpPAC:
                        pac_1 = pac_1.replace(con, self.nCircuitoAT_MT)
                        pac_2 = pac_2.replace(con, self.nCircuitoAT_MT)

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

                    temp_memoFileSEC = "New Line.{0}".format(dados_sec[ctd].cod_id) + "EQTH" + " Phases={0}".format(num_de_fases)
                    temp_memoFileSEC += " Switch={0}".format(operacao_da_chave) + " Bus1={0}".format(pac_1)
                    temp_memoFileSEC += " Bus2={0}".format(pac_2) + Linecode
                    temp_memoFileSEC += " units=km" + " enabled={0}".format(situacao)

                    memoFileSECEQTH.append(temp_memoFileSEC)

            return memoFileSECEQTH

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Seccionadoras de Conexão:")

    def exec_SEC_EQTHAT_SECAT(self):

        self.memoFileSecAT_EqThAT = self.getSECEQTH(self.nSE_MT_Selecionada)

        self.memoFileSecAT_EqThAT.insert(0, "! CHAVES SECCIONADORAS DE ALTA TENSAO - CONEXAO COM O EQUIVALENTE DE THEVENIN ")


    def getTRANSFORMADORES_DE_ALTA_PARA_MEDIA(self):
        try:
            dados_trafo = self.DataBase.getData_TrafosAT_MT(self.nSE_MT_Selecionada)

            memoFileTrafoATMT = []


            for ctd in range(0,len(dados_trafo)):
                tmp = ""

                if dados_trafo[ctd].ten_pri == "82":
                    tensao_pri = "69"
                if dados_trafo[ctd].ten_pri == "72":
                    tensao_pri = "34.5"
                if dados_trafo[ctd].ten_pri == "94":
                    tensao_pri = "138"
                if dados_trafo[ctd].ten_pri == "96":
                    tensao_pri = "230"
                if dados_trafo[ctd].ten_sec == "42":
                    tensao_sec = "11.9"
                if dados_trafo[ctd].ten_sec == "49":
                    tensao_sec = "13.8"
                if dados_trafo[ctd].ten_sec == "82":
                    tensao_sec = "69"
                if dados_trafo[ctd].ten_sec == "94":
                    tensao_sec = "138"
                if dados_trafo[ctd].ten_sec == "72":
                    tensao_sec = "230"
                if dados_trafo[ctd].lig == "2":
                    ligacao = "[delta,wey]"
                #Potência
                if dados_trafo[ctd].pot_nom == "34":
                    pot_nom = "[300,300]"
                if dados_trafo[ctd].pot_nom == "40":
                    pot_nom = "[500,500]"
                if dados_trafo[ctd].pot_nom == "45":
                    pot_nom = "[1000,1000]"
                if dados_trafo[ctd].pot_nom == "50":
                    pot_nom = "[2000,2000]"
                if dados_trafo[ctd].pot_nom == "54":
                    pot_nom = "[2500,2500]"
                if dados_trafo[ctd].pot_nom == "64":
                    pot_nom = "[5000,5000]"
                if dados_trafo[ctd].pot_nom == "68":
                    pot_nom = "[5000,5000]"
                if dados_trafo[ctd].pot_nom == "74":
                    pot_nom = "[10000,10000]"
                if dados_trafo[ctd].pot_nom == "76":
                    pot_nom = "[12500,12500]"
                if dados_trafo[ctd].pot_nom == "78":
                    pot_nom = "[7500,7500]"
                if dados_trafo[ctd].pot_nom == "82":
                    pot_nom = "[20000,20000]"
                if dados_trafo[ctd].pot_nom == "83":
                    pot_nom = "[25000,25000]"
                if dados_trafo[ctd].pot_nom == "85":
                    pot_nom = "[26600,26600]"
                if dados_trafo[ctd].pot_nom == "89":
                    pot_nom = "[33000,33000]"
                if dados_trafo[ctd].pot_nom == "91":
                    pot_nom = "[40000,40000]"
                if dados_trafo[ctd].pot_nom == "94":
                    pot_nom = "[60000,60000]"
                if dados_trafo[ctd].pot_nom == "101":
                    pot_nom = "[100000,100000]"

                tmp += "New Transformer.{0}".format(dados_trafo[ctd].cod_id) + " windings={0}".format("2") + " Phases={0}".format("3")
                tmp += " buses={0}".format("[" + dados_trafo[ctd].pac_1 + "," + dados_trafo[ctd].pac_2 + ".1.2.3.0" + "]") + " kVAs={0}".format(pot_nom)
                tmp += " kVs={0}".format("[" + tensao_pri + "," + tensao_sec + "]")
                tmp += " conns={0}".format(ligacao) + " tap=1"

                memoFileTrafoATMT.append(tmp)

            return memoFileTrafoATMT

           ##Colocar os de três ennrolamentos

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Transformadores de Alta para Média Tensão")

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
                tmp += " X1={0}".format(dados_cond[ctd].x1) + " normamps={0}".format(dados_cond[ctd].cnom) + " units=km "
                memoFileCond.append(tmp)

            return memoFileCond

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Condutores:" + tipoCondutor)


    def exec_CONDUTORES_DE_MEDIA_TENSAO(self):

        self.memoFileCondMT = self.getCONDUTORES("M")

        self.memoFileCondMT.insert(0,"! CONDUTORES DE MEDIA TENSAO ")



    def exec_CONDUTORES_DE_BAIXA_TENSAO(self):

        self.memoFileCondBT = self.getCONDUTORES("B")

        self.memoFileCondBT.insert(0,"! CONDUTORES DE BAIXA TENSAO ")


    def exec_CONDUTORES_DE_RAMAL(self):

        self.memoFileCondRamal = self.getCONDUTORES("R")

        self.memoFileCondRamal.insert(0,"! CONDUTORES DE RAMAL ")

        ################ PORQUE ISSO AQUI?

        #self.memoFileCondRamal.append("! LINECODE CHAVES ")

        #self.memoFileCondRamal.append("New Linecode.CHAVE_3 nphases=3 R1=0.0001 X1=0.0001 R0=0.02 X0=0.02 C1=0.02 C0=0.02 NormAmps=300 units=km BaseFreq=60")

    def getID_Fields(self, nameFields):

        lista_de_identificadores_dos_alimentadores = []

        for ctdDB in range(0, len(nameFields)):
            if nameFields[ctdDB].nome in self.nFieldsMT :
                lista_de_identificadores_dos_alimentadores.append(nameFields[ctdDB].cod_id)
                lista_de_identificadores_dos_alimentadores = (sorted(set(lista_de_identificadores_dos_alimentadores)))

        return lista_de_identificadores_dos_alimentadores


    def getSEC(self, nomeSE_ATMT,  tipoSEC, testAL_MT = None):
        try:
            ###Teste Alimentador para Chaves de Média Tensão

            if testAL_MT is not None: # MT
                dados_ctmt = self.DataBase.getData_CTMT(None)

                lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if testAL_MT is not None:  # MT
                dados_sec = self.DataBase.getData_SecMT(nomeSE_ATMT,  tipoSEC)
            else: #AT
                dados_sec = self.DataBase.getData_SecAT(nomeSE_ATMT)

            memoFileSEC = []

            for ctd in range(0, len(dados_sec)):

                [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_sec[ctd].fas_con, dados_sec[ctd].pac_1, dados_sec[ctd].pac_2)

                if dados_sec[ctd].fas_con == "ABC":
                    Linecode = " length=0.0001" + " LineCode=CHAVE_3 "
                else:
                    Linecode = " length=0.0001"

                if dados_sec[ctd].p_n_ope == "F":
                    operacao_da_chave = "YES"
                if dados_sec[ctd].p_n_ope == "A":
                    operacao_da_chave = "YES"
                if dados_sec[ctd].sit_ativ == "AT":
                    situacao = "true"
                if dados_sec[ctd].sit_ativ == "DS":
                    situacao = "false"

                temp_memoFileSEC = "New Line.{0}".format(dados_sec[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                temp_memoFileSEC += " Switch={0}".format(operacao_da_chave) + " Bus1={0}".format(pac_1)
                temp_memoFileSEC += " Bus2={0}".format(pac_2) + Linecode
                temp_memoFileSEC += " units=km" + " enabled={0}".format(situacao)

                # Chaves de Média
                if testAL_MT is not None: #MT
                    if dados_sec[ctd].ctmt in lista_de_identificadores_dos_alimentadores:
                        if dados_sec[ctd].tip_unid == tipoSEC:
                            memoFileSEC.append(temp_memoFileSEC)
                else: #AT
                    memoFileSEC.append(temp_memoFileSEC)

            return memoFileSEC

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Seccionadoras:" + tipoSEC)

    def exec_SEC_DE_ALTA_TENSAO(self):

        self.memoFileSecAT = self.getSEC(self.nSE_MT_Selecionada, None, None)

        self.memoFileSecAT.insert(0, "! CHAVES SECCIONADORAS DE ALTA TENSAO ")



    def getSEC_CONTROL(self, nomeSE_ATMT,  tipoSEC, testAL_MT = None):
        try:
            ###Teste Alimentador para Chaves de Média Tensão

            if testAL_MT is not None: # MT
                dados_ctmt = self.DataBase.getData_CTMT(None)

                lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if testAL_MT is not None:  # MT
                dados_sec = self.DataBase.getData_SecMT(nomeSE_ATMT,  tipoSEC)
            else: #AT
                dados_sec = self.DataBase.getData_SecAT(nomeSE_ATMT)


            memoFileSEC_CONTROL = []

            for ctd in range(0, len(dados_sec)):
                if dados_sec[ctd].p_n_ope == "F":
                    operacao_da_chave = "c"
                if dados_sec[ctd].p_n_ope == "A":
                    operacao_da_chave = "o"

                if tipoSEC == "22": # Chave Fusível

                    if dados_sec[ctd].cap_elo == "05H":
                        curva_do_fusivel = "05H"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "1H":
                        curva_do_fusivel = "1H "
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "2H":
                        curva_do_fusivel = "2H"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "3H":
                        curva_do_fusivel = "3H"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "5H":
                        curva_do_fusivel = "5H"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "6K":
                        curva_do_fusivel = "6K"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "10K":
                        curva_do_fusivel = "10K"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "15K":
                        curva_do_fusivel = "15K"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "25K":
                        curva_do_fusivel = "25K"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "40K":
                        curva_do_fusivel = "40K"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "100K":
                        curva_do_fusivel = "100K"
                        RatedCurrent = "1"
                    if dados_sec[ctd].cap_elo == "100EF":
                        curva_do_fusivel = "100EF"
                        RatedCurrent = "1"

                if tipoSEC == "22":  # Chave Fusível
                    temp_memoFileSEC_CONTROL = "New Fuse.{0}".format(dados_sec[ctd].cod_id)+ " MonitoredObj={0}".format("Line."+ dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format("Line." + dados_sec[ctd].cod_id)+ " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " FuseCurve={0}".format(curva_do_fusivel) + " RatedCurrent={0}".format(RatedCurrent)

                if tipoSEC == "29":  # Chave DJ Relé
                    temp_memoFileSEC_CONTROL = "New RELAY.{0}".format(dados_sec[ctd].cod_id) + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format("Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " type=current"

                if tipoSEC == "32": # Religador
                    temp_memoFileSEC_CONTROL = "New RECLOSER.{0}".format(dados_sec[ctd].cod_id) + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format("Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " action={0}".format(operacao_da_chave)

                else:
                    temp_memoFileSEC_CONTROL = "New swtcontrol.{0}".format(dados_sec[ctd].cod_id) + " SwitchedObj={0}".format("Line."+ dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedTerm={0}".format("1") + " Action={0}".format(operacao_da_chave)
                    temp_memoFileSEC_CONTROL += " lock=yes"

                # Chaves de Média
                if testAL_MT is not None: #MT
                    if dados_sec[ctd].ctmt in lista_de_identificadores_dos_alimentadores:
                        if dados_sec[ctd].tip_unid == tipoSEC:
                            memoFileSEC_CONTROL.append(temp_memoFileSEC_CONTROL)
                else: #AT
                    memoFileSEC_CONTROL.append(temp_memoFileSEC_CONTROL)

            return memoFileSEC_CONTROL

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Controles das Seccionadoras:" + tipoSEC)

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

        self.memoFileSecFacaTripolarMT_Control.insert(0, "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FACA TRIPOLAR ")


    def exec_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO(self):

        self.memoFileSecFusivelMT = self.getSEC(self.nSE_MT_Selecionada, "22", "SIM")

        self.memoFileSecFusivelMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL ")


    def exec_CONTROLE_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO(self):

        self.memoFileSecFusivelMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "22", "SIM")

        self.memoFileSecFusivelMT_Control.insert(0, "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO FUSIVEL ")

    def exec_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO(self):

        self.memoFileSecDJReleMT = self.getSEC(self.nSE_MT_Selecionada, "29", "SIM")

        self.memoFileSecDJReleMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO DISJUNTOR ")

    def exec_CONTROLE_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO(self):

        self.memoFileSecDJReleMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "29", "SIM")

        self.memoFileSecDJReleMT_Control.insert(0, "! CONTROLE DAS CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO DISJUNTOR ")


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

        self.memoFileSecTripolarSEMT_Control.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO TRIPOLAR SUBESTACAO ")

    def exec_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecUnipolarSEMT = self.getSEC(self.nSE_MT_Selecionada, "34", "SIM")

        self.memoFileSecUnipolarSEMT.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO UNIPOLAR SUBESTACAO")

    def exec_CONTROLE_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecUnipolarSEMT_Control = self.getSEC_CONTROL(self.nSE_MT_Selecionada, "34", "SIM")

        self.memoFileSecUnipolarSEMT_Control.insert(0, "! CHAVES SECCIONADORAS DE MEDIA TENSAO DO TIPO UNIPOLAR SUBESTACAO ")

    def getSEGLINHA_REGULADOR_MT(self, nomeSE_MT,  tipoSEG_REG):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoSEG_REG == "SEG":  # Segmentos de Linhas
                dados_db = self.DataBase.getData_SegLinhasMT(nomeSE_MT)
            elif tipoSEG_REG == "REG":  # Regulador de Média
                dados_db = self.DataBase.getData_ReguladorMT(nomeSE_MT)
            else:
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Segmentos de Linha ou Regulador, pois o tipo não foi especificado! \n" + tipoSEG_REG)

            memoFileLinha = []

            for ctd in range(0, len(dados_db)):

                [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, dados_db[ctd].pac_2)


                if tipoSEG_REG == "SEG": #Segmentos de Linhas
                    if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores) and \
                            (dados_db[ctd].pac_1 != self.nFieldsMT ):

                        tmp = "New Line.{0}".format(dados_db[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                        tmp += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        tmp += " Linecode={0}".format( dados_db[ctd].tip_cnd )
                        tmp += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                        tmp += " units=km"

                        memoFileLinha.append(tmp)

                elif tipoSEG_REG == "REG":  # Regulador de Média
                    if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                        tmp = "New Transformer.{0}".format(dados_db[ctd].cod_id) + " windings={0}".format('2')
                        tmp += " Phases={0}".format(num_de_fases) + " buses={0}".format('[' + pac_1 + ',' + pac_2 + ']')
                        tmp += " conns={0}".format('[wye, wye]') + " kVAs={0}".format('[2000,2000]')
                        tmp += " XHL={0}".format(".01") + " %LoadLoss={0}".format('0.00001')
                        tmp += " ppm={0}".format('0.0')
                        memoFileLinha.append(tmp)

                        tmp = "New RegControl.{0}".format('c' + dados_db[ctd].cod_id)
                        tmp += " Transformer={0}".format(dados_db[ctd].cod_id) + " winding=2 "
                        tmp += " vreg=125" + " ptratio=60 " + " band=2"
                        memoFileLinha.append(tmp)
                else:
                    raise class_exception.ExecOpenDSS(
                        "Erro ao carregar as informações dos Segmentos de Linha ou Regulador, pois o tipo não foi especificado! \n" + tipoSEG_REG)

            return memoFileLinha

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Segmentos de Linha ou Regulador: " + tipoSEG_REG)


    def exec_SEG_LINHAS_DE_MEDIA_TENSAO(self):

        self.memoFileSegLinhasMT = self.getSEGLINHA_REGULADOR_MT(self.nSE_MT_Selecionada, "SEG")

        self.memoFileSegLinhasMT.insert(0, "! SEGMENTOS DE LINHA DE MEDIA TENSAO ")

    def exec_REGULADORES_DE_MEDIA_TENSAO(self):

        self.memoFileReguladorMT = self.getSEGLINHA_REGULADOR_MT(self.nSE_MT_Selecionada, "REG")

        self.memoFileReguladorMT.insert(0, "! UNIDADES REGULADORAS DE  MEDIA TENSAO MODELADA COMO TARNSFORMADORES DE BAIXA IMPEDÂNCIA ")

    def getUNIDADE_CONSUMIDORA(self, nomeSE_MT, tipoUniCons):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoUniCons == "MT":  # Segmentos de Linhas
                dados_db = self.DataBase.getData_UniConsumidora(nomeSE_MT, "MT")
            elif tipoUniCons == "BT":  # Regulador de Média
                dados_db = self.DataBase.getData_UniConsumidora(nomeSE_MT, "BT")
            else:
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras, pois o tipo não foi especificado! \n" + tipoUniCons)

            memoFileSEC = []

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    if tipoUniCons == "MT":
                        if dados_db[ctd].ten_forn == "49":
                            nivel_de_tensao = "13.8"
                        if dados_db[ctd].ten_forn == "41":
                            nivel_de_tensao = "11.4"
                        if dados_db[ctd].ten_forn == "42":
                            nivel_de_tensao = "11.9"
                        if dados_db[ctd].ten_forn == "72":
                            nivel_de_tensao = "34.5"
                        if dados_db[ctd].ten_forn == "39":
                            nivel_de_tensao = "7.96"

                    elif tipoUniCons == "BT":
                        if dados_db[ctd].ten_forn == "6":
                            nivel_de_tensao = "0.127"
                        if dados_db[ctd].ten_forn == "10":
                            nivel_de_tensao = "0.220"
                        if dados_db[ctd].ten_forn == "15":
                            nivel_de_tensao = "0.380"

                    [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac, None)

                    if dados_db[ctd].fas_con == "ABCN":
                        conexao = "wye"
                    if dados_db[ctd].fas_con == "ABN":
                        conexao = "wye"
                    if dados_db[ctd].fas_con == "CAN":
                        conexao = "wye"
                    if dados_db[ctd].fas_con == "BCN":
                        conexao = "wye"
                    if dados_db[ctd].fas_con == "AN":
                        conexao = "wye"
                    if dados_db[ctd].fas_con == "BN":
                        conexao = "wye"
                    if dados_db[ctd].fas_con == "CN":
                        conexao = "wye"


                    tmp = "New Load.{0}".format(dados_db[ctd].objectid) + " Bus1={0}".format(pac_1) +  " Phases={0}".format(num_de_fases)
                    tmp += " model=8 ZIPV=[0.5 0 0.5 1 0 0]" + " Kv={0}".format(nivel_de_tensao)
                    tmp += " kW={0}".format(dados_db[ctd].car_inst) + " PF= 0.92"
                    tmp += " conn={0}".format(conexao) + " daily={0}".format(str(dados_db[ctd].tip_cc.replace(' ', "")))

                    memoFileSEC.append(tmp)

            return memoFileSEC

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoUniCons)


    def exec_UNID_CONSUMIDORAS_MT(self):

        self.memoFileUniConsumidoraMT = self.getUNIDADE_CONSUMIDORA(self.nSE_MT_Selecionada, "MT")

        self.memoFileUniConsumidoraMT.insert(0, "! UNIDADES CONSUMIDORAS DE MEDIA TENSAO ")

    def exec_UNID_CONSUMIDORAS_BT(self):

        self.memoFileUniConsumidoraBT = self.getUNIDADE_CONSUMIDORA(self.nSE_MT_Selecionada, "BT")

        self.memoFileUniConsumidoraBT.insert(0, "! UNIDADES CONSUMIDORAS DE BAIXA TENSAO ")

    def getTRANSFORMADORES_DE_DISTRIBUICAO(self, nomeSE_MT):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            dados_db = self.DataBase.getData_TrafoDIST(nomeSE_MT)

            memoFileSEC = []

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, dados_db[ctd].pac_2)

                    if dados_db[ctd].ten_pri == "42":
                        tensao_primario = "11.9"
                    if dados_db[ctd].ten_pri == "46":
                        tensao_primario = "13.2"
                    if dados_db[ctd].ten_pri == "49":
                        tensao_primario = "13.8"
                    if dados_db[ctd].ten_pri == "72":
                        tensao_primario = "34.5"
                    if dados_db[ctd].ten_pri  == "74":
                        tensao_primario = "38"
                    if dados_db[ctd].ten_pri == "39":
                        tensao_primario = "7.96"
                    if dados_db[ctd].ten_pri  == "58":
                        tensao_primario = "19.919"
                    if dados_db[ctd].ten_sec == "10":
                        tensao_sec = "0.220"
                    if dados_db[ctd].ten_sec == "14":
                        tensao_sec = "0.254"
                    if dados_db[ctd].ten_sec == "17":
                        tensao_sec = "0.440"
                    if dados_db[ctd].ten_sec == "15":
                        tensao_sec = "0.380"
                    if dados_db[ctd].ten_sec == "6":
                        tensao_sec = "0.127"
                    if dados_db[ctd].ten_sec == "11":
                        tensao_sec = "0.230"
                    if dados_db[ctd].lig == "2":
                        ligacao = "[delta,wey]"

                    #UNTRD
                    tmp = "New Transformer.{0}".format(dados_db[ctd].pac_1) + " windings={0}".format('2')
                    tmp += " Phases={0}".format(num_de_fases)
                    tmp += " buses={0}".format('[' + pac_1 + ',' + pac_2 + ']')
                    tmp += " kVAs={0}".format('[' + str( dados_db[ctd].pot_nom ) + ',' + str( dados_db[ctd].pot_nom ) + ']')
                    #EQRTD
                    tmp += " kVs={0}".format('[' + tensao_primario + ',' + tensao_sec + ']')
                    tmp += " conns={0}".format(ligacao) + " %Rs={0}".format( str( dados_db[ctd].r ) )
                    tmp += " XHL={0}".format(dados_db[ctd].xhl)

                    memoFileSEC.append(tmp)

            return memoFileSEC

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações dos Transformadores de Distribuição MT: ")

    def exec_TRANSFORMADORES_DE_DISTRIBUICAO(self):

        self.memoFileTrafoDist = self.getTRANSFORMADORES_DE_DISTRIBUICAO(self.nSE_MT_Selecionada)

        self.memoFileTrafoDist.insert(0, "! TRANSFORMADORES DE DISTRIBUIÇAO ")

    def getSEG_LINHAS_RAMAL_LIGACAO(self, nomeSE_MT, tipoLinha):
        try:

            dados_ctmt = self.DataBase.getData_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoLinha == "SEGBT":  # Segmentos de Linhas de Baixa Tensão
                dados_db = self.DataBase.getData_SegLinhasRamLigBT(nomeSE_MT, "SEGBT")
            elif tipoLinha == "RLIG":  # Ramal de Ligação
                dados_db = self.DataBase.getData_SegLinhasRamLigBT(nomeSE_MT, "RLIG")
            else:
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Linhas BT, pois o tipo não foi especificado! \n" + tipoLinha)

            memoFileLinha = []

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    for ctd in range(0, len(dados_db)):

                        [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, dados_db[ctd].pac_2)


                        tmp = "New Line.{0}".format(dados_db[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                        tmp += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        tmp += " Linecode={0}".format( dados_db[ctd].tip_cnd )
                        tmp += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                        tmp += " units=km"

                        memoFileLinha.append(tmp)

            return memoFileLinha

        except:
            raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoLinha)

    def exec_SEG_LINHAS_DE_BAIXA_TENSAO(self):

        self.memoFileSegLinhasBT = self.getSEG_LINHAS_RAMAL_LIGACAO(self.nSE_MT_Selecionada, "SEGBT")

        self.memoFileSegLinhasBT.insert(0, "! SEGMENTOS DE LINHA DE BAIXA TENSAO ")

    def exec_RAMAL_DE_LIGACAO(self):

        self.memoFileRamaisLigBT = self.getSEG_LINHAS_RAMAL_LIGACAO(self.nSE_MT_Selecionada, "RLIG")

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
                raise class_exception.ExecOpenDSS("Erro ao carregar as informações das Linhas BT, pois o tipo não foi especificado! \n" + tipoLinha)

            memoFileComp = []

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    for ctd in range(0, len(dados_db)):

                        [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, None)

                        tmp = "New Capacitor.{0}".format(dados_db[ctd].cod_id) + " Bus1={0}".format(pac_1)
                        tmp += " Phases={0}".format(num_de_fases)
                        tmp += " kVAR={0}".format(str( dados_db[ctd].pot_nom ))

                        memoFileComp.append(tmp)

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
    
    def getFasesConexao(self, fas_con, pac_1, pac_2 = None):
    
        resultfase = ''

        if pac_2 is None:
            pac_2 = ""

        if fas_con == "ABC":
            num_de_fases = "3"
            pac_1 = pac_1.replace('-', "") + ".1.2.3.0"
            pac_2 = pac_2.replace('-', "") + ".1.2.3.0"
        if fas_con == ("AB"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".1.2.0"
            pac_2 = pac_2.replace('-', "") + ".1.2.0"
        if fas_con == ("BC"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".2.3.0"
            pac_2 = pac_2.replace('-', "") + ".2.3.0"
        if fas_con == ("CA"):
            num_de_fases = "2"
            pac_1 = pac_1.replace('-', "") + ".3.1.0"
            pac_2 = pac_2.replace('-', "") + ".3.1.0"
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
            pac_2 = pac_1.replace('-', "") + ".2.3.0"
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
            pac_1 = pac_1.replace("-", "") + ".1.0"
            pac_2 = pac_2.replace("-", "") + ".1.0"
        if fas_con == ("B"):
            num_de_fases = "1"
            pac_1 = pac_1.replace("-", "") + ".2.0"
            pac_2 = pac_2.replace("-", "") + ".2.0"
        if fas_con == ("C"):
            num_de_fases = "1"
            pac_1 = pac_1.replace("-", "") + ".3.0"
            pac_2 = pac_2.replace("-", "") + ".3.0"

        resultfase = [num_de_fases, pac_1, pac_2]

        return resultfase
