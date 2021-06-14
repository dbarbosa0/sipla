from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QComboBox,\
    QLineEdit, QRadioButton,  QButtonGroup
from PyQt5.QtCore import Qt

import config as cfg

class C_TDDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.listTrafos = []

        self.titleWindow = "Transformador de Distribuição"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()


        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        ##Alimentador de Referência
        self.Field_GroupBox = QGroupBox("Dados do Alimentador")
        self.Field_GroupBox_Layout = QVBoxLayout()
        self.Field_GroupBox.setLayout(self.Field_GroupBox_Layout)

        self.Dilalog_Field_TD_Label = QLabel("Nome:")
        self.Field_GroupBox_Layout.addWidget(self.Dilalog_Field_TD_Label)

        self.Dilalog_Field_TD_LineEdit = QLineEdit()
        self.Dilalog_Field_TD_LineEdit.setReadOnly(True)
        self.Field_GroupBox_Layout.addWidget(self.Dilalog_Field_TD_LineEdit)

        self.Dialog_Layout.addWidget(self.Field_GroupBox)

        ### Selecionar Todos ou Algum específico

        self.selectTrafo_GroupBox = QGroupBox("Quais Redes de BT do alimentador deseja selecionar?")
        self.selectTrafo_GroupBox_Layout = QVBoxLayout()
        self.selectTrafo_GroupBox.setLayout(self.selectTrafo_GroupBox_Layout)

        self.selectTrafoALL_RadioBox = QRadioButton("Todas")
        self.selectTrafoALL_RadioBox.setChecked(False)
        # self.Conn_GroupBox_OpenDSSDirect.toggled.connect(lambda: self.onConnRadioBtn(self.Conn_GroupBox_OpenDSSDirect))
        self.selectTrafo_GroupBox_Layout.addWidget(self.selectTrafoALL_RadioBox)

        self.selectTrafoIND_RadioBox = QRadioButton("Apenas mais 1 (uma)")
        self.selectTrafoIND_RadioBox.setChecked(True)
        self.selectTrafo_GroupBox_Layout.addWidget(self.selectTrafoIND_RadioBox)

        self.selectTrafo_BGroup = QButtonGroup()
        self.selectTrafo_BGroup.addButton(self.selectTrafoALL_RadioBox)
        self.selectTrafo_BGroup.addButton(self.selectTrafoIND_RadioBox)
        self.selectTrafo_BGroup.buttonClicked.connect(self.setDisabled_Trafos_GroupBox)

        self.Dialog_Layout.addWidget(self.selectTrafo_GroupBox)


        ##### Transformador de Distribuição
        self.TD_GroupBox = QGroupBox("Dados do Transformador de Distribuição da Distribuidora")
        self.TD_GroupBox_Layout = QVBoxLayout()
        self.TD_GroupBox.setLayout(self.TD_GroupBox_Layout)

        self.Dilalog_ID_TD_Label = QLabel("ID do Transformador:")
        self.TD_GroupBox_Layout.addWidget(self.Dilalog_ID_TD_Label)

        self.Dilalog_ID_TD_ComboBox = QComboBox()
        self.TD_GroupBox_Layout.addWidget(self.Dilalog_ID_TD_ComboBox)


        self.Dialog_Layout.addWidget(self.TD_GroupBox)


        ###### Botões
        self.Dilalog_Btns_Layout = QHBoxLayout()
        self.Dilalog_Btns_Layout.setAlignment(Qt.AlignRight)


        self.Dilalog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dilalog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dilalog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Cancel_Btn)

        self.Dilalog_Btns_Ok_Btn = QPushButton("OK")
        self.Dilalog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dilalog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Ok_Btn.clicked.connect(self.setID_TrafoDIST)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dilalog_Btns_Layout,0)

        self.setLayout(self.Dialog_Layout)

    def updateListTrafoDIST(self):

        self.setDisabled_Trafos_GroupBox()

        self.Dilalog_ID_TD_ComboBox.clear()

        self.codTrafoDIST = ''

        self.Dilalog_ID_TD_ComboBox.addItems(self.listTrafos)

    def setID_TrafoDIST(self):
        if self.selectTrafoIND_RadioBox.isChecked():
            self.codTrafoDIST = [self.Dilalog_ID_TD_ComboBox.currentText()]
        else:
            self.codTrafoDIST = self.listTrafos
        self.close()

    def setDisabled_Trafos_GroupBox(self):
        if self.selectTrafoIND_RadioBox.isChecked():
            self.TD_GroupBox.setHidden(False)
        else:
            self.TD_GroupBox.setHidden(True)

        self.adjustSize()










