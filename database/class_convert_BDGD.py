from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, \
    QGridLayout, QWidget, QProgressBar, QApplication
from PyQt5.QtCore import Qt
import sqlite3
from timeit import default_timer as timer
import sys
import config as cfg
import class_exception
import os
import fiona
import database.class_data as class_data
import copy
import database.class_config_dialog as class_config_dialog
import threading
import concurrent.futures
import multiprocessing
import platform


class ConnectorWindowAndConverterBDGD(class_data.dadosBDGD):

    def __init__(self, config_dialog):
        super().__init__()

        # Dados gerais BDGD
        self._DataBaseInfo = {}
        self.path_BDGD_sqlite = ""
        self.config_dialog = config_dialog

    @property
    def DataBaseInfo(self):
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo
        self.path_BDGD_geodb = self.DataBaseInfo["Geodb_DirDataBase"]

        # Layer variables
        self.layers_BDGD = self.get_layers_uteis_BDGD(self.DataBaseInfo["Modelo"])
        self.n_layers_BDGD = len(self.layers_BDGD)
        self.layers_acaoes = ['...'] + ["Convertendo a layer: " + nome_da_layer + " (0/?)"
                                        for nome_da_layer in self.layers_BDGD]

    def initUI(self):
        self.window = WindowConversionStatus(self, self.n_layers_BDGD)
        self.window.show()

    def iniciar_conversao(self):
        inicio = timer()

        self.conversor = Converter_BDGD(self, self.path_BDGD_geodb)
        self.path_BDGD_sqlite, self.BDGD_sqlite_already_exists = self.conversor.criacao_novo_diretorio()

        if not self.BDGD_sqlite_already_exists:
            self.conversao()

        tempo_decorrido = timer() - inicio
        print(f'Tempo demandado em segundos: {tempo_decorrido}')


        self.config_dialog.GroupBox_BDGD_Edit.setText(self.path_BDGD_sqlite)
        self.config_dialog.loadParameters()
        self.config_dialog.close()
        self.window.close()

    def conversao(self):
        if platform.system() == 'Linux':
            self.conversao_multiprocessing_manual()
        elif platform.system() == 'Windows':
            self.conversao_padrao()
        elif platform.system() == 'Darwin':
            pass

    def conversao_padrao(self):
        for index, nome_layer in enumerate(self.layers_BDGD, start=1):
            self.window.atualizar_indicador_acao(nome_layer)
            self.conversor.convert_geodatabase_to_sqlite(nome_layer)
            self.window.atualizar_barra_progresso(index)

    def conversao_threading(self):
        with concurrent.futures.thread.ThreadPoolExecutor(max_workers=len(self.layers_BDGD)) as executor:
            executor.map(self.conversor.convert_geodatabase_to_sqlite, self.layers_BDGD)

    def conversao_multiprocessing(self):
        with multiprocessing.Pool() as pool:
            pool.map(self.conversor.convert_geodatabase_to_sqlite, self.layers_BDGD)

    def conversao_process(self):
        with concurrent.futures.ProcessPoolExecutor as executor:
            executor.map(self.conversor.convert_geodatabase_to_sqlite, self.layers_BDGD)

    def conversao_threading_manual(self):
        nCore = multiprocessing.cpu_count()
        threads = []
        for layer in self.layers_BDGD:

            thr = threading.Thread(target=self.conversor.convert_geodatabase_to_sqlite, args=(layer,))

            threads.append(thr)

            thr.start()

            print("Iniciado conversao [", layer, "]: ")

        for idxThr, thread in enumerate(threads):
            thread.join()

            print("Layer Finalizado: [", idxThr, "]")

    def conversao_multiprocessing_manual(self):
        nCore = multiprocessing.cpu_count()
        process = []
        for layer in self.layers_BDGD:

            pro = multiprocessing.Process(target=self.conversor.convert_geodatabase_to_sqlite, args=(layer,))

            process.append(pro)

            pro.start()

            print("Iniciado conversao [", layer, "]: ")

        for idxThr, pro in enumerate(process):
            pro.join()

            print("Layer Finalizado: [", idxThr, "]")

    def cancelar_conversao(self):
        self.window.close()


class WindowConversionStatus(QWidget):

    def __init__(self, connector_window_converter: ConnectorWindowAndConverterBDGD, n_layers):
        super().__init__()
        self.connector = connector_window_converter

        # Dados gerais BDGD
        self._DataBaseInfo = {}

        # Construção da janela
        self.titleWindow = "Preparação do Banco de Dados..."
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()

        # Definição dos Layouts da janela
        self.Layout_principal = QVBoxLayout()

        self.GroupBox_status_conversao = QGroupBox("Status da configuração inicial da BDGD:")
        self.GroupBox_status_conversao_Layout = QGridLayout()
        self.GroupBox_aviso_usuario = QGroupBox("Observação ao usuário:")
        self.GroupBox_aviso_usuario_Layout = QHBoxLayout()

        # Construção da barra de progresso
        self.bar_progress = QProgressBar()
        self.bar_progress_total_steps = n_layers
        self.bar_progress.setMinimumWidth(550)
        self.bar_progress.setMinimumHeight(25)
        self.bar_progress.setFormat(f"    %v / {self.bar_progress_total_steps} passos concluídos (%p%)")
        self.bar_progress.setMaximum(self.bar_progress_total_steps)
        self.bar_progress.setValue(0)

        # Construção do indicador da ação atual
        self.acao_atual = QLabel("Estado atual: ...")
        self.acao_atual.setStyleSheet("border: 2px solid green;"
                                      "border-radius: 4px;"
                                      "padding: 2px;")

        # Construção do botão de iniciar a conversão
        self.botao_iniciar = QPushButton("Iniciar a conversão")
        self.botao_iniciar.setIcon(QIcon('img/icon_save.png'))
        self.botao_iniciar.clicked.connect(self.iniciar_conv)

        # Construção do botão de interrupção da conversão
        self.botao_cancelar = QPushButton("Cancelar a conversão")
        self.botao_cancelar.setIcon(QIcon('img/icon_cancel.png'))
        self.botao_cancelar.clicked.connect(self.cancelar_conv)

        # Contrução do aviso ao usuário
        self.aviso = QLabel("Antes do primeiro uso de uma BDGD no ambiente do SIPLA, é necessário renomear, configurar "
                            "e converter as layers do padrão\nem geodatabase adotado pelas distribuidoras, a fim de "
                            "possibilitar a execução de queries em SQL pelo programa. Tal processo\npode levar alguns "
                            "minutos.")

        # Construção de um espaço em branco
        self.espaco_vazio = QLabel()

        # Disposição dos widgets nos layouts da janela
        self.GroupBox_status_conversao_Layout.addWidget(self.espaco_vazio, 0, 0)
        self.GroupBox_status_conversao_Layout.addWidget(self.bar_progress, 1, 0)
        self.GroupBox_status_conversao_Layout.addWidget(self.espaco_vazio, 2, 0)
        self.GroupBox_status_conversao_Layout.addWidget(self.botao_iniciar, 1, 1)
        self.GroupBox_status_conversao_Layout.addWidget(self.botao_cancelar, 3, 1)
        self.GroupBox_status_conversao_Layout.addWidget(self.acao_atual, 3, 0)

        self.GroupBox_status_conversao.setLayout(self.GroupBox_status_conversao_Layout)

        self.GroupBox_aviso_usuario_Layout.addWidget(self.aviso)

        self.GroupBox_aviso_usuario.setLayout(self.GroupBox_aviso_usuario_Layout)

        self.Layout_principal.addWidget(self.GroupBox_status_conversao)
        self.Layout_principal.addWidget(self.GroupBox_aviso_usuario)

        self.setLayout(self.Layout_principal)

    def iniciar_conv(self):
        self.connector.iniciar_conversao()

    def cancelar_conv(self):
        self.connector.cancelar_conversao()

    def atualizar_indicador_acao(self, nome_layer:str):
        self.acao_atual.setText("Estado atual: " + "convertendo a layer: " + nome_layer)

    def atualizar_barra_progresso(self,index_layer: int):
        self.bar_progress.setValue(index_layer)


class Converter_BDGD():

    def __init__(self, connector_window_converter, path_geodb:str):
        super().__init__()
        self.connector = connector_window_converter

        # Diretórios da BDGD
        self.path_BDGD_geodb = path_geodb
        self.path_BDGD_sqlite = ""

    def criacao_novo_diretorio(self) -> tuple[str,bool]:
        # Cria um novo diretório para a BDGD (formato sqlite)
        path_temp = os.path.join(self.path_BDGD_geodb, "SIPLA_" + os.path.basename(self.path_BDGD_geodb) + '.sqlite')
        try:
            os.mkdir(path_temp)
            self.path_BDGD_sqlite = path_temp
        except FileExistsError:
            for nome_layer in self.connector.layers_BDGD:
                if not os.path.isfile(path_temp + "\\" + nome_layer + ".sqlite"):
                    return path_temp, False
            return path_temp, True
        return path_temp, False

    def convert_geodatabase_to_sqlite(self, nome_layer):
        with fiona.open(self.path_BDGD_geodb, layer=nome_layer) as geodb:
            # Criação de uma cópia do dicionário de esquema do layout
            schema = copy.deepcopy(geodb.schema)

            # Conexão com o banco em sqlite
            if nome_layer.endswith('_tab'):
                nome_layer_sem_tab = nome_layer[:-4]
            else:
                nome_layer_sem_tab = nome_layer

            if platform.system() == 'Linux':
                conn = sqlite3.connect(os.path.join(self.path_BDGD_sqlite, f"{nome_layer_sem_tab}.sqlite"))
            elif platform.system() == 'Windows':
                conn = sqlite3.connect(self.path_BDGD_sqlite + f"\\{nome_layer_sem_tab}.sqlite")
            elif platform.system() == 'Darwin':
                pass

            c = conn.cursor()

            match schema['geometry']:
                case 'Point':
                    self.convert_layer_point(geodb, nome_layer_sem_tab, schema, c, conn)
                case 'MultiLineString':
                    self.convert_layer_MultiLineString(geodb, nome_layer_sem_tab, schema, c, conn)
                case _:
                    print('ok3')
                    self.convert_layer_table(geodb, nome_layer_sem_tab, schema, c, conn)

    def convert_layer_table(self, geodatabase, nome_layer, schema, cursor, connection):
        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (objectid INTEGER PRIMARY KEY"
        for field in schema['properties']:
            create_table_sql += f", {field} {self.convert_type_py_to_type_sqlite(schema, field)}"
        create_table_sql += ")"
        cursor.execute(create_table_sql)

        for index, feature in enumerate(geodatabase):
            values = [feature['properties'][field] for field in schema['properties']]
            cursor.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(values))})",
                           values)

        connection.commit()
        connection.close()

    def convert_layer_point(self, geodatabase, nome_layer, schema, cursor, connection):
        schema['properties']['x'] = 'float'
        schema['properties']['y'] = 'float'

        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (objectid INTEGER PRIMARY KEY"
        for field in schema['properties']:
            create_table_sql += f", {field} {self.convert_type_py_to_type_sqlite(schema, field)}"
        create_table_sql += ")"
        cursor.execute(create_table_sql)

        del schema['properties']['x']
        del schema['properties']['y']
        for feature in geodatabase:
            values = [feature['properties'][field] for field in schema['properties']]

            x, y = feature.geometry['coordinates']

            values.append(x)
            values.append(y)
            cursor.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(values))})",
                           values)

        connection.commit()
        connection.close()

    def convert_layer_MultiLineString(self, geodatabase, nome_layer, schema, cursor, connection):
        schema['properties']['vertex_index'] = 'int'
        schema['properties']['x'] = 'float'
        schema['properties']['y'] = 'float'

        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (objectid INTEGER PRIMARY KEY"
        for field in schema['properties']:
            create_table_sql += f", {field} {self.convert_type_py_to_type_sqlite(schema, field)}"
        create_table_sql += ")"
        cursor.execute(create_table_sql)

        del schema['properties']['vertex_index']
        del schema['properties']['x']
        del schema['properties']['y']
        for feature in geodatabase:

            ponto_inicial = [feature['properties'][field] for field in schema['properties']]
            ponto_final = [feature['properties'][field] for field in schema['properties']]

            Vertices = feature.geometry['coordinates']
            (x0, y0), (x1, y1) = Vertices[0][0:2]

            ponto_inicial.append(0)
            ponto_inicial.append(x0)
            ponto_inicial.append(y0)

            ponto_final.append(1)
            ponto_final.append(x1)
            ponto_final.append(y1)


            cursor.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(ponto_inicial))})",
                           ponto_inicial)
            cursor.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(ponto_final))})",
                           ponto_final)

        connection.commit()
        connection.close()

    def convert_Polygon(self):
        pass

    def convert_type_py_to_type_sqlite(self, esquema_geodb, field):
        if fiona.prop_type(esquema_geodb['properties'][f'{field}']) == type(1):
            return 'INTEGER'
        elif fiona.prop_type(esquema_geodb['properties'][f'{field}']) == type(1.45):
            return 'REAL'
        elif fiona.prop_type(esquema_geodb['properties'][f'{field}']) == type("string"):
            return 'TEXT'
        elif fiona.prop_type(esquema_geodb['properties'][f'{field}']) == type(True):
            return 'BLOB'
        else:
            return 'TEXT'


if __name__ == '__main__':

    # Setup de teste isolado do conversor
    path_BDGD_geodb = r"C:\Users\ppgsa\Documents\SIPLA\Debug_final_geodb_conv\COELBA_47_2018-12-31_M10_20190610-1331.gdb"
    modelo_BDGD = "Modelo Novo"
    layers_p_conversao = ["CTAT", "EQTRAT", "SSDAT", "CTMT","SSDMT","EQTRMT", "UNTRAT","UNTRMT"]

    #
    app = QApplication(sys.argv)
    Connector = ConnectorWindowAndConverterBDGD(QWidget())
    Connector.BDGD_layers_SIPLA = layers_p_conversao
    Connector.DataBaseInfo = {'Geodb_DirDataBase': path_BDGD_geodb, 'Modelo': modelo_BDGD}

    Connector.initUI()
    app.exec_()
