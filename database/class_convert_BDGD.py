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
import class_data
import copy
import class_conn


class WindowConversionStatus(QWidget, class_data.dadosBDGD):

    def __init__(self, adapter_window_conversion_status_converter):
        super().__init__()
        self.adapter = adapter_window_conversion_status_converter

        # Dados gerais BDGD
        self._DataBaseInfo = {}

        # Construção da janela
        self.titleWindow = "Preparação do Banco de Dados..."
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))
        self.setWindowModality(Qt.ApplicationModal)
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
        self.bar_progress_total_steps = 10
        self.bar_progress.setMinimumWidth(550)
        self.bar_progress.setMinimumHeight(25)
        self.bar_progress.setFormat(f"    %v / {self.bar_progress_total_steps} passos concluídos (%p%)")
        self.bar_progress.setMaximum(self.bar_progress_total_steps)
        self.bar_progress.setValue(0)

        # Construção do indicador da ação atual
        self.acaoes = ['...']
        self.acao_atual = QLabel("Estado atual: " + self.acaoes[0])
        self.acao_atual.setStyleSheet("border: 2px solid green;"
                                      "border-radius: 4px;"
                                      "padding: 2px;")

        # Construção do botão de iniciar a conversão
        self.botao_iniciar = QPushButton("Iniciar a conversão")
        self.botao_iniciar.setIcon(QIcon('img/icon_save.png'))
        self.botao_iniciar.clicked.connect(self.iniciar_conv)

        # Construção do botão de interrupção da conversão
        self.botao_cancelar = QPushButton("Interromper a conversão")
        self.botao_cancelar.setIcon(QIcon('img/icon_cancel.png'))
        self.botao_cancelar.clicked.connect(self.interromper_conv)

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
        self.adapter.iniciar_conversao()

    def interromper_conv(self):
        pass

    def atualizacao_indicador_acao(self):
        pass


class Converter_BDGD():

    def __init__(self, path_geodb):
        super().__init__()

        # Diretórios da BDGD
        self.path_BDGD_geodb = path_geodb
        self.path_BDGD_sqlite = ""

    def criacao_novo_diretorio(self):
        # Cria um novo diretório para a BDGD (formato sqlite)
        path_temp = os.path.join(self.path_BDGD_geodb, "SIPLA_" + os.path.basename(self.path_BDGD_geodb))
        try:
            os.mkdir(path_temp)
        except FileExistsError as erro:
            pass
        self.path_BDGD_sqlite = path_temp
        return path_temp

    def convert_geodatabase_to_sqlite(self, nome_layer):
        with fiona.open(self.path_BDGD_geodb, layer=nome_layer) as geodb:
            # Criação de uma cópia do dicionário de esquema do layout
            schema = copy.deepcopy(geodb.schema)

            # Conexão com o banco em sqlite
            conn = sqlite3.connect(self.path_BDGD_sqlite + f"\\{nome_layer}.sqlite")
            c = conn.cursor()

            match schema['geometry']:
                case 'Point':
                    self.convert_layer_point(geodb, nome_layer, schema, c, conn)
                case 'MultiLineString':
                    self.convert_layer_MultiLineString(geodb, nome_layer, schema, c, conn)
                case _:
                    self.convert_layer_table(geodb, nome_layer, schema, c, conn)

    def convert_layer_table(self, geodatabase, nome_layer, schema, cursor, connection):
        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (id INTEGER PRIMARY KEY"
        for field in schema['properties']:
            create_table_sql += f", {field} {self.convert_type_py_to_type_sqlite(schema, field)}"
        create_table_sql += ")"
        cursor.execute(create_table_sql)

        for index, feature in enumerate(geodatabase):
            values = [feature['properties'][field] for field in schema['properties']]
            cursor.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(values))})",
                           values)
            self.atualizar_progresso(index)

        connection.commit()
        connection.close()

    def convert_layer_point(self, geodatabase, nome_layer, schema, cursor, connection):
        schema['properties']['x'] = 'float'
        schema['properties']['y'] = 'float'

        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (id INTEGER PRIMARY KEY"
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

        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (id INTEGER PRIMARY KEY"
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


    def atualizar_progresso(self):
        pass


class AdapterWindowStatusAndConverter(class_data.dadosBDGD):

    def __init__(self):
        super().__init__()

        # Dados gerais BDGD
        self._DataBaseInfo = {}
        self.path_BDGD_sqlite = ""

    @property
    def DataBaseInfo(self):
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo 
        self.path_BDGD_geodb = self.DataBaseInfo["Sqlite_DirDataBase"]
        
        # Layer variables
        self.layers_BDGD = self.get_layers_uteis_BDGD(self.DataBaseInfo["Modelo"])
        self.n_layers_BDGD = len(self.layers_BDGD)
        self.acaoes = ['...']+["Convertendo a layer: " + nome_da_layer + " (0/?)" for nome_da_layer in self.layers_BDGD]

    def initUI(self):
        self.window = WindowConversionStatus(self)
        self.window.show()
        self.window.exec_()
        
    def iniciar_conversao(self):
        self.conversor = Converter_BDGD(self.path_BDGD_geodb)
        self.conversor.criacao_novo_diretorio()

        for index, nome_layer in enumerate(self.layers_BDGD, start=1):
            self.conversor.convert_geodatabase_to_sqlite(nome_layer)



if __name__ == '__main__':
    pass
    app = QApplication(sys.argv)

    adater = AdapterWindowStatusAndConverter()
    adater.initUI()
