from PyQt5.QtWidgets import *

from boundary.LoginForm import LoginForm
from boundary.RegisterForm import RegisterForm


class FirstForm(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("First Page")
        self.resize(300, 200)

        self.loginBtn = QPushButton("Login")
        self.registerBtn = QPushButton("Register")

        layout = QVBoxLayout()
        layout.addWidget(self.loginBtn)
        layout.addWidget(self.registerBtn)
        self.setLayout(layout)

        self.loginBtn.clicked.connect(self.openLogin)
        self.registerBtn.clicked.connect(self.openRegister)

    def openLogin(self):

        self.login = LoginForm()

        self.login.show()

        self.close()   # ⭐关键：关闭当前窗口

    def openRegister(self):

        self.register = RegisterForm()

        self.register.show()

        self.close()