import collections


class trafo_data():
    def __init__(self):
        self.ajusteTrafos = {}
        self.identificadorTrafo = []
        self.ajuste_memoria = []
        self.identificadorTrafo = {}
        self.trafo_ten_sec = {}
        self.fas_con_Trafo = []
        self.ten_sec_eqtrs = []

    def tratamento_dados_TrafosDist(self, tipoUniCons, dados_db,
                                    lista_de_identificadores_dos_alimentadores,
                                    identificadorTrafo):  # ESSA lista de identificadores tem que ser otimizada.

        if tipoUniCons == 'BT':
            self.ajusteTrafos.clear()
            self.ajuste_memoria.clear()
            self.identificadorTrafo = identificadorTrafo
            UniCons_filter = self.identificadorTrafo.keys()

            for ctd in range(0, len(dados_db)):
                if dados_db[ctd].uni_tr not in self.ajusteTrafos.keys():
                    self.ajusteTrafos[dados_db[ctd].uni_tr] = {"1": []}
                    self.ajusteTrafos[dados_db[ctd].uni_tr].update({"2": []})
                    self.ajusteTrafos[dados_db[ctd].uni_tr].update({"3": []})
                    self.ajusteTrafos[dados_db[ctd].uni_tr].update({"sum": []})
                    self.ajusteTrafos[dados_db[ctd].uni_tr].update(
                        {"fas_con": self.identificadorTrafo[dados_db[ctd].uni_tr][1]})

                if len(dados_db[ctd].fas_con) == 2:
                    self.ajusteTrafos[dados_db[ctd].uni_tr]["1"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].uni_tr + '1')

                elif len(dados_db[ctd].fas_con) == 3:
                    self.ajusteTrafos[dados_db[ctd].uni_tr]["2"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].uni_tr + '2')

                elif len(dados_db[ctd].fas_con) == 4:
                    self.ajusteTrafos[dados_db[ctd].uni_tr]["3"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].uni_tr + '3')
            print(self.ajusteTrafos)
        else:
            UniCons_filter = lista_de_identificadores_dos_alimentadores
            for ctd in range(0, len(dados_db)):
                if dados_db[ctd].ctmt not in self.ajusteTrafos.keys():
                    self.ajusteTrafos[dados_db[ctd].ctmt] = {"1": []}
                    self.ajusteTrafos[dados_db[ctd].ctmt].update({"2": []})
                    self.ajusteTrafos[dados_db[ctd].ctmt].update({"3": []})
                    self.ajusteTrafos[dados_db[ctd].ctmt].update({"sum": []})

                if len(dados_db[ctd].fas_con) == 2:
                    self.ajusteTrafos[dados_db[ctd].ctmt]["1"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].ctmt + '1')

                elif len(dados_db[ctd].fas_con) == 3:
                    self.ajusteTrafos[dados_db[ctd].ctmt]["2"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].ctmt + '2')

                elif len(dados_db[ctd].fas_con) == 4:
                    self.ajusteTrafos[dados_db[ctd].ctmt]["3"].append(dados_db[ctd].ten_forn)
                    self.ajuste_memoria.append(dados_db[ctd].ctmt + '3')

        for ctd in UniCons_filter:
            if ctd in self.ajusteTrafos.keys():
                for ctd_2 in range(1, 4):
                    if self.ajusteTrafos[ctd][str(ctd_2)]:
                        if self.ajusteTrafos[ctd]['sum']:
                            self.ajusteTrafos[ctd]['sum'][0] += (len(self.ajusteTrafos[ctd][str(ctd_2)]))
                        else:
                            self.ajusteTrafos[ctd]['sum'].append((len(self.ajusteTrafos[ctd][str(ctd_2)])))
                        if tipoUniCons == 'BT':
                            self.filtro_fas_con_trafo(ctd, ctd_2)
                        # c = (collections.Counter(self.ajusteTrafos[ctd][str(ctd_2)])).most_common(1)       #substituir esse c por  --  self.ajusteTrafos[ctd][str(ctd_2)]
                        self.ajusteTrafos[ctd][str(ctd_2)] = max(set(self.ajusteTrafos[ctd][str(ctd_2)]),
                                                                 key=self.ajusteTrafos[ctd][
                                                                     str(ctd_2)].count)
                        # print(self.ajusteTrafos[ctd][str(ctd_2)], '--', c[0][0])
                        # if c[0][0] != self.ajusteTrafos[ctd][str(ctd_2)]:
                        # print('diferente', ctd)

                        for contador in range(0, len(self.ajuste_memoria)):
                            ctmt_lenght = len(ctd)
                            if self.ajuste_memoria[contador][0:ctmt_lenght] == ctd and self.ajuste_memoria[contador][
                                ctmt_lenght] == str(
                                ctd_2):
                                self.ajuste_memoria[contador] = self.ajusteTrafos[ctd][
                                    str(ctd_2)]  # quando substituir o c isso aqui vai virar  --  self.ajusteTrafos[ctd][str(ctd_2)][0][0]
                                # self.ajusteTrafos[ctd][str(ctd_2)] = self.ajuste_memoria[count]

                                # NÃO AGRUPEI NEM CALCULEI A PORCENTAGEM.

        # print(len(self.ajuste_memoria))
        # print(len(self.ajusteTrafos))
        # print((self.ajuste_memoria))
        # print((self.ajusteTrafos))

    def get_trafo_sec(self,
                      trafo_ten_sec):  # aqui vai pegar a tensão do secundario no banco de dados pra fazer a decisão caso o a média não seja maior que x%
        self.trafo_ten_sec = trafo_ten_sec
        print(self.trafo_ten_sec)
        print(len(self.trafo_ten_sec))

    def filtro_fas_con_trafo(self, ctd, ctd_2):

        if len(self.ajusteTrafos[ctd]["fas_con"]) == 2:
            c = (collections.Counter(self.ajusteTrafos[ctd][str(ctd_2)])).most_common(2)
            for algumacoisa in range(0, len(c)):
                if c[algumacoisa][0] == '6':
                    print("TENSAO 6 tri")
                elif c[algumacoisa][0] == '10':
                    print("TENSAO 10 tri mono")
                elif c[algumacoisa][0] == '14':
                    print("tensao 14 tri")
                elif c[algumacoisa][0] == '15':
                    print("TENSAO 15 tri")
                elif c[algumacoisa][0] == '17':
                    print("tensao 17 tri")
                else:
                    pass

        if len(self.ajusteTrafos[ctd]["fas_con"]) == 3:
            print(ctd)
            c = (collections.Counter(self.ajusteTrafos[ctd][str(ctd_2)])).most_common(2)
            if ctd_2 == 1:
                for algumacoisa in range(0, len(c)):
                    if c[algumacoisa][0] == '6':
                        print("TENSAO 6")
                    elif c[algumacoisa][0] == '10':
                        print("tensao 10")
                    else:
                        pass
            else:
                for algumacoisa in range(0, len(c)):
                    for tensao in c[algumacoisa][0]:
                        if tensao == '14':
                            print("TENSAO 14 bi")
                        elif tensao == '17':
                            print("tensao 17 bi")
                        else:
                            pass

        if len(self.ajusteTrafos[ctd]["fas_con"]) == 4:
            print(ctd)
            c = (collections.Counter(self.ajusteTrafos[ctd][str(ctd_2)])).most_common(3)
            if ctd_2 == 1:
                for algumacoisa in range(0, len(c)):
                    if c[algumacoisa][0] == '6':
                        print("TENSAO 6 tri")
                    elif c[algumacoisa][0] == '10':
                        print("TENSAO 10 tri mono")
                    elif c[algumacoisa][0] == '14':
                        print("tensao 14 tri")
                    else:
                        pass
            else:
                for algumacoisa in range(0, len(c)):
                    if c[algumacoisa][0] == '10':
                        print("TENSAO 10 tri")
                    elif c[algumacoisa][0] == '15':
                        print("TENSAO 15 tri")
                    elif c[algumacoisa][0] == '17':
                        print("tensao 17 tri")
                    else:
                        pass

    def ajuste_tensao_trafos(self,
                             dados_db):  # TERMINAR DICIONARIOS PARA PODER AJUSTAR OS VALORES DAS UNIDADES CONSUMIDORAS
        for ctd in range(0, len(dados_db)):
            if len(dados_db[ctd].fas_con_s) == 2:
                if dados_db[ctd].ten_lin_se in [0.23, 0.254]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.127)

                elif dados_db[ctd].ten_lin_se in [0.38, 0.44]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.22)
                self.ajusteTrafos[dados_db[ctd].cod_id] = {
                    "1": [dados_db[ctd].ten_lin_se]}  # TALVEZ TENHA SITUAÇÕES QUE SERÃO MONO/ ERRROS

            elif len(dados_db[ctd].fas_con_s) == 3:
                if dados_db[ctd].ten_lin_se in [0.0, 0.127]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.254)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.254]})

                elif dados_db[ctd].ten_lin_se in [0.22, 0.23, 0.38]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.44)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.22]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.44]})

                else:
                    if dados_db[ctd].ten_lin_se == 0.254:
                        self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                        self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.254]})

                    else:
                        self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.22]}
                        self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.44]})

            else:
                if dados_db[ctd].ten_lin_se in [0.127, 0.254]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.22)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.22]})
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"3": [0.22]})

                elif dados_db[ctd].ten_lin_se == 0.44:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.38)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.22]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.38]})
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"3": [0.38]})

                else:
                    if dados_db[ctd].ten_lin_se == 0.22:
                        self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                        self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.22]})
                        self.ajusteTrafos[dados_db[ctd].cod_id].update({"3": [0.22]})
                    else:
                        self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.22]}
                        self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.38]})
                        self.ajusteTrafos[dados_db[ctd].cod_id].update({"3": [0.38]})
        #print('PRINT AJUSTETRAFO', self.ajusteTrafos)

    def ajuste_tensao_cargas(self, dados_db):
        for ctd in range(0, len(dados_db)):
            #print(dados_db[ctd].uni_tr, self.ajusteTrafos[dados_db[ctd].uni_tr][str(len(dados_db[ctd].fas_con)-1)][0])
            dados_db[ctd] = dados_db[ctd]._replace(
                ten_forn=self.ajusteTrafos[dados_db[ctd].uni_tr][str(len(dados_db[ctd].fas_con)-1)][0])

    def ajuste_tensao_cargas_MT(self, dados_trafo):
        for ctd in range(0, len(dados_trafo)):
            self.ten_sec_eqtrs = dados_trafo[ctd].ten_sec
            print('ajute_trafo_MT', self.ten_sec_eqtrs)


    def ajuste_MT(self, dados_db):
        for ctd in range(0, len(dados_db)):
            if self.ten_sec_eqtrs == '49':
                if len(dados_db[ctd].fas_con) == 2:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_forn=str(7.96))
                else:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_forn=str(13.8))
            else:
                if len(dados_db[ctd].fas_con) == 2:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_forn=str(19.919))
                else:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_forn=str(34.5))
