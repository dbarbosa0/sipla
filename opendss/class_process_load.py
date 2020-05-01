import database.class_conn
import opendss.class_data
import time
import multiprocessing
import queue

class C_LoadDataProcess(multiprocessing.Process):
    def __init__(self, ProcessID, queue, queueLock):
        multiprocessing.Process.__init__(self)
        self.ProcessID = ProcessID
        self.queue = queue
        self.queueLock = queueLock
        self.dataOpenDSS = '' #Acesso ao Banco de Dados
        self.OpenDSSConfig={}

        print("Process: " + str(self.ProcessID))

    def run(self):
        while True:
            try:
                self.queueLock.acquire()
                print("Process: " + str(self.ProcessID) + " While")
                funcData = self.queue.get_nowait()
            except queue.Empty:
                print("Process: " + str(self.ProcessID) + " Error")
                break
            else:
                print("Process: " + str(self.ProcessID) + " Queue")
                print(str(self.ProcessID) + " start " + str(funcData))
                funcData() #Executando a função
                self.queueLock.release()
                print(str(self.ProcessID) + " finished " + str(funcData))
        return True
