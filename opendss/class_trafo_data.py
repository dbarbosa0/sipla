from math import sqrt

class trafo_data:
    def __init__(self):
        self.ajusteTrafos = {}
        self.identificadorTrafo = []
        self.ajuste_memoria = []
        self.identificadorTrafo = {}
        self.trafo_ten_sec = {}
        self.fas_con_Trafo = []
        self.ten_sec_eqtrs = {}

    def ajuste_tensao_trafos(self, dados_db):
        for ctd in range(0, len(dados_db)):

            if len(dados_db[ctd].fas_con_s) == 2:
                if dados_db[ctd].ten_lin_se in [0.23, 0.254]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.127)

                elif dados_db[ctd].ten_lin_se in [0.38, 0.44]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.22)

                self.ajusteTrafos[dados_db[ctd].cod_id] = {
                    "1": [dados_db[ctd].ten_lin_se]}  # TALVEZ TENHA SITUAÇÕES QUE SERÃO MONO/ ERRROS

            elif len(dados_db[ctd].fas_con_s) == 3:
                print('Debug 8')
                if dados_db[ctd].ten_lin_se in [0.0, 0.127]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.127)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.254]})

                elif dados_db[ctd].ten_lin_se in [0.22, 0.23, 0.38]:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.22)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.22]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.44]})

                elif dados_db[ctd].ten_lin_se == 0.254:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.127)
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.254]})

                else:
                    dados_db[ctd] = dados_db[ctd]._replace(ten_lin_se=0.22)
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

                elif dados_db[ctd].ten_lin_se == 0.22:
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.127]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.22]})
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"3": [0.22]})
                else:
                    self.ajusteTrafos[dados_db[ctd].cod_id] = {"1": [0.22]}
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"2": [0.38]})
                    self.ajusteTrafos[dados_db[ctd].cod_id].update({"3": [0.38]})

    def ajuste_tensao_cargas(self, dados_db):
        print("CHAVES", self.ajusteTrafos.keys())
        for ctd in range(0, len(dados_db)):
            if dados_db[ctd].uni_tr in self.ajusteTrafos.keys():

                print(f'Debug9:{self.ajusteTrafos[dados_db[ctd].uni_tr]}')
                try:
                    dados_db[ctd] = dados_db[ctd]._replace(
                        ten_forn=self.ajusteTrafos[dados_db[ctd].uni_tr][str(len(dados_db[ctd].fas_con) - 1)][0])
                except KeyError:
                    # Tensões de linha implementada apenas em caso de erros na BDGD no registro do número de fases do
                    # transformador (ex: um transformador AN alimentando uma carga ABC)
                    dados_db[ctd] = dados_db[ctd]._replace(
                        ten_forn=self.ajusteTrafos[dados_db[ctd].uni_tr]['1'][0] * sqrt(3))

    def ajuste_tensao_cargas_MT(self, dados_trafo):
        for ctd in range(0, len(dados_trafo)):
            self.ten_sec_eqtrs[dados_trafo[ctd].pac_1] = dados_trafo[ctd].ten_sec

    #def ajuste_tensao_UNTRS(self, dados_trafo):
        #self.dados_UNTRS = dados_trafo
    """"
    def ajuste_media_tensao(self, dados_db, flag):
        for ctd in range(0, len(dados_db)):
            for ctd_2 in range(0, len(self.dados_UNTRS)):
                if dados_db[ctd].uni_tr_s == self.dados_UNTRS[ctd_2].cod_id:
                    if flag == 'alta_trafo_dist':
                        dados_db[ctd] = dados_db[ctd]._replace(
                            ten_pri=self.tensao_media(self.ten_sec_eqtrs[self.dados_UNTRS[ctd_2].pac_1],
                                                      len(dados_db[ctd].fas_con_p)))
                    else:
                        dados_db[ctd] = dados_db[ctd]._replace(
                            ten_forn=self.tensao_media(self.ten_sec_eqtrs[self.dados_UNTRS[ctd_2].pac_1],
                                                       len(dados_db[ctd].fas_con) - 1))
    """
    def tensao_media(self, tensao_mt, fas_con_p):

        if tensao_mt == '42':
            if fas_con_p == 1:
                return str(6.87)
            else:
                return str(11.9)

        elif tensao_mt == '49':
            if fas_con_p == 1:
                return str(7.96)
            else:
                return str(13.8)

        else:  # 72 -> 34.5 kv
            if fas_con_p == 1:
                return str(19.919)
            else:
                return str(34.5)

    def ajuste_media_tensao(self, dados_db, flag, media_tensao_do_circuito):
        for ctd in range(0, len(dados_db)):
            for ctd_2 in range(0, len(media_tensao_do_circuito)):
                if dados_db[ctd].uni_tr_s == media_tensao_do_circuito[ctd_2].uni_tr_s:
                    if flag == 'alta_trafo_dist':
                        dados_db[ctd] = dados_db[ctd]._replace(
                            ten_pri=self.tensao_media(media_tensao_do_circuito[ctd_2].ten_nom,
                                                      len(dados_db[ctd].fas_con_p)))
                    else:
                        dados_db[ctd] = dados_db[ctd]._replace(
                            ten_forn=self.tensao_media(media_tensao_do_circuito[ctd_2].ten_nom,
                                                       len(dados_db[ctd].fas_con) - 1))
