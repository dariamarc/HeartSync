
class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def login(self, username, password):
        return self.user_repo.login(username, password)

    def signup(self, username, password, email, firstname, lastname):
        # TODO: Move email confirmation in service
        return self.user_repo.signup(username, password, email, firstname, lastname)

    def confirm_email(self, email_token):
        return self.user_repo.confirm_email(email_token)

    def get_user_by_token(self, token):
        return self.user_repo.get_user_by_token(token)