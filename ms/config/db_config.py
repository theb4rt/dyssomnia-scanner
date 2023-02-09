import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO')

db_config = {
    'SQLALCHEMY_DATABASE_URI': f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ECHO': SQLALCHEMY_ECHO  # True or False to enable/disable print queries in console
}
print('b4rt')
print(db_config)
