import os
from dinheiro.settings.base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ['SECRET_KEY']

if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dinheiro.sqlite3',
        # 'USER': 'root',
        # 'PASSWORD': '',
        # 'HOST': os.environ['MYSQL_HOST'],
        # 'PORT': os.environ['MYSQL_PORT'],
    }
}
