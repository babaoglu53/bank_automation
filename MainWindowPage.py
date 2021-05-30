from ForgetPasswordPage import ForgetPasswordPage
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer, QDateTime, pyqtSignal
from MainWindow import Ui_MainWindow
from qtwidgets import AnimatedToggle
from SignUpPage import SignUpPage
from CustomerPage import CustomerPage
from Database import Database
import qdarkstyle
from Message import Message

class MainWindowPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)

        current_date = QDateTime.currentDateTime()
        display_date = current_date.toString("dd/MM/yyyy")
        self.ui.label_date.setText(display_date)
        
        self.ui.pushButton_login.clicked.connect(self.loginCheck)
        self.ui.lineEdit_password.returnPressed.connect(self.loginCheck)

        self.light_style = "#centralwidget{\nborder-image: url(:/icons/bnkglass.jpg);\n}"
        self.dark_style = qdarkstyle.load_stylesheet_pyqt5()
        
        animated_toggle= AnimatedToggle(
            checked_color="#000000",
            pulse_checked_color="#696969",
            pulse_unchecked_color="#FFFFFF"
        )
        
        self.ui.formLayout_switchButton.addWidget(animated_toggle)
        animated_toggle.clicked.connect(self.changeTheme)

        self.ui.label_themeMode.setText("Light Mode")
        
        self.signup_page = SignUpPage()
        
        self.ui.pushButton_createAcc.clicked.connect(self.showSignUpPage)

        self.db = Database("localhost", 3306, "root", "", "bank")
        self.db_connection = self.db.mydb

        
        self.customer_page = CustomerPage()
        
        self.customer_page.ui.label_date.setText(display_date)
        self.customer_page.ui.pushButton_signOut.clicked.connect(self.showMainWindow)

        self.username_signal = pyqtSignal(str)

        self.ui.label_forgetPassword.mousePressEvent = self.on_click
        self.forget_password_page = ForgetPasswordPage()
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    def showSignUpPage(self):
        self.signup_page.show()
    
    def showCustomerPage(self):
        self.customer_page.show()
        #self.customer_page.ui.label_username.setText(self.username)
        self.customer_page.ui.label_accountNo.setText(str(self.login_result [0]))
        self.customer_page.updateAmount()

    def changeTheme(self):
        if self.ui.label_themeMode.text() == "Light Mode":
            self.ui.label_themeMode.setText("Dark Mode")
            self.setStyleSheet(self.dark_style)
        else:
            self.ui.label_themeMode.setText("Light Mode")
            self.setStyleSheet(self.light_style)
    
    def displayTime(self):
        current_time = QTime.currentTime()
        display_text = current_time.toString("hh:mm:ss")
        self.ui.label_time.setText(display_text)
        self.customer_page.ui.label_time.setText(display_text)

    def loginCheck(self):
        self.username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        
        if self.username == "" or password == "":
            Message.showMessage("Lütfen kullanıcı adı ve şifre girdiğinizden emin olunuz..", "Uyarı")
            
        else:
            self.login_result = self.db.selectQuery("*", "customer", self.db.getCursor(self.db_connection), "one", "cus_username=%s and cus_password=%s", (self.username, password))
            if self.login_result != None:
                self.ui.lineEdit_password.clear()
                self.hide()
                self.showCustomerPage()

            else:
                self.ui.lineEdit_password.clear()
                Message.showMessage("Lütfen doğru kullanıcı adı ve şifre girdiğinizden emin olunuz..", "Uyarı")

    def on_click(self, event):
        self.forget_password_page.show()

    def forgetPassword(self):
        print("forget password")

    def showMainWindow(self):
        self.show()