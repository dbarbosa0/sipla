import os
import sqlite3

import glob
import platform



from class_database_conn import C_ConnDBase
from class_exception import ExecDataBaseError

try:
    class C_DBase():
        def __init__(self):


##########################
            
            self.dataBase = C_ConnDBase() #Criando a instância do Banco de Dados

################################# Métodos Novos

        def setBDGD(self):
            if not self.dataBase.setDirDataBase():
                return False
            else:
                return True

        def setDefBDGD(self, nomeDirBataBase):
            if not self.dataBase.setDefDirDataBase(nomeDirBataBase):
                return False
            else:
                return True

        def getBDGD(self):
            return self.dataBase.getDirDataBase()
            
        def getSE_AT_DB(self):
            try:
                lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco=[]
                lista_de_subestacoes_de_alta_tensao_disponivel=[]

                #ct_at = self.dataBase.getSQLDB("CTAT","SELECT * FROM ctat;")
                ct_at = self.dataBase.getSQLDB("CTAT","SELECT nom FROM ctat;")

                for ctat in ct_at.fetchall():
                    #lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco.append(ctat[3])
                    lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco.append(ctat[0])

                lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco_filtradas=(sorted(set(lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco)))

                for lista_sub in lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco_filtradas:
                    lista_de_subestacoes_de_alta_tensao_disponivel.append(lista_sub[0:3])

                lista_de_subestacoes_de_alta_tensao_disponivel_filtrada = (sorted(set(lista_de_subestacoes_de_alta_tensao_disponivel)))

                return lista_de_subestacoes_de_alta_tensao_disponivel_filtrada
            except:
                raise ExecDataBaseError("Erro ao pegar os Circuitos de Alta Tensão!")
        
        
        def getSE_MT_DB(self, nomeSE_AT):
            try:
                lista_de_circuitos_de_alta_para_media=[]

                #ct_at = self.dataBase.getSQLDB("CTAT","SELECT * FROM ctat;")
                ct_at = self.dataBase.getSQLDB("CTAT","SELECT nom FROM ctat;")

                #for ctat in ct_at.fetchall():
                #    if ctat[3][0:3] == nomeSE_AT:
                #        lista_de_circuitos_de_alta_para_media.append(ctat[3])
                for ctat in ct_at.fetchall():
                    if ctat[0][0:3] == nomeSE_AT:
                        lista_de_circuitos_de_alta_para_media.append(ctat[0])

                for elemento in lista_de_circuitos_de_alta_para_media:
                    if elemento[-1] == "2":
                        lista_de_circuitos_de_alta_para_media.remove(elemento)

                lista_de_circuitos_de_alta_para_media_filtradas=(sorted(set(lista_de_circuitos_de_alta_para_media)))

                return lista_de_circuitos_de_alta_para_media_filtradas
            except:
                raise ExecDataBaseError("Erro ao pegar os Circuitos de Média Tensão!")

        def getSE_MT_AL_DB(self, nomeSE_MT): #Pega os nomes dos Alimentadores de uma SE MT
            try:
                lista_de_alimentadores_de_media_tensao_disponiveis=[]

                #ct_mt = self.dataBase.getSQLDB("CTMT","SELECT * FROM ctmt;")
                ct_mt = self.dataBase.getSQLDB("CTMT","SELECT nom, sub FROM ctmt;")
                
                for linha in ct_mt.fetchall():

                    if linha[1] == nomeSE_MT[0]:
                        lista_de_alimentadores_de_media_tensao_disponiveis.append(linha[0])

                    lista_de_alimentadores_de_media_tensao_disponiveis_filtrados=(sorted(set(lista_de_alimentadores_de_media_tensao_disponiveis)))

                return lista_de_alimentadores_de_media_tensao_disponiveis_filtrados
            except:
                raise ExecDataBaseError("Erro ao pegar os Alimentadores de Média Tensão!")
            
        ######################## Visualização 
        
        def getCods_AL_SE_MT_DB(self, listaNomesAL_MT): #Pega os códigos dos alimenatadores de uma SE MT

            try:
                lista_de_identificadores_dos_alimentadores = []

                ct_mt = self.dataBase.getSQLDB("CTMT","SELECT cod_id, nom FROM ctmt;")
                
                for linha in ct_mt.fetchall():   
                    for i in range(0, len(listaNomesAL_MT) ):
                        if linha[1] == listaNomesAL_MT[i]:
                            lista_de_identificadores_dos_alimentadores.append(linha[0])

                lista_de_identificadores_dos_alimentadores_filtrados = (sorted(set(lista_de_identificadores_dos_alimentadores)))

                return lista_de_identificadores_dos_alimentadores_filtrados
            except:
                raise ExecDataBaseError("Erro ao pegar os Códigos dos Alimentadores de Média Tensão!")
        
        def getCoord_AL_SE_MT_DB(self, nomeAL_MT): #Pega as coordenadas de um alimentador de uma SE MT

            try:
                nomeAL_MTS = []
                nomeAL_MTS.append(str(nomeAL_MT))
        
                codAlimentador = self.getCods_AL_SE_MT_DB(nomeAL_MTS)

                lista_de_coordenadas_do_alimentador = []
                                
                #ct_mt = self.dataBase.getSQLDB("CTMT","SELECT * FROM ctmt;")
                
                
                sqlStr = "SELECT ctmt,x,y,vertex_index,objectid FROM ssdmt WHERE ctmt ='" + str(codAlimentador[0]) + "' ORDER BY objectid"
                    
                cod_al = self.dataBase.getSQLDB("SSDMT",sqlStr)
                
                dadosCoord =[]
                dadosCoordInicio = []
                dadosCoordFim = []
                
                for linha in cod_al.fetchall():
                        if linha[3] == 0:
                            dadosCoordInicio = [linha[2], linha[1]]
                        if linha[3] == 1:
                            dadosCoordFim = [linha[2], linha[1]]               
                            
                            dadosCoord = [dadosCoordInicio, dadosCoordFim]
                            
                            lista_de_coordenadas_do_alimentador.append(dadosCoord)

                return lista_de_coordenadas_do_alimentador

            except:
                raise ExecDataBaseError("Erro ao pegar as Coordenadas dos Alimentadores de Média Tensão!")


except AttributeError:
    print("Erro ao abrir banco.")
