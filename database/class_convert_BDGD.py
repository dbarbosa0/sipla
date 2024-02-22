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


        self._DataBaseInfo = {}

    @property
    def DataBaseInfo(self):
        return self._DataBaseInfo

    @DataBaseInfo.setter
    def DataBaseInfo(self, nDataBaseInfo):
        self._DataBaseInfo = nDataBaseInfo

    def iniciar_conv(self):
        pass

    def interromper_conv(self):
        pass


app = QApplication(sys.argv)

window = Window_conversion_status()
window.show()

app.exec_()
