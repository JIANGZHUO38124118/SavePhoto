from PyQt5.QtWidgets import *
from control.LoginService import LoginService


class MainForm(QWidget):

    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user

        self.loginService = LoginService()

        self.setWindowTitle(f"Main Menu - {self.user.username}")
        self.resize(400, 350)

        self.btnPersonal = QPushButton("Personal Space")
        self.btnCommunity = QPushButton("Community")
        self.btnLogout = QPushButton("Logout")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"<h3>Hello, {self.user.username}!</h3>"))
        layout.addSpacing(20)
        layout.addWidget(self.btnPersonal)
        layout.addWidget(self.btnCommunity)
        layout.addSpacing(20)
        layout.addWidget(self.btnLogout)
        self.setLayout(layout)

        self.btnPersonal.clicked.connect(self.goPersonal)
        self.btnCommunity.clicked.connect(self.goCommunity)
        self.btnLogout.clicked.connect(self.logout)

    def goPersonal(self):
        from boundary.PersonalForm import PersonalForm
        self.personalForm = PersonalForm(self, self.user)
        self.personalForm.show()
        self.hide()

    def goCommunity(self):
        from boundary.CommunityForm import CommunityForm
        self.communityForm = CommunityForm(self)
        self.communityForm.show()
        self.hide()

    def logout(self):
        reply = QMessageBox.question(
            self, "Logout", "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.loginService.logout()

            if self.parent:
                self.parent.show()
            else:
                from boundary.FirstForm import FirstForm
                self.firstForm = FirstForm()
                self.firstForm.show()
                
            self.close()