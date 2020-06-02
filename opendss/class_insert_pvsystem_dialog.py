from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, \
   QVBoxLayout, QTabWidget, QLabel, QComboBox, QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from PyQt5.QtCore import Qt

import opendss.class_opendss
import config as cfg

class C_Insert_PVSystem_Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "PVSystem Settings"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

