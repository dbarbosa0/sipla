import os
import platform
from PyQt5.QtWidgets import QFileDialog
from class_opendss import C_OpenDSS




class C_Dialog_OpenDSS(): # classe OpenDSSDirect

    def __init__(self):

        self.fileOpenDSS = C_OpenDSS() #Acesso ao Banco de Dados

        self.initUI()

    def initUI(self):
        pass

    def setDirDataBase(self, nomeAcessDataBase):
        self.fileOpenDSS.setDirDataBase(nomeAcessDataBase)

    def setCircuitoAT_MT(self, nomeCircuitoAT_MT):
        self.fileOpenDSS.setCircuitoAT_MT(nomeCircuitoAT_MT)

    def setSE_MT_Selecionada(self, nomeSE_MT_Selecionada):
        self.fileOpenDSS.setSE_MT_Selecionada(nomeSE_MT_Selecionada)

    def setFields_SE_MT_Selecionada(self, nomeFields_SE_MT_Selecionada):
        self.fileOpenDSS.setFields_SE_MT_Selecionada(nomeFields_SE_MT_Selecionada)

    def createFile(self):

        self.fileOpenDSS.exec()

        self.MEMO = [
            self.fileOpenDSS.memoFileTrafoATMT , #Transformadores de AT MT
            self.fileOpenDSS.memoFileCondMT , #Condutores de Média Tensão
            self.fileOpenDSS.memoFileCondBT , #Condutores de Baixa Tensão
            self.fileOpenDSS.memoFileCondRamal , #Condutores de Ramal
            self.fileOpenDSS.memoFileSecAT , #Seccionadora de Alta Tensão
            self.fileOpenDSS.memoFileSecAT_Control , # Controle da Secionadora de Alta Tensão
            self.fileOpenDSS.memoFileSecOleoMT ,  # Seccionadora a Óleo de Média Tensão
            self.fileOpenDSS.memoFileSecOleoMT_Control ,  # Controle Seccionadora a Óleo de Média Tensão
            self.fileOpenDSS.memoFileSecFacaMT ,  # Seccionadora Facade Média Tensão
            self.fileOpenDSS.memoFileSecFacaMT_Control ,  # Controle Seccionadora Faca de Média Tensão
            self.fileOpenDSS.memoFileSecFacaTripolarMT ,  # Seccionadora Faca Tripolar de Média Tensão
            self.fileOpenDSS.memoFileSecFacaTripolarMT_Control ,  # Controle Seccionadora Faca Tripolar de Média Tensão
            self.fileOpenDSS.memoFileSecFusivelMT ,  # Seccionadora Fusível Média Tensão
            self.fileOpenDSS.memoFileSecFausivelMT_Control ,  # Controle Seccionadora Fusível de Média Tensão
            self.fileOpenDSS.memoFileSecDJReleMT ,  # Seccionadora DJ Média Tensão
            self.fileOpenDSS.memoFileSecDJReleMT_Control ,  # Controle Seccionadora DJ de Média Tensão
            self.fileOpenDSS.memoFileSecReligadorMT ,  # Seccionadora Religador de  Média Tensão
            self.fileOpenDSS.memoFileSecReligadorMT_Control ,  # Controle Seccionadora Religador de de Média Tensão
            self.fileOpenDSS.memoFileSecTripolarSEMT ,  # Seccionadora Tripolar SE de  Média Tensão
            self.fileOpenDSS.memoFileSecTripolarSEMT_Control ,  # Controle Seccionadora Tripolar SE de Média Tensão
            self.fileOpenDSS.memoFileSecUnipolarSEMT ,  # Seccionadora Unipolar SE de  Média Tensão
            self.fileOpenDSS.memoFileSecUnipolarSEMT_Control ,  # Controle Seccionadora Unipolar SE de Média Tensão
            self.fileOpenDSS.memoFileReguladorMT ,  # Regulador de  Média Tensão
            self.fileOpenDSS.memoFileSegLinhasMT ,  # Segmentos de Linhas de  Média Tensão
            self.fileOpenDSS.memoFileUniConsumidoraMT ,  # Unidade Consumidora de Média Tensão
            self.fileOpenDSS.memoFileTrafoDist ,  #Transformadores de Distribuição
            self.fileOpenDSS.memoFileSegLinhasBT ,  # Segmentos de Linhas de Baixa Tensão
            self.fileOpenDSS.memoFileUniConsumidoraBT ,  # Unidade Consumidora de Baixa Tensão
            self.fileOpenDSS.memoFileRamaisLigBT , # Ramais de Ligação
            self.fileOpenDSS.memoFileUndCompReatMT , #Unidade de Compensação de Reativo de Baixa Tensão
            self.fileOpenDSS.memoFileUndCompReatBT , #Unidade de Compensação de Reativo de Baixa Tensão
        ]

        self.nomeMEMO = [
            "memoFileTrafoATMT" ,#Transformadores de AT MT
            "memoFileCondMT" ,#Condutores de Média Tensão
            "memoFileCondBT" ,#Condutores de Baixa Tensão
            "memoFileCondRamal" ,#Condutores de Ramal
            "memoFileSecAT" ,#Seccionadora de Alta Tensão
            "memoFileSecAT_Control" ,# Controle da Secionadora de Alta Tensão
            "memoFileSecOleoMT" , # Seccionadora a Óleo de Média Tensão
            "memoFileSecOleoMT_Control" , # Controle Seccionadora a Óleo de Média Tensão
            "memoFileSecFacaMT" , # Seccionadora Facade Média Tensão
            "memoFileSecFacaMT_Control" , # Controle Seccionadora Faca de Média Tensão
            "memoFileSecFacaTripolarMT" , # Seccionadora Faca Tripolar de Média Tensão
            "memoFileSecFacaTripolarMT_Control" , # Controle Seccionadora Faca Tripolar de Média Tensão
            "memoFileSecFusivelMT" , # Seccionadora Fusível Média Tensão
            "memoFileSecFausivelMT_Control" , # Controle Seccionadora Fusível de Média Tensão
            "memoFileSecDJReleMT" , # Seccionadora DJ Média Tensão
            "memoFileSecDJReleMT_Control" , # Controle Seccionadora DJ de Média Tensão
            "memoFileSecReligadorMT" , # Seccionadora Religador de  Média Tensão
            "memoFileSecReligadorMT_Control" , # Controle Seccionadora Religador de de Média Tensão
            "memoFileSecTripolarSEMT" , # Seccionadora Tripolar SE de  Média Tensão
            "memoFileSecTripolarSEMT_Control" , # Controle Seccionadora Tripolar SE de Média Tensão
            "memoFileSecUnipolarSEMT" , # Seccionadora Unipolar SE de  Média Tensão
            "memoFileSecUnipolarSEMT_Control" , # Controle Seccionadora Unipolar SE de Média Tensão
            "memoFileReguladorMT" , # Regulador de  Média Tensão
            "memoFileSegLinhasMT" , # Segmentos de Linhas de  Média Tensão
            "memoFileUniConsumidoraMT" , # Unidade Consumidora de Média Tensão
            "memoFileTrafoDist" , #Transformadores de Distribuição
            "memoFileSegLinhasBT" , # Segmentos de Linhas de Baixa Tensão
            "memoFileUniConsumidoraBT" , # Unidade Consumidora de Baixa Tensão
            "memoFileRamaisLigBT" ,# Ramais de Ligação
            "memoFileUndCompReatMT" ,#Unidade de Compensação de Reativo de Baixa Tensão
            "memoFileUndCompReatBT" ,#Unidade de Compensação de Reativo de Baixa Tensão
        ]

        self.arquivoPrincipal = self.createMainFile(self.nomeMEMO)


        

    def exec_CRIAR_ARQUIVO_NO_FORMATO_OPENDSS(self):

        
        arquivoSalvo = QFileDialog.getSaveFileName(None, "Save OpenDSS File", "Resultados/",
                                                            "DSS Files (*.dss)")[0]

        nome_do_arquivo_criado = os.path.basename(str(arquivoSalvo))

        diretorio = os.path.dirname(str(arquivoSalvo)) +  "/"

        if platform.system() == "Windows":
            diretorio = diretorio.replace('/', '\\')

        self.saveFileDSS(diretorio, nome_do_arquivo_criado, self.arquivoPrincipal)

        for ctd in range(0, len(self.nomeMEMO)):
            self.saveFileDSS(diretorio, self.nomeMEMO[ctd], self.MEMO[ctd] )




    def saveFileDSS(self, dirSave, nameMemo, dataMemo ):
        arquivo = open(dirSave +  nameMemo + ".dss", 'w', encoding='utf-8')
        arquivo.writelines( dataMemo )
        arquivo.close()

    def createMainFile(self, memo):

        mainFile = ''
        mainFile += self.fileOpenDSS.memoFileHeader  + "\n" # Cabeçalho do arquivo
        mainFile += self.fileOpenDSS.memoFileEqTh + "\n"  # Arquivo Thevenin
        mainFile += self.fileOpenDSS.memoFileEqThMT +"\n"   # Arquivo Thevenin Média

        for ctd in range(0, len(memo)):
            mainFile += '\n'+"Redirect " + memo[ctd] + ".dss "+'\n'


        mainFile += self.fileOpenDSS.memoFileFooter + "\n"   # Rodapé do arquivo

        return mainFile

