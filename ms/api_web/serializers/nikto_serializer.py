from ms.helpers import time
from ms.serializers import Serializer


class NiktoSerializer(Serializer):
    response = {
        "id": str,
        "scan_data": str,
        "target_url": str,
        "ip_address": bool,
        "user_id": str,
    }
