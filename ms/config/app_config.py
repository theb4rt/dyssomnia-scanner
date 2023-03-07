import os
from ms import app




app_config = {
    'APP_NAME': os.getenv('APP_NAME', 'app'),
    'APP_VERSION': os.getenv('APP_VERSION', '1.0.0'),
    'SECRET_KEY': os.getenv('APP_SECRET_KEY', None),
    'TIMEZONE': os.getenv('APP_TIMEZONE', 'UTC'),
    'URL_PREFIX': '/api/v1/',
    "S3_BUCKET_NAME": os.getenv('S3_BUCKET_NAME', None),
    "S3_KEY": os.getenv('S3_KEY', None),
    "S3_SECRET": os.getenv('S3_SECRET', None),
    "JWT_ALGORITHM": os.getenv('JWT_ALGORITHM', 'RS256'),
    "APP_ROOT": os.path.dirname(app.instance_path),
    "JWT_SECRET_KEY": os.path.join(os.path.dirname(app.instance_path), '.ssh', 'jwtRSA256-private.pem'),
    "JWT_PUBLIC_KEY": os.path.join(os.path.dirname(app.instance_path), '.ssh', 'jwtRSA256-public.pem'),
}

