from PyQt5.QtWidgets import *
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
        from boundary.LoginForm import LoginForm
        self.loginForm = LoginForm(self) 
        self.loginForm.show()
        
        self.hide()

    def openRegister(self):
        self.registerForm = RegisterForm(self) 
        self.registerForm.show()
        self.hide()