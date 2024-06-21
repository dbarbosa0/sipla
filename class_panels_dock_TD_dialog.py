from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (QDialog,
                             QLineEdit, QLabel, QPushButton,
                             QScrollArea, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QSpacerItem, QCompleter,
                             QFormLayout, QGroupBox, QStyleFactory
                             )
from PyQt6.QtCore import Qt
import config as cfg
from customwidgets import OnOffWidget


class C_TDDialog(QDialog):
    def __init__(self, listTrafoOtimizado):
        super().__init__()

        self.listTrafos = []
        self.parametro = listTrafoOtimizado
        self.titleWindow = "Transformador de Distribuição"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet
        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        self.controlsLayout = QVBoxLayout()  # Controls container layout.

        self.widgets = []
        self.listanmomes = []

        # List of names, widgets are stored in a dictionary by these keys.
        for name, i in zip(self.parametro, range(len(self.parametro))):
            self.item = OnOffWidget(name)
            self.listanmomes.append(self.item.btn_on.text())
            self.widgets.append(self.item)
            self.formLayout.addRow(self.widgets[i])
        self.groupBox.setLayout(self.formLayout)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        # self.groupBox.setStyleSheet("QGroupBox {background-color: white;"
        #                             "border : solid black;border-width : 1px 1px 1px 1px;}"
        #                             )

        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedWidth(600)
        # self.scroll.setStyleSheet("QScrollBar:vertical{"
        #                           "width: 25px;"
        #                           "border-radius: 5px;"
        #                           "border : solid black; "
        #                           "border-width : 10px 10px 10px 10px;"
        #                           "}"
        #                           )

        ##Alimentador de Referência
        self.Field_GroupBox = QGroupBox("Dados do Alimentador")
        self.Field_GroupBox_Layout = QVBoxLayout()
        self.Field_GroupBox.setLayout(self.Field_GroupBox_Layout)

        self.Dilalog_Field_TD_Label = QLabel("Nome:")
        self.Field_GroupBox_Layout.addWidget(self.Dilalog_Field_TD_Label)

        self.Dilalog_Field_TD_LineEdit = QLineEdit()
        self.Dilalog_Field_TD_LineEdit.setReadOnly(True)
        self.Field_GroupBox_Layout.addWidget(self.Dilalog_Field_TD_LineEdit)

        self.controlsLayout.addWidget(self.Field_GroupBox)

        # Search bar.
        self.groupBox_searchbar = QGroupBox()
        # self.groupBox_searchbar.setStyleSheet("QLineEdit"
        #                                       "{"
        #                                       "border : solid black;"
        #                                       "border-width : 1.1px 1.1px 1.1px 1.1px;"
        #                                       "}""QGroupBox{border : solid black;border-width : 1px 1px 1px 1px;}")

        self.searchbar_Label = QLabel('Barra de pesquisa')
        self.searchbar_Label.setFont(QFont('Arial', 9))
        self.searchbar_Layout = QVBoxLayout()
        self.groupBox_searchbar.setLayout(self.searchbar_Layout)
        self.searchbar_Layout.addWidget(self.searchbar_Label)
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)

        # Adding Completer.

        self.completer = QCompleter(self.parametro)
        self.completer.setMaxVisibleItems(4)
        self.completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseSensitive)
        self.searchbar.setCompleter(self.completer)
        self.searchbar_Layout.addWidget(self.searchbar)
        self.controlsLayout.addWidget(self.groupBox_searchbar)

        self.controlsLayout.addWidget(self.scroll)

        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.

        self.Dilalog_marcar_todos_Layout = QHBoxLayout()

        self.Dilalog_Btns_marcar_todos_Btn = QCheckBox("Selecionar todos")
        self.Dilalog_Btns_marcar_todos_Btn.setFixedWidth(150)
        self.Dilalog_Btns_marcar_todos_Btn.clicked.connect(self.setDisabled_Trafos_GroupBox)
        self.Dilalog_marcar_todos_Layout.addWidget(self.Dilalog_Btns_marcar_todos_Btn)
        self.Dilalog_marcar_todos_Layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.controlsLayout.addLayout(self.Dilalog_marcar_todos_Layout, 0)

        self.Dilalog_Btns_Layout = QHBoxLayout()

        self.Dilalog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dilalog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Cancel_Btn.clicked.connect(self.Cancelamento)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Cancel_Btn)

        self.Dilalog_Btns_Ok_Btn = QPushButton("OK")
        self.Dilalog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Ok_Btn.clicked.connect(self.setID_TrafoDIST)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Ok_Btn)

        self.Dilalog_Btns_Layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.controlsLayout.addLayout(self.Dilalog_Btns_Layout)

        #self.setLayout(self.controlsLayout)

        # Otimização dos Trafos.
        self.groupBox_cargas = QGroupBox()
        # self.groupBox_cargas.setStyleSheet("QLineEdit"
        #                                    "{"
        #                                    "border : solid black;"
        #                                    "border-width : 1.1px 1.1px 1.1px 1.1px;"
        #                                    "}""QGroupBox{border : solid black;border-width : 1px 1px 1px 1px;}")

        self.cargas_Label = QLabel('configuração das Cargas')
        self.cargas_Label.setFont(QFont('Arial', 9))
        self.cargas_Layout = QVBoxLayout()
        self.groupBox_cargas.setLayout(self.cargas_Layout)
        self.cargas_Layout.addWidget(self.cargas_Label)
        self.cargas = QLineEdit('Otimização das Cargas')
        self.cargas.textChanged.connect(self.update_display)

        self.controlsLayout.addWidget(self.groupBox_cargas)
        self.setLayout(self.controlsLayout)


    def keyPressEvent(self, event):
        self.naiads = self.searchbar.text()
        if event.key() == Qt.Key.Key_Return:
            if self.naiads != '':
                for i in range(len(self.listanmomes)):
                    if self.naiads == self.listanmomes[i]:
                        self.widgets[i].btn_on.nextCheckState()
                        if self.widgets[i].btn_on.isChecked():
                            self.widgets[i].btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
                            self.widgets[i].btn_off.setStyleSheet("background-color: none; color: none;")
                        else:
                            self.widgets[i].btn_on.setStyleSheet("background-color: none; color: none;")
                            self.widgets[i].btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")
                        self.searchbar.clear()
            else:
                self.setID_TrafoDIST()
        if event.key() == Qt.Key.Key_Escape:
            print('esc')
            self.close()

    def setID_TrafoDIST(self):
        self.codTrafoDIST = []
        for i in range(len(self.listanmomes)):
            if self.widgets[i].btn_on.isChecked():
                self.codTrafoDIST.append(self.widgets[i].btn_on.text())
        self.close()

    def Cancelamento(self):
        self.close()

    def setDisabled_Trafos_GroupBox(self):
        if self.Dilalog_Btns_marcar_todos_Btn.isChecked():
            for i in range(len(self.listanmomes)):
                self.widgets[i].btn_on.setChecked(True)
                if self.widgets[i].btn_on.isChecked():
                    self.widgets[i].btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
                    self.widgets[i].btn_off.setStyleSheet("background-color: none; color: none;")
                else:
                    self.widgets[i].btn_on.setStyleSheet("background-color: none; color: none;")
                    self.widgets[i].btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")
                self.searchbar.clear()
        else:
            for i in range(len(self.listanmomes)):
                self.widgets[i].btn_on.setChecked(False)
                if self.widgets[i].btn_on.isChecked():
                    self.widgets[i].btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
                    self.widgets[i].btn_off.setStyleSheet("background-color: none; color: none;")
                else:
                    self.widgets[i].btn_on.setStyleSheet("background-color: none; color: none;")
                    self.widgets[i].btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")
                self.searchbar.clear()

    def update_display(self, text):
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()