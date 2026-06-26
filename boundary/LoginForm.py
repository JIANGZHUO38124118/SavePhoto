from PyQt5.QtWidgets import *

from control.LoginService import LoginService
from boundary.MainForm import MainForm


class LoginForm(QWidget):

    def __init__(self):
        super().__init__()

        self.service = LoginService()

        self.setWindowTitle("Login")
        self.resize(300, 200)

        self.account = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.btn = QPushButton("Login")

        layout = QFormLayout()
        layout.addRow("Account", self.account)
        layout.addRow("Password", self.password)
        layout.addRow(self.btn)
        self.setLayout(layout)

        self.btn.clicked.connect(self.login)

    def login(self):

        user = self.service.login(
            self.account.text(),
            self.password.text()
        )

        if user:

            self.main = MainForm(user)

            self.main.show()

            self.close()   # ⭐关键

        else:
            QMessageBox.warning(self, "Error", "Login Failed")