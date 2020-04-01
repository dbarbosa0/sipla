from class_database_opendss import C_DBase_OpenDSS
from class_exception import ExecOpenDSS

class C_OpenDSS(): # classe OpenDSSDirect

    def __init__(self):


        self.acessDataBase = C_DBase_OpenDSS() #Acesso ao Banco de Dados

        self.initUI()


    def initUI(self):

        #Criando variáveis do Redirect
        self.memoFileHeader = "" #Cabeçalho do arquivo
        self.memoFileFooter = ""  # Rodapé do arquivo
        self.memoFileEqTh = ""  # Arquivo Thevenin
        self.memoFileEqThMT = ""  # Arquivo Thevenin Média
        self.memoFileTrafoATMT = "" #Transformadores de AT MT
        self.memoFileCondMT = "" #Condutores de Média Tensão
        self.memoFileCondBT = "" #Condutores de Baixa Tensão
        self.memoFileCondRamal = "" #Condutores de Ramal
        self.memoFileSecAT = "" #Seccionadora de Alta Tensão
        self.memoFileSecAT_Control = "" # Controle da Secionadora de Alta Tensão
        self.memoFileSecOleoMT = ""  # Seccionadora a Óleo de Média Tensão
        self.memoFileSecOleoMT_Control = ""  # Controle Seccionadora a Óleo de Média Tensão
        self.memoFileSecFacaMT = ""  # Seccionadora Facade Média Tensão
        self.memoFileSecFacaMT_Control = ""  # Controle Seccionadora Faca de Média Tensão
        self.memoFileSecFacaTripolarMT = ""  # Seccionadora Faca Tripolar de Média Tensão
        self.memoFileSecFacaTripolarMT_Control = ""  # Controle Seccionadora Faca Tripolar de Média Tensão
        self.memoFileSecFusivelMT = ""  # Seccionadora Fusível Média Tensão
        self.memoFileSecFausivelMT_Control = ""  # Controle Seccionadora Fusível de Média Tensão
        self.memoFileSecDJReleMT = ""  # Seccionadora DJ Média Tensão
        self.memoFileSecDJReleMT_Control = ""  # Controle Seccionadora DJ de Média Tensão
        self.memoFileSecReligadorMT = ""  # Seccionadora Religador de  Média Tensão
        self.memoFileSecReligadorMT_Control = ""  # Controle Seccionadora Religador de de Média Tensão
        self.memoFileSecTripolarSEMT = ""  # Seccionadora Tripolar SE de  Média Tensão
        self.memoFileSecTripolarSEMT_Control = ""  # Controle Seccionadora Tripolar SE de Média Tensão
        self.memoFileSecUnipolarSEMT = ""  # Seccionadora Unipolar SE de  Média Tensão
        self.memoFileSecUnipolarSEMT_Control = ""  # Controle Seccionadora Unipolar SE de Média Tensão
        self.memoFileReguladorMT = ""  # Regulador de  Média Tensão
        self.memoFileSegLinhasMT = ""  # Segmentos de Linhas de  Média Tensão
        self.memoFileUniConsumidoraMT = ""  # Unidade Consumidora de Média Tensão
        self.memoFileTrafoDist = ""  #Transformadores de Distribuição
        self.memoFileSegLinhasBT = ""  # Segmentos de Linhas de Baixa Tensão
        self.memoFileUniConsumidoraBT = ""  # Unidade Consumidora de Baixa Tensão
        self.memoFileRamaisLigBT = "" # Ramais de Ligação
        self.memoFileUndCompReatMT = "" #Unidade de Compensação de Reativo de Baixa Tensão
        self.memoFileUndCompReatBT = "" #Unidade de Compensação de Reativo de Baixa Tensão

    def setDirDataBase(self, nomeAcessDataBase):
        self.acessDataBase.setDefBDGD(nomeAcessDataBase)

    def setCircuitoAT_MT(self, nomeCircuitoAT_MT):
        self.unifilarCircuitoAT_MT = nomeCircuitoAT_MT

    def setSE_MT_Selecionada(self, nomeSE_MT_Selecionada):
        self.uniSE_MT_SEL = nomeSE_MT_Selecionada

    def setFields_SE_MT_Selecionada(self, nomeFields_SE_MT_Selecionada):
        self.unifilarFields_SE_MT_Selecionada = nomeFields_SE_MT_Selecionada

    def exec_HeaderFile(self):
        self.memoFileHeader = "Clear " + "\n"

        self.memoFileHeader += "\n" + "! VAMOS QUE VAMOS " + "\n" + "\n"

        self.memoFileHeader += self.getHEADER(self.uniSE_MT_SEL)


    def getHEADER(self, nomeSE_MT): # PRIMEIRA LINHA
        try:

            dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            dados_db = self.acessDataBase.getOpenDSS_SegLinhasMT(nomeSE_MT)

            memoFileLinha = ""

            for ctd in range(0, len(dados_db)):
                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores) and \
                (dados_db[ctd].pac_1 == self.unifilarFields_SE_MT_Selecionada):
                    memoFileLinha += "New Line.{0}".format(dados_db[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                    memoFileLinha += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                    memoFileLinha += " Linecode={0}".format(dados_db[ctd].tip_cnd)
                    memoFileLinha += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                    memoFileLinha += " units=km" + "\n"

            return memoFileLinha

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro no HEAD")

    def exec_FooterFile(self):
        try:

            self.memoFileFooter += '\n' + "! codigo finalizado " + '\n' + '\n'
            self.memoFileFooter += "set voltagebases = [69, 39.8371, 13.8, 11.9, 7.96, 6.87 ,0.44, 0.254, 0.38, 0.219, 0.22, 0.127 0.0733 ]" + '\n' + '\n'
            self.memoFileFooter += '\n' + "CalcVoltageBases" + '\n'
            self.memoFileFooter += '\n' + "set mode = direct" + '\n'
            self.memoFileFooter += '\n' + "set controlmode = TIME" + '\n'
            self.memoFileFooter += '\n' + "solve" + '\n'
            self.memoFileFooter += "set mode=daily stepsize=15m number=96" + '\n'
            self.memoFileFooter += "solve " + '\n'
        
        except ExecOpenDSS:
            raise ExecOpenDSS("Erro no FOOTER")

    def exec(self):
        print("Iniciando o processamento ...")


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
        print("Chave Uipolar da SE MT ...")
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
            dados_eqth = self.acessDataBase.getOpenDSS_EqThevenin(self.unifilarCircuitoAT_MT)

            memoFileEqTh = ""

            for ctd in range(0,len(dados_eqth)):

                if dados_eqth[ctd].ten_nom == "82":
                    basekv = "69"
                if dados_eqth[ctd].ten_nom  == "94":
                    basekv = "138"
                if dados_eqth[ctd].ten_nom== "96":
                    basekv = "230"

                memoFileEqTh += "! Equivalente de Thevenin "
                memoFileEqTh += "\n" + "New Circuit.{0}".format(dados_eqth[ctd].nome)
                memoFileEqTh += "  basekv={0}".format(basekv)  + "  pu=1" + "  phase=3" + "  bus1={0}".format(dados_eqth[ctd].nome)
                memoFileEqTh += "  MVAsc3=10000000000000000000000" + "  MVAsc1=1000000000000000000000" + "\n"

            return memoFileEqTh

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações do Equivalente de Thevenin")

    def exec_EQUIVALENTE_DE_THEVENIN(self):

        self.memoFileEqTh = "\n" + "! EQUIVALENTE DE THEVENIN " + "\n" + "\n"

        self.memoFileEqTh += self.getEQUIVALENTE_DE_THEVENIN()

    def getEQUIVALENTE_DE_THEVENIN_MEDIA(self):
        try:
            dados_eqth = self.acessDataBase.getOpenDSS_CTMT(self.uniSE_MT_SEL)

            memoFileEqThMT = ""

            for ctd in range(0,len(dados_eqth)):
                if dados_eqth[ctd].nome in self.unifilarFields_SE_MT_Selecionada:
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

                    memoFileEqThMT += "\n" + "New Circuit.{0}".format(dados_eqth[ctd].nome)
                    memoFileEqThMT += "  basekv={0}".format(basekv)  + " pu=1 " + "  phase=3 " + "  bus1={0}".format(dados_eqth[ctd].nome)
                    memoFileEqThMT += "  MVAsc3=10000000000000000000000" + " MVAsc1=1000000000000000000000" + "\n"

                return memoFileEqThMT

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações do Equivalente de Thevenin")

    def exec_EQUIVALENTE_DE_THEVENIN_MEDIA(self):

        self.memoFileEqThMT = "\n" + "! EQUIVALENTE DE THEVENIN " + "\n" + "\n"

        self.memoFileEqThMT += self.getEQUIVALENTE_DE_THEVENIN_MEDIA()


    def getTRANSFORMADORES_DE_ALTA_PARA_MEDIA(self):
        try:
            dados_trafo = self.acessDataBase.getOpenDSS_TrafosAT_MT(self.uniSE_MT_SEL)

            memoFileTrafoATMT = ""

            for ctd in range(0,len(dados_trafo)):

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

                memoFileTrafoATMT += "New Transformer.{0}".format(dados_trafo[ctd].cod_id) + " windings={0}".format("2") + " Phases={0}".format("3")
                memoFileTrafoATMT += " buses={0}".format("[" + dados_trafo[ctd].pac_1 + "," + dados_trafo[ctd].pac_2 + ".1.2.3.0" + "]") + " kVAs={0}".format(pot_nom)
                memoFileTrafoATMT += " kVs={0}".format("[" + tensao_pri + "," + tensao_sec + "]")
                memoFileTrafoATMT += " conns={0}".format(ligacao) + " tap=1" + "\n"

            return memoFileTrafoATMT

           ##Colocar os de três ennrolamentos

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações dos Transformadores de Alta para Média Tensão")

    def exec_TRANSFORMADORES_DE_ALTA_PARA_MEDIA(self):

        self.memoFileTrafoATMT = "\n" + "! TRANSFORMADORES DE ALTA PARA MÉDIA TENSÃO " + "\n" + "\n"

        self.memoFileTrafoATMT += self.getTRANSFORMADORES_DE_ALTA_PARA_MEDIA()


    def getCONDUTORES(self, tipoCondutor):
        try:
            dados_cond = self.acessDataBase.getOpenDSS_Condutores(tipoCondutor)

            memoFileCond = ""

            for ctd in range(0, len(dados_cond)):

                memoFileCond += "New Linecode.{0}".format(dados_cond[ctd].cod_id)
                memoFileCond += " R1={0}".format(dados_cond[ctd].r1)
                memoFileCond += " X1={0}".format(dados_cond[ctd].x1) + " normamps={0}".format(dados_cond[ctd].cnom) + " units=km " + "\n"

            return memoFileCond

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações dos Condutores:" + tipoCondutor)


    def exec_CONDUTORES_DE_MEDIA_TENSAO(self):

        self.memoFileCondMT = "\n" + "! CONDUTORES DE MÉDIA TENSÃO " + "\n" + "\n"

        self.memoFileCondMT += self.getCONDUTORES("M")

    def exec_CONDUTORES_DE_BAIXA_TENSAO(self):

        self.memoFileCondBT = "\n" + "! CONDUTORES DE BAIXA TENSÃO " + "\n" + "\n"

        self.memoFileCondBT += self.getCONDUTORES("B")


    def exec_CONDUTORES_DE_RAMAL(self):

        self.memoFileCondRamal = "\n" + "! CONDUTORES DE RAMAL " + "\n" + "\n"

        self.memoFileCondRamal += self.getCONDUTORES("R")

        ################ PORQUE ISSO AQUI?

        self.memoFileCondRamal +=  "\n" + "! LINECODE CHAVES " + "\n" + "\n"

        self.memoFileCondRamal += "New Linecode.CHAVE_3 nphases=3 R1=0.0001 X1=0.0001 R0=0.02 X0=0.02 C1=0.02 C0=0.02 NormAmps=300 units=km BaseFreq=60" + "\n"

    def getID_Fields(self, nameFields):

        lista_de_identificadores_dos_alimentadores = []

        for ctdDB in range(0, len(nameFields)):
            if nameFields[ctdDB].nome in self.unifilarFields_SE_MT_Selecionada:
                lista_de_identificadores_dos_alimentadores.append(nameFields[ctdDB].cod_id)
                lista_de_identificadores_dos_alimentadores = (sorted(set(lista_de_identificadores_dos_alimentadores)))

        return lista_de_identificadores_dos_alimentadores


    def getSEC(self, nomeSE_ATMT,  tipoSEC, testAL_MT = None):
        try:
            ###Teste Alimentador para Chaves de Média Tensão

            if testAL_MT is not None: # MT
                dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

                lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if testAL_MT is not None:  # MT
                dados_sec = self.acessDataBase.getOpenDSS_SecMT(nomeSE_ATMT,  tipoSEC)
            else: #AT
                dados_sec = self.acessDataBase.getOpenDSS_SecAT(nomeSE_ATMT)

            memoFileSEC = ""

            for ctd in range(0, len(dados_sec)):

                [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_sec[ctd].fas_con, dados_sec[ctd].pac_1, dados_sec[ctd].pac_2)

                if dados_sec[ctd].fas_con == "ABC":
                    Linecode = " length=0.0001" + " LineCode=CHAVE_3 "
                else:
                    Linecode = " length=0.0001"

                if dados_sec[ctd].p_n_ope == "F":
                    operacao_da_chave = " YES "
                if dados_sec[ctd].p_n_ope == "A":
                    operacao_da_chave = " YES "
                if dados_sec[ctd].sit_ativ == "AT":
                    situacao = "true"
                if dados_sec[ctd].sit_ativ == "DS":
                    situacao = "false"

                temp_memoFileSEC = "New Line.{0}".format(dados_sec[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                temp_memoFileSEC += " Switch={0}".format(operacao_da_chave) + " Bus1={0}".format(pac_1)
                temp_memoFileSEC += " Bus2={0}".format(pac_2) + Linecode
                temp_memoFileSEC += " units=km" + " enabled={0}".format(situacao) + "\n"

                # Chaves de Média
                if testAL_MT is not None: #MT
                    if dados_sec[ctd].ctmt in lista_de_identificadores_dos_alimentadores:
                        if dados_sec[ctd].tip_unid == tipoSEC:
                            memoFileSEC += temp_memoFileSEC
                else: #AT
                    memoFileSEC += temp_memoFileSEC

            return  memoFileSEC

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações das Seccionadoras:" + tipoSEC)

    def exec_SEC_DE_ALTA_TENSAO(self):

        self.memoFileSecAT = "\n"+"! CHAVES SECCIONADORAS DE ALTA TENSÃO " +"\n"+"\n"

        self.memoFileSecAT += self.getSEC(self.uniSE_MT_SEL, None, None)

    def getSEC_CONTROL(self, nomeSE_ATMT,  tipoSEC, testAL_MT = None):
        try:
            ###Teste Alimentador para Chaves de Média Tensão

            if testAL_MT is not None: # MT
                dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

                lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if testAL_MT is not None:  # MT
                dados_sec = self.acessDataBase.getOpenDSS_SecMT(nomeSE_ATMT,  tipoSEC)
            else: #AT
                dados_sec = self.acessDataBase.getOpenDSS_SecAT(nomeSE_ATMT)


            memoFileSEC_CONTROL = ""

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
                    temp_memoFileSEC_CONTROL += " FuseCurve={0}".format(curva_do_fusivel) + " RatedCurrent={0}".format(RatedCurrent) + "\n"

                if tipoSEC == "29":  # Chave DJ Relé
                    temp_memoFileSEC_CONTROL = "New RELAY.{0}".format(dados_sec[ctd].cod_id) + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format("Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " type=current" + "\n"

                if tipoSEC == "32": # Religador
                    temp_memoFileSEC_CONTROL = "New RECLOSER.{0}".format(dados_sec[ctd].cod_id) + " MonitoredObj={0}".format("Line." + dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedObj={0}".format("Line." + dados_sec[ctd].cod_id) + " SwitchedTerm={0}".format("1")
                    temp_memoFileSEC_CONTROL += " action={0}".format(operacao_da_chave)+ "\n"

                else:
                    temp_memoFileSEC_CONTROL = "New swtcontrol.{0}".format(dados_sec[ctd].cod_id) + " SwitchedObj={0}".format("Line."+ dados_sec[ctd].cod_id)
                    temp_memoFileSEC_CONTROL += " SwitchedTerm={0}".format("1") + " Action={0}".format(operacao_da_chave)
                    temp_memoFileSEC_CONTROL += " lock=yes" + "\n"

                # Chaves de Média
                if testAL_MT is not None: #MT
                    if dados_sec[ctd].ctmt in lista_de_identificadores_dos_alimentadores:
                        if dados_sec[ctd].tip_unid == tipoSEC:
                            memoFileSEC_CONTROL  += temp_memoFileSEC_CONTROL
                else: #AT
                    memoFileSEC_CONTROL  += temp_memoFileSEC_CONTROL

            return memoFileSEC_CONTROL

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações dos Controles das Seccionadoras:" + tipoSEC)

    def exec_CONTROLE_SEC_DE_ALTA_TENSAO(self):

        self.memoFileSecAT_Control = "\n"+"! CONTROLE DAS CHAVES SECCIONADORAS DE ALTA TENSÃO " +"\n"+"\n"

        self.memoFileSecAT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, None, None)

    def exec_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO(self):

        self.memoFileSecOleoMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO A OLÉO " + "\n" + "\n"

        self.memoFileSecOleoMT += self.getSEC(self.uniSE_MT_SEL, "17", "SIM")

    def exec_CONTROLE_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO(self):

        self.memoFileSecOleoMT_Control = "\n"+"! CONTROLE DAS CHAVES SECCIONADORAS DE MÉDIA TENSÃO TIPO OLEO " +"\n"+"\n"

        self.memoFileSecOleoMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "17", "SIM")

    def exec_SEC_CHAVE_FACA_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO FACA " + "\n" + "\n"

        self.memoFileSecFacaMT += self.getSEC(self.uniSE_MT_SEL, "19", "SIM")

    def exec_CONTROLE_SEC_CHAVE_FACA_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaMT_Control = "\n"+"! CONTROLE DAS CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO FACA " +"\n"+"\n"

        self.memoFileSecFacaMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "19", "SIM")

    def exec_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaTripolarMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO FACA TRIPOLAR " + "\n" + "\n"

        self.memoFileSecFacaTripolarMT += self.getSEC(self.uniSE_MT_SEL, "20", "SIM")

    def exec_CONTROLE_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO(self):

        self.memoFileSecFacaTripolarMT_Control = "\n"+"! CONTROLE DAS CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO FACA TRIPOLAR " +"\n"+"\n"

        self.memoFileSecFacaTripolarMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "20", "SIM")

    def exec_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO(self):

        self.memoFileSecFusivelMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO FUSIVEL " + "\n" + "\n"

        self.memoFileSecFusivelMT += self.getSEC(self.uniSE_MT_SEL, "22", "SIM")

    def exec_CONTROLE_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO(self):

        self.memoFileSecFusivelMT_Control = "\n"+"! CONTROLE DAS CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO FUSIVEL " +"\n"+"\n"

        self.memoFileSecFusivelMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "22", "SIM")

    def exec_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO(self):

        self.memoFileSecDJReleMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO DISJUNTOR " + "\n" + "\n"

        self.memoFileSecDJReleMT += self.getSEC(self.uniSE_MT_SEL, "29", "SIM")

    def exec_CONTROLE_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO(self):

        self.memoFileSecDJReleMT_Control = "\n"+"! CONTROLE DAS CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO DISJUNTOR " +"\n"+"\n"

        self.memoFileSecDJReleMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "29", "SIM")

    def exec_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO(self):

        self.memoFileSecReligadorMT = "\n" + "! CHAVES SECCIONADORAS RELIGADORES DE MÉDIA TENSÃO " + "\n" + "\n"

        self.memoFileSecReligadorMT += self.getSEC(self.uniSE_MT_SEL, "32", "SIM")

    def exec_CONTROLE_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO(self):

        self.memoFileSecReligadorMT_Control = "\n" + "! CHAVES SECCIONADORAS RELIGADORES DE MÉDIA TENSÃO  " + "\n" + "\n"

        self.memoFileSecReligadorMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "32", "SIM")

    def exec_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecTripolarSEMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO TRIPOLAR SUBESTACAO" + "\n" + "\n"

        self.memoFileSecTripolarSEMT += self.getSEC(self.uniSE_MT_SEL, "33", "SIM")

    def exec_CONTROLE_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecTripolarSEMT_Control = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO TRIPOLAR SUBESTACAO " + "\n" + "\n"

        self.memoFileSecTripolarSEMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "33", "SIM")

    def exec_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecUnipolarSEMT = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO UNIPOLAR SUBESTACAO" + "\n" + "\n"

        self.memoFileSecUnipolarSEMT += self.getSEC(self.uniSE_MT_SEL, "34", "SIM")

    def exec_CONTROLE_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO(self):

        self.memoFileSecUnipolarSEMT_Control = "\n" + "! CHAVES SECCIONADORAS DE MÉDIA TENSÃO DO TIPO UNIPOLAR SUBESTACAO " + "\n" + "\n"

        self.memoFileSecUnipolarSEMT_Control += self.getSEC_CONTROL(self.uniSE_MT_SEL, "34", "SIM")

    def getSEGLINHA_REGULADOR_MT(self, nomeSE_MT,  tipoSEG_REG):
        try:

            dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoSEG_REG == "SEG":  # Segmentos de Linhas
                dados_db = self.acessDataBase.getOpenDSS_SegLinhasMT(nomeSE_MT)
            elif tipoSEG_REG == "REG":  # Regulador de Média
                dados_db = self.acessDataBase.getOpenDSS_ReguladorMT(nomeSE_MT)
            else:
                raise ExecOpenDSS("Erro ao carregar as informações dos Segmentos de Linha ou Regulador, pois o tipo não foi especificado! \n" + tipoSEG_REG)


            memoFileLinha = ""

            for ctd in range(0, len(dados_db)):

                [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, dados_db[ctd].pac_2)

                if tipoSEG_REG == "SEG": #Segmentos de Linhas
                    if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores) and \
                            (dados_db[ctd].pac_1 != self.unifilarFields_SE_MT_Selecionada):

                        memoFileLinha += "New Line.{0}".format(dados_db[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                        memoFileLinha += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        memoFileLinha += " Linecode={0}".format( dados_db[ctd].tip_cnd )
                        memoFileLinha += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                        memoFileLinha += " units=km" + "\n"

                elif tipoSEG_REG == "REG":  # Regulador de Média
                    if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                        memoFileLinha += "New Transformer.{0}".format(dados_db[ctd].cod_id) + " windings={0}".format('2')
                        memoFileLinha += " Phases={0}".format(num_de_fases) + " buses={0}".format('[' + pac_1 + ',' + pac_2 + ']')
                        memoFileLinha += " conns={0}".format('[wye, wye]') + " kVAs={0}".format('[2000,2000]')
                        memoFileLinha += " XHL={0}".format(".01") + " %LoadLoss={0}".format('0.00001')
                        memoFileLinha += " ppm={0}".format('0.0') + '\n'

                        memoFileLinha += "New RegControl.{0}".format('c' + dados_db[ctd].cod_id)
                        memoFileLinha += " Transformer={0}".format(dados_db[ctd].cod_id) + " winding=2 "
                        memoFileLinha += " vreg=125" + " ptratio=60 " + " band=2" + '\n'
                else:
                    raise ExecOpenDSS(
                        "Erro ao carregar as informações dos Segmentos de Linha ou Regulador, pois o tipo não foi especificado! \n" + tipoSEG_REG)

            return memoFileLinha

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações dos Segmentos de Linha ou Regulador: " + tipoSEG_REG)


    def exec_SEG_LINHAS_DE_MEDIA_TENSAO(self):
        self.memoFileSegLinhasMT = "\n" + "! SEGMENTOS DE LINHA DE MÉDIA TENSÃO " + "\n" + "\n"

        self.memoFileSegLinhasMT += self.getSEGLINHA_REGULADOR_MT(self.uniSE_MT_SEL, "SEG")

    def exec_REGULADORES_DE_MEDIA_TENSAO(self):

        self.memoFileReguladorMT = "\n" + "! UNIDADES REGULADORAS DE  MÉDIA TENSÃO MODELADA COMO TARNSFORMADORES DE BAIXA IMPEDÂNCIA " + "\n" + "\n"

        self.memoFileReguladorMT += self.getSEGLINHA_REGULADOR_MT(self.uniSE_MT_SEL, "REG")

    def getUNIDADE_CONSUMIDORA(self, nomeSE_MT, tipoUniCons):
        try:

            dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoUniCons == "MT":  # Segmentos de Linhas
                dados_db = self.acessDataBase.getOpenDSS_UniConsumidora(nomeSE_MT, "MT")
            elif tipoUniCons == "BT":  # Regulador de Média
                dados_db = self.acessDataBase.getOpenDSS_UniConsumidora(nomeSE_MT, "BT")
            else:
                raise ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras, pois o tipo não foi especificado! \n" + tipoUniCons)

            memoFileSEC = ""

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


                    memoFileSEC += "New Load.{0}".format(dados_db[ctd].objectid) + " Bus1={0}".format(pac_1) +  " Phases={0}".format(num_de_fases)
                    memoFileSEC += " model=8 ZIPV=[0.5 0 0.5 1 0 0]" + " Kv={0}".format(nivel_de_tensao)
                    memoFileSEC += " kW={0}".format(dados_db[ctd].car_inst) + " PF= 0.92"
                    memoFileSEC += " conn={0}".format(conexao) + " daily={0}".format(str(dados_db[ctd].tip_cc.replace(' ', ""))) + '\n'

            return memoFileSEC

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoUniCons)


    def exec_UNID_CONSUMIDORAS_MT(self):

        self.memoFileUniConsumidoraMT = "\n" + "! UNIDADES CONSUMIDORAS DE MÉDIA TENSÃO " + "\n" + "\n"

        self.memoFileUniConsumidoraMT += self.getUNIDADE_CONSUMIDORA(self.uniSE_MT_SEL, "MT")

    def exec_UNID_CONSUMIDORAS_BT(self):

        self.memoFileUniConsumidoraBT = "\n" + "! UNIDADES CONSUMIDORAS DE BAIXA TENSÃO " + "\n" + "\n"

        self.memoFileUniConsumidoraBT += self.getUNIDADE_CONSUMIDORA(self.uniSE_MT_SEL, "BT")

    def getTRANSFORMADORES_DE_DISTRIBUICAO(self, nomeSE_MT):
        try:

            dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            dados_db = self.acessDataBase.getOpenDSS_TrafoDIST(nomeSE_MT)

            memoFileSEC = ""

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
                    memoFileSEC += "New Transformer.{0}".format(dados_db[ctd].pac_1) + " windings={0}".format('2')
                    memoFileSEC += " Phases={0}".format(num_de_fases)
                    memoFileSEC += " buses={0}".format('[' + pac_1 + ',' + pac_2 + ']')
                    memoFileSEC += " kVAs={0}".format('[' + str( dados_db[ctd].pot_nom ) + ',' + str( dados_db[ctd].pot_nom ) + ']')
                    #memoFileSEC += "\n"
                    #EQRTD
                    memoFileSEC += " kVs={0}".format('[' + tensao_primario + ',' + tensao_sec + ']')
                    memoFileSEC += " conns={0}".format(ligacao) + " %Rs={0}".format( str( dados_db[ctd].r ) )
                    memoFileSEC += " XHL={0}".format(dados_db[ctd].xhl)
                    memoFileSEC += " \n"

            return memoFileSEC

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações dos Transformadores de Distribuição MT: ")

    def exec_TRANSFORMADORES_DE_DISTRIBUICAO(self):

        self.memoFileTrafoDist = "\n" + "! TRANSFORMADORES DE DISTRIBUIÇÃO " + "\n" + "\n"

        self.memoFileTrafoDist += self.getTRANSFORMADORES_DE_DISTRIBUICAO(self.uniSE_MT_SEL)

    def getSEG_LINHAS_RAMAL_LIGACAO(self, nomeSE_MT, tipoLinha):
        try:

            dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoLinha == "SEGBT":  # Segmentos de Linhas de Baixa Tensão
                dados_db = self.acessDataBase.getOpenDSS_SegLinhasRamLigBT(nomeSE_MT, "SEGBT")
            elif tipoLinha == "RLIG":  # Ramal de Ligação
                dados_db = self.acessDataBase.getOpenDSS_SegLinhasRamLigBT(nomeSE_MT, "RLIG")
            else:
                raise ExecOpenDSS("Erro ao carregar as informações das Linhas BT, pois o tipo não foi especificado! \n" + tipoLinha)

            memoFileLinha = ""

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    for ctd in range(0, len(dados_db)):

                        [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, dados_db[ctd].pac_2)


                        memoFileLinha += "New Line.{0}".format(dados_db[ctd].cod_id) + " Phases={0}".format(num_de_fases)
                        memoFileLinha += " Bus1={0}".format(pac_1) + " Bus2={0}".format(pac_2)
                        memoFileLinha += " Linecode={0}".format( dados_db[ctd].tip_cnd )
                        memoFileLinha += " Length={0}".format((str(int(dados_db[ctd].comp) / 1000)))
                        memoFileLinha += " units=km" + "\n"

            return memoFileLinha

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoLinha)

    def exec_SEG_LINHAS_DE_BAIXA_TENSAO(self):
        self.memoFileSegLinhasBT = "\n" + "! SEGMENTOS DE LINHA DE BAIXA TENSÃO " + "\n" + "\n"

        self.memoFileSegLinhasBT += self.getSEG_LINHAS_RAMAL_LIGACAO(self.uniSE_MT_SEL, "SEGBT")

    def exec_RAMAL_DE_LIGACAO(self):
        self.memoFileRamaisLigBT = "\n" + "! RAMAL_DE_LIGACAO " + "\n" + "\n"

        self.memoFileRamaisLigBT += self.getSEG_LINHAS_RAMAL_LIGACAO(self.uniSE_MT_SEL, "RLIG")


    def getUNID_COMPENSADORAS_DE_REATIVO(self, nomeSE_MT, tipoCAP):
        try:

            dados_ctmt = self.acessDataBase.getOpenDSS_CTMT(None)

            lista_de_identificadores_dos_alimentadores = self.getID_Fields(dados_ctmt)

            if tipoCAP == "MT":  # Segmentos de Linhas de Baixa Tensão
                dados_db = self.acessDataBase.getOpenDSS_UniCompReativo(nomeSE_MT, "MT")
            elif tipoCAP == "BT":  # Ramal de Ligação
                dados_db = self.acessDataBase.getOpenDSS_UniCompReativo(nomeSE_MT, "BT")
            else:
                raise ExecOpenDSS("Erro ao carregar as informações das Linhas BT, pois o tipo não foi especificado! \n" + tipoLinha)

            memoFileComp = ""

            for ctd in range(0, len(dados_db)):

                if (dados_db[ctd].ctmt in lista_de_identificadores_dos_alimentadores):

                    for ctd in range(0, len(dados_db)):

                        [num_de_fases, pac_1, pac_2] = self.getFasesConexao(dados_db[ctd].fas_con, dados_db[ctd].pac_1, None)

                        memoFileComp += "New Capacitor.{0}".format(dados_db[ctd].cod_id) + " Bus1={0}".format(pac_1)
                        memoFileComp += " Phases={0}".format(num_de_fases)
                        memoFileComp += " kVAR={0}".format(str( dados_db[ctd].pot_nom )) + '\n'

            return memoFileComp

        except ExecOpenDSS:
            raise ExecOpenDSS("Erro ao carregar as informações das Unidades Consumidoras: " + tipoCAP)

    def exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO(self):
        self.memoFileUndCompReatMT = "\n" + "! UNIDADES COMPENSADORAS DE REATIVO DE MÉDIA TENSÃO" + "\n" + "\n"

        self.memoFileUndCompReatMT += self.getUNID_COMPENSADORAS_DE_REATIVO(self.uniSE_MT_SEL, "MT")

    def exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO(self):
        self.memoFileUndCompReatBT = "\n" + "! UNIDADES COMPENSADORAS DE REATIVO DE BAIXA TENSÃO " + "\n" + "\n"

        self.memoFileUndCompReatBT += self.getUNID_COMPENSADORAS_DE_REATIVO(self.uniSE_MT_SEL, "BT")
        
        
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
