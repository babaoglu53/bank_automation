from Mail import Mail
from PyQt5 import QtCore
from PaymentPage import PaymentPage
from Customer import Ui_MainWindow
from PyQt5 import QtWidgets
from Database import Database
from Message import Message
from TransactionsPage import TransactionsPage

class CustomerPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtWidgets.qApp.focusChanged.connect(self.on_focusChanged)

        self.setWindowFlags(QtCore.Qt.WindowTitleHint)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb

        self.ui.pushButton_signOut.clicked.connect(self.signOut)
        self.ui.pushButton_depositingMoney.clicked.connect(self.depositingMoney)
        self.ui.pushButton_withdrawMoney.clicked.connect(self.withdrawMoney)

        self.ui.pushButton_send.clicked.connect(self.sendMoney)
        
        self.account_history_page = TransactionsPage()

        self.ui.pushButton_accountHistory.clicked.connect(self.accountHistory)

        self.ui.pushButton_deleteAccount.clicked.connect(self.deleteAccount)

        self.ui.pushButton_debtMoney.clicked.connect(lambda: self.showPaymentPage("borc"))
        self.ui.pushButton_institution.clicked.connect(lambda: self.showPaymentPage("egitim"))
        self.ui.pushButton_donation.clicked.connect(lambda: self.showPaymentPage("bagis"))

        self.mail_sender = Mail()
        self.mail = "info.bb.bank@yandex.com"
        self.mail_pass = "123456789+bb"


    def on_focusChanged(self):
        if self.isActiveWindow():
            self.ui.label_username.setText(self.getAccountName())
            self.updateAmount()

    def signOut(self):
        self.close()

    def getAccountNo(self):
        return self.ui.label_accountNo.text()
    
    def getAccountName(self):
        try:
            result = self.db.otherSelectQuery("SELECT cus_name, cus_surname FROM customer WHERE account_no={}".format(self.getAccountNo()), self.db.getCursor(self.db_connection), "one")
            return result[0] + " " + result[1]
        except TypeError:
            pass

    def getAccountEmail(self):
        result = self.db.otherSelectQuery("SELECT cus_email FROM customer WHERE account_no={}".format(self.getAccountNo()), self.db.getCursor(self.db_connection), "one")
        return result[0]

    def updateAmount(self):
        self.amount = str(int(self.db.selectQuery("customer_balance", "customer_balances", self.db.getCursor(self.db_connection), "one", "account_no=" +self.getAccountNo()+  " AND accountType='T??rk Liras??'")[0]))
        self.ui.label_amount.setText(self.amount)
        self.ui.label_amount_2.setText(self.amount)
        self.ui.label_amount_3.setText(self.amount)
        self.ui.label_amount_4.setText(self.amount)

    def depositingMoney(self):
        money = self.ui.lineEdit_depositingMoney.text()

        if not money.isdecimal():
            Message.showMessage("L??tfen do??ru bir de??er girdi??inizden emin olunuz", "????lem Ba??ar??s??z")
            self.ui.lineEdit_depositingMoney.clear()
            return

        money_to_send = str(int(self.amount) + int(money))

        try:
            self.db.executeQuery("UPDATE customer_balances SET customer_balance = " + money_to_send + " WHERE account_no = " + self.getAccountNo(), self.db.getCursor(self.db_connection))
            self.updateAmount()
            self.ui.lineEdit_depositingMoney.clear()
            Message.showMessage("Paran??z Yat??r??ld??", "????lem Ba??ar??l??")
            self.db.insertToTransactions(self.getAccountNo(), "Para Yat??r??ld??", money, self.db.getCursor(self.db_connection))
            self.mail_sender.sendMailForMoneyTransactions("Bilgilendirme Mesaj??", "Hesab??n??za Para Yat??r??ld??",  "Para Yat??r??ld??", self.getAccountNo(), money, self.mail, self.mail_pass, self.getAccountEmail())
        except:
            Message.showMessage("Paran??z Yat??r??lamad??", "????lem Ba??ar??s??z")

    def withdrawMoney(self):
        withdraw_money = self.ui.lineEdit_withdrawMoney.text()

        if not withdraw_money.isdecimal():
            Message.showMessage("L??tfen do??ru bir de??er girdi??inizden emin olunuz", "????lem Ba??ar??s??z")
            self.ui.lineEdit_withdrawMoney.clear()
            return

        money_to_withdraw = int(self.amount) - int(withdraw_money)
        print(money_to_withdraw)

        if int(withdraw_money) <= 0 or money_to_withdraw < 0 or int(self.amount) <= 0:
            Message.showMessage("Hesab??n??zda yeterli bakiye bulunmamaktad??r.", "Yetersiz Bakiye")

        else:
            try:
                money_to_withdraw = str(money_to_withdraw)
                self.db.executeQuery("UPDATE customer_balances SET customer_balance = " + money_to_withdraw + " WHERE account_no = " + self.getAccountNo(), self.db.getCursor(self.db_connection))
                self.updateAmount()
                self.ui.lineEdit_withdrawMoney.clear()
                Message.showMessage("Paran??z ??ekildi", "????lem Ba??ar??l??")
                self.db.insertToTransactions(self.getAccountNo(), "Para ??ekildi", withdraw_money, self.db.getCursor(self.db_connection))
                self.mail_sender.sendMailForMoneyTransactions("Bilgilendirme Mesaj??", "Hesab??n??zdan Para ??ekildi", "Para ??ekildi", self.getAccountNo(), withdraw_money, self.mail, self.mail_pass, self.getAccountEmail())
            except:
                Message.showMessage("Paran??z ??ekilemedi", "????lem Ba??ar??s??z")

    def sendMoney(self):
        to_be_sent_account_no = self.ui.lineEdit_toBeSentAccountNo.text()
        to_be_sent_amount = self.ui.lineEdit_toBeSentAmount.text()

        if to_be_sent_account_no == "" or to_be_sent_amount == "":
            Message.showMessage("L??tfen bir de??er girdi??inizden emin olunuz", "????lem Ba??ar??s??z")
            return
            
        if not to_be_sent_amount.isdecimal():
            Message.showMessage("L??tfen do??ru bir de??er girdi??inizden emin olunuz", "????lem Ba??ar??s??z")
            self.ui.lineEdit_toBeSentAmount.clear()
            return

        try:
            to_be_sent_account_amount = self.db.selectQuery("customer_balance", "customer_balances", self.db.getCursor(self.db_connection), "one", "account_no=" + to_be_sent_account_no +  " AND accountType='T??rk Liras??'")[0]
        except TypeError:
            Message.showMessage("L??tfen do??ru bir hesap numaras?? girdi??inizden emin olunuz", "????lem Ba??ar??s??z")
            self.ui.lineEdit_toBeSentAccountNo.clear()
            self.ui.lineEdit_toBeSentAmount.clear()
            return

        if int(self.amount) <= 0 or int(to_be_sent_amount) > float(self.amount):
            Message.showMessage("Hesab??n??zda yeterli bakiye bulunmamaktad??r.", "Yetersiz Bakiye")
            self.ui.lineEdit_toBeSentAmount.clear()

        else:
            to_be_sent_end_account_amount = int(to_be_sent_amount) + to_be_sent_account_amount
            new_amount = int(self.amount) - int(to_be_sent_amount)
            self.db.executeQuery("UPDATE customer_balances SET customer_balance = " + str(to_be_sent_end_account_amount) + " WHERE account_no = " + to_be_sent_account_no, self.db.getCursor(self.db_connection))
            self.db.executeQuery("UPDATE customer_balances SET customer_balance = " + str(new_amount) + " WHERE account_no = " + self.getAccountNo(), self.db.getCursor(self.db_connection))
            self.ui.lineEdit_toBeSentAccountNo.clear()
            self.ui.lineEdit_toBeSentAmount.clear()
            self.updateAmount()
            Message.showMessage("Paran??z G??nderildi", "????lem Ba??ar??l??")
            self.db.insertToTransactions(self.getAccountNo(), "Para G??nderildi", to_be_sent_amount, self.db.getCursor(self.db_connection))
            self.mail_sender.sendMailForMoneyTransactions("Bilgilendirme Mesaj??", "Hesab??n??zdan Para G??nderildi", to_be_sent_account_no + " Numaral?? Hesaba Para G??nderildi", self.getAccountNo(), to_be_sent_amount, self.mail, self.mail_pass, self.getAccountEmail())
            to_be_sent_account_email = self.db.otherSelectQuery("SELECT cus_email FROM customer WHERE account_no={}".format(to_be_sent_account_no), self.db.getCursor(self.db_connection), "one")[0]
            self.mail_sender.sendMailForMoneyTransactions("Bilgilendirme Mesaj??", "Hesab??n??za Para Geldi", self.getAccountNo() + " Numaral?? Hesaptan Para Geldi", to_be_sent_account_no, to_be_sent_amount, self.mail, self.mail_pass, to_be_sent_account_email)

    def accountHistory(self):
        self.account_history_page.ui.label_temp.setText(self.getAccountNo())
        self.account_history_page.show()

    def deleteAccount(self):
        return_value = Message.showYesNoMessage("Hesab??n??z?? silmek istedi??inizden emin misiniz?", "Hesab??m?? Sil")
        if return_value == QtWidgets.QMessageBox.Yes:
            columns = ["customer", "customer_balances", "registration", "transactions"]
            for column in columns:
                self.db.executeQuery("DELETE FROM {} WHERE account_no=".format(column) + self.getAccountNo(), self.db.getCursor(self.db_connection))
                self.close()

    def showPaymentPage(self, func_name):
        self.payment_page = PaymentPage()
        self.payment_page.ui.label_temp.setText(self.getAccountNo())
        
        if func_name == "borc":
            names = [   
                        "Cebe TL Y??kleme",
                        "Fatura ??deme",
                        "SGK/SSK/BA??KUR",
                        "Sigorta ve Emeklilik",
                        "Trafik ??demeleri",
                        "Vergiler ve Resmi Kurumlar"
                    ]

        if func_name == "egitim":
            names = [   
                        "KYK",
                        "MEB",
                        "??SYM",
                        "Sigorta ve Emeklilik",
                        "??niversite Har?? ve S??nav ??demeleri"
                    ]

        if func_name == "bagis":
            names = [   
                        "AFAD",
                        "Be??ir Derne??i",
                        "Biz Bize Yeteriz T??rkiyem",
                        "Cansuyu",
                        "Dar??laceze Ba??kanl??????",
                        "Dar??????afaka",
                        "Deniz Feneri",
                        "??HH ??nsani Yard??m Vakf??",
                        "??yilikder Derne??i",
                        "Karde??eli Derne??i",
                        "K??z??lay",
                        "L??SEV",
                        "Miras??m??z Kud??s Derne??i",
                        "Ogem Vakf??",
                        "Omurilik Fel??lileri Derne??i",
                        "Sadaka Ta???? Yard??m Derne??i",
                        "??efkateli ??nsani Yard??m Derne??i",
                        "TSK Vakf??",
                        "T??rk Hava Kurumu",
                        "T??rk Polis Te??kilat??n?? G????lendirme Vakf??",
                        "T??rkiye Diyanet Vakf??",
                        "T??rkiye Maarif Vakf??",
                        "Vuslat Derne??i",
                        "Yard??meli",
                        "Yery??z?? Doktorlar?? Derne??i",
                        "Ye??ilay Derne??i",
                        "Z????EV"
                    ]

        for name in names:
            self.payment_page.ui.comboBox.addItem(name)
        
        self.payment_page.show()

    def focusInEvent(self, event):
        print("burdaaa")






