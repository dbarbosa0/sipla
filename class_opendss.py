import os
import platform
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QGroupBox, QLabel, QProgressBar, QDialog, QStyleFactory
from PyQt5.QtGui import QIcon

import class_opendss_conn
import class_database_conn
import class_opendss_data
import class_exception


class C_OpenDSS(): # classe OpenDSSDirect

    def __init__(self):

        self.dataOpenDSS = class_opendss_data.C_OpenDSS_Data() #Acesso ao Banco de Dados

        self._DataBaseConn = class_database_conn.C_DBaseConn()  # Criando a instância do Banco de Dados

        self._nCircuitoAT_MT = ''
        self._nSE_MT_Selecionada = ''
        self._nFieldsMT = ''

        self._OpenDSSConn = ''

    @property
    def OpenDSSConn(self):
        return self._OpenDSSConn

    @OpenDSSConn.setter
    def OpenDSSConn(self, value):
        self._OpenDSSConn = value

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


    def loadData(self):

        ### Passando as variáveis
        self.dataOpenDSS.DataBaseConn = self.DataBaseConn

        self.dataOpenDSS.nFieldsMT = self.nFieldsMT
        self.dataOpenDSS.nCircuitoAT_MT = self.nCircuitoAT_MT
        self.dataOpenDSS.nSE_MT_Selecionada = self.nSE_MT_Selecionada

        ######## Define o Engine do OpenDSS
        try:
            if self.OpenDSSConn == "OpenDSSDirect":
                self.OpenDSSEngine = class_opendss_conn.C_OpenDSSDirect_Conn()
            elif self.OpenDSSConn == "COM":
                self.OpenDSSEngine = class_opendss_conn.C_OpenDSSCOM_Conn()
            else:
                raise class_exception.ExecOpenDSS("Erro ao definir o Engine do OpenDSS!")
        except:
            pass



    ##########
       # self.OpenDSS_Progress_Dialog = C_OpenDSS_ExecDialog()


        ##### Executa os Arquitvos que serão executados e inseridos

        self.execOpenDSSFunc = {"header": ["Cabeçalho ...", self.dataOpenDSS.exec_HeaderFile],
                      "EqThAT": ["Equivalente de Thevenin ...", self.dataOpenDSS.exec_EQUIVALENTE_DE_THEVENIN],
                      # "EqThMT":["Equivalente de Thevenin MT...",self.dataOpenDSS.exec_EQUIVALENTE_DE_THEVENIN_MEDIA],
                      "TrafoATMT": ["Trafo AT - MT...", self.dataOpenDSS.exec_TRANSFORMADORES_DE_ALTA_PARA_MEDIA],
                      "CondMT": ["Condutores MT...", self.dataOpenDSS.exec_CONDUTORES_DE_MEDIA_TENSAO],
                      # "CondBT":["Condutores de BT...",self.dataOpenDSS.exec_CONDUTORES_DE_BAIXA_TENSAO],
                      "CondRamais": ["Condutores de Ramais ...", self.dataOpenDSS.exec_CONDUTORES_DE_RAMAL],
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
                      # ObsSandy1             #"Reg":["Regulador MT ...",self.dataOpenDSS.exec_REGULADORES_DE_MEDIA_TENSAO],
                      "SegMT": ["Segmentos de Linhas MT ...", self.dataOpenDSS.exec_SEG_LINHAS_DE_MEDIA_TENSAO],
                      "UConMT": ["Unidades Consumidoras MT ...", self.dataOpenDSS.exec_UNID_CONSUMIDORAS_MT],
                      # ObsSandy2            #"TrafoDist":["Trafos de Distribuição ...",self.dataOpenDSS.exec_TRANSFORMADORES_DE_DISTRIBUICAO],
                      # "SegBT":["Segmentos de Linhas BT ...",self.dataOpenDSS.exec_SEG_LINHAS_DE_BAIXA_TENSAO],
                      # "UConBT":["Unidades Consumidoras BT ...",self.dataOpenDSS.exec_UNID_CONSUMIDORAS_BT],
                      # "RamLig":["Ramais de Ligação  ...",self.dataOpenDSS.exec_RAMAL_DE_LIGACAO,self.dataOpenDSS.memoFileRamaisLigBT],
                      "CompMT": ["Unidades Compensadoras de MT ...",self.dataOpenDSS.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO],
                      # "CompBT":["Unidades Compensadoras de BT ...",self.dataOpenDSS.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO],
                      "footer": ["Rodapé ...", self.dataOpenDSS.exec_FooterFile],
                      }


       # self.OpenDSS_Progress_Dialog.progBar.setMaximum(len(self.execFunc))

        #self.OpenDSS_Progress_Dialog.show()

        #ctdN = 0
        for ctd in self.execOpenDSSFunc:
            msg = self.execOpenDSSFunc[ctd][-2]
            #Executando a função
            self.execOpenDSSFunc[ctd][-1]()

        #   ctdN += 1
        #    self.OpenDSS_Progress_Dialog.Info_GroupBox_MsgLabel.setText(msg)
       #     self.OpenDSS_Progress_Dialog.progBar.setValue(ctdN)
       #     print(self.OpenDSS_Progress_Dialog.progBar.value())
            #self.OpenDSS_Progress_Dialog.close()


        self.OpenDSSDataResult = {"header": self.dataOpenDSS.memoFileHeader,
                      "EqThAT": self.dataOpenDSS.memoFileEqTh,
                      # "EqThMT":self.dataOpenDSS.memoFileEqThMT,
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
                      # ObsSandy1             #"Reg":self.dataOpenDSS.memoFileReguladorMT,
                      "SegMT":self.dataOpenDSS.memoFileSegLinhasMT,
                      "UConMT":self.dataOpenDSS.memoFileUniConsumidoraMT,
                      # ObsSandy2            #"TrafoDist":self.dataOpenDSS.memoFileTrafoDist,
                      # "SegBT":self.dataOpenDSS.memoFileSegLinhasBT,
                      # "UConBT":self.dataOpenDSS.memoFileUniConsumidoraBT,
                      # "RamLig":self.dataOpenDSS.memoFileRamaisLigBT,self.memoFileRamaisLigBT,
                      "CompMT": self.dataOpenDSS.memoFileUndCompReatMT,
                      # "CompBT":self.dataOpenDSS.memoFileUndCompReatBT,
                      "footer":self.memoFileFooter,
                      }


    def exec_SaveFileDialogDSS(self):

        arquivoSalvo = QFileDialog.getSaveFileName(None, "Save OpenDSS File", "Results/",
                                                            "DSS Files (*.dss)")[0]

        nome_do_arquivo_criado = os.path.basename(str(arquivoSalvo))

        diretorio = os.path.dirname(str(arquivoSalvo)) +  "/"

        if platform.system() == "Windows":
            diretorio = diretorio.replace('/', '\\')

        self.saveFileDSS(diretorio, nome_do_arquivo_criado, self.createMainFileDSS())


        for ctd in self.OpenDSSDataResult:
            redirectFile = ''
            if (ctd != "header") and (ctd != "EqThAT") and (ctd != "footer"):  # Cabeçalho do arquivo
                data = self.OpenDSSDataResult[ctd]
                for cont in data:
                    redirectFile += str(cont) + '\n'

            self.saveFileDSS(diretorio, ctd, redirectFile )


    def saveFileDSS(self, dirSave, nameMemo, dataMemo ): #Salvar em Arquivo
        arquivo = open(dirSave +  nameMemo + ".dss", 'w', encoding='utf-8')
        arquivo.writelines( dataMemo )
        arquivo.close()

    def createMainFileDSS(self): # Para salvar em arquivo

        mainFile = ''

        for ctd in self.OpenDSSDataResult:
            if (ctd == "header") or (ctd == "EqThAT") or (ctd == "footer"): # Cabeçalho do arquivo
                data = self.OpenDSSDataResult[ctd]
                for cont in data:
                    mainFile += str(cont) + '\n'
            else:
                mainFile += "Redirect " + ctd + ".dss "+'\n'

        #Falta o final do arquivo

        return mainFile

    def definedSettings(self, config):

        self.OpenDSSConn = config.openDSSConn

        self.memoFileFooter = self.dataOpenDSS.memoFileFooter
        self.memoFileFooter.append("set voltagebases = [" +  config.VoltageBase +  "]")
        self.memoFileFooter.append("set mode = direct")
        #self.FooterFile.append("set mode = " + config.VoltageBase + " stepsize = " +  config.StepSize + " number = " + Number)

        #Maxiterations: int
        #Maxcontroliter: int


    def exec_OpenDSS(self):

        for ctd in self.OpenDSSDataResult:

            command = self.OpenDSSDataResult[ctd]

            for com in command:
                print(com)
                self.OpenDSSEngine.run(com)

            self.OpenDSSEngine.run("New Line.PIT32J75 Phases=3 Switch=YES Bus1=PTUPIT.1.2.3 Bus2=PIT2.1.2.3 r1=1e-6 r0=1e-6 x1=0.000 x0=0.000 c1=0.000 c0=0.000 Units=km")
            self.OpenDSSEngine.run("New Line.PIT32J65 Phases=3 Switch=YES Bus1=PIT9.1.2.3 Bus2=PTUPIT.1.2.3 r1=1e-6 r0=1e-6 x1=0.000 x0=0.000 c1=0.000 c0=0.000 Units=km")

            self.OpenDSSEngine.run("Solve")
            self.OpenDSSEngine.run("Show Voltages")


        print(self.OpenDSSEngine.AllBusNames())





