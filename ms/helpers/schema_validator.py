from typing import Any, Tuple, Union, Dict, List

from flask_marshmallow import Schema
from marshmallow import ValidationError


def is_valid_data(schema: Schema, data: Any) -> tuple[bool, dict[str, str]] | tuple[bool, Any] | tuple[bool, list[Any]] | tuple[bool, list[str]]:
    if data is None:
        return False, {"error": "Invalid Json"}
    try:
        result = schema.load(data=data)
        return True, result
    except ValidationError as e:
        return False, list(e.args)
    except ValueError as e:
        return False, list(e.args)
    except Exception as e:
        print(e.args)
        return False, list({"error": "Unknown error"})
