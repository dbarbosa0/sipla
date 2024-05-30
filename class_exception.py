from PyQt6 import QtGui
from  PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon


# define Python user-defined exceptions
class C_Error(Exception):
    pass

class ConnDataBaseError(C_Error):
    def __init__(self, msgText):
        super(ConnDataBaseError, self).__init__()
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "Data Base Connection Error",
                          msgText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()

class ExecDataBaseError(C_Error):
    def __init__(self, msgText):
        super(ExecDataBaseError, self).__init__()
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "Data Base Execution Error",
                          msgText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()

class FileDataBaseError(C_Error):
    def __init__(self, msgText, errorText = None):
        super(FileDataBaseError, self).__init__()
        if errorText is None:
            errorText = ""
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "Data Base Error",
                          msgText + "\n" + errorText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()

class ExecOpenDSS(C_Error):
    def __init__(self, msgText, errorText = None):
        if errorText is None:
            errorText = ""

        super(ExecOpenDSS, self).__init__(errorText)
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "OpenDSS Execution Error",
                          msgText + "\n" + errorText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()

class ExecSelectionFields(C_Error):
    def __init__(self, msgText, errorText = None):
        if errorText is None:
            errorText = ""

        super(ExecSelectionFields, self).__init__(errorText)
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "Selection Error",
                          msgText + "\n" + errorText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()

class ExecConfigOpenDSS(C_Error):
    def __init__(self, msgText, errorText = None):
        if errorText is None:
            errorText = ""

        super(ExecConfigOpenDSS, self).__init__(errorText)
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "OpenDSS Configuration Error",
                          msgText + "\n" + errorText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()


class ExecEnergyMeter(C_Error):
    def __init__(self, msgText):
        super(ExecEnergyMeter, self).__init__()
        # Display the errors
        msg = QMessageBox(QMessageBox.Icon.Warning, "Insert Error",
                          msgText,
                          QMessageBox.StandardButton.Ok)
        msg.setWindowIcon(QtGui.QIcon("Imagens/logo.png"))
        msg.exec_()
