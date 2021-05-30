from Mail import Mail
from Payment import Ui_MainWindow
from PyQt5 import QtWidgets
from Database import Database
from Message import Message

class PaymentPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.payment)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb
        
        self.mail_sender = Mail()
        self.mail = "info.bb.bank@yandex.com"
        self.mail_pass = "123456789+bb"

        self.ui.label_temp.close()

    def getAccountNo(self):
        return self.ui.label_temp.text()
    
    def getAccountEmail(self):
        result = self.db.otherSelectQuery("SELECT cus_email FROM customer WHERE account_no={}".format(self.getAccountNo()), self.db.getCursor(self.db_connection), "one")
        return result[0]

    def payment(self):
        self.amount = str(int(self.db.selectQuery("customer_balance", "customer_balances", self.db.getCursor(self.db_connection), "one", "account_no=" + self.getAccountNo() +  " AND accountType='Türk Lirası'")[0]))
        text_amount = self.ui.lineEdit.text()
        
        if not text_amount.isdecimal():
            Message.showMessage("Lütfen doğru bir değer girdiğinizden emin olunuz", "İşlem Başarısız")
            return
        
        if int(text_amount) > int(self.amount) or int(text_amount) <= 0:
            Message.showMessage("Hesabınızda yeterli bakiye bulunmamaktadır.", "Yetersiz Bakiye")
            return
        
        last_money = str(int(self.amount) - int(text_amount))

        self.db.executeQuery("UPDATE customer_balances SET customer_balance = " + last_money + " WHERE account_no = " + self.getAccountNo(), self.db.getCursor(self.db_connection))
        
        self.db.insertToTransactions(self.getAccountNo(), self.ui.comboBox.currentText() + " Ödemesi Yapıldı", text_amount, self.db.getCursor(self.db_connection))
        self.mail_sender.sendMailForMoneyTransactions("Bilgilendirme Mesajı", "Hesabınızdan Ödeme Yapıldı",  self.ui.comboBox.currentText() + " Ödemesi Yapıldı", self.getAccountNo(), text_amount, self.mail, self.mail_pass, self.getAccountEmail())
        self.ui.lineEdit.clear()


    def closeEvent(self, event):
        self.ui.comboBox.clear()

