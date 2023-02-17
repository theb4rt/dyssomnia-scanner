from marshmallow import ValidationError


def is_valid(schema, data):
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
