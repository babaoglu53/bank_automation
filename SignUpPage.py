from SignUp import Ui_MainWindow
from VerificationPage import VerificationPage
from PyQt5 import QtCore, QtWidgets
from Database import Database
from Message import Message

class SignUpPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb

        self.ui.pushButton_signUp.clicked.connect(self.signUp)
        

    def signUp(self):
        self.name = self.ui.lineEdit_name.text()
        self.surname = self.ui.lineEdit_surname.text()
        self.age = self.ui.lineEdit_age.text()
        self.email = self.ui.lineEdit_email.text()
        self.username = self.ui.lineEdit_username.text()
        self.password = self.ui.lineEdit_password.text()
        self.password_repeat = self.ui.lineEdit_passwordRepeat.text()
        

        if self.name == "" or self.surname == "" or self.age == "" or self.email == "" or self.username == "" or self.password == "" or self.password_repeat == "":
            Message.showMessage("Lütfen tüm alanları doldurduğunuzdan emin olunuz!", "Uyarı")
        else:
            if self.password != self.password_repeat:
                Message.showMessage("Şifreler birbirleriyle uyuşmuyor!", "Uyarı")
            else:
                self.verification_page = VerificationPage("Kayıt için gerekli kodunuz aşağıdaki gibidir:")
                self.hide()
                self.verification_page.show()
                self.verification_page.ui.label_temp_email.setText(self.email)
                self.verification_page.ui.lineEdit_info.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        if self.verification_page.ui.lineEdit_info.text() == "Girilen Kod Doğru":
            self.verification_page.close()
            try:
                self.db.insertQuery("customer", "(cus_name, cus_surname, cus_email, cus_username, cus_password, cus_age)", "(%s, %s, %s, %s, %s, %s)", (self.name, self.surname, self.email, self.username, self.password, self.age), self.db.getCursor(self.db_connection))
                Message.showMessage("Hesabınız başarıyla oluşturuldu.\nHesap bilgilerinizle giriş yapabilirsiniz.", "İşlem Başarılı")
            except:
                Message.showMessage("Hesabınız oluşturulamadı.", "İşlem Başarısız")
            self.db.executeQuery("INSERT INTO customer_balances (account_no, accountType, customer_balance) VALUES ((SELECT account_no FROM customer WHERE cus_email = '{}'), 'Türk Lirası', 0)".format(self.email), self.db.getCursor(self.db_connection))
            self.name, self.surname, self.email, self.username, self.password, self.age = "","","","","",""
            self.close()

