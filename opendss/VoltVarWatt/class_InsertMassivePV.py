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
         for numero in range(0, len(self.AllBusNames)):
            name = self.AllBusNames[numero]
            opendssdirect.run_command(
                "New PVSystem.{bus_name} Bus1={bus_name} phases=1 kVA=600 irrad=0.98 Pmpp=500 temperature=25 PF=1 %cutin=0.1 %cutout=0.1".format(
                    bus_name=name,
                )
            )
         print(opendssdirect.PVsystems.AllNames())
         self.OpenDSS = opendss.class_opendss.C_OpenDSS()

    def Solve(self):
         self.OpenDSS.exec_OpenDSS()

