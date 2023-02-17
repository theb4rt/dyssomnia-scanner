import jwt
from ms import app
from ms.helpers.time import epoch_now


class JwtHelper():
    def __init__(self, algorithms='HS256',
                 token_lifetime=43200,
                 refresh_token_lifetime=86400,
                 token_type='Bearer'):
        self.key = app.config.get('SECRET_KEY')
        self.algorithms = algorithms
        self.token_type = token_type
        self.token_lifetime = token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def encode(self, payload, lifetime):
        payload['exp'] = epoch_now() + lifetime
        encoded = jwt.encode(payload, self.key, algorithm=self.algorithms)
        return encoded

    def decode(self, token):
        token = token.replace(self.token_type, '').strip()
        payload = jwt.decode(token, self.key, algorithms=self.algorithms)
        return payload

    def get_tokens(self, payload):
        token = self.encode(payload, self.token_lifetime)
        refresh_token = self.encode(payload, self.refresh_token_lifetime)
        return {
            'token': token,
            'refresh_token': refresh_token,
        }

    def check(self, token: str) -> bool:
        try:
            payload = self.decode(token)
            return epoch_now() <= payload['exp']
        except (jwt.InvalidSignatureError,
                jwt.DecodeError,
                jwt.ExpiredSignatureError,
                KeyError):
            return False
