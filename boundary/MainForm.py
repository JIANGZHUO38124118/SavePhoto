from PyQt5.QtWidgets import *

from boundary.PersonalForm import PersonalForm
from boundary.CommunityForm import CommunityForm


class MainForm(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Main Menu")
        self.resize(400, 300)

        self.label = QLabel(f"Welcome {user.username}")

        self.personalBtn = QPushButton("Personal Photos")
        self.communityBtn = QPushButton("Community")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.personalBtn)
        layout.addWidget(self.communityBtn)

        self.setLayout(layout)

        self.personalBtn.clicked.connect(self.openPersonal)
        self.communityBtn.clicked.connect(self.openCommunity)

    def openPersonal(self):

        self.personalForm = PersonalForm(self, self.user)
        self.personalForm.show()
        self.hide()

    def openCommunity(self):

        self.communityForm = CommunityForm(self)
        self.communityForm.show()
        self.hide()