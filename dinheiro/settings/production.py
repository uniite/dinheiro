import os
from dinheiro.settings.base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ['SECRET_KEY']

if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'dinheiro'),
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', 3306),
        'OPTIONS': {
            'ssl': {
                'ca': os.environ.get('DB_CA_PATH', '/app/config/rds-ca-2015-us-east-1.pem')
            }
        }
    }
}

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER
# Assumes nginx or smilar is running as a SSL proxy in front of this app
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
