import os
import platform


import class_database_conn
import class_exception 

class C_DBase():
    def __init__(self):

##########################

        self.DataBaseConn = class_database_conn.C_DBaseConn() #Criando a instância do Banco de Dados

################################# Métodos Novos

    def getSE_AT_DB(self):
        try:
            lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco=[]
            lista_de_subestacoes_de_alta_tensao_disponivel=[]

            #ct_at = self.DataBaseConn.getSQLDB("CTAT","SELECT * FROM ctat;")
            ct_at = self.DataBaseConn.getSQLDB("CTAT","SELECT nom FROM ctat;")

            for ctat in ct_at.fetchall():
                #lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco.append(ctat[3])
                lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco.append(ctat[0])

            lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco_filtradas=(sorted(set(lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco)))

            for lista_sub in lista_de_subestacoes_de_alta_tensao_disponivel_formato_proprio_do_banco_filtradas:
                lista_de_subestacoes_de_alta_tensao_disponivel.append(lista_sub[0:3])

            lista_de_subestacoes_de_alta_tensao_disponivel_filtrada = (sorted(set(lista_de_subestacoes_de_alta_tensao_disponivel)))

            return lista_de_subestacoes_de_alta_tensao_disponivel_filtrada
        except:
            raise class_exception.ExecDataBaseError("Erro ao pegar os Circuitos de Alta Tensão!")


    def getCirAT_MT_DB(self, nomeSE_AT):
        try:
            lista_de_circuitos_de_alta_para_media=[]

            #ct_at = self.DataBaseConn.getSQLDB("CTAT","SELECT * FROM ctat;")
            ct_at = self.DataBaseConn.getSQLDB("CTAT","SELECT nom FROM ctat;")

            for ctat in ct_at.fetchall():
                if ctat[0][0:3] == nomeSE_AT:
                    lista_de_circuitos_de_alta_para_media.append(ctat[0])

            for elemento in lista_de_circuitos_de_alta_para_media:
                if elemento[-1] == "2":
                    lista_de_circuitos_de_alta_para_media.remove(elemento)

            lista_de_circuitos_de_alta_para_media_filtradas=(sorted(set(lista_de_circuitos_de_alta_para_media)))

            return lista_de_circuitos_de_alta_para_media_filtradas
        except:
            raise class_exception.ExecDataBaseError("Erro ao pegar os Circuitos de Média Tensão!")


    def getSE_MT_AL_DB(self, nomeSE_MT): #Pega os nomes dos Alimentadores de uma SE MT
        try:
            lista_de_alimentadores_de_media_tensao_disponiveis=[]

            #ct_mt = self.DataBaseConn.getSQLDB("CTMT","SELECT * FROM ctmt;")
            ct_mt = self.DataBaseConn.getSQLDB("CTMT","SELECT nom, sub FROM ctmt;")

            for linha in ct_mt.fetchall():

                if linha[1] == nomeSE_MT[0]:
                    lista_de_alimentadores_de_media_tensao_disponiveis.append(linha[0])

                lista_de_alimentadores_de_media_tensao_disponiveis_filtrados=(sorted(set(lista_de_alimentadores_de_media_tensao_disponiveis)))

            return lista_de_alimentadores_de_media_tensao_disponiveis_filtrados
        except:
            raise class_exception.ExecDataBaseError("Erro ao pegar os Alimentadores de Média Tensão!")

