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
    
    def logout(self) -> None:
        try:
            print("User session cleared successfully.")
        except Exception as e:
            print(f"Logout cleanup error: {e}")