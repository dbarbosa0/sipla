from typing import NamedTuple


##Classes de Dados
class dadosTrafoDist(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    pac_3: str
    fas_con_p: str
    fas_con_s: str
    fas_con_t: str
    sit_ativ: str
    tip_unid: str
    ten_lin_se: str
    cap_elo: str
    cap_cha: str
    tap: str
    pot_nom: str
    per_fer: str
    per_tot: str
    ctmt: str
    tip_trafo: str
    uni_tr_s: str
    cod_id_eqtrd: str
    pac_1_eqtrd: str
    pac_2_eqtrd: str
    pac_3_eqtrd: str
    fas_con: str
    pot_nom_eqtrd: str
    lig: str
    ten_pri: str
    ten_sec: str
    ten_ter: str
    lig_fas_p: str
    lig_fas_s: str
    lig_fas_t: str
    per_fer_eqtrd: str
    per_tot_eqtrd: str
    r: str
    xhl: str


class dadosUnidCompReat(NamedTuple):
    cod_id: str
    fas_con: str
    pot_nom: str
    pac_1: str
    ctmt: str


class dadosSegLinhas(NamedTuple):
    cod_id: str
    ctmt: str
    pac_1: str
    pac_2: str
    fas_con: str
    comp: str
    tip_cnd: str
    uni_tr: str


class dadosUNREMT(NamedTuple):
    cod_id: str
    ctmt: str
    pac_1: str
    pac_2: str
    fas_con: str
    sit_ativ: str
    descr: str


class dadosUnidCons(NamedTuple):
    objectid: str
    pac: str
    ctmt: str
    fas_con: str
    ten_forn: str
    sit_ativ: str
    tip_cc: str
    car_inst: str
    ene_01: str
    ene_02: str
    ene_03: str
    ene_04: str
    ene_05: str
    ene_06: str
    ene_07: str
    ene_08: str
    ene_09: str
    ene_10: str
    ene_11: str
    ene_12: str
    uni_tr_s: str
    uni_tr: str


class dadosCondutores(NamedTuple):
    cod_id: str
    r1: str
    x1: str
    cnom: str
    cmax: str


class dadosCTATMT(NamedTuple):
    nome: str
    ten_nom: str
    cod_id: str


class dadosTransformador(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    pot_nom: str
    lig: str
    ten_pri: str
    ten_sec: str
    ten_ter: str


class dadosTransformadorUNTRS(NamedTuple):
    cod_id: str
    pac_1: str
    barr_2: str


class dadosSECAT(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    fas_con: str
    tip_unid: str
    p_n_ope: str
    cap_elo: str
    cor_nom: str
    sit_ativ: str


class dadosSECMT(NamedTuple):
    cod_id: str
    pac_1: str
    pac_2: str
    fas_con: str
    tip_unid: str
    ctmt: str
    uni_tr_s: str
    p_n_ope: str
    cap_elo: str
    cor_nom: str
    sit_ativ: str


class dadosALIMENTADOR(NamedTuple):
    ten_nom: str
    uni_tr_s: str
    nom: str
    cod_id: str


class dadosBDGD:
    def __init__(self):
        self.BDGD_n_layers_Modelo_Versao_1_0 = 43
        self.BDGD_layers_Modelo_Versao_1_0 = {"ARAT": "ARAT",  # Área de atuação
                                              "BAR": "BAR",  # Barramento
                                              "BASE": "BASE",  # Informações de envio da BDGD
                                              "BAY": "BAY",  # Bays de uma subestação
                                              "BE": "BE",  # Balanço de energia
                                              "CONJ": "CONJ",  # Conjunto de unidades consumidoras
                                              "CRVCRG": "CRVCRG",  # Curvas de carga
                                              "CTAT": "CTAT",  # Circuitos de alta tensao
                                              "CTMT": "CTMT",  # Circuitos de alta tensao
                                              "EP": "EP",  # Energia passante
                                              "EQCR": "EQCR",  # Equipamento de compensador de reativo
                                              "EQME": "EQME",  # Equipamento medidor
                                              "EQRE": "EQRE",  # Equipamento regulador
                                              "EQSE": "EQSE",  # Equipamento seccionador
                                              "EQTRAT": "EQTRAT",  # Equipamento transformador de alta tensao
                                              "EQTRM": "EQTRM",  # Equipamento transformador de medicao
                                              "EQTRMT": "EQTRMT",  # Equipamento transformador de media tensao
                                              "PIP": "PIP",  # Ponto de iluminacao publica
                                              "PNT": "PNT",  # Perda nao tecnica
                                              "PONNOT": "PONNOT",  # Ponto notavel
                                              "PT": "PT",  # Perda tecnica
                                              "RAMLIG": "RAMLIG",  # Ramao de ligacao
                                              "SEGCON": "SEGCON",  # Segmento condutor
                                              "SSDAT": "SSDAT",  # Segmento de distribucao de alta tensao
                                              "SSDMT": "SSDMT",  # Segmento de distribucao de media tensao
                                              "SSDBT": "SSDBT",  # Segmento de distribucao de baixa tensao
                                              "SUB": "SUB",  # Subestacao
                                              "UCAT": "UCAT_tab",  # Unidade consumidora de alta tensao
                                              "UCMT": "UCMT_tab",  # Unidade consumidora de media tensao
                                              "UCBT": "UCBT_tab",  # Unidade consumidora de baixa tensao
                                              "UGAT": "UGAT_tab",  # Unidade geradora de alta tensao
                                              "UGMT": "UGMT_tab",  # Unidade geradora de media tensao
                                              "UGBT": "UGBT_tab",  # Unidade geradora de baixa tensao
                                              "UNCRAT": "UNCRAT",  # Unidade compensadora de reativo de alta tensao
                                              "UNCRMT": "UNCRMT",  # Unidade compensadora de reativo de media tensao
                                              "UNCRBT": "UNCRBT",  # Unidade compensadora de reativo de baixa tensao
                                              "UNREAT": "UNREAT",  # Unidade reguladora de alta tensao
                                              "UNREMT": "UNREMT",  # Unidade reguladora de media tensao
                                              "UNSEAT": "UNSEAT",  # Unidade seccionadora de alta tensao
                                              "UNSEMT": "UNSEMT",  # Unidade seccionadora de media tensao
                                              "UNSEBT": "UNSEBT",  # Unidade seccionadora de baixa tensao
                                              "UNTRAT": "UNTRAT",  # Unidade transformadora de media tensao
                                              "UNTRMT": "UNTRMT",  # Unidade transformadora de media tensao
                                              }

        self.BDGD_n_layers_Modelo_Novo = 45
        self.BDGD_layers_Modelo_Novo = {"ARAT": "ARAT",  # Área de atuação
                                        "BAR": "BAR",  # Barramento
                                        "BASE": "BASE",  # Informações de envio da BDGD
                                        "BAY": "BAY",  # Bays de uma subestação
                                        "BE": "BE",  # Balanço de energia
                                        "CONJ": "CONJ",  # Conjunto de unidades consumidoras
                                        "CTAT": "CTAT",  # Circuitos de alta tensao
                                        "CTMT": "CTMT",  # Circuitos de alta tensao
                                        "EP": "EP",  # Energia passante
                                        "EQCR": "EQCR",  # Equipamento de compensador de reativo
                                        "EQME": "EQME",  # Equipamento medidor
                                        "EQRE": "EQRE",  # Equipamento regulador
                                        "EQSE": "EQSE",  # Equipamento seccionador
                                        "EQSIAT": "EQSIAT", # Equipamento do sistema de aterramento (*)
                                        "EQTRAT": "EQTRS",  # Equipamento transformador de alta tensao (*)
                                        "EQTRM": "EQTRM",  # Equipamento transformador de medicao
                                        "EQTRMT": "EQTRD",  # Equipamento transformador de media tensao (*)
                                        "EQTRSX": "EQTRSX",  # Equipamento transformador de serviço auxiliar (*)
                                        "INDGER": "INDGER",  # Indicadores gerenciais (*)
                                        "PIP": "PIP",  # Ponto de iluminacao publica
                                        "PNT": "PNT",  # Perda nao tecnica
                                        "PONNOT": "PONNOT",  # Ponto notavel
                                        "PT": "PT",  # Perda tecnica
                                        "RAMLIG": "RAMLIG",  # Ramao de ligacao
                                        "SEGCON": "SEGCON",  # Segmento condutor
                                        "SSDAT": "SSDAT",  # Segmento de distribucao de alta tensao
                                        "SSDMT": "SSDMT",  # Segmento de distribucao de media tensao
                                        "SSDBT": "SSDBT",  # Segmento de distribucao de baixa tensao
                                        "SUB": "SUB",  # Subestacao
                                        "UCAT": "UCAT_tab",  # Unidade consumidora de alta tensao
                                        "UCMT": "UCMT_tab",  # Unidade consumidora de media tensao
                                        "UCBT": "UCBT_tab",  # Unidade consumidora de baixa tensao
                                        "UGAT": "UGAT_tab",  # Unidade geradora de alta tensao
                                        "UGMT": "UGMT_tab",  # Unidade geradora de media tensao
                                        "UGBT": "UGBT_tab",  # Unidade geradora de baixa tensao
                                        "UNCRAT": "UNCRAT",  # Unidade compensadora de reativo de alta tensao
                                        "UNCRMT": "UNCRMT",  # Unidade compensadora de reativo de media tensao
                                        "UNCRBT": "UNCRBT",  # Unidade compensadora de reativo de baixa tensao
                                        "UNREAT": "UNREAT",  # Unidade reguladora de alta tensao
                                        "UNREMT": "UNREMT",  # Unidade reguladora de media tensao
                                        "UNSEAT": "UNSEAT",  # Unidade seccionadora de alta tensao
                                        "UNSEMT": "UNSEMT",  # Unidade seccionadora de media tensao
                                        "UNSEBT": "UNSEBT",  # Unidade seccionadora de baixa tensao
                                        "UNTRAT": "UNTRS",  # Unidade transformadora de media tensao (*)
                                        "UNTRMT": "UNTRD",  # Unidade transformadora de media tensao (*)
                                        }

        self.BDGD_n_layers_Modelo_Antigo = 35
        self.BDGD_layers_Modelo_Antigo = {}

        self.BDGD_n_layers_SIPLA = 18
        self.BDGD_layers_SIPLA = ["CTAT", "EQTRM", "SSDMT", "UNREMT", "UNTRAT", "CTMT", "EQTRAT", "UCBT", "UNSEAT",
                                  "SSDBT", "RAMLIG", "UCMT", "UNSEMT", "EQTRMT", "SEGCON", "UNCRMT", "UNCRBT", "UNTRMT"]

    def get_layers_uteis_BDGD(self, modelo_BDGD):
        match modelo_BDGD:
            case "Modelo Versao 1.0":
                return [self.BDGD_layers_Modelo_Versao_1_0[layer] for layer in self.BDGD_layers_SIPLA]
            case "Modelo Novo":
                return [self.BDGD_layers_Modelo_Novo[layer] for layer in self.BDGD_layers_SIPLA]
            case "Modelo Antigo":
                pass
            case _:
                pass
