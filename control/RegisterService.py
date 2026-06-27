from dao.UserDAO import UserDAO
from entity.User import User


class RegisterService:

    def __init__(self):
        self.userDAO = UserDAO()

    def register(self, account, password, username) -> bool:
        if self.checkAccount(account):
            return False

        user = User(
            None,
            account,
            password,
            username
        )

        self.userDAO.insertUser(user)
        return True

    def checkAccount(self, account) -> bool:
        return self.userDAO.findByAccount(account) is not None