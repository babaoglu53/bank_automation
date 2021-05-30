from PyQt5 import QtGui, QtWidgets

class Message:
    def showMessage(message, title):
        mes = QtWidgets.QMessageBox()
        mes.setWindowIcon(QtGui.QIcon(':/icons/logo.png'))
        mes.setIcon(QtWidgets.QMessageBox.Information)
        mes.setText(message)
        mes.setInformativeText("")
        mes.setWindowTitle(title)
        mes.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mes.exec_()

    def showYesNoMessage(message, title):
        mes = QtWidgets.QMessageBox()
        mes.setWindowIcon(QtGui.QIcon(':/icons/logo.png'))
        mes.setIcon(QtWidgets.QMessageBox.Warning)
        mes.setText(message)
        mes.setInformativeText("")
        mes.setWindowTitle(title)
        mes.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        mes.button(QtWidgets.QMessageBox.Yes).setText("Evet")
        mes.button(QtWidgets.QMessageBox.No).setText("Hayır")
        return mes.exec_()