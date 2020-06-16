from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QStyleFactory, QDialog,  QVBoxLayout,  QLabel, QDialogButtonBox
from PyQt5.QtCore import Qt

import config as cfg


class C_AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "OpenDSS About"
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
        self.Dialog_Layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.Dialog_Layout)

        logoWidget_qpixmap = QPixmap('img/Logo_SIPLA.png')
        logoWidget_Label = QLabel()
        logoWidget_Label.setPixmap(logoWidget_qpixmap)
        self.Dialog_Layout.addWidget(logoWidget_Label)

        nameWidget_Label = QLabel(cfg.__name__)
        nameWidget_font = QFont()
        nameWidget_font.setBold(True)
        nameWidget_Label.setFont(nameWidget_font)
        self.Dialog_Layout.addWidget(nameWidget_Label)

        versionWidget_Label = QLabel(cfg.__version__)
        self.Dialog_Layout.addWidget(versionWidget_Label)

        obsWidget_Label = QLabel('Este programa vem com absolutamente nenhuma garantia.')
        self.Dialog_Layout.addWidget(obsWidget_Label)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.Dialog_Layout.addWidget(self.buttonBox)











