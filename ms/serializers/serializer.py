import types
from collections.abc import Iterable


class Serializer:
    response = dict()

    def __init__(self, model, collection=False, paginate=False):
        self.__data = None
        self.__original = model
        self.__model = model.items if paginate else model
        self.__is_paginated = paginate
        self.__is_collection = collection or paginate

    def get_data(self):
        self.__data = self.handler()
        return self.__data

    def handler(self):
        data = self.handler_collection(self.__model) \
            if self.__is_collection else self.serialize(self.__model)
        if self.__is_paginated:
            pagination_data = {
                'page': self.__original.page,
                'pages': self.__original.pages,
                'per_page': self.__original.per_page,
                'prev': self.__original.prev_num,
                'next': self.__original.next_num,
                'total': self.__original.total,
            }
            data = {'data': data, 'pagination': pagination_data}
        return data

    def handler_collection(self, collection):
        res = list()
        for model in collection:
            data = self.serialize(model)
            res.append(data)
        return res

    def serialize(self, model):
        data = dict()
        for attr, attrType in self.response.items():
            label = attr
            if isinstance(attrType, dict):
                if 'label' in attrType:
                    label = attrType.get('label')
                try:
                    attrType = attrType['type']
                except KeyError:
                    raise Exception(
                        f"The key `type` is required on the attribute {attr}")
            value = getattr(model, attr, None)
            if isinstance(attrType, types.FunctionType):
                data[label] = attrType(value)
            elif issubclass(attrType, Serializer):
                collection = isinstance(value, Iterable)
                serializer = attrType(value, collection=collection)
                data[label] = serializer.get_data()
            else:
                data[label] = attrType(value) if value is not None else None
        return data
