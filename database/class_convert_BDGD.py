from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QFileDialog, QGroupBox, QHBoxLayout,\
    QPushButton, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QMessageBox,\
    QGridLayout, QCheckBox, QWidget, QProgressBar, QApplication, QSpacerItem
from PyQt5.QtCore import Qt
import sqlite3
import class_config_dialog

import sys
import config as cfg
import class_exception
import os
import fiona
import class_data
import copy


class Window_conversion_status(QWidget):

    def __init__(self):
        super().__init__()

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
        self.bar_progress_total_steps = 8
        self.bar_progress.setMinimumWidth(550)
        self.bar_progress.setMinimumHeight(25)
        self.bar_progress.setFormat(f"    %v / {self.bar_progress_total_steps} passos concluídos (%p%)")
        self.bar_progress.setMaximum(self.bar_progress_total_steps)
        self.bar_progress.setValue(4)

        # Construção do indicador da ação atual
        self.acaoes = ["Renomeando layers da geodatabase...", "bla bla...", "bla blo..."]
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
        pass

    def interromper_conv(self):
        pass

class Conversor(class_data.dadosBDGD):

    def __init__(self):
        super().__init__()
        self._DataBaseInfo = {}
        self.path_BDGD_sqlite = ""

    @property
    def DataBaseInfo(self):
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo

    def criacao_novo_diretorio(self):
        input_geodb = self.DataBaseInfo["Sqlite_DirDataBase"]

        # Cria um novo diretório para a BDGD (formato sqlite)
        path_temp = os.path.join(input_geodb, "SIPLA_" + os.path.basename(input_geodb))
        try:
            os.mkdir(path_temp)
        except FileExistsError as erro:
            pass
        self.path_BDGD_sqlite = path_temp

    def convert_geodatabase_to_sqlite(self):
        input_geodb = self.DataBaseInfo["Sqlite_DirDataBase"]

        for nome_layer in self.get_layers_uteis_BDGD(self.DataBaseInfo["Modelo"]):
            with fiona.open(input_geodb, layer=nome_layer) as src:
                # Criação de uma cópia do dicionário de esquema do layout
                schema = copy.deepcopy(src.schema)

                #Conexão com o banco em sqlite
                conn = sqlite3.connect(self.path_BDGD_sqlite + f"\\{nome_layer}")
                c = conn.cursor()

                match schema['geometry']:
                    case 'Point':
                        schema['properties']['x'] = 'float'
                        schema['properties']['y'] = 'float'

                        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (id INTEGER PRIMARY KEY"
                        for field in schema['properties']:
                            if fiona.prop_type(schema['properties'][f'{field}']) in [fiona.prop_type('float'), fiona.prop_type('int')]:
                                pass
                            create_table_sql += f", {field} TEXT"
                        create_table_sql += ")"
                        c.execute(create_table_sql)

                    case 'LineString':
                        pass
                    case _:
                        create_table_sql = f"CREATE TABLE {nome_layer.lower()} (id INTEGER PRIMARY KEY"
                        for field in schema['properties']:
                            create_table_sql += f", {field} TEXT"
                        create_table_sql += ")"
                        c.execute(create_table_sql)

                for feature in src:
                    values = [feature['properties'][field] for field in schema['properties']]
                    c.execute(f"INSERT INTO {nome_layer.lower()} VALUES (NULL, {','.join(['?'] * len(values))})",
                              values)

                conn.commit()
                conn.close()

    def convert_type_fiona_to_type_sqlite(self, esquema_geodb, feature):
        if isinstance(fiona.prop_type(esquema_geodb['properties'][f'{feature}']), int):
            return 'INTEGER'
        elif isinstance(fiona.prop_type(esquema_geodb['properties'][f'{feature}']), float):
            return 'REAL'
        elif isinstance(fiona.prop_type(esquema_geodb['properties'][f'{feature}']), str):
            return 'TEXT'
        elif isinstance(fiona.prop_type(esquema_geodb['properties'][f'{feature}']), bool):
            return 'BLOB'

app = QApplication(sys.argv)

window = Window_conversion_status()
window.show()

app.exec_()
