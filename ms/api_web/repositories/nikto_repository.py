from ms.api_web.models.nikto import NiktoScanResults
from ms.repositories import Repository
from ms.db import db


class NiktoRepository(Repository):
    def __init__(self):
        super().__init__()

    def get_model(self):
        return NiktoScanResults

    def add(self, data):
        print('b4444444rt2')
        print('b4444444rt2')
        print('b4444444rt2')
        print('b4444444rt2')
        print(data)
        instance = self._model(data)
        self.db_save(instance)
        return instance

