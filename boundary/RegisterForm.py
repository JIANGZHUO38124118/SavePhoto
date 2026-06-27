from PyQt5.QtWidgets import *
from control.RegisterService import RegisterService 

class RegisterForm(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.registerService = RegisterService() 

        self.setWindowTitle("Register")
        self.resize(400, 300)

        self.txtAccount = QLineEdit()
        self.txtAccount.setPlaceholderText("Account")

        self.txtPassword = QLineEdit()
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setPlaceholderText("Password")

        self.txtUserName = QLineEdit()
        self.txtUserName.setPlaceholderText("User Name")

        self.btnRegister = QPushButton("Register")
        self.btnBack = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h3>Create Account</h3>"))
        layout.addWidget(self.txtAccount)
        layout.addWidget(self.txtPassword)
        layout.addWidget(self.txtUserName)
        layout.addWidget(self.btnRegister)
        layout.addWidget(self.btnBack)
        self.setLayout(layout)

        self.btnRegister.clicked.connect(self.register)
        self.btnBack.clicked.connect(self.goLogin)

    def register(self):
        account = self.txtAccount.text().strip()
        password = self.txtPassword.text().strip()
        username = self.txtUserName.text().strip()

        if not account or not password or not username:
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        success = self.registerService.register(account, password, username)

        if success:
            QMessageBox.information(self, "Success", "Registration successful!")
            self.switchBack()
        else:
            QMessageBox.critical(self, "Error", "Registration failed. Account already exists!")

    def goLogin(self):
        self.switchBack()

    def switchBack(self):
        if hasattr(self.parent, 'goLogin'):
            self.parent.goLogin()  
        else:
            self.parent.show()
            self.parent.raise_()
        self.close()