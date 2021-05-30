from Database import Database
from PyQt5 import QtCore
from Verification import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from Message import Message
from Mail import Mail
import random
from time import sleep

DURATION_INT = 200

class VerificationPage(QtWidgets.QMainWindow):
    def __init__(self, message_text):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb
        
        self.message_text = message_text
        
        self.time_left_int = DURATION_INT

        self.verification_key = self.generateRandomNumber()

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        self.mail_sender = Mail()
        self.mail = "info.bb.bank@yandex.com"
        self.mail_pass = "123456789+bb"

        self.user_email = ""
        
        print("\nKod: " + str(self.verification_key))
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerTimeout)
        self.timer.start(1000)
        self.ui.lineEdit.textChanged.connect(self.onTextBoxChanged)
        
        self.count = 1

        self.ui.label_temp_email.close()

    def onTextBoxChanged(self):
        user_input = self.ui.lineEdit.text()

        if not user_input.isdecimal():
            self.ui.lineEdit_info.setText("Lütfen sayı giriniz!")
            return
        
        if len(user_input) == 0:
            self.ui.lineEdit_info.setText("")
            return

        if len(user_input) != 6:
            self.ui.lineEdit_info.setText(user_input)
            return
        
        if int(user_input) != self.verification_key:
            self.ui.lineEdit_info.setText("Girilen Kod Yanlış")
            return

        self.ui.lineEdit_info.setText("Girilen Kod Doğru")

    def timerTimeout(self):
        self.time_left_int -= 1

        if self.time_left_int == 0:
            if self.ui.lineEdit_info.text() == "Girilen Kod Doğru":
                return
            Message.showMessage("Süreniz zaman aşımına uğramıştır.", "Uyarı")
            self.timer.stop()
            self.close()

        self.updateGui()

    def updateGui(self):
        if self.count == 1:
            self.user_email = self.ui.label_temp_email.text()
            self.mail_sender.sendMailForVerification("Kod Doğrulama", self.message_text, self.verification_key, self.mail, self.mail_pass, self.user_email)
            self.count = 2
        self.ui.label_2.setText(str(self.time_left_int))

    def generateRandomNumber(self):
        return random.randint(100000, 1000000)
