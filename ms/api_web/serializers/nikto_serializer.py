from ms.helpers import time
from ms.serializers import Serializer


class NiktoSerializer(Serializer):
    response = {
        "id": str,
        "username": str,
        "email": str,
        "is_active": bool,
    }

