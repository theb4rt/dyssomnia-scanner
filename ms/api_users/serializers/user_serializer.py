from ms.helpers import time
from ms.serializers import Serializer


class RegisterSerializer(Serializer):
    response = {
        "id": str,
        "username": str,
        "email": str,
        "is_active": bool,
    }
