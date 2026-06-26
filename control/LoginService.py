from dao.UserDAO import UserDAO


class LoginService:

    def __init__(self):

        self.userDAO = UserDAO()

    def login(
            self,
            account,
            password):

        user = self.userDAO.findByAccount(account)

        if user is None:
            return None

        if user.password != password:
            return None

        return user