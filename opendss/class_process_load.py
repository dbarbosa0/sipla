import database.class_conn
import opendss.class_data
import time
import multiprocessing
import queue

class C_LoadDataProcess(multiprocessing.Process):
    def __init__(self, ProcessID, queue, dataOpenDSS):
        multiprocessing.Process.__init__(self)
        self.ProcessID = ProcessID
        self.queue = queue

        self.dataOpenDSS = dataOpenDSS #Acesso ao Banco de Dados
        self.nCircuitoAT_MT = ''
        self.nSE_MT_Selecionada = ''
        self.nFieldsMT = ''
        self.OpenDSSConfig={}

        #print("Process: " + str(self.ProcessID))

    def run(self):
        while True:
            try:
                print("Process: " + str(self.ProcessID) + " While")
                funcData = self.queue.get()
            except queue.Empty:
                print("Process: " + str(self.ProcessID) + " Error")
                break
            else:
                print("Process: " + str(self.ProcessID) + " Queue")
                funcData = self.queue.get()
                print(str(self.ProcessID) + " processing a" + str(funcData))
                funcData() #Executando a função
                print(str(self.ProcessID) + " processing d" + str(funcData))
        return True
