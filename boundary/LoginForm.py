# boundary/LoginForm.py
from PyQt5.QtWidgets import *
from control.LoginService import LoginService


class LoginForm(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.loginService = LoginService()

        self.setWindowTitle("Login")
        self.resize(380, 250)

        self.txtAccount = QLineEdit()
        self.txtAccount.setPlaceholderText("Enter Account")

        self.txtPassword = QLineEdit()
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setPlaceholderText("Enter Password")

        self.btnLogin = QPushButton("Login")
        self.btnBack = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h3>User Login</h3>"))
        layout.addWidget(self.txtAccount)
        layout.addWidget(self.txtPassword)
        layout.addWidget(self.btnLogin)
        layout.addWidget(self.btnBack)
        self.setLayout(layout)

        self.btnLogin.clicked.connect(self.login)
        self.btnBack.clicked.connect(self.goBack)

    def login(self):
        account = self.txtAccount.text().strip()
        password = self.txtPassword.text().strip()

        if not account or not password:
            QMessageBox.warning(self, "Warning", "Please enter account and password.")
            return

        user = self.loginService.login(account, password)

        if user:
            QMessageBox.information(self, "Success", f"Welcome, {user.username}!")
            
            from boundary.MainForm import MainForm
            self.mainForm = MainForm(self, user) 
            self.mainForm.show()
            self.hide() 
        else:
            QMessageBox.critical(self, "Error", "Invalid account or password.")

    def goBack(self):
        if self.parent:
            self.parent.show()
        self.close()