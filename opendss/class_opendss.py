import os
import platform
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
import cmath

import opendss.class_conn
import database.class_conn
import opendss.class_data
import class_exception
import time
import multiprocessing

##Thread
#import opendss.class_thread_load
#import queue
#import threading

##Process
#import opendss.class_process_load
import queue

class C_OpenDSS(): # classe OpenDSSDirect

    def __init__(self):

        self.dataOpenDSS = opendss.class_data.C_Data() #Acesso ao Banco de Dados
        self._DataBaseConn = database.class_conn.C_DBaseConn()  # Criando a instância do Banco de Dados


        self._nCircuitoAT_MT = ''
        self._nSE_MT_Selecionada = ''
        self._nFieldsMT = ''

        #### Energy Meters
        self._EnergyMeters = []
        #### Monitors
        self._Monitors = []
        ##SC Carvalho
        self._SCDataInfo = []
        ## FlagLoadData - Só roda se tiver alguma alteração nos alimentadores
        self.loadDataFlag = False


        self.OpenDSSEngine = opendss.class_conn.C_Conn() ## Apenas para o Objeto Existir, depois será sobrecarregado
        self._OpenDSSConfig = {}

        self.memoLoadShapes = ''

        self.tableVoltageResults = QTableWidget() # Tabela de Resultados

        ###
        self.StatusSolutionProcessTime = 0.0


    @property
    def OpenDSSConfig(self):
        return self._OpenDSSConfig

    @OpenDSSConfig.setter
    def OpenDSSConfig(self, value):
        self._OpenDSSConfig = value

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
    def EnergyMeters(self):
        return self._EnergyMeters

    @EnergyMeters.setter
    def EnergyMeters(self, value):
        self._EnergyMeters = value

    @property
    def Monitors(self):
        return self._Monitors

    @Monitors.setter
    def Monitors(self, value):
        self._Monitors = value

    @property
    def SCDataInfo(self):
        return self._SCDataInfo

    @SCDataInfo.setter
    def SCDataInfo(self, value):
        self._SCDataInfo = value

    def loadData(self):

        if not self.loadDataFlag:
            ### Passando as variáveis
            self.dataOpenDSS.DataBaseConn = self.DataBaseConn
            self.dataOpenDSS.nFieldsMT = self.nFieldsMT
            self.dataOpenDSS.nCircuitoAT_MT = self.nCircuitoAT_MT
            self.dataOpenDSS.nSE_MT_Selecionada = self.nSE_MT_Selecionada
            ##Zerando a lista de barras
            self.dataOpenDSS.busList = []
            self.dataOpenDSS.elementList = []


            ##### Executa os Arquitvos que serão executados e inseridos

            self.execOpenDSSFunc = {"header": ["Cabeçalho ...", self.dataOpenDSS.exec_HeaderFile],
                          "EqThAT": ["Equivalente de Thevenin ...", self.dataOpenDSS.exec_EQUIVALENTE_DE_THEVENIN],
                          "LoadShapes": ["Curvas de Carga ...", self.exec_LOADSHAPES],
                          # "EqThMT":["Equivalente de Thevenin MT...",self.dataOpenDSS.exec_EQUIVALENTE_DE_THEVENIN_MEDIA],
                          "SecEqThAT_SecAT": ["Chaves entre o Equivalente e a SecAT ...", self.dataOpenDSS.exec_SEC_EQTHAT_SECAT],
                          "TrafoATMT": ["Trafo AT - MT...", self.dataOpenDSS.exec_TRANSFORMADORES_DE_ALTA_PARA_MEDIA],
                          "CondMT": ["Condutores MT...", self.dataOpenDSS.exec_CONDUTORES_DE_MEDIA_TENSAO],
                          # "CondBT":["Condutores de BT...",self.dataOpenDSS.exec_CONDUTORES_DE_BAIXA_TENSAO],
                          #"CondRamais": ["Condutores de Ramais ...", self.dataOpenDSS.exec_CONDUTORES_DE_RAMAL],
                          "SecAT": ["Seccionadoras de AT...", self.dataOpenDSS.exec_SEC_DE_ALTA_TENSAO],
                          "SecATControl": ["Controle Seccionadoras de AT...",self.dataOpenDSS.exec_CONTROLE_SEC_DE_ALTA_TENSAO],
                          "SecOleoMT": ["Chave a óleo de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO],
                          "SecOleoMTControl": ["Controle Chave a óleo de MT...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO],
                          "SecFacaMT": ["Chave Faca de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_FACA_DE_MEDIA_TENSAO],
                          "SecFacaMTControl": ["Controle Chave Faca de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_FACA_DE_MEDIA_TENSAO],
                          "SecTripolarMT": ["Chave Faca Tripolar de MT ...",self.dataOpenDSS.exec_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO],
                          "SecTripolarMTControl": ["Controle Chave Faca Tripolar de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO],
                          "ChFusMT": ["Chave Fusível de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO],
                          "ChFusMTControl": ["Controle Chave Fusível de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO],
                          "DJMT": ["DJ de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO],
                          "DJMTControl": ["Controle DJ de MT ...", self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO],
                          "ReligMT": ["Religador de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO],
                          "ReligMTControl": ["Controle do Religador de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO],
                          "ChTripolarSEMT": ["Chave Tripolar da SE MT ...",self.dataOpenDSS.exec_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                          "ChTripolarSEMTControl": ["Controle Chave Tripolar da SE MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                          "ChUnipolarSEMT": ["Chave Unipolar da SE MT ...",self.dataOpenDSS.exec_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                          "ChUnipolarSEMTControl": ["Controle da Chave Unipolar da SE MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                          #"Reg":["Regulador MT ...",self.dataOpenDSS.exec_REGULADORES_DE_MEDIA_TENSAO],
                          "SegMT": ["Segmentos de Linhas MT ...", self.dataOpenDSS.exec_SEG_LINHAS_DE_MEDIA_TENSAO],
                          "UConMT": ["Unidades Consumidoras MT ...", self.dataOpenDSS.exec_UNID_CONSUMIDORAS_MT],
                          "UConMTLoadShapes": ["Unidades Consumidoras MT - Curvas de Carga ...", self.dataOpenDSS.exec_UNID_CONSUMIDORAS_LOADSHAPES_MT],
                          "TrafoDist":["Trafos de Distribuição ...",self.dataOpenDSS.exec_TRANSFORMADORES_DE_DISTRIBUICAO],
                          # "SegBT":["Segmentos de Linhas BT ...",self.dataOpenDSS.exec_SEG_LINHAS_DE_BAIXA_TENSAO],
                          #"UConBT":["Unidades Consumidoras BT ...",self.dataOpenDSS.exec_UNID_CONSUMIDORAS_BT],
                          "UConBTTD": ["Unidades Consumidoras BT no Transformador de Distribuição ...", self.dataOpenDSS.exec_UNID_CONSUMIDORAS_BT_TD],
                          "UConBTLoadShapes": ["Unidades Consumidoras BT - Curvas de Carga ...", self.dataOpenDSS.exec_UNID_CONSUMIDORAS_LOADSHAPES_BT],
                          # "RamLig":["Ramais de Ligação  ...",self.dataOpenDSS.exec_RAMAL_DE_LIGACAO,self.dataOpenDSS.memoFileRamaisLigBT],
                          "CompMT": ["Unidades Compensadoras de MT ...",self.dataOpenDSS.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO],
                          # "CompBT":["Unidades Compensadoras de BT ...",self.dataOpenDSS.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO],
                          }


            ##Thread
            #https://www.tutorialspoint.com/python/python_multithreading.htm
            # nCPU = multiprocessing.cpu_count()
            # queueLock = threading.Lock()
            # workQueue = queue.Queue(len(self.execOpenDSSFunc)) ## Quantidade de Tarefas para serem realizadas
            # threads = []
            #
            # # Create new threads
            # for threadID in range(1, nCPU):
            #     thread = opendss.class_thread_load.C_LoadDataThread(threadID, workQueue, queueLock)
            #     ##Variávies que as Threads podem utilizar nas funções que irão executar
            #     thread.DataBaseConn = self.DataBaseConn
            #     thread.nFieldsMT = self.nFieldsMT
            #     thread.nCircuitoAT_MT = self.nCircuitoAT_MT
            #     thread.nSE_MT_Selecionada = self.nSE_MT_Selecionada
            #     thread.OpenDSSConfig = self.OpenDSSConfig
            #
            #     thread.start()
            #     threads.append(thread)
            #
            #
            # # Fill the queue
            # queueLock.acquire()
            #
            # for ctd in self.execOpenDSSFunc:
            #     msg = self.execOpenDSSFunc[ctd][-2]
            #     #Executando a função
            #     ### Verificando o modo de operação
            #
            #     ### Roda com a flag em 1
            #     if (ctd == "UConMT") and (self.OpenDSSConfig["UNCMT"] == "1"):
            #         workQueue.put(self.execOpenDSSFunc[ctd][-1])
            #         #print(msg)
            #     elif (ctd == "UConBTTD") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
            #         workQueue.put(self.execOpenDSSFunc[ctd][-1])
            #         #print(msg)
            #     elif (ctd == "UConMTLoadShapes") or (ctd == "LoadShapes"):
            #         if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCMT"] == "1"):
            #             workQueue.put(self.execOpenDSSFunc[ctd][-1])
            #             #print(msg)
            #     elif (ctd == "UConBTTD") or (ctd == "UConBTLoadShapes"):
            #         if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
            #             workQueue.put(self.execOpenDSSFunc[ctd][-1])
            #             #print(msg)
            #     else:
            #         workQueue.put(self.execOpenDSSFunc[ctd][-1])
            #
            # queueLock.release()
            #
            # # Wait for queue to empty
            # while not workQueue.empty():
            #     pass
            #
            # # Wait for all threads to complete
            # for t in threads:
            #     t.exitFlag = 1
            #     t.join()
            # print("Exiting Main Thread")

            for ctd in self.execOpenDSSFunc:
                msg = self.execOpenDSSFunc[ctd][-2]
                # Executando a função
                ### Verificando o modo de operação

                ### Roda com a flag em 1
                if (ctd == "UConMT") and (self.OpenDSSConfig["UNCMT"] == "1"):
                    self.execOpenDSSFunc[ctd][-1]()
                    #print(msg)
                elif (ctd == "UConBTTD") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
                    self.execOpenDSSFunc[ctd][-1]()
                    #print(msg)
                elif (ctd == "UConMTLoadShapes") or (ctd == "LoadShapes"):
                    if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCMT"] == "1"):
                        self.execOpenDSSFunc[ctd][-1]()
                        #print(msg)
                elif (ctd == "UConBTTD") or (ctd == "UConBTLoadShapes"):
                    if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
                        self.execOpenDSSFunc[ctd][-1]()
                        #print(msg)
                else:
                    self.execOpenDSSFunc[ctd][-1]()
                    #print(msg)

                ## Setando a Flag
        self.loadDataFlag = True


    def loadData_All(self):
        self.execOpenDSSFuncAll= {
                "VoltageBase": ["Bases de Tensão ...", self.exec_VoltageBase],
                "EnergyMeters": ["Inserindo os Energy Meters ...", self.exec_EnergyMeters],
                "Monitors": ["Inserindo os Monitors ...", self.exec_Monitors],
                "Mode": ["Modo de Operação ...", self.exec_Mode],
                }

        for ctd in self.execOpenDSSFuncAll:
            msg = self.execOpenDSSFuncAll[ctd][-2]
            self.execOpenDSSFuncAll[ctd][-1]()


    def loadDataResult(self):

        self.OpenDSSDataResult = {"header": self.dataOpenDSS.memoFileHeader,
                      "EqThAT": self.dataOpenDSS.memoFileEqTh,
                      "LoadShapes": self.memoLoadShapes,
                      # "EqThMT":self.dataOpenDSS.memoFileEqThMT,
                      "SecEqThAT_SecAT": self.dataOpenDSS.memoFileSecAT_EqThAT,
                      "TrafoATMT": self.dataOpenDSS.memoFileTrafoATMT,
                      "CondMT": self.dataOpenDSS.memoFileCondMT,
                      # "CondBT": self.dataOpenDSS.memoFileCondBT,
                      "CondRamais": self.dataOpenDSS.memoFileCondRamal,
                      "SecAT": self.dataOpenDSS.memoFileSecAT ,
                      "SecATControl":  self.dataOpenDSS.memoFileSecAT_Control,
                      "SecOleoMT": self.dataOpenDSS.memoFileSecOleoMT,
                      "SecOleoMTControl": self.dataOpenDSS.memoFileSecOleoMT_Control,
                      "SecFacaMT": self.dataOpenDSS.memoFileSecFacaMT,
                      "SecFacaMTControl": self.dataOpenDSS.memoFileSecFacaMT_Control,
                      "SecTripolarMT": self.dataOpenDSS.memoFileSecFacaTripolarMT,
                      "SecTripolarMTControl": self.dataOpenDSS.memoFileSecFacaTripolarMT_Control,
                      "ChFusMT":self.dataOpenDSS.memoFileSecFusivelMT,
                      "ChFusMTControl": self.dataOpenDSS.memoFileSecFusivelMT_Control,
                      "DJMT":self.dataOpenDSS.memoFileSecDJReleMT,
                      "DJMTControl": self.dataOpenDSS.memoFileSecDJReleMT_Control,
                      "ReligMT": self.dataOpenDSS.memoFileSecReligadorMT,
                      "ReligMTControl": self.dataOpenDSS.memoFileSecReligadorMT_Control,
                      "ChTripolarSEMT":self.dataOpenDSS.memoFileSecTripolarSEMT,
                      "ChTripolarSEMTControl": self.dataOpenDSS.memoFileSecTripolarSEMT_Control,
                      "ChUnipolarSEMT":self.dataOpenDSS.memoFileSecUnipolarSEMT,
                      "ChUnipolarSEMTControl": self.dataOpenDSS.memoFileSecUnipolarSEMT_Control ,
                      #"Reg":self.dataOpenDSS.memoFileReguladorMT,
                      "SegMT":self.dataOpenDSS.memoFileSegLinhasMT,
                      "UConMT":self.dataOpenDSS.memoFileUniConsumidoraMT,
                      "UConMTLoadShapes": self.dataOpenDSS.memoFileUniConsumidoraLoadShapesMT,
                      "TrafoDist":self.dataOpenDSS.memoFileTrafoDist,
                      # "SegBT":self.dataOpenDSS.memoFileSegLinhasBT,
                      #"UConBT":self.dataOpenDSS.memoFileUniConsumidoraBT,
                      "UConBTTD": self.dataOpenDSS.memoFileUniConsumidoraBT_TD,
                      "UConBTLoadShapes": self.dataOpenDSS.memoFileUniConsumidoraLoadShapesBT,
                      # "RamLig":self.dataOpenDSS.memoFileRamaisLigBT,self.memoFileRamaisLigBT,
                      "CompMT": self.dataOpenDSS.memoFileUndCompReatMT,
                      # "CompBT":self.dataOpenDSS.memoFileUndCompReatBT,
                      "VoltageBase":self.memoFileVoltageBase,
                      "EnergyMeters": self.memoFileEnergyMeters,
                      "Monitors": self.memoFileMonitors,
                      "Mode": self.memoFileMode,
                      }


    def exec_SaveFileDialogDSS(self):

        arquivoSalvo = QFileDialog.getSaveFileName(None, "Save OpenDSS File", "Results/",
                                                            "DSS Files (*.dss)")[0]

        nome_do_arquivo_criado = os.path.basename(str(arquivoSalvo)).replace(".dss","")

        diretorio = os.path.dirname(str(arquivoSalvo)) + "/"

        if platform.system() == "Windows":
            diretorio = diretorio.replace('/', '\\')

        self.saveFileDSS(diretorio, nome_do_arquivo_criado, self.createMainFileDSS())


        for ctd in self.OpenDSSDataResult:
            redirectFile = ''
            if (ctd != "header") and (ctd != "EqThAT") and (ctd != "VoltageBase") and (ctd != "Mode"):  # Cabeçalho do arquivo
                data = self.OpenDSSDataResult[ctd]
                for cont in data:
                    redirectFile += str(cont) + '\n'

            if (ctd == "UConMT") and (self.OpenDSSConfig["UNCMT"] == "1"):
                self.saveFileDSS(diretorio, ctd, redirectFile)
            elif (ctd == "UConBTTD") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
                self.saveFileDSS(diretorio, ctd, redirectFile)
            elif (ctd == "UConMTLoadShapes") or (ctd == "LoadShapes"):
                if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCMT"] == "1"):
                    self.saveFileDSS(diretorio, ctd, redirectFile)
            elif (ctd == "UConBTTD") or (ctd == "UConBTLoadShapes"):
                if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
                    self.saveFileDSS(diretorio, ctd, redirectFile)
            else:
                self.saveFileDSS(diretorio, ctd, redirectFile)


    def saveFileDSS(self, dirSave, nameMemo, dataMemo ): #Salvar em Arquivo

        arquivo = open(dirSave + nameMemo + ".dss", 'w', encoding='utf-8')
        arquivo.writelines( dataMemo )
        arquivo.close()

    def createMainFileDSS(self): # Para salvar em arquivo

        mainFile = ''

        for ctd in self.execOpenDSSFunc:
            if (ctd == "header") or (ctd == "EqThAT") or (ctd != "VoltageBase") or (ctd != "Mode"): # Cabeçalho do arquivo
                data = self.OpenDSSDataResult[ctd]
                for cont in data:
                    mainFile += str(cont) + '\n'
            else:

                if (ctd == "UConMT") and (self.OpenDSSConfig["UNCMT"] == "1"):
                    mainFile += "! " + self.execOpenDSSFunc[ctd][-2] + "\n"
                    mainFile += "Redirect " + ctd + ".dss " + '\n'
                elif (ctd == "UConBTTD") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
                    mainFile += "! " + self.execOpenDSSFunc[ctd][-2] + "\n"
                    mainFile += "Redirect " + ctd + ".dss " + '\n'
                elif (ctd == "UConMTLoadShapes") or (ctd == "LoadShapes"):
                    if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCMT"] == "1"):
                        mainFile += "! " + self.execOpenDSSFunc[ctd][-2] + "\n"
                        mainFile += "Redirect " + ctd + ".dss " + '\n'
                elif (ctd == "UConBTTD") or (ctd == "UConBTLoadShapes"):
                    if (self.OpenDSSConfig["Mode"] == "Daily") and (self.OpenDSSConfig["UNCBTTD"] == "1"):
                        mainFile += "! " + self.execOpenDSSFunc[ctd][-2] + "\n"
                        mainFile += "Redirect " + ctd + ".dss " + '\n'
                else:
                    mainFile += "! " + self.execOpenDSSFunc[ctd][-2] + "\n"
                    mainFile += "Redirect " + ctd + ".dss " + '\n'

        #Falta o final do arquivo

        return mainFile

    def exec_VoltageBase(self):

        ######
        self.memoFileVoltageBase = []
        self.memoFileVoltageBase.append("set voltagebases = [" + self.OpenDSSConfig["VoltageBase"] + "]")
        self.memoFileVoltageBase.append("Calcvoltagebases")

    def exec_Mode(self):

        self.memoFileMode = []

        if self.OpenDSSConfig["Mode"] == "Daily":
            sztime = self.OpenDSSConfig["StepSizeTime"][0]
            self.memoFileMode.append("set mode=" + self.OpenDSSConfig["Mode"] + " stepsize=" \
                                       + str(self.OpenDSSConfig["StepSize"]) + sztime + " number=" + str(self.OpenDSSConfig["Number"]))
        else:
            self.memoFileMode.append("set mode=" + self.OpenDSSConfig["Mode"])


    def exec_LOADSHAPES(self):

        loadShapes = self.OpenDSSConfig["LoadShapes"]

        self.memoLoadShapes = []

        sztime = self.OpenDSSConfig["StepSizeTime"][0]
        if sztime == "h":
            sztime = ""

        for ctd in loadShapes:
            self.memoLoadShapes.append("New LoadShape.{0}".format(ctd) + " npts={0}".format(self.OpenDSSConfig["Number"]) \
                                       + " "+ sztime + "interval={0}".format(self.OpenDSSConfig["StepSize"]) \
                                       + " mult =" + str(loadShapes[ctd]).replace("[","(").replace("]",")") + " Action=Normalize")

    def exec_OpenDSS(self):

        start_time = time.time()

        ######## Define o Engine do OpenDSS
        try:
            if self.OpenDSSConfig["openDSSConn"] == "OpenDSSDirect":
                self.OpenDSSEngine = opendss.class_conn.C_OpenDSSDirect_Conn()
            elif self.OpenDSSConfig["openDSSConn"] == "COM":
                self.OpenDSSEngine = opendss.class_conn.C_OpenDSSCOM_Conn()
        except:
            raise class_exception.ExecOpenDSS("Erro ao definir o Engine do OpenDSS!")

        #Executa as consultas no Banco de Dados
        self.loadData()
        #Executa os Monitores
        self.loadData_All()
        #Pega os Memo
        self.loadDataResult()

        self.OpenDSSEngine.clear()

        for ctd in self.OpenDSSDataResult:

            command = self.OpenDSSDataResult[ctd]

            for com in command:
                self.exec_OpenDSSRun(com)

        try:

            #for ctd in self.Monitors:
            #    self.exec_OpenDSSRun("Export monitor " + ctd["Name"])

            self.exec_OpenDSSRun("Solve")

        except:
            class_exception.ExecOpenDSS("Erro ao executar o fluxo de potência resolvido!")

#            self.OpenDSSEngine.run("Show Voltage LN Nodes")
        self.getVoltageResults() ## Mostrando o resultado das tensões
        #self.OpenDSSEngine.run("Solve")


        ##Status
        self.StatusSolutionProcessTime = time.time() - start_time

    def exec_OpenDSSRun(self, command):
        self.OpenDSSEngine.run(command)

    def getVoltageResults(self):

        busNames = self.OpenDSSEngine.get_Circuit_AllBusNames() ## Lista com nomes de todos os nós
        VoltagePhaseAPU = self.OpenDSSEngine.get_Circuit_AllNodeVmagPUByPhase(1) ## Lista com todas as tensões de LN da fase A em PU
        VoltagePhaseBPU = self.OpenDSSEngine.get_Circuit_AllNodeVmagPUByPhase(2) ## Lista com todas as tensões de LN da fase B em PU
        VoltagePhaseCPU = self.OpenDSSEngine.get_Circuit_AllNodeVmagPUByPhase(3) ## Lista com todas as tensões de LN da fase C em PU
        busVoltagesALL = self.OpenDSSEngine.get_Circuit_AllBusVolts() ## Lista com todas as tensões de LN da fase ABN complexa  em PU

        self.tableVoltageResults.setRowCount(len(busNames))

        for ctdBus in range(0, len(busNames)):
            ## Nome da Barra
            self.tableVoltageResults.setItem(ctdBus, 0, QTableWidgetItem( busNames[ctdBus] ))
        for ctdVoltageA in range(0, len(VoltagePhaseAPU)):
            ##Tensão nodal fase A em pu
            self.tableVoltageResults.setItem(ctdVoltageA, 7, QTableWidgetItem(str(round(VoltagePhaseAPU[ctdVoltageA] , 5 ))))
        for ctdVoltageB in range(0, len(VoltagePhaseBPU)):
            ##Tensão nodal fase B em pu
            self.tableVoltageResults.setItem(ctdVoltageB, 9, QTableWidgetItem(str(round(VoltagePhaseBPU[ctdVoltageB] , 5 ))))
        for ctdVoltageC in range(0, len(VoltagePhaseCPU)):
            ##Tensão nodal fase C em pu
            self.tableVoltageResults.setItem(ctdVoltageC, 11, QTableWidgetItem(str(round(VoltagePhaseCPU[ctdVoltageC] , 5 ))))

        try:
            for ctdVoltageA in range(0, len(busVoltagesALL)):
                ## Tensões nodais fase A em V
                Va = complex(busVoltagesALL[ctdVoltageA], busVoltagesALL[ctdVoltageA+1])
                self.tableVoltageResults.setItem(ctdVoltageA, 1, QTableWidgetItem(str(round(abs(Va)/1000, 5))))
                self.tableVoltageResults.setItem(ctdVoltageA, 2, QTableWidgetItem(str(round((cmath.phase(Va) * 180 / cmath.pi) ,3 ))))
                self.tableVoltageResults.setItem(ctdVoltageA, 8, QTableWidgetItem(str(round((cmath.phase(Va) * 180 / cmath.pi), 3))))
        except:
            pass
        #    class_exception.ExecOpenDSS("Erro ao processar as tensões!", "Fase A")

        try:
            for ctdVoltageB in range(0, len(busVoltagesALL)):
                ## Tensões nodais fase B em V
                Vb = complex(busVoltagesALL[ctdVoltageB+2], busVoltagesALL[ctdVoltageB+3])
                self.tableVoltageResults.setItem(ctdVoltageB, 3, QTableWidgetItem(str(round(abs(Vb)/1000 , 5))))
                self.tableVoltageResults.setItem(ctdVoltageB, 4, QTableWidgetItem(str(round( cmath.phase(Vb) * 180 / cmath.pi , 3))))
                self.tableVoltageResults.setItem(ctdVoltageB, 10, QTableWidgetItem(str(round( cmath.phase(Vb) * 180 / cmath.pi, 3))))
        except:
            pass
            #class_exception.ExecOpenDSS("Erro ao processar as tensões!", "Fase B")

        try:
            for ctdVoltageC in range(0, len(busVoltagesALL)):
                ## Tensões nodais fase C em V
                Vc = complex(busVoltagesALL[ctdVoltageC+4], busVoltagesALL[ctdVoltageC+5])
                self.tableVoltageResults.setItem(ctdVoltageC, 5, QTableWidgetItem(str(round(abs(Vc)/1000 , 5))))
                self.tableVoltageResults.setItem(ctdVoltageC, 6, QTableWidgetItem(str(round((cmath.phase(Vc) * 180 / cmath.pi),3))))
                self.tableVoltageResults.setItem(ctdVoltageC, 12, QTableWidgetItem(str(round((cmath.phase(Vc) * 180 / cmath.pi), 3))))
        except:
            pass
            #class_exception.ExecOpenDSS("Erro ao processar as tensões!", "Fase C")

    #######Monitor

    def exec_EnergyMeters(self):

        self.memoFileEnergyMeters = []

        for ctd in self.EnergyMeters:
            tmp = "New EnergyMeter." + ctd["Name"] + \
                  " Element=" + ctd["Element"] + \
                  " Terminal=" + ctd["Terminal"] + \
                  " 3phaseLosses=" + ctd["3phaseLosses"]  + \
                  " LineLosses=" + ctd["LineLosses"] + \
                  " Losses=" + ctd["Losses"]  + \
                  " SeqLosses=" + ctd["SeqLosses"] + \
                  " VbaseLosses=" + ctd["VbaseLosses"] + \
                  " XfmrLosses=" + ctd["XfmrLosses"] + \
                  " LocalOnly=" + ctd["LocalOnly"]  + \
                  " PhaseVoltageReport=" + ctd["PhaseVoltageReport"] + \
                  " Action=" + ctd["Action"] + \
                  " Enabled=" + ctd["Enabled"]

            self.memoFileEnergyMeters.append(tmp)

    def exec_Monitors(self):

        self.memoFileMonitors = []

        for ctd in self.Monitors:
            tmp = "New Monitor." + ctd["Name"] + \
                  " Element=" + ctd["Element"] + \
                  " Terminal=" + ctd["Terminal"] + \
                  " Mode=" + str(ctd["Mode"])  + \
                  " Action=" + ctd["Action"] + \
                  " Enable=" + ctd["Enable"] + \
                  " Ppolar=" + ctd["Ppolar"] + \
                  " VIPolar="  + ctd["VIpolar"]


            self.memoFileMonitors.append(tmp)


    ######################################################################################
    ###
    def exec_DynamicFlt(self):

        self.memoFileSC = []
        faultstr = ''
        for stdSC in self.SCDataInfo:
            faultstr = 'New Fault.DynamicFault'
            faultstr += " bus1=" + stdSC["FltBus"]
            faultstr += " phases=" + stdSC["FltPhases"]
            faultstr += " r=" + stdSC["FltRst"]
            faultstr += " ontime=" + stdSC["FltTime"]
            faultstr += " temporary=" + stdSC["FltType"]

            if not (stdSC["FltBus2"] == " " or stdSC["FltBus2"] == 'None'):
                faultstr += " bus2=" + stdSC["FltBus2"]

            faultstr += " basefreq=" + stdSC["FltBaseFreq"]

            if stdSC["FltRstDev"] != "" :
                faultstr += " %stddev=" + stdSC["FltRstDev"]

            if stdSC["FltRepair"] != "" :
                faultstr += " repair=" + stdSC["FltRepair"]

        self.exec_OpenDSSRun(faultstr)
        self.exec_OpenDSSRun("set mode=dynamic controlmode=time time=(0,0) stepsize=0.01 number=4000")
        self.exec_OpenDSSRun("Solve")
        self.exec_OpenDSSRun("show eventlog")


    ##
    def getBusList(self):
        return self.dataOpenDSS.busList

    def getElementList(self):
        return self.dataOpenDSS.elementList

    ## Gets class_insert_dialog


    def getAllNamesEnergyMeter(self):

        return self.OpenDSSEngine.get_EnergyMeter_AllNames()

    def getAllNamesMonitor(self):
        return self.OpenDSSEngine.get_Monitor_AllNames()

    def getAllNamesElements(self):
        return self.OpenDSSEngine.get_Circuit_AllElementNames()

    def getAllBusNames(self):
        return self.OpenDSSEngine.get_Circuit_AllBusNames()

    def setMonitorActive(self, name):
        self.OpenDSSEngine.set_MonitorActive(name)

    def getMonitorActive_ChannelNames(self):
        return self.OpenDSSEngine.get_MonitorActive_ChannelNames()

    def getMonitorActive_DataChannel(self, idx):
        return self.OpenDSSEngine.get_MonitorActive_DataChannel(idx)
