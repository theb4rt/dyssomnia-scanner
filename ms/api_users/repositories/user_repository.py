from sqlalchemy.exc import SQLAlchemyError

from ms.api_users.models import User, Person

from ms.repositories import Repository
from ms.db import db


class UserRepository(Repository):
    def __init__(self):
        super().__init__()
        self.person_model = Person

    def get_model(self):
        return User

    def add_new_user(self, user_data: dict, person_data: dict):
        if self.check_unique_user(user_data['username'], user_data['email']):
            user = self._model(user_data)
            user.is_active = True
            user.is_admin = False
            self.db_save(user, commit=False)
            person = self.person_model(person_data)
            user.person = person
            self.db_save(person)
            return user
        return False

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
