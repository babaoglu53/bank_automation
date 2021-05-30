from Message import Message
from PasswordConfirmationPage import PasswordConfirmationPage
from VerificationPage import VerificationPage
from Message import Message
from ForgetPassword import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from Database import Database

class ForgetPasswordPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb

        self.ui.pushButton.clicked.connect(self.forgetPasswordButton)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
    def onTextChanged(self):
        self.close()
        if self.verification_page.ui.lineEdit_info.text() == "Girilen Kod Doğru":
            self.verification_page.close()
            self.password_confirmation_page = PasswordConfirmationPage()
            self.password_confirmation_page.show()
            self.password_confirmation_page.ui.label_temp.setText(str(self.account_no))

    def forgetPasswordButton(self):
        textbox_email = self.ui.lineEdit.text()

        if textbox_email == "":
            Message.showMessage("Lütfen doğru bir e-posta adresi girdiğinizden emin olunuz.", "Uyarı")
            self.ui.lineEdit.clear()
            return

        try:
            self.account_no = self.db.otherSelectQuery("SELECT account_no FROM customer WHERE cus_email='{}'".format(textbox_email), self.db.getCursor(self.db_connection), "one")[0]
            self.verification_page = VerificationPage("Şifre değiştirmek için gerekli kodunuz aşağıdaki gibidir:")
            self.hide()
            self.verification_page.show()
            self.verification_page.ui.label_temp_email.setText(textbox_email)
            self.verification_page.ui.lineEdit_info.textChanged.connect(self.onTextChanged)
        
        except TypeError:
            Message.showMessage("Lütfen doğru bir e-posta adresi girdiğinizden emin olunuz.", "Uyarı")
            self.ui.lineEdit.clear()
            return
