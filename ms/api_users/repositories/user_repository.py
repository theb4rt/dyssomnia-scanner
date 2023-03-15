from ms.api_users.models.user import User
from ms.repositories import Repository


class UserRepository(Repository):

    def get_model(self):
        return User

    def add(self, data):
        if self.check_unique_user(data['username'], data['email']):
            user = self._model(data)
            user.is_active = True
            user.is_admin = False
            self.db_save(user)
            return user
        return None

    def find_user(self, id):
        q = self._model.query.filter_by(id=id)
        users = q.all()
        return users if len(users) > 0 else False

    def find_user_by_username(self, username):
        q = self._model.query.filter_by(username=username)
        user = q.first()
        return user

    def find_user_by_email(self, email):
        q = self._model.query.filter_by(email=email)
        user = q.first()
        return user

    def check_unique_user(self, username, email):
        user = self.find_user_by_username(username)
        if user is not None:
            return False
        user = self.find_user_by_email(email)
        if user is not None:
            return False
        return True

    def check_admin(self, id):
        user = self.find(id=id)
        if user is not None:
            return user.is_admin
        return False
