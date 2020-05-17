from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

import csv
import random
import pathlib
import platform
import pyqtgraph
import class_exception

import opendss.class_opendss
import config as cfg

class C_Reactive_Pow_DispMode_Dialog(QDialog): ## Classe Dialog Despacho da Potencia Reativa
    def __init__(self):
        super().__init__()

        self.titleWindow = "Despacho da Potência Reativa"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

        # self.OpenDSS = opendss.class_opendss.C_OpenDSS()


    def InitUI(self):
        self.setWindowTitle(self.titleWindow) # titulo janela
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface