from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QFileDialog, QColorDialog, QMessageBox, QInputDialog, QCheckBox
from PyQt5.QtCore import Qt

import random
import math
import opendss.class_conn
import opendss.class_opendss
import opendss.class_data
import config as cfg
import opendss.PSO.class_pso_dialog


class C_Opendss():
    def __init__(self):
        super().__init__()
        self.a = opendss.class_opendss
        self.variaveis = opendss.class_conn
        self.rodar_SIPLA()

    def rodar_SIPLA(self):
        self.a.exec_OpenDSSRun("solve")
