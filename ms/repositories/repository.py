import abc

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from ms.db import db, Model
from ms.helpers import time
from typing import Any, Dict, Optional
from ms.utils.logger import error_logger, info_logger


class Repository(abc.ABC):
    def __init__(self) -> None:
        self._model = self.get_model()
        self._db = db

    @abc.abstractmethod
    def get_model(self) -> None:
        pass

    def db_save(self, model: Model = None, commit: bool = True) -> None:
        try:
            self._db.session.add(model)
            if commit:
                self._db.session.commit()
        except SQLAlchemyError as e:
            self._db.session.rollback()
            error_logger.error(e)
            raise e

    def db_delete(self, model: Model = None, commit: bool = True) -> None:
        try:
            self._db.session.delete(model)
            if commit:
                self._db.session.commit()
        except SQLAlchemyError as e:
            self._db.session.rollback()
            error_logger.error(e)
            raise e

    def add(self, data: Dict[str, Any]) -> Model:
        instance = self._model()
        self.db_save(instance)
        return instance

    def all(
        self,
        order_column: str = 'created_at',
        order: str = 'desc',
        paginate: bool = False,
        page: int = 1,
        per_page: int = 15
    ) -> Any:
        column = getattr(self._model, order_column)
        order_by = getattr(column, order)
        query = self._model.query.order_by(order_by())
        if paginate:
            return query.paginate(page, per_page=per_page)
        return query.all()

    def find(self, id: int, fail: bool = True) -> Optional[Model]:
        instance = self._model.query.get(id)
        if not instance and fail:
            # Handle the error or raise an appropriate exception
            raise Exception(f"Instance with ID {id} not found.")
        return instance

    def find_by_attr(
        self,
        column: str,
        value: Any,
        fail: bool = True
    ) -> Optional[Model]:
        query = self._model.query.filter(getattr(self._model, column) == value)
        instance = query.first()
        if not instance and fail:
            raise Exception(f"No instance found with {column}={value}.")
        return instance

    def find_optional(self, filter: Dict[str, Any], fail: bool = True) -> Optional[Model]:
        filters = [getattr(self._model, key) == val for key, val in filter.items()]
        query = self._model.query.filter(or_(*filters))
        instance = query.first()
        if not instance and fail:
            raise Exception(f"No instance found with the provided filter.")
        return instance

    def update(self, id: int, data: Dict[str, Any], fail: bool = True) -> Optional[Model]:
        instance = self.find(id, fail=fail)
        if instance:
            instance.update(data)
            instance.updated_at = time.now()
            self.db_save(instance)
        return instance

    def delete(self, id: int, fail: bool = True) -> Optional[Model]:
        instance = self.find(id, fail=fail)
        if instance:
            self.db_delete(instance)
        return instance
