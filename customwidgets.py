# customwidgets.py
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton,
                             QHBoxLayout, QCheckBox,QDialog)

from functools import partial

from PyQt6.QtCore import Qt

class OnOffWidget(QDialog):

    def __init__(self, name):
        super(OnOffWidget, self).__init__()

        self.is_on = False
        self.name = name
        #self.lbl = QLabel(self.name)

        self.btn_on = QCheckBox(self.name)
        self.btn_on.setFixedSize(150, 25)
        self.btn_on.setFont(QFont('Arial', 9))

        self.btn_off = QPushButton("Off")
        self.btn_off.setFixedSize(130, 25)

        self.hbox = QHBoxLayout()
        #self.hbox.addWidget(self.lbl)
        self.hbox.addWidget(self.btn_on)
        self.hbox.addWidget(self.btn_off)

        self.btn_on.clicked.connect(self.on)
        self.btn_off.clicked.connect(self.off)

        self.setLayout(self.hbox)
        self.update_button_state()


    def show(self):
        """
        Show this widget, and all child widgets.
        """

        for w in [self, self.btn_on, self.btn_off]:
            w.setVisible(True)

    def hide(self):
        """
        Hide this widget, and all child widgets.
        """

        for w in [self, self.btn_on, self.btn_off]:
            w.setVisible(False)

    def off(self):
        self.is_on = False
        self.update_button_state()
        print('oi')

    def on(self):
        if self.btn_on.isChecked():
            self.is_on = True
        else:
            self.is_on = False
        self.update_button_state()
        print('tchau')

    def update_button_state(self):
        """
        Update the appearance of the control buttons (On/Off)
        depending on the current state.
        """

        if self.is_on == True:
            self.btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: none; border-color: solid black; border-width: 2px;")
        else:
            self.btn_off.clicked.connect(partial(self.btn_on.setChecked, False))
            self.btn_on.setStyleSheet("background-color: none; color: none;")
            self.btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")
