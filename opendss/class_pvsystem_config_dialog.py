from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyleFactory, QDialog

class C_PVSystem_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "PVSystem Settings"
        self.iconWindow = "img/logo.png"
        self.stylesheet = "fusion"

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

