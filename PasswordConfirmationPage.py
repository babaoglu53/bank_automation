from Database import Database
from PasswordConfirmation import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from Message import Message

class PasswordConfirmationPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.ui.pushButton.clicked.connect(self.changePassword)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb

        self.ui.label_temp.close()

    def getAccountNo(self):
        return self.ui.label_temp.text()

    def changePassword(self):
        password_text = self.ui.lineEdit.text()
        password_repeat_text = self.ui.lineEdit_2.text()

        if password_text == "" or password_repeat_text == "":
            Message.showMessage("Lütfen tüm alanları eksiksiz doldurduğunuzdan emin olunuz", "Uyarı")
            return
        
        if password_text != password_repeat_text:
            Message.showMessage("Girilen şifreler birbiriyle uyuşmuyor", "Uyarı")
            return
        
        try:
            self.db.executeQuery("UPDATE customer SET cus_password = " + password_text + " WHERE account_no = " + self.getAccountNo(), self.db.getCursor(self.db_connection))
            Message.showMessage("Şifreniz başarılı bir şekilde değiştirildi.", "İşlem Başarılı")
        except:
            Message.showMessage("Şifreniz değiştirilemedi.", "İşlem Başarısız")
        self.close()
