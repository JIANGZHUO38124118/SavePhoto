from PyQt5.QtWidgets import *

from control.RegisterService import RegisterService


class RegisterForm(QWidget):

    def __init__(self):
        super().__init__()

        self.service = RegisterService()

        self.setWindowTitle("Register")

        self.accountEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.usernameEdit = QLineEdit()

        self.registerBtn = QPushButton("Register")

        layout = QFormLayout()

        layout.addRow("Account", self.accountEdit)
        layout.addRow("Password", self.passwordEdit)
        layout.addRow("Username", self.usernameEdit)
        layout.addRow(self.registerBtn)

        self.setLayout(layout)

        self.registerBtn.clicked.connect(self.register)

    def register(self):

        result = self.service.register(
            self.accountEdit.text(),
            self.passwordEdit.text(),
            self.usernameEdit.text()
        )

        if result:
            QMessageBox.information(self, "Success", "Register Success")
        else:
            QMessageBox.warning(self, "Error", "Account Exists")