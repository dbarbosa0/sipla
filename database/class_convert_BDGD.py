import sqlite3, fiona

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyleFactory, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, \
    QGridLayout, QWidget, QProgressBar, QApplication
from PyQt6.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot, pyqtSignal ,QObject

import traceback, sys, os, copy, threading, concurrent.futures, multiprocessing, platform

import config as cfg
import database.class_data as class_data

from timeit import default_timer as timer

class ConnectorInterfaceConversor:

    def __init__(self, config_dialog):
        # Dados gerais BDGD
        self._DataBaseInfo = {}
        self.path_BDGD_sqlite = ""
        self.config_dialog = config_dialog
        self.dadosBDGD = class_data.dadosBDGD()

        # Flags para utilização segura dos threads
        self.is_running_flag = False
        self.exit_request_flag = False
        self.current_state_flag = 0

    @property
    def DataBaseInfo(self):
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo
        self.path_BDGD_geodb = self.DataBaseInfo["Geodb_DirDataBase"]

        # Layer variables
        self.layers_BDGD = self.dadosBDGD.get_layers_uteis_BDGD(self.DataBaseInfo["Modelo"])
        self.n_layers_BDGD = len(self.layers_BDGD)

    def initUI(self):
        self.window = InterfaceJanelaConversao(self, self.n_layers_BDGD)
        self.window.show()

    def coversao_layer_iniciada(self, nome_layer):
        self.window.atualizar_indicador_acao(nome_layer)

    def conversao_layer_finalizada(self, index_layer):
        self.window.atualizar_barra_progresso(index_layer)

    def conversao_finalizada(self):
        # Print do tempo demandado para correção
        tempo_decorrido = timer() - self.inicio_conv
        print(f'Tempo demandado em segundos: {tempo_decorrido}')

        if self.is_running_flag:
            # Atualizacao_flag:
            self.is_running_flag = False

            self.config_dialog.GroupBox_BDGD_Edit.setText(self.path_BDGD_sqlite)
            self.config_dialog.loadParameters()
            self.config_dialog.close()
            self.window.close()


    def iniciar_conversao(self):
        # Tempo inicial da conversão
        self.inicio_conv = timer()

        self.conversor = Conversor_BDGD(self, self.path_BDGD_geodb)
        self.path_BDGD_sqlite, self.BDGD_sqlite_already_exists = self.conversor.criacao_novo_diretorio()

        # Flags para utilização segura dos threads e processos
        self.is_running_flag = True
        self.exit_request_flag = False

        if not self.BDGD_sqlite_already_exists:
            self.seletor_tipo_conversao()

    def seletor_tipo_conversao(self):
        if platform.system() == 'Linux':
            self.conversao_multiprocessing_manual()
        elif platform.system() == 'Windows':
            self.conversao_threading_Qt()
        elif platform.system() == 'Darwin':
            pass

    def conversao_threading_Qt(self):
        self.threadpool = QThreadPool()
        self.thread_conversao_single_core = ThreadConversaoSingleCore(self.layers_BDGD, self.conversor, self)

        # Sinais associados ao thread
        self.thread_conversao_single_core.signais.resultado_layer_iniciada.connect(self.coversao_layer_iniciada)
        self.thread_conversao_single_core.signais.finalizacao_layer.connect(self.conversao_layer_finalizada)
        self.thread_conversao_single_core.signais.finalizacao_completa.connect(self.conversao_finalizada)

        self.threadpool.start(self.thread_conversao_single_core)

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

    def interromper_conversao(self):
        if self.is_running_flag:
            self.exit_request_flag = True
            self.window.alterar_indicador_acao('Estado atual: interrompendo a conversão\n'
                '(Aguarde a conversão da layer atual para que seja possível retomar a conversão desse ponto).')



class ThreadConversaoSingleCore(QRunnable):

    def __init__(self, *args, **kwargs):
        super(ThreadConversaoSingleCore, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signais = SinaisConversao()

    @pyqtSlot()
    def run(self):
        try:
            layers_BDGD, conversor, connector = self.args
            connector: ConnectorInterfaceConversor
            for index, nome_layer in enumerate(layers_BDGD[connector.current_state_flag:],
                                               start=connector.current_state_flag + 1):
                try:
                    if not connector.exit_request_flag:
                        print('converte layer')
                        self.signais.resultado_layer_iniciada.emit(nome_layer)
                        conversor.convert_geodatabase_to_sqlite(nome_layer)
                    else:
                        # Atualização da flag de estado
                        index = index - 1
                        connector.current_state_flag = (index)
                        connector.is_running_flag = False

                        self.signais.resultado_layer_iniciada.emit('xx - Conversão interrompida - xx')
                        break
                except:
                    traceback.print_exc()
                    exctype, value = sys.exc_info()[:2]
                    self.signais.error_conversao.emit((exctype, value, traceback.format_exc()))
                finally:
                    self.signais.finalizacao_layer.emit(index)
        finally:
            self.signais.finalizacao_completa.emit()

    def conversao_padrao(self, argumentos):
        layers_BDGD, conversor = argumentos
        for index, nome_layer in enumerate(layers_BDGD, start=1):
            conversor.convert_geodatabase_to_sqlite(nome_layer)

class SinaisConversao(QObject):
    
    finalizacao_layer = pyqtSignal(object)
    resultado_layer_iniciada = pyqtSignal(object)
    finalizacao_completa = pyqtSignal()
    error_conversao = pyqtSignal(tuple)


class InterfaceJanelaConversao(QWidget):

    def __init__(self, connector_window_converter: ConnectorInterfaceConversor, n_layers: int):
        super().__init__()
        self.connector = connector_window_converter

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
        self.botao_iniciar.clicked.connect(self.clique_botao_conv)

        # Construção do botão de interrupção da conversão
        self.botao_cancelar = QPushButton("Interromper a conversão")
        self.botao_cancelar.setIcon(QIcon('img/icon_cancel.png'))
        self.botao_cancelar.clicked.connect(self.clique_botao_interromper)

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

    def clique_botao_conv(self):
        self.connector.iniciar_conversao()

    def clique_botao_interromper(self):
        self.connector.interromper_conversao()

    def atualizar_indicador_acao(self, nome_layer:str):
        self.acao_atual.setText("Estado atual: " + "convertendo a layer " + nome_layer)

    def alterar_indicador_acao(self, texto:str):
        self.acao_atual.setText(texto)

    def atualizar_barra_progresso(self, index_layer: int):
        self.bar_progress.setValue(index_layer)


class Conversor_BDGD:

    def __init__(self, connector_window_converter, path_geodb:str):
        super().__init__()
        self.connector = connector_window_converter

        # Diretórios da BDGD
        self.path_BDGD_geodb = path_geodb
        self.path_BDGD_sqlite = None

    def criacao_novo_diretorio(self) -> tuple[str,bool]:
        """
        Cria um diretório para a BDGD que será convertida para o formato sqlite ou o retorna, se já criado
        com o nome: "SIPLA_nomeBDGD.sqlite"


        :return path_temp, is_layers_presentes: tuple[str,bool], Diretório e indicador se já está preenchido
        """
        path_temp = os.path.join(self.path_BDGD_geodb, "SIPLA_" + os.path.basename(self.path_BDGD_geodb) + '.sqlite')

        try:
            os.mkdir(path_temp)
            self.path_BDGD_sqlite = path_temp
        except FileExistsError:
            self.path_BDGD_sqlite = path_temp

        layers_estao_presentes = self.verificar_presenca_layers_sqlite(path_temp)
        return path_temp, layers_estao_presentes

    def verificar_presenca_layers_sqlite(self, path_sqlite: str):
        """
        Verifica a presença dos layers no caminho que já existe


        :param path_sqlite: str, Diretório analisado


        :return  layers_estao_presentes: bool, Indicador se todos os layers estão no diretório
        """
        for nome_layer in self.connector.layers_BDGD:
            if not os.path.isfile(path_sqlite + "\\" + nome_layer + ".sqlite"):
                layers_estao_presentes = False
                return layers_estao_presentes

        layers_estao_presentes = True
        return layers_estao_presentes


    def convert_geodatabase_to_sqlite(self, nome_layer):
        """
        Cria um banco em sqlite para uma layer dentro do arquivo GIS e aciona sua conversao de acorco com sua geometria


        :param nome_layer: str, Nome da layer a ser convertida
        """
        with fiona.open(self.path_BDGD_geodb, layer=nome_layer) as geodb:
            # Criação de uma cópia do dicionário de esquema do layout
            schema = copy.deepcopy(geodb.schema)

            # Haja vista que algumas layers possuem o sufixos _tab em seu nome, retiramos o sufixo para chamada direta
            if nome_layer.endswith('_tab'):
                nome_layer_sem_tab = nome_layer[:-4]
            else:
                nome_layer_sem_tab = nome_layer

            # Cria e se conecta com o banco em sqlite
            conn = sqlite3.connect(os.path.join(self.path_BDGD_sqlite, f"{nome_layer_sem_tab}.sqlite"))
            c = conn.cursor()

            match schema['geometry']:
                case 'Point':
                    self.convert_layer_point(geodb, nome_layer_sem_tab, schema, c, conn)
                case 'MultiLineString':
                    self.convert_layer_MultiLineString(geodb, nome_layer_sem_tab, schema, c, conn)
                case _:
                    self.convert_layer_table(geodb, nome_layer_sem_tab, schema, c, conn)

    def convert_layer_table(self, geodatabase, nome_layer, schema, cursor, connection):
        """
        Adiciona todas as features de uma layer do tipo tabela em uma tabela do seu referido banco em sqlite


        :param geodatabase: GIS, Geodatabase
        :param nome_layer: str, Nome da layer a ser convertida
        :param schema: dict, Dicionário de esquema do layout
        :param cursor: sqlite3.connect.cursor, Curso do banco de dados
        :param connection: sqlite3.connect, Conexão ao banco de dados
        """
        # Cria uma tabela no banco com uma coluna para cada atributo das features
        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (objectid INTEGER PRIMARY KEY"
        for field in schema['properties']:
            create_table_sql += f", {field} {self.convert_type_py_to_type_sqlite(schema, field)}"
        create_table_sql += ")"
        cursor.execute(create_table_sql)

        # Adiciona os valores de cada feature a tabela
        for index, feature in enumerate(geodatabase):
            values = [feature['properties'][field] for field in schema['properties']]
            cursor.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(values))})",
                           values)

        connection.commit()
        connection.close()

    def convert_layer_point(self, geodatabase, nome_layer, schema, cursor, connection):
        """
        Adiciona todas as features de uma layer do tipo ponto em uma tabela do seu referido banco em sqlite


        :param geodatabase: GIS, Geodatabase
        :param nome_layer: str, Nome da layer a ser convertida
        :param schema: dict, Dicionário de esquema do layout
        :param cursor: sqlite3.connect.cursor, Curso do banco de dados
        :param connection: sqlite3.connect, Conexão ao banco de dados
        """
        # Cria os atributos de coordenadas para os pontos, apenas para criação da tabela
        schema['properties']['x'] = 'float'
        schema['properties']['y'] = 'float'

        # Cria uma tabela no banco com uma coluna para cada atributo das features
        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (objectid INTEGER PRIMARY KEY"
        for field in schema['properties']:
            create_table_sql += f", {field} {self.convert_type_py_to_type_sqlite(schema, field)}"
        create_table_sql += ")"
        cursor.execute(create_table_sql)
        del schema['properties']['x']
        del schema['properties']['y']

        # Adiciona os valores de cada feature a tabela
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
        """
        Adiciona todas as features de uma layer do tipo multilinestring em uma tabela do seu referido banco em sqlite


        :param geodatabase: GIS, Geodatabase
        :param nome_layer: str, Nome da layer a ser convertida
        :param schema: dict, Dicionário de esquema do layout
        :param cursor: sqlite3.connect.cursor, Curso do banco de dados
        :param connection: sqlite3.connect, Conexão ao banco de dados
        """
        # Cria os atributos para os vertices das linhas, apenas para criação da tabela
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

        # Adiciona os valores de cada feature a tabela
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
        """
        Relaciona os tipo presentes em GIS com um dos quatro tipos do sqlite (nao consideramos o tipo NULL)


        :param esquema_geodb: dict, Dicionário de esquema do layout
        :param field: str, Campo ao qual o tipo será relacionado
        """
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

    #
    app = QApplication(sys.argv)
    Connector = ConnectorInterfaceConversor(QWidget())
    Connector.DataBaseInfo = {'Geodb_DirDataBase': path_BDGD_geodb, 'Modelo': modelo_BDGD}

    Connector.initUI()
    app.exec()
