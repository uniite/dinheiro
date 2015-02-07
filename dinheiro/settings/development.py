from dinheiro.settings.base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'iy0c*kpd(_l)o27ye&t%#e&sq!yl=ob%0*(@a5i29t+p(05yds'

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
