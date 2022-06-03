from PyQt5.QtWidgets import QLabel, QFormLayout, QGroupBox, QDockWidget, QGridLayout, QComboBox, QPushButton, QCheckBox, \
    QVBoxLayout, QTreeWidget, QTreeWidgetItem, QColorDialog, QTabWidget, QTableWidget, QMessageBox
from PyQt5.QtCore import Qt
import random
from PyQt5.QtGui import QColor, QIcon
import main_actions
import class_exception
import config
import class_panels_dock_TD_dialog

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
        self.Deck_GroupBox.setFixedWidth(500)

        self.Deck_GroupBox_Layout = QFormLayout()


        ###### Configuração #####################

        self.NetPanel_Config_GroupBox = QGroupBox("&Configuração")

        self.NetPanel_Config_GroupBox_Layout = QGridLayout()

        self.NetPanel_Config_GroupBox_SEAT_Label = QLabel("SE - Alta Tensão")
        self.NetPanel_Config_GroupBox_SEAT_ComboBox = QComboBox()
        self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentIndexChanged.connect(self.setDisabled_NetPanel_Config_GroupBox_SEAT_Btn)
        self.NetPanel_Config_GroupBox_SEAT_Btn = QPushButton("Ok")
        self.NetPanel_Config_GroupBox_SEAT_Btn.setFixedWidth(30)
        self.NetPanel_Config_GroupBox_SEAT_Btn.clicked.connect(self.get_FieldsMT)

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
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.setHeaderLabels(['Alimentador', 'Cor', 'BT', '','']) #Alterado para visualizar a BT
        # self.NetPanel_Fields_GroupBox_TreeWidget.setColumnWidth(250,30)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(0, 180)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(1, 70)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(2, 15)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.headerItem().setTextAlignment(2, Qt.AlignCenter)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(3, 15)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.header().resizeSection(4, 15)
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.itemClicked.connect(self.checkOnSelectAllFields)

        self.NetPanel_Fields_GroupBox_Select_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select_TreeWidget)


        self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll = QCheckBox("Selecionar todos os alimentadores")
        self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll.clicked.connect(self.onSelectAllFields)
        self.NetPanel_Fields_GroupBox_Select_Layout.addWidget(self.NetPanel_Fields_GroupBox_Select_Checkbox_SelectAll)


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
        self.mainActions.getSE_MT_AL_DB(self.getSelectedSEAT())

    ### Métodos para Acesso da Classe

    def getSelectedSEAT (self):

        if self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText()

    def get_CirATMT_Selected (self): #INFORMA_CIRCUITO_DE_ALTA_PARA_MEDIA
        if self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText():
            print(self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText())
            return self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText()

    #def getSelectedSEMT_CirATMT(self): #   PASSA_O_NOME_DA_SUBESTACAO_DE_MEDIA_ASSOCIADA_AO_CIRCUITO_DE_ALTA_PARA_MEDIA_SELECIONADO
        #return [self.get_CirATMT_Selected()[-3:]]

    def getSelectedSEMT(self): #metodo_INFORMA_SUBESTACAO_DE_MEDIA)
        if self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText():
            return self.NetPanel_Config_GroupBox_SEAT_ComboBox.currentText()


    ######################################################################################
    def getSelectedFieldsNames(self, fieldID=None):

        listFields = []
        listFieldsID = []

        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)
            if Item.checkState(0) == Qt.Checked:
                listFields.append(Item.name)
                listFieldsID.append(ctd)
            print("listFields", listFields)
        if fieldID:
            return [listFields, listFieldsID]
        else:
            return listFields


    def getSelectedFieldsColors(self):

        listFieldsColors = []

        for ctd in range(0, self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItemCount()):
            Item = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(ctd)

            if Item.checkState(0) == Qt.Checked:
                listFieldsColors.append(Item.getColor())

        return listFieldsColors

    ########################################################################################

    ######################################################################################
    def getSelectedTDFieldsNames(self, idItemField):

        listTDFields = []

        ItemParent = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(idItemField)

        for ctd in range(0, ItemParent.childCount()):

            Item = ItemParent.child(ctd)

            if Item.checkState(0) == Qt.Checked:
                listTDFields.append(Item.name)

        return listTDFields


    ######################################################################################
    def getSelectedTDFieldsNamesALL(self):

        listTDFieldsAll = []

        listFields = self.getSelectedFieldsNames(True)

        for ctdAL in range(0, len(listFields[0])):
            listTDFields =self.getSelectedTDFieldsNames(listFields[1][ctdAL])

            for ctdTD in listTDFields:
                listTDFieldsAll.append(ctdTD)

        return listTDFieldsAll

    def getSelectedTDFieldsColors(self, idItemField):

        listTDFieldsColors = []

        ItemParent = self.NetPanel_Fields_GroupBox_Select_TreeWidget.topLevelItem(idItemField)

        for ctd in range(0, ItemParent.childCount()):

            Item = ItemParent.child(ctd)

            if Item.checkState(0) == Qt.Checked:
                listTDFieldsColors.append(Item.getColor())

        return listTDFieldsColors

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
        vetor_nomes=[]
        self.NetPanel_Fields_GroupBox_Select_TreeWidget.clear()
        for ctd in range(0, len(dadosFields)):
            vetor_nomes.append(dadosFields[ctd][0])
            listTrafos = self.mainActions.getSE_MT_AL_TD_DB(dadosFields[ctd][1])
            NetPanel_Fields_GroupBox_Select_TreeWidget_Item(self.NetPanel_Fields_GroupBox_Select_TreeWidget,
                                                                      dadosFields[ctd][0], dadosFields[ctd][1],
                                                                      config.colorsList[ctd],
                                                                      listTrafos, vetor_nomes)





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
    def __init__(self, parent, name, codField, color, listTrafosAL, vetor_nomes):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(NetPanel_Fields_GroupBox_Select_TreeWidget_Item, self).__init__(parent)

        ### Dialog Transformador de Distribuição


        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        #print(self.flags())
        self.setCheckState(0, Qt.Unchecked)
        self.color = color
        self.codField = codField
        self.listTrafos = listTrafosAL
        self.vetor_nomes = vetor_nomes

        ## Column 1 - Button:
        self.TreeWidget_Item_Btn = QPushButton()
        self.TreeWidget_Item_Btn.setFixedSize(50, 20)
        self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
        self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
        self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)

        ## Column 2:
        self.TreeWidget_Item_Add_Btn = QPushButton()
        self.TreeWidget_Item_Add_Btn.setFixedSize(20, 20)
        self.TreeWidget_Item_Add_Btn.setIcon(QIcon('img/icon_add.png'))
        self.TreeWidget_Item_Add_Btn.clicked.connect(self.openTDDialog)
        self.treeWidget().setItemWidget(self, 2, self.TreeWidget_Item_Add_Btn)

        ## Column 3:
        self.TreeWidget_Item_Remove_Btn = QPushButton()
        self.TreeWidget_Item_Remove_Btn.setFixedSize(20, 20)
        self.TreeWidget_Item_Remove_Btn.setIcon(QIcon('img/icon_remove.png'))
        self.TreeWidget_Item_Remove_Btn.clicked.connect(self.removerTrafo)
        self.treeWidget().setItemWidget(self, 3, self.TreeWidget_Item_Remove_Btn)

        ## Column 4:
        self.TreeWidget_Item_CheckALL_Btn = QCheckBox()
        self.TreeWidget_Item_CheckALL_Btn.setFixedSize(20, 20)
        self.TreeWidget_Item_CheckALL_Btn.clicked.connect(self.onSelectAllTDs)
        self.treeWidget().setItemWidget(self, 4, self.TreeWidget_Item_CheckALL_Btn)

        ########

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

    def getListTrafoOtimizado(self): #faz a lista de transfomadores de forma que não se repita na seleção

        listTrafoOtimizado = self.listTrafos.copy()

        for ctd in range(0, self.childCount()):
            Item = self.child(ctd)

            if Item.name in listTrafoOtimizado:
                listTrafoOtimizado.remove(Item.name)

        return listTrafoOtimizado


    def openTDDialog(self):

        soma = []
        massa=[]
        i = 0
        listTrafoOtimizado = self.getListTrafoOtimizado()
        copia_lista_cores = config.colorsList.copy()
        if listTrafoOtimizado:
            self.dialogTD = class_panels_dock_TD_dialog.C_TDDialog(listTrafoOtimizado)
            self.dialogTD.Dilalog_Field_TD_LineEdit.setText(self.name)
            self.dialogTD.listTrafos = listTrafoOtimizado
            #self.dialogTD.updateListTrafoDIST()
            self.dialogTD.exec()
            while self.name != self.vetor_nomes[i]:
                i = i + 1
            copia_lista_cores.pop(i)
            for contador_colors in range(len(copia_lista_cores)):
                soma.append(contador_colors)
            if self.dialogTD.codTrafoDIST:
                for cont in range(len(self.dialogTD.codTrafoDIST)//(len(copia_lista_cores)) + 1):
                    massa.extend(soma)
                for inde, ctd in zip(range(len(self.listTrafos)-len(listTrafoOtimizado), len(self.dialogTD.codTrafoDIST)+(len(self.listTrafos)-len(listTrafoOtimizado))), self.dialogTD.codTrafoDIST):
                    NetPanel_Fields_GroupBox_Select_TreeWidget_Child_Item(self,
                                                                        ctd,
                                                                        copia_lista_cores[massa[inde]])
                self.checkOnSelectAllTDs()
            self.setExpanded(True)

        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Rede de Baixa Tensão")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setText("Todas as Redes de Baixa Tensão já foram selecionadas!")
            msgBox.exec()

    def removerTrafo(self):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Rede de Baixa Tensão")
        msgBox.setStandardButtons(QMessageBox.Ok)

        if self.childCount() > 0:

            contChecked = 0

            for ctd in reversed(range(0, self.childCount())):
                Item = self.child(ctd)
                if Item.checkState(0) == Qt.Checked:
                    self.removeChild(Item)
                    contChecked += 1

            if contChecked > 0:
                msgBox.setText(str(contChecked) + " transformador(es) removido(s)!")
                msgBox.exec()
            else:
                msgBox.setText("Nenhuma transformador selecionado!")
                msgBox.exec()

        else:
            msgBox.setText("Não existe(m) Rede(s) Baixa Tensão carregada(s) para esse alimentador!")
            msgBox.exec()


    def onSelectAllTDs(self):

        for ctd in range(0, self.childCount()):
            Item = self.child(ctd)
            Item.setCheckState(0, self.TreeWidget_Item_CheckALL_Btn.checkState())

    def checkOnSelectAllTDs(self):
        ctdChecked = True

        for ctd in range(0, self.childCount()):
            Item = self.child(ctd)
            if Item.checkState(0) == Qt.Unchecked:
                self.TreeWidget_Item_CheckALL_Btn.setCheckState(Qt.Unchecked)
                ctdChecked = False

        if ctdChecked:
            self.TreeWidget_Item_CheckALL_Btn.setCheckState(Qt.Checked)


class NetPanel_Fields_GroupBox_Select_TreeWidget_Child_Item(QTreeWidgetItem):
    def __init__(self, parent, name, color):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(NetPanel_Fields_GroupBox_Select_TreeWidget_Child_Item, self).__init__(parent)


        ### Dialog Transformador de Distribuição
        #self.dialogTD = class_panels_dock_TD_dialog.C_TDDialog(listatrafos)

        ## Column 0 - Text:
        self.setText(0, name)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Checked)
        self.color = color

        ## Column 1 - Button:
        self.TreeWidget_Item_Btn = QPushButton()
        self.TreeWidget_Item_Btn.setFixedSize(50, 20)
        self.TreeWidget_Item_Btn.setStyleSheet('QPushButton {background-color:' + QColor(self.color).name() + '}')
        self.TreeWidget_Item_Btn.clicked.connect(self.setColor)
        self.treeWidget().setItemWidget(self, 1, self.TreeWidget_Item_Btn)

        self.treeWidget().itemClicked.connect(self.parent().checkOnSelectAllTDs)


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



