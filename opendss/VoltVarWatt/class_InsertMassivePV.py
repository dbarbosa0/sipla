from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox, QLabel, QLineEdit, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout, QDoubleSpinBox, QSpinBox
from PyQt5.QtCore import Qt

import opendssdirect
import opendss.class_opendss
import opendss.class_conn
import opendss.class_data
import config as cfg
import unidecode
from opendss.class_conn import C_OpenDSSDirect_Conn


class C_Insert_MassivePV(C_OpenDSSDirect_Conn):
    def __init__(self):
         super().__init__()
         self.AllBusNames = self.engineCircuit.AllBusNames()

    def ImprimirNomesBus(self):
         print(self.AllBusNames)

