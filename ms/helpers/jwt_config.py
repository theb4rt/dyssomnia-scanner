from jose import jwt
from ms import app
from ms.helpers.time import epoch_now
from cryptography.hazmat.primitives import serialization
import os


class JwtHelper:
    def __init__(self, algorithms='RS256',
                 token_lifetime=43200,
                 refresh_token_lifetime=86400,
                 token_type='Bearer'):
        self.private_key_path = app.config.get('JWT_SECRET_KEY')
        self.public_key_path = app.config.get('JWT_PUBLIC_KEY')
        self.algorithms = algorithms
        self.token_type = token_type
        self.token_lifetime = token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def load_private_key(self) -> str | None:
        if os.path.exists(self.private_key_path):
            with open(self.private_key_path, 'r') as key_file:
                key = key_file.read()
            return key
        print('Private key not found')
        return None

    def load_public_key(self) -> str | None:
        if os.path.exists(self.public_key_path):
            key = open(self.public_key_path, 'r').read()
            return key
        print('Public key not found')
        return None

    def encode(self, payload, lifetime) -> str:
        payload['exp'] = epoch_now() + lifetime
        encoded = jwt.encode(payload, self.load_private_key(), algorithm=self.algorithms)
        return encoded

    def decode(self, token) -> dict:
        token = token.replace(self.token_type, '').strip()
        payload = jwt.decode(token, self.load_public_key(), algorithms=self.algorithms)
        return payload

    def get_tokens(self, payload) -> dict:
        token = self.encode(payload, self.token_lifetime)
        refresh_token = self.encode(payload, self.refresh_token_lifetime)
        return {
            'token': token,
            'refresh_token': refresh_token,
        }

    def check(self, token: str) -> bool | None:
        try:
            payload = self.decode(token)
            return epoch_now() <= payload['exp']
        except (jwt.JWTError,
                jwt.ExpiredSignatureError,
                KeyError) as e:
            print(str(e))
            return False
