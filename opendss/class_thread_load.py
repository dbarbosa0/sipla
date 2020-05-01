import database.class_conn
import opendss.class_data
import time
import threading


class C_LoadDataThread(threading.Thread):
    def __init__(self, threadID, queue, queueLock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = queue
        self.queueLock = queueLock

        self.dataOpenDSS = opendss.class_data.C_Data() #Acesso ao Banco de Dados
        self.DataBaseConn = database.class_conn.C_DBaseConn()  # Criando a instância do Banco de Dados
        self.nCircuitoAT_MT = ''
        self.nSE_MT_Selecionada = ''
        self.nFieldsMT = ''
        self.exitFlag = 0
        self.OpenDSSConfig={}

        self.dataOpenDSS.DataBaseConn = self.DataBaseConn
        self.dataOpenDSS.nFieldsMT = self.nFieldsMT
        self.dataOpenDSS.nCircuitoAT_MT = self.nCircuitoAT_MT
        self.dataOpenDSS.nSE_MT_Selecionada = self.nSE_MT_Selecionada

    def run(self):
        while not self.exitFlag:
            self.queueLock.acquire()
            if not self.queue.empty():
                funcData = self.queue.get()
                self.queueLock.release()
                funcData() #Executando a função
                print(str(self.threadID) + " processing " + str(funcData))
            else:
                self.queueLock.release()
            time.sleep(1)
