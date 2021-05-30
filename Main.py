from MainWindowPage import MainWindowPage
from PyQt5 import QtWidgets

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])
    window = MainWindowPage()
    window.show()
    app.exec_()