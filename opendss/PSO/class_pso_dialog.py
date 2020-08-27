from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QTreeWidgetItem, \
    QPushButton, QTreeWidget, QMessageBox, QLabel, QLineEdit, QRadioButton, \
    QComboBox, QTabWidget, QWidget, QHBoxLayout
from PyQt5.QtWidgets import QStatusBar, QMessageBox
from PyQt5.QtWidgets import QDockWidget, QAction, QMenuBar, QToolBar
from PyQt5.QtGui import QIcon
###


# import class_exception
import maps.class_view
import main_panels_dock
import main_actions
import main_toolbar
import opendss.class_opendss

import class_about_dialog
import datetime


class C_PSO_Dialog():
    def __init__(self):
        super().__init__()

        self.OpenDSS = opendss.class_opendss.C_OpenDSS()

        # self.solve = main_actions.C_MainActions.execOpenDSS()


        #self.solve1 = main_toolbar.C_MenuToolBar()
        #self.solve1.OpenDSS_Run_Act.triggered.conne )ct(


    def teste_pso(self):

        self.OpenDSS.exec_OpenDSSRun("Show Voltage LN Nodes")

        #opendss.class_opendss.C_OpenDSS.exec_OpenDSSRun("Show Voltage LN Nodes")

        #print( 'rodou' )

        #print( 'ok1' )

    # self.Actions.execOpenDSS()

    # self.titleWindow = "Optimização por Enxame de Partículas (PSO)"
    # self.iconWindow = cfg.sipla_icon
    # self.stylesheet = cfg.sipla_stylesheet
