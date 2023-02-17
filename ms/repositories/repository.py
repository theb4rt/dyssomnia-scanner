import abc
from sqlalchemy import or_
from ms.db import db, Model
from ms.helpers import time


class Repository(abc.ABC):
    def __init__(self) -> None:
        self._model = self.get_model()
        self._db = db

    @abc.abstractmethod
    def get_model(self):
        pass

    def db_save(self, model=None):
        db.session.add(model)
        db.session.commit()

    def db_delete(self, model):
        db.session.delete(model)
        db.session.commit()

    def add(self, data):
        user = self._model(data)
        self.db_save(user)
        return user

    def all(
        self,
        order_column='created_at',
        order='desc',
        paginate=False,
        page=1,
        per_page=15):
        column = getattr(self._model, order_column)
        order_by = getattr(column, order)
        q = self._model.query.order_by(order_by())
        return q.paginate(page, per_page=per_page) if paginate else q.all()

    def find(self, id, fail=True):
        q = self._model.query.filter_by(id=id)
        q.first()

    def find_by_attr(self, column, value, fail=True):
        q = self._model.query.filter_by(**{column: value})
        return q.first_or_404() if fail else q.first()

    def find_optional(self, filter, fail=True):
        filters = [
            getattr(self._model, key) == val for key,
            val in filter.items()]
        q = self._model.query.filter(or_(*filters))
        return q.first_or_404() if fail else q.first()

    def update(self, id, data, fail=True):
        model = self.find(id, fail=fail)
        if model is not None:
            model.update(data)
            model.updated_at = time.now()
            self.db_save(model)
        return model

    def delete(self, id, fail=True):
        model = self.find(id, fail=fail)
        if model is not None:
            self.db_delete(model)
        return model
