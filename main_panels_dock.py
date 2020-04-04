from PyQt5.QtWidgets import QLabel, QFormLayout, QGroupBox, QDockWidget, QGridLayout, QComboBox, QPushButton, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QTreeWidget, QTreeWidgetItem, QColorDialog
from PyQt5.QtCore import Qt
import random
from PyQt5.QtGui import QColor
import main_actions
import class_exception


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
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.itemClicked.connect(
            self.setDisabled_NetPanel_Fields_GroupBox_Select_Btn)

        self.NetPanel_Fields_GroupBox_Select_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select_TreeWidget)

        self.NetPanel_Fields_GroupBox_Select.setLayout(self.NetPanel_Fields_GroupBox_Select_Layout)

        self.NetPanel_Fields_GroupBox_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select)

        self.NetPanel_Fields_GroupBox.setLayout(self.NetPanel_Fields_GroupBox_Layout)

        self.Deck_GroupBox_Layout.addRow(self.NetPanel_Fields_GroupBox)  # Adiciona

        ######################################

        ###### Opções #####################

        self.NetPanel_Options_GroupBox = QGroupBox("&Itens para Mostrar")
        self.NetPanel_Options_GroupBox_Layout = QGridLayout()

        self.NetPanel_Options_GroupBox_TreeWidget = QTreeWidget()
        self.NetPanel_Options_GroupBox_TreeWidget.setHeaderLabels(['Item','Option'])
        #self.NetPanel_Options_GroupBox_TreeWidget.setColumnWidth(250,30)
        self.NetPanel_Options_GroupBox_TreeWidget.header().resizeSection(0,190)
        self.NetPanel_Options_GroupBox_TreeWidget.header().resizeSection(1, 20)
        self.NetPanel_Options_GroupBox_TreeWidget.hideColumn(1)

        self.NetPanel_Options_GroupBox_Layout.addWidget(self.NetPanel_Options_GroupBox_TreeWidget, 1, 1, 1, 1)

        self.NetPanel_Options_GroupBox.setLayout(self.NetPanel_Options_GroupBox_Layout)

        self.Deck_GroupBox_Layout.addRow(self.NetPanel_Options_GroupBox)  # Adiciona o Grupo de Alimentadores ao Deck

        #####################################

        self.Deck_GroupBox_MapView_CheckBox = QCheckBox("Visualizar o Mapa")
        self.Deck_GroupBox_MapView_CheckBox.setChecked(True)
        self.Deck_GroupBox_Layout.addRow(self.Deck_GroupBox_MapView_CheckBox)

        #####################################

        self.Deck_GroupBox_MapView_Btn = QPushButton("Visualizar")
        self.Deck_GroupBox_MapView_Btn.setFixedWidth(300)
        self.Deck_GroupBox_MapView_Btn.clicked.connect(self.execView)

        self.Deck_GroupBox_Layout.addRow(self.Deck_GroupBox_MapView_Btn)
        #####################################



        self.Deck_GroupBox.setLayout(self.Deck_GroupBox_Layout)

        self.setWidget(self.Deck_GroupBox)

        ######## Disabilitando os botões
        self.setDisabled_NetPanel_Config_GroupBox_SEAT_Btn()
        self.NetPanel_Config_GroupBox_SEAT_Btn.setEnabled(False)
        ###########################
        # Carrega as opções
        self.NetPanel_Options_GroupBox_TreeWidget_LoadOptions()


    @property
    def MainWidget(self):
        return self.__parent

    @MainWidget.setter
    def MainWidget(self, value):
        self.__parent = value

    #Métodos dos Botões

    def get_CirATMT (self): #INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA
        self.mainActions.getCirAT_MT_DB(self.get_SEAT_Selected())

    def get_SEMT(self): #metodo_INFORMA_SUBESTACAO_DE_MEDIA)
        self.set_SEMT(self.get_SEMT_CirATMT_Selected())

    def get_FieldsMT(self): #metodo_FORMA_LAYOUT_ALIMENTADORES_DA_SUBESTACAO_DE_MEDIA_TENSAO)
        self.mainActions.getSE_MT_AL_DB(self.get_SEMT_Selected())

    ### Métodos para Acesso da Classe

    def get_SEAT_Selected (self): #IN

        if self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText()

    def get_CirATMT_Selected (self): #INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA
        if self.NetPanel_Config_GroupBox_CirATMT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_CirATMT_ComboBox.currentText()

    def get_SEMT_CirATMT_Selected (self): #   PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO
        return [self.get_CirATMT_Selected()[-3:]]

    def get_SEMT_Selected(self): #metodo_INFORMA_SUBESTACAO_DE_MEDIA)
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
        return  listFieldsColors

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

        ##colorsList = QColor.colorNames()
        colorsList = ['aqua', 'aquamarine', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood',
             'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue',
             'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen',
             'darkorange', 'darkorchid', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey',
             'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
             'forestgreen', 'fuchsia', 'gainsboro', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew',
             'hotpink', 'indigo', 'khaki', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
             'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue',
             'lightslategray', 'lightslategrey', 'lightsteelblue', 'lime', 'limegreen', 'magenta', 'maroon',
             'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue',
             'mediumspringgreen', 'mediumturquoise', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navy',
             'oldlace', 'olive', 'olivedrab', 'orange', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
             'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rosybrown', 'royalblue',
             'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
             'slategray', 'slategrey', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'transparent',
             'turquoise', 'violet', 'wheat', 'yellow', 'yellowgreen']

        for ctd in range(0, len(dadosFields)):
            NetPanel_Fields_GroupBox_Select_TreeWidget_Item(self.NetPanel_Fields_GroupBox_Select_TreeWidget,
                                                     dadosFields[ctd],
                                                     colorsList[random.randint(0, len(colorsList))])



    ############# Configuração para aparecer ou não os botões ################



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


    #############################################
    def NetPanel_Options_GroupBox_TreeWidget_LoadOptions(self):
        NetPanel_Options_GroupBox_TreeWidget_Item(self.NetPanel_Options_GroupBox_TreeWidget , "Capacitores", "CAP")

    ### Executa o Mapa e passa os parâmetros
    def execView(self):
        listOptions = []
        for ctd in range(0, self.NetPanel_Options_GroupBox_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Options_GroupBox_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                listOptions.append(Item.getOption())
                print(Item.getOption())


        self.mainActions.execMapView(self.Deck_GroupBox_MapView_CheckBox, listOptions)


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


class NetPanel_Options_GroupBox_TreeWidget_Item(QTreeWidgetItem):
    def __init__(self, parent, name, option):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(NetPanel_Options_GroupBox_TreeWidget_Item, self).__init__(parent)

        ## Column 0 - Text:
        self.option = option
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Unchecked)
        self.setText(1, option)

    @property
    def name(self):
        return self.text(0)

    def getOption(self):
        return self.option












