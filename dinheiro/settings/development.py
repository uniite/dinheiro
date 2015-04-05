from dinheiro.settings.base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'iy0c*kpd(_l)o27ye&t%#e&sq!yl=ob%0*(@a5i29t+p(05yds'

boxen_socket = os.environ.get('BOXEN_MYSQL_SOCKET')
if boxen_socket:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dinheiro',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': os.environ['BOXEN_MYSQL_SOCKET'],
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dinheiro.sqlite3',
        }
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {},
    'loggers': {
        'django.request': {
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
