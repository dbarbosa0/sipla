from PyQt5.QtWidgets import QLabel, QFormLayout, QGroupBox, QDockWidget, QGridLayout, QComboBox, QPushButton, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QTreeWidget, QTreeWidgetItem, QColorDialog, QTabWidget, QTableWidget
from PyQt5.QtCore import Qt
import random
from PyQt5.QtGui import QColor, QIcon
import main_actions
import class_exception
import config

class C_NetPanel(QDockWidget):
    def __init__(self, MainWidget):
        QDockWidget.__init__(self)
        self.MainWidget = MainWidget
        self.mainActions = main_actions.C_MainActions

        self.setWindowTitle("Dados da Rede")
        self.setLayout(QFormLayout())
        self.setContentsMargins(2, 0, 0, 0)
        #self.hide()


        self.Deck_GroupBox = QGroupBox()
        self.Deck_GroupBox.setFixedWidth(330)

        self.Deck_GroupBox_Layout = QFormLayout()


        ###### Configuração #####################

        self.NetPanel_Config_GroupBox = QGroupBox("&Configuração")

        self.NetPanel_Config_GroupBox_Layout = QGridLayout()

        self.NetPanel_Config_GroupBox_SEAT_Label = QLabel("SE - Alta Tensão")
        self.NetPanel_Config_GroupBox_SEAT_ComboBox = QComboBox()
        self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentIndexChanged.connect(self.setDisabled_NetPanel_Config_GroupBox_SEAT_Btn)
        self.NetPanel_Config_GroupBox_SEAT_Btn = QPushButton("Ok")
        self.NetPanel_Config_GroupBox_SEAT_Btn.setFixedWidth(30)
        self.NetPanel_Config_GroupBox_SEAT_Btn.clicked.connect(self.get_CirATMT)
        
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_SEAT_Label, 1, 1, 1, 1)
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_SEAT_ComboBox, 1, 2, 1, 1)
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_SEAT_Btn, 1, 3, 1, 1)

        self.NetPanel_Config_GroupBox_CirATMT_Label = QLabel("Alimentador AT MT")
        self.NetPanel_Config_GroupBox_CirATMT_ComboBox = QComboBox()
        self.NetPanel_Config_GroupBox_CirATMT_ComboBox.currentIndexChanged.connect(self.setDisabled_NetPanel_Config_GroupBox_CirATMT_Btn)
        self.NetPanel_Config_GroupBox_CirATMT_Btn = QPushButton("Ok")
        self.NetPanel_Config_GroupBox_CirATMT_Btn.setFixedWidth(30)
        self.NetPanel_Config_GroupBox_CirATMT_Btn.clicked.connect(self.get_SEMT)

        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_CirATMT_Label, 2, 1, 1, 1)
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_CirATMT_ComboBox, 2, 2, 1, 1)
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_CirATMT_Btn, 2, 3, 1, 1)

        self.NetPanel_Config_GroupBox_SEMT_Label = QLabel("SE - Média Tensão")
        self.NetPanel_Config_GroupBox_SEMT_ComboBox = QComboBox()
        self.NetPanel_Config_GroupBox_SEMT_Btn = QPushButton("Ok")
        self.NetPanel_Config_GroupBox_SEMT_ComboBox.currentIndexChanged.connect(self.setDisabled_NetPanel_Config_GroupBox_SEMT_Btn)
        self.NetPanel_Config_GroupBox_SEMT_Btn.setFixedWidth(30)
        self.NetPanel_Config_GroupBox_SEMT_Btn.clicked.connect(self.get_FieldsMT)

        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_SEMT_Label, 3, 1, 1, 1)
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_SEMT_ComboBox, 3, 2, 1, 1)
        self.NetPanel_Config_GroupBox_Layout.addWidget(self.NetPanel_Config_GroupBox_SEMT_Btn, 3, 3, 1, 1)

        self.NetPanel_Config_GroupBox.setLayout(self.NetPanel_Config_GroupBox_Layout)

        self.Deck_GroupBox_Layout.addRow(self.NetPanel_Config_GroupBox) # Adiciona o Grupo de Configuração ao Deck

        ############## Alimentadores ######################

        self.NetPanel_Fields_GroupBox = QGroupBox("&Alimentadores")
        self.NetPanel_Fields_GroupBox_Layout = QGridLayout()

        self.NetPanel_Fields_GroupBox_Select = QGroupBox("&Selecione os Alimentadores")
        self.NetPanel_Fields_GroupBox_Select_Layout = QVBoxLayout(self)


        self.NetPanel_Fields_GroupBox_Select_TreeWidget = QTreeWidget()
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.setHeaderLabels(['Alimentador', 'Cor'])
        # self.NetPanel_Fields_GroupBox_TreeWidget.setColumnWidth(250,30)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(0, 190)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(1, 20)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.itemClicked.connect(self.checkOnSelectAllFields)


        self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll = QCheckBox("Selecionar todos os alimentadores")
        self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll.clicked.connect(self.onSelectAllFields)
        self.NetPanel_Fields_GroupBox_Select_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll)
        self.NetPanel_Fields_GroupBox_Select_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select_TreeWidget)





        self.NetPanel_Fields_GroupBox_Select.setLayout(self.NetPanel_Fields_GroupBox_Select_Layout)

        self.NetPanel_Fields_GroupBox_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select)

        self.NetPanel_Fields_GroupBox.setLayout(self.NetPanel_Fields_GroupBox_Layout)

        self.Deck_GroupBox_Layout.addRow(self.NetPanel_Fields_GroupBox)  # Adiciona

        #####################################

        self.Deck_GroupBox_MapView_Btn = QPushButton("Visualizar")
        self.Deck_GroupBox_MapView_Btn.setIcon(QIcon('img/icon_map.png'))
       # self.Deck_GroupBox_MapView_Btn.setFixedWidth(300)
        self.Deck_GroupBox_MapView_Btn.clicked.connect(self.execView)

        self.Deck_GroupBox_Layout.addRow(self.Deck_GroupBox_MapView_Btn)
        #####################################

        self.Deck_GroupBox.setLayout(self.Deck_GroupBox_Layout)

        self.setWidget(self.Deck_GroupBox)

        ######## Disabilitando os botões
        self.setDisabled_NetPanel_Config_GroupBox_SEAT_Btn()
        self.NetPanel_Config_GroupBox_SEAT_Btn.setEnabled(False)
        ###########################


    @property
    def MainWidget(self):
        return self.__parent

    @MainWidget.setter
    def MainWidget(self, value):
        self.__parent = value

    #Métodos dos Botões

    def get_CirATMT (self): #INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA
        self.mainActions.getCirAT_MT_DB(self.getSelectedSEAT())

    def get_SEMT(self): #metodo_INFORMA_SUBESTACAO_DE_MEDIA)
        self.set_SEMT(self.getSelectedSEMT_CirATMT())

    def get_FieldsMT(self): #metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO)
        self.mainActions.getSE_MT_AL_DB(self.getSelectedSEMT())

    ### Métodos para Acesso da Classe

    def getSelectedSEAT (self): #IN

        if self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText()

    def get_CirATMT_Selected (self): #INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA
        if self.NetPanel_Config_GroupBox_CirATMT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_CirATMT_ComboBox.currentText()

    def getSelectedSEMT_CirATMT(self): #   PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO
        return [self.get_CirATMT_Selected()[-3:]]

    def getSelectedSEMT(self): #metodo_INFORMA_SUBESTACAO_DE_MEDIA)
        if self.NetPanel_Config_GroupBox_SEMT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_SEMT_ComboBox.currentText()


    ######################################################################################
    def getSelectedFieldsNames(self):

        listFields = []

        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                listFields.append(Item.name)

        return listFields

    def getSelectedFieldsColors(self):

        listFieldsColors = []

        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                listFieldsColors.append(Item.getColor())
        return listFieldsColors

    ########################################################################################


    def set_SEAT(self, dadosSEAT):
        self.NetPanel_Config_GroupBox_SEAT_ComboBox.clear()
        self.NetPanel_Config_GroupBox_SEAT_ComboBox.addItems(dadosSEAT)

    def set_CirATMT(self, dadosCirATMT):
        self.NetPanel_Config_GroupBox_CirATMT_ComboBox.clear()
        self.NetPanel_Config_GroupBox_CirATMT_ComboBox.addItems(dadosCirATMT)

    def set_SEMT(self, dadosSE):
        self.NetPanel_Config_GroupBox_SEMT_ComboBox.clear()
        self.NetPanel_Config_GroupBox_SEMT_ComboBox.addItems(dadosSE)

    def set_SEMT_Fields(self, dadosFields):

        # Fazer uma função para Predeterminar as cores
        # melhora a questão das multiplas adiciones

        self.NetPanel_Fields_GroupBox_Select_TreeWidget.clear()

        for ctd in range(0, len(dadosFields)):
            NetPanel_Fields_GroupBox_Select_TreeWidget_Item(self.NetPanel_Fields_GroupBox_Select_TreeWidget,
                                                     dadosFields[ctd],
                                                     config.colorsList[random.randint(0, len(config.colorsList) -1 )])



    ############# Configuração para aparecer ou não os botões ################
    def setDisabled_NetPanel_Config_GroupBox_SEAT(self):
        self.NetPanel_Config_GroupBox_SEAT_ComboBox.clear()
        self.NetPanel_Config_GroupBox_SEAT_Btn.setEnabled(False)

    def setDisabled_NetPanel_Config_GroupBox_SEAT_Btn(self):
        self.NetPanel_Config_GroupBox_SEAT_Btn.setEnabled(True)
        self.NetPanel_Config_GroupBox_CirATMT_ComboBox.clear()
        self.setDisabled_NetPanel_Config_GroupBox_CirATMT_Btn()
        self.NetPanel_Config_GroupBox_CirATMT_Btn.setEnabled(False)


    def setDisabled_NetPanel_Config_GroupBox_CirATMT_Btn(self):
        self.NetPanel_Config_GroupBox_CirATMT_Btn.setEnabled(True)
        self.NetPanel_Config_GroupBox_SEMT_ComboBox.clear()
        self.setDisabled_NetPanel_Config_GroupBox_SEMT_Btn()
        self.NetPanel_Config_GroupBox_SEMT_Btn.setEnabled(False)


    def setDisabled_NetPanel_Config_GroupBox_SEMT_Btn(self):
        self.NetPanel_Config_GroupBox_SEMT_Btn.setEnabled(True)
        self.Deck_GroupBox_MapView_Btn.setEnabled(True)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.clear()
        self.setDisabled_NetPanel_Fields_GroupBox_Select_Btn()

    def setDisabled_NetPanel_Fields_GroupBox_Select_Btn(self):

        self.Deck_GroupBox_MapView_Btn.setEnabled(False)

        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)
            if Item.checkState(0) == Qt.Checked:
                self.Deck_GroupBox_MapView_Btn.setEnabled(True)

            self.mainActions.updateToobarMenu()

        ##Alteração dos alimentadores obriga rodar o LoadData

            self.mainActions.fieldsChangedDSS()

    def onSelectAllFields(self):

        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)
            Item.setCheckState(0, self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll.checkState())

        self.setDisabled_NetPanel_Fields_GroupBox_Select_Btn()

    def checkOnSelectAllFields(self):

        ctdChecked = True
        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)
            if Item.checkState(0) == Qt.Unchecked:
                self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll.setCheckState(Qt.Unchecked)
                ctdChecked = False

        if ctdChecked:
            self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll.setCheckState(Qt.Checked)

        self.setDisabled_NetPanel_Fields_GroupBox_Select_Btn()

    #############################################

    ### Executa o Mapa e passa os parâmetros
    def execView(self):
        self.mainActions.execMapView()

        ### Executa o LoadData para agilizar
        self.mainActions.execLoadDataDSS()



class NetPanel_Fields_GroupBox_Select_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(NetPanel_Fields_GroupBox_Select_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:


        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Unchecked)

        self.color = color

        ## Column 1 - Button:
        self.TreeWidget_Item_Btn = QPushButton()
        self.TreeWidget_Item_Btn.setFixedSize(50, 20)
        self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
        self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
        self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)


    @property
    def name(self):
        return self.text(0)

    def getColor(self):
        return self.color

    def setColor(self):
        self.openColorDialog()

    def openColorDialog(self):

        colorSelectDialog = QColorDialog()

        colorSelected = colorSelectDialog.getColor()

        if colorSelected.isValid():
            self.color = colorSelected.name()
            self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + colorSelected.name() + '}')


class C_ResultsPanel(QDockWidget):

    def __init__(self, MainWidget):
        QDockWidget.__init__(self)
        self.MainWidget = MainWidget

        self.mainActions = main_actions.C_MainActions

        self.setWindowTitle("Resultados")
        self.setLayout(QFormLayout())
        self.setContentsMargins(2, 0, 0, 0)
        self.hide()

        self.InitUI()

    def InitUI(self):

        ## Tabs
        self.TabWidget = QTabWidget()
        ######
        self.reloadTabs() ##Carregando os Tabs
        self.setWidget(self.TabWidget)

    def reloadTabs(self):

        for ctd in range(0, self.TabWidget.count()):
            self.TabWidget.removeTab(ctd)

        ##### Voltage

        self.TableVoltage = TableVoltageResults()  # QWidget
        self.TabWidget.addTab(self.TableVoltage, "Tensões")


class TableVoltageResults(QTableWidget):
    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):

        columnsTable = ('Barras', 'Va (kV)', '\u03B8a ( \u03B1 )', 'Vb (kV)', '\u03B8b ( \u03B1 )', 'Vc (kV)', '\u03B8c ( \u03B1 )', \
                        'Va (pu)', '\u03B8a ( \u03B1 )', 'Vb (pu)', '\u03B8b ( \u03B1 )', 'Vc (pu)', '\u03B8c ( \u03B1 )')

        self.setColumnCount(len(columnsTable))

        self.setHorizontalHeaderLabels(columnsTable)

        self.setEditTriggers(QTableWidget.NoEditTriggers)



